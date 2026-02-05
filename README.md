# 내 손으로 조작하며 배우는 5일 강화학습

5일 동안 실습 중심으로 강화학습(Reinforcement Learning)을 배우는 교육 자료입니다.

---

## 📅 1일차: 강화학습의 기본 재료

### 슬라이드
- **[1일차 슬라이드 (Google Slides)](https://docs.google.com/presentation/d/1O0jhtoBpirw4rwFN7P22uf0R9Hb1dxXhJfXHK2uvXWE/edit)**
- **[2일차 슬라이드 (Google Slides)](https://docs.google.com/presentation/d/1Ru9jaxTsFyj013mYSva3pBKUpWVlfvpHygTDBJZbiPk/edit)**
- **[3일차 슬라이드 (Google Slides)](https://docs.google.com/presentation/d/1gtWKwWt3dqAbaH0d7c_0UX2JL1KLGiS7Li0vhQbarZw/edit)**
- **[4일차 슬라이드 (Google Slides)](https://docs.google.com/presentation/d/17APDWVy4amnpWtT_Wcmh-QHoQDamwyo27ItDrQSl7YQ/edit)**
- **[5일차 슬라이드 (Google Slides)](https://docs.google.com/presentation/d/10Rl-3eAGIML4Fxpusg0Sv3D2A1laKbzineoyvg48Fy4/edit)**


### 1일차 파일 구성
| 파일 | 설명 |
|------|------|
| `day1/01_ml_paradigms.py` | 지도/비지도학습과 강화학습 비교 (scikit-learn 예제) |
| `day1/02_cartpole_demo.ipynb` | Gymnasium CartPole 환경 기초 실습 |
| `day1/03_cartpole_streamlit.py` | CartPole Streamlit 앱 (`streamlit run day1/03_cartpole_streamlit.py`) |
| `day1/04_cartpole_streamlit_colab.ipynb` | **Colab 전용** Gymnasium + Streamlit 실습 (TODO: `take_step` 등 직접 구현) |
| `day1/05_cartpole_streamlit_colab_runable.ipynb` | **Colab 전용** 04와 동일 실습이지만 구현이 완료된 실행 가능 버전 (참고용) |
| `day1/06_cartpole_dqn_demo.ipynb` | DQN으로 CartPole 학습 (PyTorch, 경험 리플레이, epsilon-greedy, 학습 전·후 GIF 저장) |

---

## 📅 2일차: MDP와 파라미터 튜닝

### 2일차 파일 구성
| 파일 | 설명 |
|------|------|
| `day2/01_grid_world_overlay.py` | 나만의 그리드 월드 (클릭 편집, 할인율 γ 슬라이더, Value Iteration 가치 히트맵) — `streamlit run day2/01_grid_world_overlay.py` |
| `day2/02_frozenlake_intro.ipynb` | FrozenLake-v1 환경 소개 (상태·행동·보상, 맵 시각화) |
| `day2/03_frozenlake_manual.py` | FrozenLake 버튼 조종 (is_slippery=False, 결정적 이동) — `streamlit run day2/03_frozenlake_manual.py` |
| `day2/04_frozenlake_manual_slippy.py` | FrozenLake 버튼 조종 (is_slippery=True, 미끄러짐) — `streamlit run day2/04_frozenlake_manual_slippy.py` |
| `day2/05_env_P_analysis.ipynb` | FrozenLake env.P (전이 확률) 분석 노트북 |
| `day2/06_hill_climbing_cartpole.py` | 힐 클라이밍 CartPole (선형 정책 + 무작위 섭동) — `python day2/06_hill_climbing_cartpole.py [--render_mode all\|play\|none]` |
| `day2/07_hill_climbing_mountaincar.py` | 힐 클라이밍 MountainCar Continuous (선형 정책, 보상 shaping) — `python day2/07_hill_climbing_mountaincar.py [--render_mode all\|play\|none]` |
| `day2/08_colab_gradio_cartpole.ipynb` | **Colab 전용** CartPole 힐 클라이밍 (Gradio UI) |
| `day2/09_colab_gradio_mountaincar.ipynb` | **Colab 전용** MountainCar Continuous 힐 클라이밍 (Gradio UI) |
| `day2/render_helpers.py` | 06·07 로컬 렌더용 헬퍼 (Pygame 창, 오버레이) |

---

## 📅 3일차: Q-러닝과 Taxi-v3 정복

### 3일차 파일 구성
| 파일 | 설명 |
|------|------|
| `day3/01_frozenlake_qlearning_pygame.py` | FrozenLake 4x4 Q-러닝 학습 후 Pygame 시각화 (맵 + 정보 패널). `python day3/01_frozenlake_qlearning_pygame.py [--render_mode all\|play\|none] [--slippery]` |
| `day3/02_taxi_qlearning_pygame.py` | Taxi-v3 Q-러닝 학습 후 Pygame 시각화 (맵 + 정보 패널). `python day3/02_taxi_qlearning_pygame.py [--render_mode all\|play\|none]` |
| `day3/03_qlearning_dashboard.py` | Q-러닝 대시보드 (학습 곡선, Q-테이블 히트맵). FrozenLake-v1 / Taxi-v3 선택. `streamlit run day3/03_qlearning_dashboard.py` |
| `day3/04_qtable_heatmap.ipynb` | Q-테이블 히트맵 시각화 및 학습 결과 확인 (Gradio, Colab 활용). FrozenLake 4x4, 최적 경로·영역 표시 |
| `day3/06_cliffwalking_qlearning_pygame.py` | CliffWalking-v1 Q-러닝 학습 후 Pygame 시각화. `python day3/06_cliffwalking_qlearning_pygame.py [--render_mode all\|play\|none]` |
| `day3/07_cliffwalking_sarsa_pygame.py` | CliffWalking-v1 SARSA 학습 후 Pygame 시각화 (on-policy, Q-러닝과 비교용). `python day3/07_cliffwalking_sarsa_pygame.py [--render_mode all\|play\|none]` |
| `day3/08_mountaincar_continuous_compare.py` | MountainCarContinuous: 이산화 Q-러닝 vs PPO 리워드 비교. ShapedReward, PPO 모델 로드/저장, MP4는 `day3/renders/`에 저장. `python day3/08_mountaincar_continuous_compare.py [--render_mode all\|play\|none]` |


※ 01·02·06·07·08(compare)은 `day2/render_helpers.py`를 사용합니다. Pygame 창에서 학습/재생을 보려면 `--render_mode all` 또는 `play`를 지정하세요.

---

## 📅 4일차: DQN과 LunarLander

### 4일차 파일 구성
| 파일 | 설명 |
|------|------|
| `day4/01_iris_visualization.html` | 신경망 시각화 (Iris, 슬라이더로 가중치 조절) — 브라우저에서 HTML 열기 |
| `day4/02_cartpole_compare.py` | CartPole 비교: 이산화 Q-Learning vs Vanilla DQN vs Stable DQN. 학습 곡선 비교. `day4/models/`에 모델 캐시. `python day4/02_cartpole_compare.py [--total_timesteps 100000] [--seed 0] [--force_train]` |
| `day4/03_dqn_lunarlander_colab.ipynb` | **Colab 전용** DQN으로 LunarLander-v3 학습 (Gradio 하이퍼파라미터, RecordVideo, GPU 지원) |
| `day4/04_policy_kwargs_dqn.py` | DQN 뇌 구조 비교: MlpPolicy + `policy_kwargs` net_arch ([64,64] / 기본 / [256,256,128]). `python day4/04_policy_kwargs_dqn.py [--total_timesteps 50000] [--seed 0] [--out 07_policy_kwargs_compare.png]` |
| `day4/05_dqn_param_effect.py` | DQN 핵심 파라미터 효과: buffer_size, train_freq, target_update_interval (기본 / 공격적 / 보수적). `python day4/05_dqn_param_effect.py [--total_timesteps 50000] [--seed 0] [--out 08_dqn_param_effect.png]` |
| `day4/06_callback_reward_loss_gradio.ipynb` | **Colab 전용** CartPole DQN + Callback으로 보상·Loss 수집, Gradio 학습 곡선 및 Q-value·정책 히트맵 |
| `day4/07_reinforce_gradio_mountaincar.ipynb` | **Colab 전용** MountainCarContinuous REINFORCE (가우시안 정책, 보상 shaping), Gradio UI |
| `day4/08_onpolicy_compare.py` | LunarLander-v3 온폴리시 비교: REINFORCE(PyTorch) vs A2C vs PPO. `day4/models/` 캐시. `python day4/08_onpolicy_compare.py [--total_timesteps 200000] [--seed 0] [--force_train]` |
| `day4/device_utils.py` | SB3/PyTorch용 디바이스 선택 (CUDA → MPS → CPU). 02·04·05·08에서 사용 |

※ 02·08은 `day4/models/`에 모델이 있으면 로드, 없으면 학습 후 저장합니다. 비교 그래프는 `day4/renders/` 등에 PNG로 저장됩니다.

---

## 🗓 전체 로드맵

| 일차 | 주제 |
|------|------|
| 1일차 | 강화학습의 기본 재료 |
| 2일차 | MDP와 파라미터 튜닝 |
| 3일차 | Q-러닝과 Taxi-v3 정복 |
| 4일차 | DQN과 LunarLander |
| 5일차 | 최종 프로젝트: AI 엘리베이터 |

---

## ⚙️ 환경 설정

### Python 설치

#### Windows
- **[Microsoft Store Python 3.12](https://apps.microsoft.com/detail/9NCVDN91XZQP?hl=neutral&gl=KR&ocid=pdpshare)**  
  - Microsoft Store에서 설치하면 `PATH`가 자동 설정됩니다.

#### Linux (Ubuntu/Debian)
```bash
# 기본 저장소에 3.12가 없는 경우 deadsnakes PPA 사용
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update

# Python 3.12 및 venv, pip 설치
sudo apt install python3.12 python3.12-venv python3-pip

# 버전 확인
python3.12 --version
```

### 가상 환경(venv) 생성 및 활성화

```bash
# 프로젝트 폴더에서 venv 생성
python -m venv venv
```

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (명령 프롬프트):**
```batch
venv\Scripts\activate.bat
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

활성화되면 프롬프트 앞에 `(venv)` 표시가 나타납니다.

### 의존성 설치

```bash
pip install -r requirements.txt
```
