"""
지도 학습과 비지도 학습 비교 (scikit-learn 예제)

머신러닝의 두 가지 패러다임을 scikit-learn 코드로 이해합니다.
"""

from sklearn.datasets import load_iris, load_wine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, confusion_matrix
import numpy as np


def _log(msg, indent=0):
    prefix = "  " * indent
    print(f"{prefix}{msg}")


# =============================================================================
# 1. 지도 학습 (Supervised Learning)
# =============================================================================
# - 입력 X와 정답 레이블 Y가 주어짐
# - 학습 목표: f(X) ≈ Y
# - 예: 이미지 분류, 회귀 예측

def supervised_learning_example():
    """지도 학습: 정답(레이블)을 알려주고 배움 — scikit-learn 분류 예제"""
    print("\n[지도 학습] 단계별 로그")
    print("-" * 50)

    # scikit-learn 내장 데이터: Iris (붓꽃 분류)
    _log("1. load_iris()으로 Iris(붓꽃) 데이터 로드", 0)
    iris = load_iris()
    X, y = iris.data, iris.target
    target_names = iris.target_names
    _log(f"   → X.shape = {X.shape}, y.shape = {y.shape}", 1)
    _log(f"   → 특성 이름: {list(iris.feature_names)}", 1)
    _log(f"   → 클래스(품종): {list(target_names)} (레이블 0,1,2)", 1)

    _log("2. train_test_split()으로 훈련 70% / 테스트 30% 분할", 0)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    _log(f"   → 훈련: X_train {X_train.shape}, y_train {y_train.shape}", 1)
    _log(f"   → 테스트: X_test {X_test.shape}, y_test {y_test.shape}", 1)

    _log("3. LogisticRegression 모델 생성 후 fit(X_train, y_train) 호출", 0)
    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)
    _log("   → 학습 완료 (정답 y를 사용해 X→y 매핑 학습)", 1)

    _log("4. model.predict(X_test)로 테스트셋 예측", 0)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    _log(f"   → 맞춘 개수: {(y_pred == y_test).sum()} / {len(y_test)}", 1)
    _log(f"   → 정확도(accuracy): {acc:.4f} ({acc:.2%})", 1)

    cm = confusion_matrix(y_test, y_pred)
    _log("5. 혼동 행렬 (confusion_matrix):", 0)
    header = "   예측→  " + "  ".join(f"{target_names[j]:>10}" for j in range(len(target_names)))
    _log(header, 1)
    for i, row in enumerate(cm):
        _log(f"   실제 {target_names[i]:10} " + "  ".join(f"{v:6d}" for v in row), 1)

    print("-" * 50)
    return f"정답(레이블)이 있음 → 손실 최소화로 학습 → 테스트 정확도: {acc:.2%}"


# =============================================================================
# 2. 비지도 학습 (Unsupervised Learning)
# =============================================================================
# - 입력 X만 주어짐 (정답 없음)
# - 학습 목표: 데이터의 구조/패턴 발견
# - 예: 클러스터링, 차원 축소

def unsupervised_learning_example():
    """비지도 학습: 정답 없이 구조 발견 — scikit-learn K-Means 클러스터링"""
    print("\n[비지도 학습] 단계별 로그")
    print("-" * 50)

    # scikit-learn 내장 데이터: Wine (와인 품종, 레이블은 사용하지 않음)
    _log("1. load_wine()으로 Wine(와인) 데이터 로드 (레이블 미사용)", 0)
    wine = load_wine()
    X = wine.data
    _log(f"   → X.shape = {X.shape} (특성만 사용, 정답 y는 학습에 사용하지 않음)", 1)
    _log(f"   → 특성 이름: {list(wine.feature_names)[:5]} ... (총 {X.shape[1]}개)", 1)

    _log("2. KMeans(n_clusters=3) 생성 후 fit_predict(X) 호출", 0)
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)
    _log("   → 레이블 없이 X만으로 3개 그룹(클러스터) 할당 완료", 1)

    _log("3. 클러스터별 샘플 개수:", 0)
    unique, counts = np.unique(labels, return_counts=True)
    for c, n in zip(unique, counts):
        _log(f"   클러스터 {c}: {n}개", 1)
    _log(f"   → 총 {len(set(labels))}개 클러스터", 1)

    _log("4. 평균 클러스터 중심 (각 클러스터에 속한 샘플들의 특성별 평균):", 0)
    for i, center in enumerate(kmeans.cluster_centers_):
        vals = np.round(center, 3).tolist()
        _log(f"   클러스터 {i} 평균 = {vals}", 1)

    print("-" * 50)
    return f"정답 없음 → 데이터 패턴으로 {len(set(labels))}개 그룹(클러스터) 발견"


# =============================================================================
# 비교표 출력
# =============================================================================
def print_comparison():
    print("=" * 60)
    print("머신러닝 두 가지 패러다임 비교 (지도 vs 비지도)")
    print("=" * 60)
    print()
    print("| 구분        | 지도 학습      | 비지도 학습    |")
    print("|-------------|----------------|----------------|")
    print("| 학습 신호   | 정답 레이블    | 없음           |")
    print("| 목표        | X→Y 매핑      | 구조 발견      |")
    print("| 예시        | 분류, 회귀     | 클러스터링     |")
    print("| scikit-learn| fit(X, y)      | fit(X)         |")
    print()


if __name__ == "__main__":
    print_comparison()

    print("\n" + "=" * 60)
    print("실행: 지도 학습 예제")
    print("=" * 60)
    result_supervised = supervised_learning_example()
    print("\n[지도 학습 요약]", result_supervised)

    print("\n" + "=" * 60)
    print("실행: 비지도 학습 예제")
    print("=" * 60)
    result_unsupervised = unsupervised_learning_example()
    print("\n[비지도 학습 요약]", result_unsupervised)

    print("\n" + "=" * 60)
    print("전체 실행 완료")
    print("=" * 60)
