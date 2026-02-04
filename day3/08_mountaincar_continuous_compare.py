"""
MountainCarContinuous-v0: 이산화 Q러닝 vs PPO 리워드 비교

- 이산화 Q러닝: 상태(위치, 속도)와 행동(추력)을 이산화하여 테이블 Q러닝
- Q러닝·PPO 공통: ShapedReward(높이 보너스)로 학습 곡선 부드럽게 (--no_shaping으로 끄기)
- PPO: gSDE + ShapedReward. 모델 있으면 로드, 없으면 학습 후 day3/models/에 저장
- 각 방법 학습/로딩 후 1에피소드 재생을 day3/renders/에 MP4로 저장하여 비교

실행: python day3/08_mountaincar_continuous_compare.py [--render_mode all|play|none]
  --render_mode: all(학습 시연+비교창), play(비교창만), none(콘솔만). 기본값: none
"""

import argparse
import os
import sys
import warnings

warnings.filterwarnings("ignore", message=".*pkg_resources.*")

_script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_script_dir, "..", "day2"))

import gymnasium as gym
import numpy as np
import imageio
from render_helpers import tick_fps, check_user_stop

# 모델/재생 영상 저장 경로 (스크립트 기준 day3/models, day3/renders)
MODELS_DIR = os.path.join(_script_dir, "models")
RENDERS_DIR = os.path.join(_script_dir, "renders")
PPO_MODEL_PATH = os.path.join(MODELS_DIR, "mountaincar_ppo.zip")
VIDEO_Q_PATH = os.path.join(RENDERS_DIR, "mountaincar_q.mp4")
VIDEO_PPO_PATH = os.path.join(RENDERS_DIR, "mountaincar_ppo.mp4")

# ---------------------------------------------------------------------------
# 이산화 Q러닝: 상태/행동 이산화
# ---------------------------------------------------------------------------
POS_MIN, POS_MAX = -1.2, 0.6
VEL_MIN, VEL_MAX = -0.07, 0.07
N_POS_BINS = 30
N_VEL_BINS = 30
# 행동: 추력 [-1, 1] → 5단계
DISCRETE_ACTIONS = np.array([-1.0, -0.5, 0.0, 0.5, 1.0], dtype=np.float32)
N_ACTIONS = len(DISCRETE_ACTIONS)


def discretize_state(obs):
    """연속 상태 (position, velocity) → 이산 인덱스."""
    pos, vel = float(obs[0]), float(obs[1])
    pos_n = np.clip(
        int((pos - POS_MIN) / (POS_MAX - POS_MIN) * N_POS_BINS), 0, N_POS_BINS - 1
    )
    vel_n = np.clip(
        int((vel - VEL_MIN) / (VEL_MAX - VEL_MIN) * N_VEL_BINS), 0, N_VEL_BINS - 1
    )
    return pos_n * N_VEL_BINS + vel_n


def discrete_to_continuous_action(a_idx):
    """이산 행동 인덱스 → env.step에 넣을 연속 행동 [shape (1,)]."""
    return np.array([DISCRETE_ACTIONS[a_idx]], dtype=np.float32)


def print_discretization_info():
    """이산화 Q러닝에서 사용하는 상태/행동 이산화 정보를 간략히 출력."""
    n_s = N_POS_BINS * N_VEL_BINS
    print(
        f"   [이산화] 상태: 위치 [{POS_MIN}, {POS_MAX}] → {N_POS_BINS} bins, "
        f"속도 [{VEL_MIN}, {VEL_MAX}] → {N_VEL_BINS} bins  →  {n_s}개 상태"
    )
    print(f"   [이산화] 행동: 추력 5단계 {DISCRETE_ACTIONS.tolist()}  →  Q테이블 shape ({n_s}, {N_ACTIONS})")
    print()


def train_discretized_qlearning(
    env,
    n_episodes=3000,
    alpha=0.12,
    gamma=0.99,
    epsilon_start=1.0,
    epsilon_decay=0.9995,
    epsilon_min=0.02,
):
    """이산화 Q러닝 학습. env는 render_mode=None 권장."""
    n_s = N_POS_BINS * N_VEL_BINS
    n_a = N_ACTIONS
    Q = np.zeros((n_s, n_a))
    epsilon = epsilon_start
    returns_list = []

    for ep in range(n_episodes):
        obs, _ = env.reset()
        s = discretize_state(obs)
        total_reward = 0
        done = False

        while not done:
            if np.random.random() < epsilon:
                a_idx = np.random.randint(0, N_ACTIONS)
            else:
                a_idx = int(np.argmax(Q[s]))

            action = discrete_to_continuous_action(a_idx)
            next_obs, reward, term, trunc, _ = env.step(action)
            done = term or trunc
            s_next = discretize_state(next_obs)

            td_target = reward + gamma * Q[s_next].max()
            Q[s, a_idx] += alpha * (td_target - Q[s, a_idx])

            s = s_next
            total_reward += reward

        epsilon = max(epsilon_min, epsilon * epsilon_decay)
        returns_list.append(total_reward)
        if (ep + 1) % 1000 == 0:
            avg = np.mean(returns_list[-500:]) if len(returns_list) >= 500 else np.mean(returns_list)
            print(f"  [Q러닝] Episode {ep+1}/{n_episodes}, epsilon={epsilon:.3f}, avg500={avg:.1f}")

    return Q, returns_list


def evaluate_discretized_q(env, Q, n_episodes=10):
    """이산화 Q 정책으로 n_episodes 평가, 평균/표준편차 리워드 반환."""
    rewards = []
    for _ in range(n_episodes):
        obs, _ = env.reset()
        total = 0
        done = False
        while not done:
            s = discretize_state(obs)
            a_idx = int(np.argmax(Q[s]))
            action = discrete_to_continuous_action(a_idx)
            obs, reward, term, trunc, _ = env.step(action)
            total += reward
            done = term or trunc
        rewards.append(total)
    return float(np.mean(rewards)), float(np.std(rewards)), rewards


# ---------------------------------------------------------------------------
# PPO (stable-baselines3) + ShapedReward
# ---------------------------------------------------------------------------
class ShapedRewardWrapper(gym.Wrapper):
    """높이(위치) 보너스로 학습 곡선 부드럽게. 목표(0.45) 방향 기울기 제공."""

    def __init__(self, env, scale=1.0):
        super().__init__(env)
        self.scale = scale

    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)
        position = float(obs[0])
        shaping_reward = max(0, position + 0.5) * self.scale
        return obs, reward + shaping_reward, terminated, truncated, info


def evaluate_sb3(env, model, n_episodes=10):
    """SB3 모델로 n_episodes 평가."""
    rewards = []
    for _ in range(n_episodes):
        obs, _ = env.reset()
        total = 0
        done = False
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, term, trunc, _ = env.step(action)
            total += reward
            done = term or trunc
        rewards.append(total)
    return float(np.mean(rewards)), float(np.std(rewards)), rewards


def get_or_train_ppo(
    env_id,
    total_timesteps=100_000,
    gamma=0.9999,
    ent_coef=0.01,
    use_sde=True,
    sde_sample_freq=4,
    use_shaping=True,
    shaping_scale=1.0,
    log_std_init=-1.0,
    n_steps=4096,
    seed=0,
):
    """모델 파일이 있으면 로드, 없으면 gSDE+ShapedReward 적용 PPO로 학습 후 저장. 반환: model."""
    import torch.nn as nn
    from stable_baselines3 import PPO

    if os.path.exists(PPO_MODEL_PATH):
        print(f"   PPO 모델 로드: {PPO_MODEL_PATH}")
        return PPO.load(PPO_MODEL_PATH)

    env = gym.make(env_id, render_mode=None)
    if use_shaping:
        env = ShapedRewardWrapper(env, scale=shaping_scale)
    model = PPO(
        policy="MlpPolicy",
        env=env,
        learning_rate=3e-4,
        n_steps=n_steps,
        batch_size=64,
        n_epochs=10,
        gamma=gamma,
        gae_lambda=0.98,
        ent_coef=ent_coef,
        use_sde=use_sde,
        sde_sample_freq=sde_sample_freq,
        policy_kwargs=dict(
            net_arch=[64, 64],
            activation_fn=nn.Tanh,
            log_std_init=log_std_init,
        ),
        verbose=1,
        seed=seed,
    )
    model.learn(total_timesteps=total_timesteps)
    os.makedirs(MODELS_DIR, exist_ok=True)
    model.save(PPO_MODEL_PATH)
    env.close()
    print(f"   PPO 모델 저장: {PPO_MODEL_PATH}")
    return model


def record_episode_to_video(
    env_id, get_action_fn, video_path, fps=50, use_shaping=False, shaping_scale=1.0
):
    """
    환경에서 1 에피소드 재생하며 rgb_array 프레임 수집 후 MP4 저장.
    get_action_fn(obs) -> action. use_shaping: PPO와 동일하게 ShapedReward 적용 시 True.
    반환: 해당 에피소드 총 보상.
    """
    env = gym.make(env_id, render_mode="rgb_array")
    if use_shaping:
        env = ShapedRewardWrapper(env, scale=shaping_scale)
    obs, _ = env.reset()
    frames = []
    total_reward = 0
    done = False
    while not done:
        action = get_action_fn(obs)
        obs, reward, term, trunc, _ = env.step(action)
        total_reward += reward
        done = term or trunc
        frame = env.render()
        if frame is not None:
            frames.append(frame)
    env.close()

    if frames:
        os.makedirs(RENDERS_DIR, exist_ok=True)
        ext = os.path.splitext(video_path)[1].lower()
        if ext == ".mp4":
            # MP4: 용량 작음. imageio는 ffmpeg/pyav 플러그인 사용 (pip install imageio[ffmpeg] 권장)
            imageio.v3.imwrite(video_path, np.array(frames, dtype=np.uint8), fps=fps, codec="libx264")
        else:
            imageio.mimsave(video_path, frames, duration=1.0 / fps, loop=0)
    return total_reward


# ---------------------------------------------------------------------------
# 비교 결과 pygame 시각화
# ---------------------------------------------------------------------------
def draw_comparison_pygame(results, n_eval=10):
    """results: [(method_name, mean, std, color), ...]. pygame 창에 막대 그래프 + 텍스트."""
    import pygame

    pygame.init()
    width, height = 520, 380
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("MountainCarContinuous-v0 리워드 비교")

    font_l = pygame.font.Font(None, 28)
    font_s = pygame.font.Font(None, 22)
    bg = (28, 32, 40)
    panel = (40, 44, 52)
    white = (240, 248, 255)
    colors = [
        (120, 200, 120),  # Q러닝
        (255, 180, 100),  # PPO
    ]

    # 리워드 범위로 막대 스케일 (음수 ~ 양수 가능)
    means = [r[1] for r in results]
    stds = [r[2] for r in results]
    lo = min(means) - (max(stds) if stds else 10)
    hi = max(means) + (max(stds) if stds else 10)
    if hi - lo < 20:
        mid = (lo + hi) / 2
        lo, hi = mid - 60, mid + 60
    scale_y = 180 / max(hi - lo, 1)
    base_y = 260

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN) or (event.type == pygame.MOUSEBUTTONDOWN):
                running = False

        screen.fill(bg)
        # 제목
        title = font_l.render("MountainCarContinuous-v0  Reward comparison", True, white)
        screen.blit(title, (20, 16))
        sub = font_s.render(f"(mean +/- std over {n_eval} episodes)", True, (180, 180, 180))
        screen.blit(sub, (20, 42))

        # 0 기준선
        zero_y = base_y + (0 - lo) * scale_y
        pygame.draw.line(screen, (80, 80, 80), (80, zero_y), (width - 40, zero_y), 1)

        # 막대
        bar_w = 80
        gap = 40
        start_x = 100
        for i, (name, mean, std, _) in enumerate(results):
            x = start_x + i * (bar_w + gap)
            color = colors[i % len(colors)]
            # 막대 높이: mean 기준
            h = mean * scale_y
            if h >= 0:
                bar_y = zero_y - h
                pygame.draw.rect(screen, color, (x, bar_y, bar_w, h))
            else:
                bar_y = zero_y
                pygame.draw.rect(screen, color, (x, bar_y, bar_w, -h))
            # std 오차선 (작은 세로선)
            pygame.draw.line(
                screen, (255, 255, 200),
                (x + bar_w // 2, zero_y - (mean - std) * scale_y),
                (x + bar_w // 2, zero_y - (mean + std) * scale_y),
                2,
            )
            label = font_s.render(name, True, white)
            screen.blit(label, (x, base_y + 18))
            val = font_s.render(f"{mean:.1f}±{std:.1f}", True, (200, 200, 200))
            screen.blit(val, (x, base_y + 38))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


# ---------------------------------------------------------------------------
# 메인
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="MountainCarContinuous-v0: 이산화 Q러닝 vs PPO"
    )
    parser.add_argument(
        "--render_mode",
        choices=["all", "play", "none"],
        default="none",
        help="all: 학습 시연+비교창, play: 비교창만, none: 콘솔만 (기본값)",
    )
    parser.add_argument(
        "--q_episodes",
        type=int,
        default=3000,
        help="이산화 Q러닝 에피소드 수",
    )
    parser.add_argument(
        "--ppo_timesteps",
        type=int,
        default=100_000,
        help="PPO 학습 타임스텝 (기본 10만)",
    )
    parser.add_argument(
        "--no_shaping",
        action="store_true",
        help="Q러닝·PPO 공통 ShapedReward(높이 보너스) 비활성화",
    )
    parser.add_argument(
        "--shaping_scale",
        type=float,
        default=1.0,
        help="Q러닝·PPO 공통 높이 보너스 스케일 (기본 1.0)",
    )
    parser.add_argument(
        "--n_eval",
        type=int,
        default=10,
        help="평가 에피소드 수 (각 방법당)",
    )
    args = parser.parse_args()

    env_id = "MountainCarContinuous-v0"
    render_compare = args.render_mode in ("all", "play")

    # 환경: 학습 시 기본 none
    def make_env(render=None):
        return gym.make(env_id, render_mode=render)

    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(RENDERS_DIR, exist_ok=True)
    use_shaping = not args.no_shaping

    # ----- 1) 이산화 Q러닝 (ShapedReward 적용 시 동일) -----
    print("1) 이산화 Q러닝 학습 중...")
    if use_shaping:
        print(f"   ShapedReward 적용 (높이 보너스 scale={args.shaping_scale})")
    print_discretization_info()
    env_q = make_env(render=None)
    if use_shaping:
        env_q = ShapedRewardWrapper(env_q, scale=args.shaping_scale)
    Q, _ = train_discretized_qlearning(
        env_q, n_episodes=args.q_episodes,
        alpha=0.12, gamma=0.99,
        epsilon_start=1.0, epsilon_decay=0.9995, epsilon_min=0.02,
    )
    env_q.close()

    env_eval = make_env(render=None)
    if use_shaping:
        env_eval = ShapedRewardWrapper(env_eval, scale=args.shaping_scale)
    mean_q, std_q, _ = evaluate_discretized_q(env_eval, Q, n_episodes=args.n_eval)
    env_eval.close()
    print(f"   이산화 Q러닝 평가 ({args.n_eval} 에피소드): mean={mean_q:.1f}, std={std_q:.1f}")

    def get_action_q(obs):
        s = discretize_state(obs)
        return discrete_to_continuous_action(int(np.argmax(Q[s])))

    reward_vid_q = record_episode_to_video(
        env_id, get_action_q, VIDEO_Q_PATH,
        use_shaping=use_shaping, shaping_scale=args.shaping_scale,
    )
    print(f"   Q러닝 1에피소드 재생 MP4 저장: {VIDEO_Q_PATH}  (reward={reward_vid_q:.1f})")

    # ----- 2) PPO (gSDE + ShapedReward) -----
    print("\n2) PPO (모델 있으면 로드, 없으면 gSDE+ShapedReward 적용 학습 후 저장)...")
    model_ppo = get_or_train_ppo(
        env_id,
        total_timesteps=args.ppo_timesteps,
        gamma=0.9999,
        ent_coef=0.01,
        use_sde=True,
        sde_sample_freq=4,
        use_shaping=use_shaping,
        shaping_scale=args.shaping_scale,
        log_std_init=-1.0,
        n_steps=4096,
    )

    env_eval = make_env(render=None)
    if use_shaping:
        env_eval = ShapedRewardWrapper(env_eval, scale=args.shaping_scale)
    mean_ppo, std_ppo, _ = evaluate_sb3(env_eval, model_ppo, n_episodes=args.n_eval)
    env_eval.close()
    print(f"   PPO 평가 ({args.n_eval} 에피소드): mean={mean_ppo:.1f}, std={std_ppo:.1f}")

    print("   PPO 녹화: 위에서 학습/로딩한 동일 모델로 1에피소드 재생 중...")
    reward_vid_ppo = record_episode_to_video(
        env_id,
        lambda obs: model_ppo.predict(obs, deterministic=True)[0],
        VIDEO_PPO_PATH,
        use_shaping=use_shaping,
        shaping_scale=args.shaping_scale,
    )
    print(f"   PPO 1에피소드 재생 MP4 저장: {VIDEO_PPO_PATH}  (reward={reward_vid_ppo:.1f})")

    # ----- 비교 요약 -----
    print("\n--- 리워드 비교 요약 ---")
    print(f"  이산화 Q러닝:  {mean_q:+.1f} ± {std_q:.1f}")
    print(f"  PPO:           {mean_ppo:+.1f} ± {std_ppo:.1f}")

    print("\n--- 비교용 영상 (1에피소드 재생, MP4) ---")
    print(f"  Q러닝:  {VIDEO_Q_PATH}")
    print(f"  PPO:    {VIDEO_PPO_PATH}")

    if render_compare:
        results = [
            ("Discretized Q", mean_q, std_q, None),
            ("PPO", mean_ppo, std_ppo, None),
        ]
        draw_comparison_pygame(results, n_eval=args.n_eval)


if __name__ == "__main__":
    main()
