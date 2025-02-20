import numpy as np
import random
import time
import pandas as pd
from collections import defaultdict

# 사용자 정의 환경 가져오기
from dynamic_gridworld import DynamicGridWorldEnv

# 하이퍼파라미터
alpha = 0.1  # 학습률
gamma = 0.99  # 할인 계수
epsilon = 1.0  # 탐험률
epsilon_decay = 0.995  # 탐험 감소율
min_epsilon = 0.01  # 최소 탐험률
episodes = 400  # 에피소드 수
max_steps_per_episode = 100  # 에피소드당 최대 스텝 수

# 환경 초기화
env = DynamicGridWorldEnv(size=4, render_mode=None)

# Q-테이블을 0으로 초기화된 defaultdict로 초기화
q_table = defaultdict(lambda: np.zeros(env.action_space.n))

# Q-러닝 알고리즘
for episode in range(episodes):
    obs = env.create_maze()
    state = tuple(obs["agent"])
    total_reward = 0
    
    for step in range(max_steps_per_episode):
        # 입실론-그리디 행동 선택
        if random.uniform(0, 1) < epsilon:
            action = env.action_space.sample()  # 탐험: 무작위 행동
        else:
            action = np.argmax(q_table[state])  # 활용: 알려진 최적의 행동
        
        # 환경에서 행동 수행
        next_obs, reward, done, _ = env.step(action)
        next_state = tuple(next_obs["agent"])
        
        # Q-러닝 공식을 사용하여 Q-값 업데이트
        best_next_action = np.argmax(q_table[next_state])
        q_table[state][action] += alpha * (reward + gamma * q_table[next_state][best_next_action] - q_table[state][action])
        
        state = next_state
        total_reward += reward
        
        if done:
            break
    
    # 각 에피소드 후 엡실론 감소
    epsilon = max(min_epsilon, epsilon * epsilon_decay)
    
    # Q-테이블을 DataFrame으로 변환하여 시각화하고 주기적으로 저장 (예: 10 에피소드마다)
    if (episode + 1) % 10 == 0:
        q_table_df = pd.DataFrame.from_dict(q_table, orient='index', columns=[f'Action_{i}' for i in range(env.action_space.n)]).sort_index()
        q_table_df.index.name = '상태'
        print(f"에피소드 {episode + 1} 이후의 Q-테이블:\n{q_table_df}\n")
        time.sleep(1)  # 렌더링 속도 늦추기
    
print("학습 완료!")

# 학습 완료 후 에이전트 행동 시각화
env = DynamicGridWorldEnv(size=4, render_mode='human')  # render_mode를 'human'으로 변경

obs = env.create_maze()
state = tuple(obs["agent"])
done = False

while not done:
    # 학습된 정책을 사용하여 최적의 행동 선택
    action = np.argmax(q_table[state])
    
    # 환경에서 행동 수행
    next_obs, reward, done, _ = env.step(action)
    next_state = tuple(next_obs["agent"])
    
    state = next_state
    
    # 렌더링 속도 조절
    time.sleep(0.5)  # 0.5초 간격으로 행동 표시
    env.render()  # 현재 상태 시각화

env.close()