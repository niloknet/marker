"""
Key DQN params: buffer_size, train_freq, target_update_interval

- Experience Replay -> SB3 buffer_size, train_freq
- Target Network -> SB3 target_update_interval
- Compare how changing these affects learning.

Train with three configs and plot episode reward curves.
  - Default: buffer_size=50_000, train_freq=4, target_update_interval=1_000
  - Aggressive (unstable): small buffer, train every step, frequent target update
  - Conservative: large buffer, less frequent train/target update

Run: python 05_dqn_param_effect.py [--total_timesteps 50000] [--seed 0]
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


def train_with_params(
    env_id,
    buffer_size,
    train_freq,
    target_update_interval,
    total_timesteps,
    seed=None,
):
    """Train DQN with given params, return list of episode rewards."""
    env = gym.make(env_id)
    device = get_device()

    model = DQN(
        policy="MlpPolicy",
        env=env,
        device=device,
        learning_rate=1e-3,
        buffer_size=buffer_size,
        learning_starts=min(1_000, buffer_size // 10),
        batch_size=32,
        gamma=0.99,
        target_update_interval=target_update_interval,
        train_freq=train_freq,
        gradient_steps=1,
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
    parser = argparse.ArgumentParser(description="DQN key params effect comparison")
    parser.add_argument("--total_timesteps", type=int, default=50_000)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--out", type=str, default=os.path.join(RENDERS_DIR, "05_dqn_param_effect.png"))
    args = parser.parse_args()

    device = get_device()
    print(f"Device: {get_device_name(device)}")
    print("Compare buffer_size, train_freq, target_update_interval effects.\n")

    configs = [
        (
            "Default (recommended)",
            dict(
                buffer_size=50_000,
                train_freq=4,
                target_update_interval=1_000,
            ),
        ),
        (
            "Aggressive (unstable)\nSmall buffer, train every step, frequent target",
            dict(
                buffer_size=1_000,
                train_freq=1,
                target_update_interval=100,
            ),
        ),
        (
            "Conservative\nLarge buffer, less frequent train/target",
            dict(
                buffer_size=100_000,
                train_freq=16,
                target_update_interval=5_000,
            ),
        ),
    ]

    results = {}
    for name, params in configs:
        print(f"Training: {name.replace(chr(10), ' ')} ...")
        rewards = train_with_params(
            "CartPole-v1",
            total_timesteps=args.total_timesteps,
            seed=args.seed,
            **params,
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
    ax.set_title(
        "DQN key params effect (CartPole-v1)\n"
        "buffer_size, train_freq, target_update_interval"
    )
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    os.makedirs(RENDERS_DIR, exist_ok=True)
    plt.savefig(args.out, dpi=120)
    plt.close()
    print(f"Saved: {args.out}")


if __name__ == "__main__":
    main()
