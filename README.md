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
