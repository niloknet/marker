"""
BuildingElevator-v0 Streamlit 앱 (랜덤 에이전트).

day5/building_elevator_env.py 환경으로 에피소드를 돌리고,
통계(리워드, 배달 수, 대기 인원 등)를 표시합니다.
가속: day4/device_utils (CUDA > MPS > CPU), 필요 시 벡터화 환경 병렬 실행.

설계: 앱 실행 중일 때는 모델(에이전트/환경)을 보유하도록 설계합니다.
예: st.session_state에 env 또는 policy를 보관해 세션 동안 재사용합니다.

공정한 채점을 위해 제출 관련 코드(리더보드 제출, userId/username/score 전송 등)는 수정하지 마세요.
"""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
# day5 환경
sys.path.insert(0, str(_ROOT))
from building_elevator_env import (
    BuildingElevatorEnv,
    LEADERBOARD_URL,
    get_mac_address,
    NUM_FLOORS_DEFAULT,
    NUM_ELEVATORS_DEFAULT,
    DEFAULT_MAX_STEPS,
)
# day4 device_utils (가속용). torch 없으면 CPU로 표시
try:
    sys.path.insert(0, str(_ROOT.parent / "day4"))
    from device_utils import get_device, get_device_name
except Exception:
    def get_device():
        return "cpu"
    def get_device_name(device):
        return "CPU (torch 미설치 시)"

import streamlit as st
import numpy as np


# 앱 실행 중에는 모델(에이전트)을 보유하도록 설계. (예: st.session_state에 env 또는 policy 보관)
def run_episode(env: BuildingElevatorEnv, max_steps: int, seed: int | None):
    """랜덤 에이전트로 1 에피소드 실행. (obs, reward, terminated, truncated, info) 기록 반환."""
    obs, info = env.reset(seed=seed)
    trajectory = {
        "rewards": [],
        "infos": [info],
        "actions": [],
    }
    for _ in range(max_steps - 1):
        action = env.action_space.sample()
        obs, reward, term, trunc, info = env.step(action)
        trajectory["rewards"].append(reward)
        trajectory["infos"].append(info)
        trajectory["actions"].append(int(action))
        if term or trunc:
            break
    return trajectory


def run_episodes_vectorized(num_floors, num_elevators, max_steps, n_episodes, seed, n_envs):
    """SyncVectorEnv로 n_envs개 환경 병렬 실행 (가속)."""
    from gymnasium.vector import SyncVectorEnv

    def make_env():
        def _init():
            return BuildingElevatorEnv(
                num_floors=num_floors,
                num_elevators=num_elevators,
                max_steps=max_steps,
                mode="training",
            )
        return _init

    env = SyncVectorEnv([make_env() for _ in range(n_envs)])
    all_returns = []
    all_delivered = []
    all_max_waiting = []
    obs, _ = env.reset(seed=seed)
    ep_rew = np.zeros(n_envs)
    done_count = 0

    while done_count < n_episodes:
        actions = np.array([env.single_action_space.sample() for _ in range(n_envs)])
        obs, rewards, terms, truncs, infos = env.step(actions)
        ep_rew += rewards
        ed = infos.get("episode_delivered", np.zeros(n_envs, dtype=np.int64))
        mp = infos.get("max_passengers", np.zeros(n_envs, dtype=np.int64))
        if not isinstance(ed, np.ndarray):
            ed = np.full(n_envs, ed if np.isscalar(ed) else 0)
        if not isinstance(mp, np.ndarray):
            mp = np.full(n_envs, mp if np.isscalar(mp) else 0)
        dones = terms | truncs
        for i in range(n_envs):
            if dones[i]:
                done_count += 1
                all_returns.append(float(ep_rew[i]))
                all_delivered.append(int(ed[i]) if i < len(ed) else 0)
                all_max_waiting.append(int(mp[i]) if i < len(mp) else 0)
                ep_rew[i] = 0.0
                if done_count >= n_episodes:
                    break
        if done_count >= n_episodes:
            break
    env.close()
    return all_returns, all_delivered, all_max_waiting


def main():
    st.set_page_config(page_title="Building Elevator (Random Agent)", layout="wide")
    st.title("Building Elevator — 랜덤 에이전트")

    # 가속: device_utils (CUDA > MPS > CPU)
    device = get_device()
    device_label = get_device_name(device)

    # 앱 실행 중 모델(에이전트) 보유: session_state에 에이전트/환경 보관
    if "agent" not in st.session_state:
        st.session_state.agent = {"type": "random"}  # 추후 학습된 policy 등으로 교체 가능
    if "env" not in st.session_state:
        st.session_state.env = None  # 필요 시 한 번 만든 env 재사용

    # 환경·에피소드·스텝은 고정, 학습 iter 수만 조절
    num_floors = NUM_FLOORS_DEFAULT
    num_elevators = NUM_ELEVATORS_DEFAULT
    max_steps = DEFAULT_MAX_STEPS

    with st.sidebar:
        st.caption("**가속**")
        st.text(f"Device: {device_label}")
        n_iters = st.slider("학습 iter 수", 1, 50, 10, help="실행할 에피소드(반복) 수")
        n_envs = st.slider("병렬 env 수 (가속)", 1, 8, 1, help="2 이상이면 벡터화 환경으로 병렬 실행")
        seed = st.number_input("시드 (재현용, -1=랜덤)", value=-1, min_value=-1, step=1)
        run_seed = None if seed < 0 else int(seed)
        st.divider()
        st.caption("**리더보드 제출**")
        username = st.text_input("유저 이름", value="", placeholder="제출 시 표시될 이름")
        do_submit = st.button("제출 (10회 평균)")

    # ---------- 제출 관련: 공정한 채점을 위해 아래 블록은 수정하지 마세요 ----------
    # 제출: 10회 평가 모드 실행 후 평균 점수로 리더보드 제출
    if do_submit:
        try:
            import requests
        except ImportError:
            st.sidebar.error("제출하려면 pip install requests 필요")
        else:
            submit_env = BuildingElevatorEnv(
                num_floors=num_floors,
                num_elevators=num_elevators,
                max_steps=max_steps,
                mode="evaluation",
                submit_score=False,
                user_id=(username.strip() or None),
            )
            SUBMIT_RUNS = 10
            submit_returns = []
            submit_delivered = []
            for _ in range(SUBMIT_RUNS):
                obs, info = submit_env.reset(seed=48879)
                ep_rew = 0.0
                while True:
                    action = submit_env.action_space.sample()
                    obs, r, term, trunc, info = submit_env.step(action)
                    ep_rew += r
                    if term or trunc:
                        break
                submit_returns.append(ep_rew)
                submit_delivered.append(info.get("episode_delivered", 0))
            submit_env.close()
            avg_score = float(np.mean(submit_returns))
            avg_passengers = int(round(np.mean(submit_delivered)))
            user_id_val = username.strip() or get_mac_address()  # userId는 반드시 있음
            user_display = username.strip()
            data = {"userId": user_id_val, "username": user_display, "score": int(round(avg_score)), "passengers": avg_passengers}
            try:
                resp = requests.post(LEADERBOARD_URL, json=data, timeout=10)
                if resp.status_code == 200:
                    st.sidebar.success(f"제출 완료: {user_display or '(이름 없음)'} (10회 평균 {avg_score:.1f}, 배달 {avg_passengers})")
                else:
                    st.sidebar.warning(f"제출 실패: HTTP {resp.status_code}")
            except Exception as e:
                st.sidebar.error(f"제출 오류: {e}")

    if st.button("에피소드 실행"):
        progress = st.progress(0)
        status = st.empty()

        if n_envs <= 1:
            env = BuildingElevatorEnv(
                num_floors=num_floors,
                num_elevators=num_elevators,
                max_steps=max_steps,
                mode="training",
            )
            all_returns = []
            all_delivered = []
            all_max_waiting = []
            for i in range(n_iters):
                status.text(f"에피소드 {i+1}/{n_iters} 실행 중... (Device: {device_label})")
                traj = run_episode(env, max_steps, run_seed)
                last_info = traj["infos"][-1]
                ep_return = sum(traj["rewards"])
                all_returns.append(ep_return)
                all_delivered.append(last_info.get("episode_delivered", 0))
                all_max_waiting.append(last_info.get("max_passengers", 0))
                progress.progress((i + 1) / n_iters)
            env.close()
        else:
            status.text(f"벡터화 환경 {n_envs}개 병렬 실행 중... (Device: {device_label})")
            all_returns, all_delivered, all_max_waiting = run_episodes_vectorized(
                num_floors, num_elevators, max_steps, n_iters, run_seed, n_envs
            )
            progress.progress(1.0)

        status.empty()
        progress.empty()

        st.caption(f"가속: **{device_label}**" + (f" · 병렬 env {n_envs}개" if n_envs > 1 else ""))

        # 요약 통계
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("평균 에피소드 리워드", f"{np.mean(all_returns):.1f}")
        with col2:
            st.metric("평균 배달 수 (에피소드당)", f"{np.mean(all_delivered):.1f}")
        with col3:
            st.metric("평균 최대 대기 인원", f"{np.mean(all_max_waiting):.1f}")

        st.subheader("에피소드별 결과")
        st.dataframe(
            {
                "에피소드": list(range(1, n_iters + 1)),
                "리워드": all_returns,
                "배달 수": all_delivered,
                "최대 대기": all_max_waiting,
            },
            use_container_width=True,
        )


if __name__ == "__main__":
    main()
