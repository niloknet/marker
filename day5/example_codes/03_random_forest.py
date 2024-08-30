import numpy as np
from sklearn.ensemble import RandomForestClassifier
from data_utils import load_datasets, preprocess_and_split, evaluate_model

# 데이터셋 로드
datasets = load_datasets()

# 각 데이터셋에 대해 반복
for dataset_name, (X, y) in datasets.items():
    # 데이터 전처리 및 분할
    X_train, X_test, y_train, y_test = preprocess_and_split(X, y)
    
    # 랜덤 포레스트 모델 초기화
    model = RandomForestClassifier(random_state=42)
    
    # 모델 평가
    print(f"\n{dataset_name} Dataset - Random Forest:")
    evaluate_model(model, X_train, y_train, X_test, y_test, "Random Forest", np.unique(y))
    