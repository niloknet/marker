"""
Streamlit에 보상 그래프 기능 추가
Q-러닝 학습 곡선, Q-테이블 시각화

실행: streamlit run app.py
"""

import streamlit as st
import gymnasium as gym
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# 한글 제외: matplotlib는 영문 폰트만 사용해 렌더 문제 방지
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.unicode_minus"] = False

st.set_page_config(page_title="Q-러닝 대시보드", layout="wide")
st.title("Q-러닝 대시보드")

col1, col2 = st.columns(2)
with col1:
    n_episodes = st.slider("에피소드 수", 500, 5000, 2000)
    alpha = st.slider("학습률 α", 0.01, 0.5, 0.1, 0.01)
with col2:
    gamma = st.slider("할인율 γ", 0.9, 1.0, 0.99, 0.01)
    env_name = st.selectbox("환경", ["FrozenLake-v1", "Taxi-v3"], 0)

run = st.button("학습 실행")

if run:
    if env_name == "FrozenLake-v1":
        env = gym.make("FrozenLake-v1", map_name="4x4")
    else:
        env = gym.make("Taxi-v3")
    
    n_s = env.observation_space.n
    n_a = env.action_space.n
    Q = np.zeros((n_s, n_a))
    eps = 1.0
    returns_list = []
    
    progress = st.progress(0)
    for ep in range(n_episodes):
        s, _ = env.reset()
        total = 0
        done = False
        while not done:
            a = env.action_space.sample() if np.random.random() < eps else np.argmax(Q[s])
            s2, r, term, trunc, _ = env.step(a)
            done = term or trunc
            Q[s, a] += alpha * (r + gamma * Q[s2].max() - Q[s, a])
            s = s2
            total += r
        eps = max(0.01, eps * 0.995)
        returns_list.append(total)
        progress.progress((ep + 1) / n_episodes)
    env.close()
    progress.empty()
    
    st.success(f"학습 완료. 평균 보상(마지막 100): {np.mean(returns_list[-100:]):.2f}")
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(returns_list, alpha=0.5)
    window = min(100, len(returns_list) // 10)
    if window > 0:
        smoothed = np.convolve(returns_list, np.ones(window)/window, mode='valid')
        ax.plot(range(window-1, len(returns_list)), smoothed, 'r-', linewidth=2, label='Moving avg')
    ax.set_xlabel("Episode")
    ax.set_ylabel("Reward")
    ax.set_title("Learning curve")
    ax.legend()
    st.pyplot(fig)
    plt.close()
    
    st.subheader("Q-테이블 히트맵")
    fig2, ax2 = plt.subplots(figsize=(10, 8))
    im = ax2.imshow(Q, cmap='YlOrRd', aspect='auto')
    ax2.set_xlabel("Action")
    ax2.set_ylabel("State")
    plt.colorbar(im, ax=ax2)
    st.pyplot(fig2)
    plt.close()
