"""
On-policy comparison: REINFORCE vs A2C (Actor-Critic) vs PPO

Train three on-policy methods on LunarLander-v3 and compare learning curves.

- REINFORCE: Custom PyTorch (episode-wise policy gradient). Not in SB3.
- A2C: Stable Baselines3 A2C (synchronous Actor-Critic).
- PPO: Stable Baselines3 PPO (Proximal Policy Optimization).

Run: python 08_onpolicy_compare.py [--total_timesteps 200000] [--seed 0] [--force_train]
"""

import argparse
import os
import warnings
warnings.filterwarnings("ignore", message=".*pkg_resources is deprecated.*")

import numpy as np
import torch
import torch.nn as nn

_script_dir = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(_script_dir, "models")
RENDERS_DIR = os.path.join(_script_dir, "renders")

import gymnasium as gym
from stable_baselines3 import A2C, PPO
from stable_baselines3.common.callbacks import BaseCallback

from device_utils import get_device, get_device_name

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# -----------------------------------------------------------------------------
# REINFORCE (custom PyTorch, discrete action)
# -----------------------------------------------------------------------------

class PolicyNetwork(nn.Module):
    """Softmax policy for discrete actions."""
    def __init__(self, obs_dim, act_dim, hidden=128, seed=None):
        super().__init__()
        if seed is not None:
            torch.manual_seed(seed)
        self.net = nn.Sequential(
            nn.Linear(obs_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, act_dim),
        )
        self.obs_dim = obs_dim
        self.act_dim = act_dim

    def forward(self, x):
        logits = self.net(x)
        return torch.softmax(logits, dim=-1)

    def get_action(self, obs, deterministic=False):
        with torch.no_grad():
            p = self.forward(obs)
            if deterministic:
                return p.argmax(dim=-1).item()
            dist = torch.distributions.Categorical(probs=p)
            return dist.sample().item()

    def log_prob(self, obs, action):
        p = self.forward(obs)
        dist = torch.distributions.Categorical(probs=p)
        # For batch size 1, log_prob expects (1,) tensor
        a = torch.tensor([action], device=obs.device, dtype=torch.long)
        return dist.log_prob(a).squeeze(0)


def run_reinforce_lunarlander(env_id, total_timesteps, lr=1e-3, gamma=0.99, seed=None, device="cpu"):
    """Train LunarLander with REINFORCE. Returns list of episode returns."""
    env = gym.make(env_id)
    if seed is not None:
        env.reset(seed=seed)
        torch.manual_seed(seed)
        np.random.seed(seed)

    obs_dim = env.observation_space.shape[0]
    act_dim = env.action_space.n
    policy = PolicyNetwork(obs_dim, act_dim, seed=seed).to(device)
    optimizer = torch.optim.Adam(policy.parameters(), lr=lr)

    episode_returns = []
    step_count = 0

    while step_count < total_timesteps:
        obs, _ = env.reset()
        obs_t = torch.as_tensor(obs, dtype=torch.float32, device=device).unsqueeze(0)
        traj_log_probs = []
        traj_rewards = []
        episode_return = 0.0

        while True:
            action = policy.get_action(obs_t, deterministic=False)
            log_prob = policy.log_prob(obs_t, action)
            traj_log_probs.append(log_prob)
            nobs, reward, term, trunc, _ = env.step(action)
            traj_rewards.append(reward)
            episode_return += reward
            step_count += 1
            if term or trunc:
                break
            obs_t = torch.as_tensor(nobs, dtype=torch.float32, device=device).unsqueeze(0)

        episode_returns.append(episode_return)

        # G_t = sum_{k=t}^{T-1} gamma^{k-t} r_k
        T = len(traj_rewards)
        G = np.zeros(T)
        G[-1] = traj_rewards[-1]
        for t in range(T - 2, -1, -1):
            G[t] = traj_rewards[t] + gamma * G[t + 1]

        # Loss = - sum_t G_t * log pi(a_t|s_t); minimize -> policy gradient ascent
        loss = torch.tensor(0.0, device=device)
        for lp, g in zip(traj_log_probs, G):
            loss = loss - lp * torch.tensor(g, dtype=torch.float32, device=device)
        loss = loss / max(T, 1)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    env.close()
    return episode_returns


# -----------------------------------------------------------------------------
# SB3 A2C / PPO (callback collects episode returns)
# -----------------------------------------------------------------------------

class EpisodeRewardCallback(BaseCallback):
    """Callback that collects return on episode end."""
    def __init__(self):
        super().__init__()
        self.episode_rewards = []
        self.current_reward = 0.0

    def _on_step(self):
        self.current_reward += self.locals["rewards"][0]
        if self.locals["dones"][0]:
            self.episode_rewards.append(self.current_reward)
            self.current_reward = 0.0
        return True


def get_or_train_sb3_a2c_ll(env_id, total_timesteps, seed=None, force_train=False):
    """A2C LunarLander. Load if exists, else train and save. Returns list of episode rewards."""
    model_path = os.path.join(MODELS_DIR, "lunarlander_a2c.zip")
    rewards_path = os.path.join(MODELS_DIR, "lunarlander_a2c_rewards.npy")

    if not force_train and os.path.exists(model_path):
        print("   A2C model loaded:", model_path)
        model = A2C.load(model_path)
        if os.path.exists(rewards_path):
            return np.load(rewards_path, allow_pickle=True).tolist()
        env = gym.make(env_id)
        rewards = []
        obs, _ = env.reset()
        ep_rew = 0.0
        for _ in range(total_timesteps):
            action, _ = model.predict(obs, deterministic=True)
            obs, r, term, trunc, _ = env.step(action)
            ep_rew += r
            if term or trunc:
                rewards.append(ep_rew)
                obs, _ = env.reset()
                ep_rew = 0.0
        env.close()
        return rewards

    env = gym.make(env_id)
    device = get_device()
    model = A2C(
        "MlpPolicy",
        env,
        device=device,
        learning_rate=7e-4,
        n_steps=5,
        gamma=0.99,
        seed=seed,
        verbose=0,
    )
    cb = EpisodeRewardCallback()
    model.learn(total_timesteps=total_timesteps, callback=cb)
    os.makedirs(MODELS_DIR, exist_ok=True)
    model.save(model_path)
    np.save(rewards_path, np.array(cb.episode_rewards))
    env.close()
    print("   A2C model saved:", model_path)
    return cb.episode_rewards


def get_or_train_sb3_ppo_ll(env_id, total_timesteps, seed=None, force_train=False):
    """PPO LunarLander. Load if exists, else train and save. Returns list of episode rewards."""
    model_path = os.path.join(MODELS_DIR, "lunarlander_ppo.zip")
    rewards_path = os.path.join(MODELS_DIR, "lunarlander_ppo_rewards.npy")

    if not force_train and os.path.exists(model_path):
        print("   PPO model loaded:", model_path)
        model = PPO.load(model_path)
        if os.path.exists(rewards_path):
            return np.load(rewards_path, allow_pickle=True).tolist()
        env = gym.make(env_id)
        rewards = []
        obs, _ = env.reset()
        ep_rew = 0.0
        for _ in range(total_timesteps):
            action, _ = model.predict(obs, deterministic=True)
            obs, r, term, trunc, _ = env.step(action)
            ep_rew += r
            if term or trunc:
                rewards.append(ep_rew)
                obs, _ = env.reset()
                ep_rew = 0.0
        env.close()
        return rewards

    env = gym.make(env_id)
    device = get_device()
    model = PPO(
        "MlpPolicy",
        env,
        device=device,
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=64,
        n_epochs=10,
        gamma=0.99,
        seed=seed,
        verbose=0,
    )
    cb = EpisodeRewardCallback()
    model.learn(total_timesteps=total_timesteps, callback=cb)
    os.makedirs(MODELS_DIR, exist_ok=True)
    model.save(model_path)
    np.save(rewards_path, np.array(cb.episode_rewards))
    env.close()
    print("   PPO model saved:", model_path)
    return cb.episode_rewards


def smooth_curve(values, window=10):
    if len(values) < window:
        return values
    kernel = np.ones(window) / window
    smoothed = np.convolve(values, kernel, mode="valid")
    return np.concatenate([values[: window - 1], smoothed])


def main():
    parser = argparse.ArgumentParser(description="LunarLander on-policy compare: REINFORCE vs A2C vs PPO")
    parser.add_argument("--total_timesteps", type=int, default=200_000)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--out", type=str, default=os.path.join(RENDERS_DIR, "08_onpolicy_compare.png"))
    parser.add_argument("--force_train", action="store_true", help="Ignore cache and force A2C/PPO retrain")
    args = parser.parse_args()

    total = args.total_timesteps
    seed = args.seed
    env_id = "LunarLander-v3"
    device = get_device()
    print("Device:", get_device_name(device))

    print("1/3 REINFORCE (custom PyTorch)...")
    rew_reinforce = run_reinforce_lunarlander(env_id, total_timesteps=total, seed=seed, device=device)

    print("2/3 A2C (SB3, load if exists)...")
    rew_a2c = get_or_train_sb3_a2c_ll(env_id, total_timesteps=total, seed=seed, force_train=args.force_train)

    print("3/3 PPO (SB3, load if exists)...")
    rew_ppo = get_or_train_sb3_ppo_ll(env_id, total_timesteps=total, seed=seed, force_train=args.force_train)

    fig, ax = plt.subplots(figsize=(10, 5))
    w = max(1, min(50, len(rew_reinforce) // 10))
    ax.plot(smooth_curve(rew_reinforce, w), alpha=0.7, label="REINFORCE (Custom)")
    w_a2c = max(1, min(50, len(rew_a2c) // 10))
    ax.plot(smooth_curve(rew_a2c, w_a2c), alpha=0.7, label="A2C (SB3)")
    w_ppo = max(1, min(50, len(rew_ppo) // 10))
    ax.plot(smooth_curve(rew_ppo, w_ppo), alpha=0.7, label="PPO (SB3)")
    ax.set_xlabel("Episode")
    ax.set_ylabel("Episode return (smoothed)")
    ax.set_title(f"{env_id}: REINFORCE vs A2C vs PPO (On-Policy)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    os.makedirs(RENDERS_DIR, exist_ok=True)
    plt.savefig(args.out, dpi=120)
    plt.close()
    print("Saved:", args.out)

    def last_mean(x, k=100):
        return np.mean(x[-k:]) if len(x) >= k else np.mean(x) if x else 0.0
    print("  REINFORCE (Custom)  last 100 ep mean:", f"{last_mean(rew_reinforce):.1f}")
    print("  A2C (SB3)           last 100 ep mean:", f"{last_mean(rew_a2c):.1f}")
    print("  PPO (SB3)           last 100 ep mean:", f"{last_mean(rew_ppo):.1f}")


if __name__ == "__main__":
    main()
