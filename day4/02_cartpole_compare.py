"""
CartPole comparison: Q-Learning (discretized) vs Vanilla DQN (unstable) vs Stable DQN (stable)

Train three approaches and compare learning curves.

- Q-Learning: Discretize continuous state into bins, table-based. Coarse bins hurt learning;
  fine bins are slow or suffer curse of dimensionality.
- Vanilla DQN: SB3 DQN with unstable settings (small buffer, frequent target update, etc.).
- Stable DQN: SB3 DQN default (recommended) settings.

SB3 DQN: Load from day4/models/ if exists, else train and save.

Run: python 02_cartpole_compare.py [--total_timesteps 100000] [--seed 0] [--force_train]
"""

import argparse
import os
import warnings
warnings.filterwarnings("ignore", message=".*pkg_resources is deprecated.*")

import numpy as np

_script_dir = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(_script_dir, "models")
RENDERS_DIR = os.path.join(_script_dir, "renders")
import gymnasium as gym
from stable_baselines3 import DQN

from device_utils import get_device, get_device_name
from stable_baselines3.common.callbacks import BaseCallback
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# CartPole observation bounds (approx). For discretization
CART_POSITION_BOUNDS = (-4.8, 4.8)
CART_VELOCITY_BOUNDS = (-5.0, 5.0)
ANGLE_BOUNDS = (-0.418, 0.418)
ANGLE_VELOCITY_BOUNDS = (-5.0, 5.0)


def discretize_state(obs, n_bins=5):
    """Convert continuous observation to bin indices. n_bins per dimension."""
    pos, vel, angle, avel = obs[0], obs[1], obs[2], obs[3]
    pos = np.clip(pos, *CART_POSITION_BOUNDS)
    vel = np.clip(vel, *CART_VELOCITY_BOUNDS)
    angle = np.clip(angle, *ANGLE_BOUNDS)
    avel = np.clip(avel, *ANGLE_VELOCITY_BOUNDS)

    def to_bin(x, low, high, n):
        p = (x - low) / (high - low + 1e-8)
        p = np.clip(p, 0, 1)
        return min(int(p * n), n - 1)

    i0 = to_bin(pos, *CART_POSITION_BOUNDS, n_bins)
    i1 = to_bin(vel, *CART_VELOCITY_BOUNDS, n_bins)
    i2 = to_bin(angle, *ANGLE_BOUNDS, n_bins)
    i3 = to_bin(avel, *ANGLE_VELOCITY_BOUNDS, n_bins)
    n = n_bins
    return i0 * (n ** 3) + i1 * (n ** 2) + i2 * n + i3


def run_qlearning_cartpole(total_timesteps, n_bins=5, alpha=0.1, gamma=0.99, seed=None):
    """Train CartPole with discretized Q-Learning. Returns list of episode returns."""
    rng = np.random.default_rng(seed)
    env = gym.make("CartPole-v1")
    if seed is not None:
        env.reset(seed=seed)

    n_states = n_bins ** 4
    n_actions = 2
    Q = np.zeros((n_states, n_actions))
    returns_list = []
    eps = 1.0
    eps_decay = 0.9995
    eps_min = 0.05

    step_count = 0
    while step_count < total_timesteps:
        obs, _ = env.reset()
        s = discretize_state(obs, n_bins)
        episode_return = 0.0
        done = False
        while not done and step_count < total_timesteps:
            if rng.random() < eps:
                a = env.action_space.sample()
            else:
                a = int(np.argmax(Q[s]))
            obs, r, term, trunc, _ = env.step(a)
            done = term or trunc
            s2 = discretize_state(obs, n_bins)
            Q[s, a] += alpha * (r + gamma * Q[s2].max() - Q[s, a])
            s = s2
            episode_return += r
            step_count += 1
        eps = max(eps_min, eps * eps_decay)
        returns_list.append(episode_return)
    env.close()
    return returns_list


class EpisodeRewardCallback(BaseCallback):
    """Callback that collects episode return on episode end."""
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


def get_or_train_sb3_dqn(env_id, total_timesteps, unstable=False, seed=None, force_train=False):
    """Load model if exists, else train SB3 DQN and save. Returns list of episode rewards."""
    tag = "vanilla" if unstable else "stable"
    model_path = os.path.join(MODELS_DIR, f"cartpole_dqn_{tag}.zip")
    rewards_path = os.path.join(MODELS_DIR, f"cartpole_dqn_{tag}_rewards.npy")

    if not force_train and os.path.exists(model_path):
        print(f"   DQN model loaded: {model_path}")
        model = DQN.load(model_path)
        if os.path.exists(rewards_path):
            return np.load(rewards_path, allow_pickle=True).tolist()
        # No reward file: evaluate instead
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
    if unstable:
        # Unstable: small buffer, train every step, frequent target update
        model = DQN(
            "MlpPolicy",
            env,
            device=device,
            buffer_size=100,
            learning_rate=0.01,
            batch_size=1,
            train_freq=1,
            target_update_interval=1,
            tau=1.0,
            gamma=0.99,
            exploration_fraction=0.1,
            learning_starts=10,
            seed=seed,
            verbose=0,
        )
    else:
        # Stable settings (similar to 01_dqn_cartpole)
        model = DQN(
            "MlpPolicy",
            env,
            device=device,
            learning_rate=1e-3,
            buffer_size=50_000,
            learning_starts=1_000,
            batch_size=32,
            tau=1.0,
            gamma=0.99,
            target_update_interval=1_000,
            train_freq=4,
            gradient_steps=1,
            exploration_fraction=0.1,
            exploration_initial_eps=1.0,
            exploration_final_eps=0.05,
            seed=seed,
            verbose=0,
        )
    cb = EpisodeRewardCallback()
    model.learn(total_timesteps=total_timesteps, callback=cb)
    os.makedirs(MODELS_DIR, exist_ok=True)
    model.save(model_path)
    np.save(rewards_path, np.array(cb.episode_rewards))
    env.close()
    print(f"   DQN model saved: {model_path}")
    return cb.episode_rewards


def smooth_curve(values, window=10):
    """Smooth curve with moving average."""
    if len(values) < window:
        return values
    kernel = np.ones(window) / window
    smoothed = np.convolve(values, kernel, mode="valid")
    return np.concatenate([values[: window - 1], smoothed])


def main():
    parser = argparse.ArgumentParser(description="CartPole: Q-Learning vs Vanilla DQN vs Stable DQN")
    parser.add_argument("--total_timesteps", type=int, default=100_000)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--out", type=str, default=os.path.join(RENDERS_DIR, "02_cartpole_compare.png"))
    parser.add_argument("--force_train", action="store_true", help="Ignore cache and force DQN retrain")
    args = parser.parse_args()

    total = args.total_timesteps
    seed = args.seed
    force_train = args.force_train

    device = get_device()
    print(f"Device: {get_device_name(device)}")

    print("1/3 Q-Learning (discretized table)...")
    rew_q = run_qlearning_cartpole(total_timesteps=total, seed=seed)

    print("2/3 Vanilla DQN (unstable, load if exists)...")
    rew_vanilla = get_or_train_sb3_dqn("CartPole-v1", total_timesteps=total, unstable=True, seed=seed, force_train=force_train)

    print("3/3 Stable DQN (default, load if exists)...")
    rew_stable = get_or_train_sb3_dqn("CartPole-v1", total_timesteps=total, unstable=False, seed=seed, force_train=force_train)

    # Plot
    fig, ax = plt.subplots(figsize=(10, 5))
    window = max(1, min(50, len(rew_q) // 10))
    ax.plot(smooth_curve(rew_q, window), alpha=0.7, label="Q-Learning (discretized)")
    window_v = max(1, min(50, len(rew_vanilla) // 10))
    ax.plot(smooth_curve(rew_vanilla, window_v), alpha=0.7, label="Vanilla DQN (unstable)")
    window_s = max(1, min(50, len(rew_stable) // 10))
    ax.plot(smooth_curve(rew_stable, window_s), alpha=0.7, label="Stable DQN (default)")
    ax.set_xlabel("Episode")
    ax.set_ylabel("Episode return (smoothed)")
    ax.set_title("CartPole-v1: Q-Learning vs Vanilla DQN vs Stable DQN")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    os.makedirs(RENDERS_DIR, exist_ok=True)
    plt.savefig(args.out, dpi=120)
    plt.close()
    print(f"Saved: {args.out}")

    # Summary
    def last_mean(x, k=100):
        return np.mean(x[-k:]) if len(x) >= k else np.mean(x) if x else 0.0
    print(f"  Q-Learning (discretized)  last 100 ep mean: {last_mean(rew_q):.1f}")
    print(f"  Vanilla DQN (unstable)     last 100 ep mean: {last_mean(rew_vanilla):.1f}")
    print(f"  Stable DQN (default)      last 100 ep mean: {last_mean(rew_stable):.1f}")


if __name__ == "__main__":
    main()
