"""
힐 클라이밍 (Hill Climbing) - CartPole

막대 중심 잡기: CartPole-v1 환경에서 선형 정책 + 힐 클라이밍
- 이산 행동 (0: 왼쪽, 1: 오른쪽)
- 선형 정책: action = argmax(W @ state)
- 파라미터 W를 무작위 섭동으로 최적화 (평균 리턴이 나아지면 수용)

실행: python 06_hill_climbing_cartpole.py [--render_mode all|play|none]
  --render_mode: all(학습+플레이 렌더), play(마지막 1회만 렌더), none(렌더 없음). 기본값: play
"""

import argparse
import warnings
warnings.filterwarnings("ignore", message=".*pkg_resources is deprecated.*")

import gymnasium as gym
import numpy as np

from render_helpers import init_display, render_frame_with_overlay, tick_fps, check_user_stop


class LinearPolicyCartPole:
    """선형 정책: W @ state → 행동 점수 → argmax로 이산 행동 선택"""

    def __init__(self, obs_dim, n_actions, seed=None):
        self.obs_dim = obs_dim
        self.n_actions = n_actions
        # W: (n_actions, obs_dim+1), 맨 앞 1은 bias
        rng = np.random.default_rng(seed)
        self.W = rng.standard_normal((n_actions, obs_dim + 1)) * 0.1

    def get_action(self, state, deterministic=True):
        state_b = np.concatenate([[1.0], np.asarray(state, dtype=np.float64)])
        scores = self.W @ state_b
        return int(np.argmax(scores))

    def set_params(self, W):
        self.W = np.asarray(W, dtype=np.float64).reshape(self.n_actions, self.obs_dim + 1)

    def get_params(self):
        return self.W.copy()


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
    best_W = policy.get_params()
    best_return = evaluate_policy(env, policy, n_episodes=n_evals)
    eval_returns = [best_return]  # 러닝 중 돌린 평가 결과들

    for it in range(n_iterations):
        # 후보: 현재 최적 + 가우시안 노이즈
        candidate_W = best_W + noise_scale * np.random.standard_normal(best_W.shape)
        policy.set_params(candidate_W)
        candidate_return = evaluate_policy(env, policy, n_episodes=n_evals)
        eval_returns.append(candidate_return)

        if candidate_return >= best_return:
            best_W = candidate_W.copy()
            best_return = candidate_return
            policy.set_params(best_W)

        noise_scale *= noise_decay

        if (it + 1) % 10 == 0:
            avg_so_far = sum(eval_returns) / len(eval_returns)
            print(f"Iteration {it+1}/{n_iterations}, 러닝 중 평가 결과 평균: {avg_so_far:.1f}, noise_scale: {noise_scale:.4f}")

        # 학습 중 재생: screen이 있으면 매 10 iter마다 한 에피소드 렌더링
        if screen is not None and (it + 1) % 10 == 0:
            if run_one_episode_with_render(env, policy, screen, it, n_iterations):
                print("  사용자에 의해 학습 중 재생 종료")
                policy.set_params(best_W)
                return

    policy.set_params(best_W)


def main():
    parser = argparse.ArgumentParser(description="CartPole 힐 클라이밍 (선형 정책)")
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
        "CartPole-v1",
        render_mode="rgb_array" if train_render else None,
    )
    screen = None
    if train_render:
        env.reset()
        screen = init_display(env.render().shape)
        print("학습 중... (pygame 창에서 실시간 보상 확인)")
    else:
        print("학습 중...")

    obs_dim = env.observation_space.shape[0]
    n_actions = env.action_space.n
    policy = LinearPolicyCartPole(obs_dim, n_actions)

    env_eval = gym.make("CartPole-v1")
    mean_before = evaluate_policy(env_eval, policy, n_episodes=100)
    env_eval.close()
    print(f"학습 전 평균 리워드 (100회): {mean_before:.1f}")

    train_hill_climbing(env, policy, n_iterations=200, n_evals=10, noise_scale=0.15, noise_decay=0.995, screen=screen)
    env.close()

    env_eval = gym.make("CartPole-v1")
    mean_after = evaluate_policy(env_eval, policy, n_episodes=100)
    env_eval.close()

    print(f"\n학습 후 평균 리워드 (100회): {mean_after:.1f}")
    print(f"  → 개선: {mean_after - mean_before:+.1f}")

    play_render = render_mode in ("play", "all")
    if play_render:
        env = gym.make("CartPole-v1", render_mode="rgb_array")
        env.reset()
        if screen is None:
            screen = init_display(env.render().shape)
    else:
        env = gym.make("CartPole-v1")

    if play_render:
        import pygame
        pygame.display.set_caption("CartPole - 아무 키/클릭으로 종료")
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
            print(f"  에피소드 {ep_count}: Return = {total}")
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
        print(f"  Return = {total}")

    env.close()


if __name__ == "__main__":
    main()
