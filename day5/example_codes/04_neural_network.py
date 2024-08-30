import warnings
import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier
from data_utils import load_datasets, preprocess_and_split, evaluate_model

warnings.filterwarnings('ignore', category=UserWarning)

# 데이터셋 로드
datasets = load_datasets()

# 각 데이터셋에 대한 최적의 epoch 설정
optimal_epochs = {
    "Breast Cancer": 15,
    "Titanic": 10,
    "Digits": 30
}

# 각 데이터셋에 대해 신경망 모델 평가
for dataset_name, (X, y) in datasets.items():
    X_train, X_test, y_train, y_test = preprocess_and_split(X, y)
    best_epoch = optimal_epochs[dataset_name]

    # 신경망 모델 설정
    model = MLPClassifier(hidden_layer_sizes=(128, 128, 128, 128), 
                          learning_rate_init=0.001, 
                          max_iter=best_epoch, 
                          random_state=42, 
                          warm_start=True)

    # 모델 평가
    print(f"\n{dataset_name} Dataset:")
    evaluate_model(model, X_train, y_train, X_test, y_test, "Neural Network", np.unique(y))