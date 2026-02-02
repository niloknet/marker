"""
CartPole-v1 Streamlit 앱 (1일차 실습)

실행: streamlit run day1/03_cartpole_streamlit.py
"""
import sys

import gymnasium as gym
import streamlit as st

# python으로 실행하면 session state가 동작하지 않음 → 안내 후 종료
if __name__ == "__main__":
    try:
        from streamlit.runtime.scriptrunner_utils.script_run_context import (
            get_script_run_ctx,
        )
        if get_script_run_ctx() is None:
            print(
                "이 앱은 'streamlit run'으로 실행하세요. 'python'으로 실행하면 동작하지 않습니다.",
                file=sys.stderr,
            )
            print("  streamlit run day1/03_cartpole_streamlit.py", file=sys.stderr)
            sys.exit(1)
    except Exception:
        pass

st.set_page_config(layout="wide")
st.title("🛺 CartPole-v1 Gymnasium 환경 Streamlit 앱")

if "env" not in st.session_state:
    st.session_state.env = gym.make("CartPole-v1", render_mode="rgb_array")


def reset_environment():
    observation, info = st.session_state.env.reset()
    st.session_state.state = observation
    st.session_state.reward = 0.0
    st.session_state.terminated = False
    st.session_state.truncated = False
    st.session_state.total_reward = 0.0
    st.session_state.step_count = 0


def take_step(action):
    if st.session_state.terminated or st.session_state.truncated:
        st.warning("⚠️ 게임이 종료되었습니다. '다시 시작' 버튼을 눌러주세요.")
        return
    next_state, reward, terminated, truncated, info = st.session_state.env.step(action)
    st.session_state.state = next_state
    st.session_state.reward = reward
    st.session_state.terminated = terminated
    st.session_state.truncated = truncated
    st.session_state.total_reward += reward
    st.session_state.step_count += 1


if "state" not in st.session_state:
    reset_environment()

col1, col2 = st.columns([2, 1])
with col1:
    st.header("CartPole 시뮬레이션")
    img_array = st.session_state.env.render()
    st.image(
        img_array,
        caption=f"스텝: {st.session_state.step_count}, 총 보상: {st.session_state.total_reward:.1f}",
        width="stretch",
    )

with col2:
    st.header("환경 정보 및 제어")
    st.subheader("현재 스텝 결과")
    st.write(f"**보상 (Reward):** {st.session_state.reward:.1f}")
    st.write(
        f"**에피소드 종료 (Terminated):** {'예' if st.session_state.terminated else '아니오'}"
    )
    st.write(
        f"**시간 초과 (Truncated):** {'예' if st.session_state.truncated else '아니오'}"
    )
    st.subheader("현재 상태 (Observation)")
    state_labels = [
        "카트 위치 (Cart Position)",
        "카트 속도 (Cart Velocity)",
        "막대 각도 (Pole Angle)",
        "막대 각속도 (Pole Angular Velocity)",
    ]
    for i, (val, label) in enumerate(zip(st.session_state.state, state_labels)):
        st.write(f"  - **[{i}] {label}:** {val:+.6f}")
    st.subheader("행동 선택 (Action)")
    b1, b2 = st.columns(2)
    with b1:
        st.button("⬅️ 왼쪽으로 밀기", on_click=take_step, args=(0,))
    with b2:
        st.button("➡️ 오른쪽으로 밀기", on_click=take_step, args=(1,))
    if st.session_state.terminated or st.session_state.truncated:
        st.markdown("---")
        st.error("🎮 게임 오버!")
        st.write(f"최종 스텝 수: {st.session_state.step_count}")
        st.write(f"총 보상: {st.session_state.total_reward:.1f}")
        st.button("다시 시작", on_click=reset_environment)
