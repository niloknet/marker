"""
SB3 DQN architecture: MlpPolicy + policy_kwargs to change hidden layers

- MlpPolicy means SB3 manages the MLP policy (no raw PyTorch).
- policy_kwargs net_arch changes hidden layer size/depth.

This script: train with three net_archs and compare episode reward curves.
  - Small: [64, 64]
  - Default (SB3): [] (SB3 default, typically [64, 64])
  - Large: [256, 256, 128]

Run: python 04_policy_kwargs_dqn.py [--total_timesteps 50000] [--seed 0]
"""

import argparse
import os
import warnings
warnings.filterwarnings("ignore", message=".*pkg_resources is deprecated.*")

import numpy as np
import gymnasium as gym
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import BaseCallback
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from device_utils import get_device, get_device_name

_script_dir = os.path.dirname(os.path.abspath(__file__))
RENDERS_DIR = os.path.join(_script_dir, "renders")


class EpisodeRewardCallback(BaseCallback):
    """Collect reward at end of each episode."""

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


def train_with_net_arch(env_id, net_arch, total_timesteps, seed=None):
    """
    Train DQN with given net_arch, return list of episode rewards.
    net_arch: [] (default), [64, 64], [256, 256, 128], etc.
    """
    env = gym.make(env_id)
    device = get_device()

    policy_kwargs = {}
    if net_arch is not None:
        policy_kwargs["net_arch"] = net_arch

    model = DQN(
        policy="MlpPolicy",
        env=env,
        device=device,
        policy_kwargs=policy_kwargs if policy_kwargs else None,
        learning_rate=1e-3,
        buffer_size=50_000,
        learning_starts=1_000,
        batch_size=32,
        gamma=0.99,
        target_update_interval=1_000,
        train_freq=4,
        exploration_fraction=0.1,
        exploration_initial_eps=1.0,
        exploration_final_eps=0.05,
        seed=seed,
        verbose=0,
    )
    cb = EpisodeRewardCallback()
    model.learn(total_timesteps=total_timesteps, callback=cb)
    env.close()
    return cb.episode_rewards


def main():
    parser = argparse.ArgumentParser(description="DQN policy_kwargs net_arch comparison")
    parser.add_argument("--total_timesteps", type=int, default=50_000)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--out", type=str, default=os.path.join(RENDERS_DIR, "04_policy_kwargs_compare.png"))
    args = parser.parse_args()

    device = get_device()
    print(f"Device: {get_device_name(device)}")
    print("Compare training with different net_arch (MlpPolicy + policy_kwargs).\n")

    configs = [
        ("Small [64, 64]", [64, 64]),
        ("Default (SB3 net_arch)", None),
        ("Large [256, 256, 128]", [256, 256, 128]),
    ]

    results = {}
    for name, net_arch in configs:
        print(f"Training: {name} ...")
        rewards = train_with_net_arch(
            "CartPole-v1",
            net_arch=net_arch,
            total_timesteps=args.total_timesteps,
            seed=args.seed,
        )
        results[name] = rewards
        last_100 = np.mean(rewards[-100:]) if len(rewards) >= 100 else np.mean(rewards)
        print(f"  Last 100 episode mean reward: {last_100:.1f}\n")

    # Plot
    fig, ax = plt.subplots(figsize=(10, 5))
    for name, rewards in results.items():
        window = max(1, min(50, len(rewards) // 10))
        kernel = np.ones(window) / window
        smoothed = np.convolve(rewards, kernel, mode="valid")
        x = np.arange(len(smoothed))
        ax.plot(x, smoothed, alpha=0.8, label=name)
    ax.set_xlabel("Episode")
    ax.set_ylabel("Episode reward (moving avg)")
    ax.set_title("DQN net_arch comparison (CartPole-v1)\npolicy_kwargs=dict(net_arch=[...])")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    os.makedirs(RENDERS_DIR, exist_ok=True)
    plt.savefig(args.out, dpi=120)
    plt.close()
    print(f"Saved: {args.out}")


if __name__ == "__main__":
    main()
