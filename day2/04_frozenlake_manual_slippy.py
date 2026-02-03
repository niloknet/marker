"""
실습 2: 버튼으로 직접 조종 (미끄러짐)

- is_slippery=True: 이동 시 1/3 확률로 의도와 다른 방향으로 미끄러짐 (확률적 환경)
- 방향 버튼을 눌러 한 칸씩 이동
- 목표(G) 도달 또는 구멍(H) 낙사 시 에피소드 종료
- 맵은 Gymnasium Pygame 렌더(rgb_array)로 표시

실행: streamlit run 04_frozenlake_manual_slippy.py
"""

import os
import sys
import warnings

# macOS: pygame/SDL이 창을 열 때 NSException 발생 방지 (SDL 더미 드라이버 사용)
if sys.platform == "darwin":
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

warnings.filterwarnings("ignore", category=UserWarning, message=".*pkg_resources.*")

import streamlit as st
import gymnasium as gym
import numpy as np

LEFT, DOWN, RIGHT, UP = 0, 1, 2, 3
ACTION_NAMES = ["← 왼쪽", "↓ 아래", "→ 오른쪽", "↑ 위"]


def _render_frozenlake_fallback(env, state):
    """Pygame 실패 시(예: macOS) matplotlib로 FrozenLake 그리드 그려 RGB 배열 반환."""
    import io
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    desc = env.unwrapped.desc  # 2D bytes: S, F, H, G
    nrow, ncol = desc.shape
    cell_labels = {b"S": "S", b"F": "F", b"H": "H", b"G": "G"}
    colors = {"S": "#6DD5ED", "F": "#E0F7FA", "H": "#263238", "G": "#81C784"}
    fig, ax = plt.subplots(1, 1, figsize=(ncol * 1.2, nrow * 1.2))
    ax.set_xlim(-0.5, ncol - 0.5)
    ax.set_ylim(nrow - 0.5, -0.5)
    ax.set_aspect("equal")
    ax.axis("off")
    cur_r, cur_c = state // ncol, state % ncol
    for r in range(nrow):
        for c in range(ncol):
            cell = cell_labels.get(desc[r, c], "F")
            face = "#FFF59D" if (r, c) == (cur_r, cur_c) else colors[cell]
            rect = plt.Rectangle((c - 0.5, r - 0.5), 1, 1, facecolor=face, edgecolor="#37474F", linewidth=1.5)
            ax.add_patch(rect)
            ax.text(c, r, cell, ha="center", va="center", fontsize=14, fontweight="bold")
    plt.tight_layout(pad=0.2)
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=100, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    from PIL import Image
    img = np.array(Image.open(buf).convert("RGB"))
    return img


def get_render_frame(env, state=0):
    """env.render()로 현재 상태의 맵 이미지(RGB 배열) 반환. 실패 시 matplotlib 폴백."""
    try:
        frame = env.render()
        if frame is not None and frame.size > 0:
            return frame
    except Exception:
        pass
    # macOS 등에서 pygame/SDL 오류 시 matplotlib로 그리드 렌더
    return _render_frozenlake_fallback(env, state)


def init_session():
    if "env" not in st.session_state:
        st.session_state.env = gym.make(
            "FrozenLake-v1",
            map_name="4x4",
            is_slippery=True,
            render_mode="rgb_array",
        )
        st.session_state.state, _ = st.session_state.env.reset()
        st.session_state.steps = 0
        st.session_state.done = False
        st.session_state.reward = 0


st.set_page_config(page_title="FrozenLake 직접 조종", layout="centered")
st.title("실습 2: FrozenLake 직접 조종 (미끄러짐)")
st.caption("is_slippery=True · 미끄러짐 있음 · 버튼으로 한 칸씩 이동")

init_session()

# 상태 표시
col_info, col_map = st.columns([1, 2])
with col_info:
    st.metric("스텝", st.session_state.steps)
    st.metric("상태(칸 번호)", st.session_state.state)
    if st.session_state.done:
        st.success("목표 도달! 🎉" if st.session_state.reward == 1 else "구멍에 빠짐 💀")

with col_map:
    frame = get_render_frame(st.session_state.env, st.session_state.state)
    if frame is not None:
        st.image(frame, width="stretch", channels="RGB")
    st.caption("Pygame 렌더 · S=시작, F=얼음, H=구멍, G=목표")

# 방향 버튼
st.markdown("**이동할 방향을 선택하세요**")
if not st.session_state.done:
    cols = st.columns(4)
    with cols[0]:
        if st.button("← 왼쪽", key="left"):
            st.session_state.state, st.session_state.reward, term, trunc, _ = (
                st.session_state.env.step(LEFT)
            )
            st.session_state.steps += 1
            st.session_state.done = term or trunc
            st.rerun()
    with cols[1]:
        if st.button("↓ 아래", key="down"):
            st.session_state.state, st.session_state.reward, term, trunc, _ = (
                st.session_state.env.step(DOWN)
            )
            st.session_state.steps += 1
            st.session_state.done = term or trunc
            st.rerun()
    with cols[2]:
        if st.button("→ 오른쪽", key="right"):
            st.session_state.state, st.session_state.reward, term, trunc, _ = (
                st.session_state.env.step(RIGHT)
            )
            st.session_state.steps += 1
            st.session_state.done = term or trunc
            st.rerun()
    with cols[3]:
        if st.button("↑ 위", key="up"):
            st.session_state.state, st.session_state.reward, term, trunc, _ = (
                st.session_state.env.step(UP)
            )
            st.session_state.steps += 1
            st.session_state.done = term or trunc
            st.rerun()
else:
    st.info("에피소드가 종료되었습니다. '다시 시작'을 눌러 새 게임을 시작하세요.")

if st.button("🔄 다시 시작"):
    st.session_state.state, _ = st.session_state.env.reset()
    st.session_state.steps = 0
    st.session_state.done = False
    st.session_state.reward = 0
    st.rerun()
