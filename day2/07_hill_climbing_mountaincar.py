"""
힐 클라이밍 (Hill Climbing) - Mountain Car Continuous

산 오르기: MountainCarContinuous-v0 환경에서 선형 정책 + 힐 클라이밍
- 연속 행동: 엔진 추력 [-1, 1]
- 선형 정책: action = clip(w @ state, -1, 1)
- 파라미터 w를 무작위 섭동으로 최적화 (평균 리턴이 나아지면 수용)

실행: python 07_hill_climbing_mountaincar.py [--render_mode all|play|none]
  --render_mode: all(학습+플레이 렌더), play(마지막 1회만), none(렌더 없음). 기본값: play
"""

import argparse
import warnings
warnings.filterwarnings("ignore", message=".*pkg_resources is deprecated.*")

import gymnasium as gym
import numpy as np

from render_helpers import init_display, render_frame_with_overlay, tick_fps, check_user_stop


class PositionRewardShaping(gym.Wrapper):
    """위치 진행 보너스: 오른쪽(목표 방향)으로 갈수록 작은 보상. 희소 보상 완화."""
    def __init__(self, env, scale=0.3):
        super().__init__(env)
        self.scale = scale

    def step(self, action):
        obs, reward, term, trunc, info = self.env.step(action)
        position = float(obs[0])
        reward = reward + self.scale * position
        return obs, reward, term, trunc, info


class LinearPolicyMountainCar:
    """선형 정책: action = clip(w @ state_b, -1, 1), 연속 행동 1차원"""

    def __init__(self, obs_dim, action_dim, seed=None):
        self.obs_dim = obs_dim
        self.action_dim = action_dim
        # w: (obs_dim+1,) bias 포함
        rng = np.random.default_rng(seed)
        self.w = rng.standard_normal(obs_dim + 1) * 0.2  # 초기 탐험 넓게

    def get_action(self, state, deterministic=True):
        state_b = np.concatenate([[1.0], np.asarray(state, dtype=np.float64)])
        out = np.clip(float(self.w @ state_b), -1.0, 1.0)
        return np.array([out], dtype=np.float32)

    def set_params(self, w):
        self.w = np.asarray(w, dtype=np.float64).ravel()

    def get_params(self):
        return self.w.copy()


def evaluate_policy(env, policy, n_episodes=100):
    """정책으로 n_episodes 실행 후 평균 리워드 반환 (렌더 없음)"""
    rewards = []
    for _ in range(n_episodes):
        state, _ = env.reset()
        total = 0
        while True:
            action = policy.get_action(state, deterministic=True)
            state, reward, term, trunc, _ = env.step(action)
            total += reward
            if term or trunc:
                break
        rewards.append(total)
    return sum(rewards) / len(rewards)


def run_one_episode_with_render(env, policy, screen, it, n_iterations):
    """한 에피소드를 화면에 렌더링하며 실행. 사용자 종료 시 True 반환."""
    state, _ = env.reset()
    total = 0
    while True:
        if check_user_stop():
            return True
        action = policy.get_action(state, deterministic=True)
        state, reward, term, trunc, _ = env.step(action)
        total += reward
        render_frame_with_overlay(env, screen, reward, total, episode=f"iter {it+1}/{n_iterations}")
        tick_fps(env)
        if term or trunc:
            break
    return False


def train_hill_climbing(env, policy, n_iterations=500, n_evals=5, noise_scale=0.1, noise_decay=0.995, screen=None):
    """힐 클라이밍: 파라미터에 노이즈를 더해 후보를 만들고, 평균 리턴이 나아지면 수용.
    screen이 주어지면 주기적으로 한 에피소드를 렌더링하며 재생."""
    best_w = policy.get_params()
    best_return = evaluate_policy(env, policy, n_episodes=n_evals)
    eval_returns = [best_return]  # 러닝 중 돌린 평가 결과들

    for it in range(n_iterations):
        candidate_w = best_w + noise_scale * np.random.standard_normal(best_w.shape)
        policy.set_params(candidate_w)
        candidate_return = evaluate_policy(env, policy, n_episodes=n_evals)
        eval_returns.append(candidate_return)

        if candidate_return >= best_return:
            best_w = candidate_w.copy()
            best_return = candidate_return
            policy.set_params(best_w)

        noise_scale *= noise_decay

        if (it + 1) % 100 == 0:
            avg_so_far = sum(eval_returns) / len(eval_returns)
            print(f"Iteration {it+1}/{n_iterations}, 러닝 중 평가 결과 평균: {avg_so_far:.1f}, noise_scale: {noise_scale:.4f}")

        # 학습 중 재생: screen이 있으면 매 100 iter마다 한 에피소드 렌더링
        if screen is not None and (it + 1) % 100 == 0:
            if run_one_episode_with_render(env, policy, screen, it, n_iterations):
                print("  사용자에 의해 학습 중 재생 종료")
                policy.set_params(best_w)
                return

    policy.set_params(best_w)


def main():
    parser = argparse.ArgumentParser(description="MountainCar Continuous 힐 클라이밍 (선형 정책)")
    parser.add_argument(
        "--render_mode",
        choices=["all", "play", "none"],
        default="play",
        help="all: 학습+플레이 렌더, play: 마지막 1회만, none: 렌더 없음",
    )
    args = parser.parse_args()
    render_mode = args.render_mode

    train_render = render_mode == "all"
    env = gym.make(
        "MountainCarContinuous-v0",
        render_mode="rgb_array" if train_render else None,
    )
    env = PositionRewardShaping(env, scale=0.5)  # 오른쪽 진행 보너스 강화
    screen = None
    if train_render:
        env.reset()
        screen = init_display(env.render().shape)
        print("학습 중... (pygame 창에서 실시간 보상 확인)")
    else:
        print("학습 중...")

    obs_dim = env.observation_space.shape[0]
    action_dim = env.action_space.shape[0]
    policy = LinearPolicyMountainCar(obs_dim, action_dim)

    env_eval = PositionRewardShaping(gym.make("MountainCarContinuous-v0"), scale=0.5)
    mean_before = evaluate_policy(env_eval, policy, n_episodes=100)
    env_eval.close()
    print(f"학습 전 평균 리워드 (100회): {mean_before:.1f}")

    train_hill_climbing(
        env, policy,
        n_iterations=800,
        n_evals=30,   # 후보당 평가 횟수. 적으면 분산 커져 학습 중 수치와 최종 100회 평가가 어긋날 수 있음
        noise_scale=0.25,
        noise_decay=0.997,
        screen=screen,
    )
    env.close()

    env_eval = PositionRewardShaping(gym.make("MountainCarContinuous-v0"), scale=0.5)
    mean_after = evaluate_policy(env_eval, policy, n_episodes=100)
    env_eval.close()

    print(f"\n학습 후 평균 리워드 (100회, shaped): {mean_after:.1f}  ← 이 값이 정책의 안정적인 성능 추정")
    print(f"  → 개선: {mean_after - mean_before:+.1f}")

    env_raw = gym.make("MountainCarContinuous-v0")
    mean_raw = evaluate_policy(env_raw, policy, n_episodes=100)
    env_raw.close()
    print(f"  원본 환경 평균 리워드 (100회): {mean_raw:.1f} (목표 도달 시 +100)")

    play_render = render_mode in ("play", "all")
    if play_render:
        env = gym.make("MountainCarContinuous-v0", render_mode="rgb_array")
        env.reset()
        if screen is None:
            screen = init_display(env.render().shape)
    else:
        env = gym.make("MountainCarContinuous-v0")

    if play_render:
        import pygame
        pygame.display.set_caption("MountainCar - 아무 키/클릭으로 종료")
        print("\n학습된 정책 시연 (키/클릭 시 종료)")
        ep_count = 0
        while True:
            ep_count += 1
            state, _ = env.reset()
            total = 0
            while True:
                if check_user_stop():
                    print(f"  시연 종료 (총 {ep_count}회 재생)")
                    env.close()
                    return
                action = policy.get_action(state, deterministic=True)
                state, reward, term, trunc, _ = env.step(action)
                total += reward
                render_frame_with_overlay(env, screen, reward, total, ep_count)
                tick_fps(env)
                if term or trunc:
                    break
            print(f"  에피소드 {ep_count}: Return = {total:.1f}")
    else:
        print("\n학습된 정책 시연 (1회)")
        state, _ = env.reset()
        total = 0
        while True:
            action = policy.get_action(state, deterministic=True)
            state, reward, term, trunc, _ = env.step(action)
            total += reward
            if term or trunc:
                break
        print(f"  Return = {total:.1f}")

    env.close()


if __name__ == "__main__":
    main()
