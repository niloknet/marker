"""
CliffWalking Q-Learning - Pygame 렌더링

Q-러닝으로 CliffWalking-v1 학습 후, pygame으로 학습 과정과 재생 과정을 시각화합니다.
왼쪽: 환경 맵, 오른쪽: 별도 정보 패널 (학습률, 할인율, 탐험율, 에피소드 등)

실행: python day3/03_cliffwalking_qlearning_pygame.py [--render_mode all|play|none]
  --render_mode: all(학습+재생 렌더), play(재생만 렌더), none(렌더 없음). 기본값: all
"""

import argparse
import os
import sys
import warnings

warnings.filterwarnings("ignore", message=".*pkg_resources.*")

# day2 render_helpers 사용을 위한 경로 추가
_script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_script_dir, "..", "day2"))

import gymnasium as gym
import numpy as np
import pandas as pd
import pygame

from render_helpers import tick_fps, check_user_stop


# 액션 이름 (CliffWalking: UP=0, RIGHT=1, DOWN=2, LEFT=3)
ACTION_NAMES = ["UP", "RIGHT", "DOWN", "LEFT"]
ACTION_SHORT = ["U", "R", "D", "L"]

# 정보 패널 너비 (환경 맵 옆에 별도 패널)
PANEL_WIDTH = 260


def init_display_with_panel(frame_shape):
    """환경 프레임 + 오른쪽 정보 패널용 pygame 창 초기화."""
    h, w = frame_shape[0], frame_shape[1]
    total_width = w + PANEL_WIDTH
    pygame.init()
    screen = pygame.display.set_mode((total_width, h))
    return screen


def render_frame_with_side_panel(env, screen, overlay_info, font_size=22):
    """
    왼쪽에 환경 프레임, 오른쪽에 별도 정보 패널을 그립니다.
    overlay_info: dict - alpha, gamma, epsilon, episode, step, total_reward,
                 avg_reward_100, last_action, phase 등
    """
    frame = env.render()
    if frame is None:
        return
    # numpy (H, W, 3) → pygame Surface
    frame = np.transpose(frame, (1, 0, 2))
    surf = pygame.surfarray.make_surface(frame)
    screen.blit(surf, (0, 0))

    # 오른쪽 패널 영역 (배경)
    panel_x = surf.get_width()
    panel_h = screen.get_height()
    panel_surf = pygame.Surface((PANEL_WIDTH, panel_h))
    panel_surf.fill((30, 35, 45))
    screen.blit(panel_surf, (panel_x, 0))

    try:
        font = pygame.font.Font(None, font_size)
    except Exception:
        font = pygame.font.SysFont("consolas", font_size - 4)

    info = overlay_info
    alpha_val = info.get("alpha", 0)
    gamma_val = info.get("gamma", 0)
    eps_val = info.get("epsilon", 0)
    avg_val = info.get("avg_reward_100", 0)
    alpha_str = f"{alpha_val:.3f}" if isinstance(alpha_val, (int, float)) else str(alpha_val)
    gamma_str = f"{gamma_val:.2f}" if isinstance(gamma_val, (int, float)) else str(gamma_val)
    eps_str = f"{eps_val:.3f}" if isinstance(eps_val, (int, float)) else str(eps_val)
    avg_str = f"{avg_val:.2f}" if isinstance(avg_val, (int, float)) else str(avg_val)

    lines = [
        f"Phase: {info.get('phase', 'Train')}",
        f"Episode: {info.get('episode', 0)}",
        f"Step: {info.get('step', 0)}",
        f"Env: CliffWalking-v1",
        f"Learning rate (alpha): {alpha_str}",
        f"Discount (gamma): {gamma_str}",
        f"Exploration (epsilon): {eps_str}",
        f"Total Reward: {info.get('total_reward', 0)}",
        f"Avg(100 ep): {avg_str}",
        f"Last action: {info.get('last_action', '-')}",
    ]

    y = 12
    text_color = (220, 255, 220)
    for line in lines:
        text = font.render(line, True, text_color)
        screen.blit(text, (panel_x + 12, y))
        y += font_size + 2

    pygame.display.flip()


def train_qlearning(
    env,
    n_episodes=2000,
    alpha=0.1,
    gamma=0.99,
    epsilon_start=1.0,
    epsilon_decay=0.995,
    epsilon_min=0.01,
    render=False,
    screen=None,
    render_interval=1,
):
    """
    Q-러닝 학습. render=True이고 screen이 있으면 매 render_interval 에피소드마다 시각화.
    반환: (Q, returns_list)
    """
    n_s = env.observation_space.n
    n_a = env.action_space.n
    Q = np.zeros((n_s, n_a))
    epsilon = epsilon_start
    returns_list = []

    for ep in range(n_episodes):
        state, _ = env.reset()
        total_reward = 0
        step = 0
        done = False
        last_action = "-"

        while not done:
            if screen is not None and check_user_stop():
                return Q, returns_list

            # epsilon-greedy
            if np.random.random() < epsilon:
                action = env.action_space.sample()
            else:
                action = select_greedy_action(Q, state)

            next_state, reward, term, trunc, _ = env.step(action)
            done = term or trunc

            # Q 업데이트: Q[s,a] += alpha * (r + gamma * max_a' Q[s',a'] - Q[s,a])
            td_target = reward + gamma * Q[next_state].max()
            Q[state, action] += alpha * (td_target - Q[state, action])

            state = next_state
            total_reward += reward
            step += 1
            last_action = ACTION_NAMES[action]

            # 학습 중 렌더링
            if render and screen is not None and (ep + 1) % render_interval == 0:
                avg100 = np.mean(returns_list[-100:]) if returns_list else 0
                overlay_info = {
                    "phase": "TRAIN",
                    "episode": ep + 1,
                    "step": step,
                    "alpha": alpha,
                    "gamma": gamma,
                    "epsilon": epsilon,
                    "total_reward": total_reward,
                    "avg_reward_100": avg100,
                    "last_action": last_action,
                }
                render_frame_with_side_panel(env, screen, overlay_info)
                tick_fps(env)

        epsilon = max(epsilon_min, epsilon * epsilon_decay)
        returns_list.append(total_reward)

        if (ep + 1) % 200 == 0:
            avg = np.mean(returns_list[-100:]) if len(returns_list) >= 100 else np.mean(returns_list)
            print(f"Episode {ep+1}/{n_episodes}, epsilon={epsilon:.3f}, avg100={avg:.2f}")

    return Q, returns_list


def print_qtable(Q, action_names=None):
    """Q 테이블을 DataFrame으로 콘솔에 출력 (state x action)."""
    if action_names is None:
        action_names = ACTION_SHORT
    df = pd.DataFrame(Q, columns=action_names)
    df.index.name = "state"
    df["best"] = [action_names[int(np.argmax(Q[s]))] for s in range(Q.shape[0])]
    print("\n[ Q Table ]")
    print(df.to_string(float_format=lambda x: f"{x:.3f}"))
    print()


def select_greedy_action(Q, state):
    """Q[state]에서 최대 Q값을 가진 행동 선택. 동점이면 무작위 선택."""
    max_q = Q[state].max()
    best_actions = np.where(Q[state] == max_q)[0]
    return int(np.random.choice(best_actions))


def playback(
    env, Q, screen, n_episodes=5, label="PLAYBACK",
    train_alpha=None, train_gamma=None, avg_reward_100=None,
):
    """학습된 Q로 그리디하게 에피소드 재생. 키/클릭 시 종료."""
    for ep in range(n_episodes):
        state, _ = env.reset()
        total_reward = 0
        step = 0
        done = False
        last_action = "-"

        while not done:
            if check_user_stop():
                return True  # 사용자 종료

            action = select_greedy_action(Q, state)
            next_state, reward, term, trunc, _ = env.step(action)
            done = term or trunc

            state = next_state
            total_reward += reward
            step += 1
            last_action = ACTION_NAMES[action]

            overlay_info = {
                "phase": label,
                "episode": ep + 1,
                "step": step,
                "alpha": train_alpha if train_alpha is not None else "-",
                "gamma": train_gamma if train_gamma is not None else "-",
                "epsilon": "0 (greedy)",
                "total_reward": total_reward,
                "avg_reward_100": avg_reward_100 if avg_reward_100 is not None else "-",
                "last_action": last_action,
            }
            render_frame_with_side_panel(env, screen, overlay_info)
            tick_fps(env)

        # CliffWalking: -100 = cliff, -13 정도 = goal (최단 경로 11칸 + 보상)
        result = "GOAL!" if total_reward > -50 else "FELL (cliff)"
        print(f"  Playback ep {ep+1}: {result} (reward={total_reward})")

    return False


def main():
    parser = argparse.ArgumentParser(
        description="CliffWalking-v1 Q-Learning with Pygame"
    )
    parser.add_argument(
        "--render_mode",
        choices=["all", "play", "none"],
        default="all",
        help="all: 학습+재생 렌더, play: 재생만, none: 렌더 없음",
    )
    parser.add_argument(
        "--n_episodes",
        type=int,
        default=2000,
        help="학습 에피소드 수",
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=0.1,
        help="학습률",
    )
    parser.add_argument(
        "--gamma",
        type=float,
        default=0.99,
        help="할인율",
    )
    parser.add_argument(
        "--render_interval",
        type=int,
        default=5,
        help="학습 중 렌더링할 에피소드 간격",
    )
    args = parser.parse_args()

    render_train = args.render_mode == "all"
    render_play = args.render_mode in ("all", "play")

    env = gym.make("CliffWalking-v1", render_mode="rgb_array")

    screen = None
    if render_train:
        env.reset()
        frame = env.render()
        if frame is not None:
            screen = init_display_with_panel(frame.shape)
            pygame.display.set_caption(
                "CliffWalking Q-Learning - 학습 중 (키/클릭으로 종료)"
            )
            print("학습 중... (pygame 창에서 실시간 확인)")
    else:
        print("학습 중...")

    Q, returns_list = train_qlearning(
        env,
        n_episodes=args.n_episodes,
        alpha=args.alpha,
        gamma=args.gamma,
        render=render_train,
        screen=screen,
        render_interval=args.render_interval,
    )

    avg_final = np.mean(returns_list[-100:]) if len(returns_list) >= 100 else np.mean(returns_list)
    print(f"\n학습 완료. 마지막 100 에피소드 평균 보상: {avg_final:.2f}")
    print_qtable(Q, action_names=ACTION_SHORT)

    if render_play:
        if screen is None:
            env.reset()
            frame = env.render()
            if frame is not None:
                screen = init_display_with_panel(frame.shape)
        pygame.display.set_caption(
            "CliffWalking Q-Learning - 재생 (키/클릭으로 종료)"
        )
        print("\n학습된 정책 재생 (키/클릭 시 종료)")
        avg_final_val = np.mean(returns_list[-100:]) if len(returns_list) >= 100 else np.mean(returns_list)
        if playback(
            env, Q, screen, n_episodes=10,
            train_alpha=args.alpha, train_gamma=args.gamma, avg_reward_100=avg_final_val,
        ):
            print("  사용자에 의해 종료")
        env.close()
    else:
        env.close()
        env = gym.make("CliffWalking-v1")
        state, _ = env.reset()
        total = 0
        while True:
            action = select_greedy_action(Q, state)
            state, reward, term, trunc, _ = env.step(action)
            total += reward
            if term or trunc:
                break
        env.close()
        print(f"테스트 1회: reward={total}")

    pygame.quit()


if __name__ == "__main__":
    main()
