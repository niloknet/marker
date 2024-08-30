import numpy as np
import pandas as pd
from sklearn.datasets import load_digits, load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 유방암 데이터셋을 로드하는 함수
def load_breast_cancer_dataset():
    data = load_breast_cancer()
    X = data.data
    y = data.target
    return X, y

# 숫자 데이터셋을 로드하는 함수
def load_digits_dataset():
    data = load_digits()
    X = data.data
    y = data.target
    return X, y

# 타이타닉 데이터셋을 로드하는 전용 함수
def load_titanic_dataset():
    # CSV 파일 경로 설정
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(script_dir, 'titanic.csv')
    
    # 타이타닉 데이터셋 로드
    titanic_data = pd.read_csv(csv_file_path)
    
    # 입력(X)과 출력(y) 데이터 분리
    X_titanic = titanic_data.drop(columns=['Survived'])
    y_titanic = titanic_data['Survived']
    
    return X_titanic, y_titanic

# 모든 데이터셋을 로드하는 함수
def load_datasets():
    breast_cancer = load_breast_cancer_dataset()
    titanic = load_titanic_dataset()
    digits = load_digits_dataset()
    
    return {
        "Breast Cancer": breast_cancer,
        "Titanic": titanic,
        "Digits": digits
    }

# 데이터 전처리 및 분할 함수
def preprocess_and_split(X, y):
    if isinstance(X, np.ndarray):
        X = pd.DataFrame(X)
    
    numeric_features = X.select_dtypes(exclude=['category', 'object']).columns
    X[numeric_features] = X[numeric_features].fillna(X[numeric_features].mean())

    categorical_features = X.select_dtypes(include=['category', 'object']).columns.tolist()
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(), categorical_features)
        ]
    )
    
    pipeline = Pipeline(steps=[('preprocessor', preprocessor)])
    X_processed = pipeline.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

# 모델 평가 함수
def evaluate_model(model, X_train, y_train, X_test, y_test, model_name, class_names):
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, average='weighted')
    recall = recall_score(y_test, predictions, average='weighted')
    f1 = f1_score(y_test, predictions, average='weighted')
    cm = confusion_matrix(y_test, predictions)
    
    print(f"모델 평가 - 정확도: {accuracy:.4f}, 정밀도: {precision:.4f}, "
          f"재현율: {recall:.4f}, F1-점수: {f1:.4f}")
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
    plt.title(f'{model_name} Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.show()

# 모듈로서 사용할 수 있도록 간단하게 정리
__all__ = ['load_breast_cancer_dataset', 'load_digits_dataset', 'load_titanic_dataset', 'load_datasets', 'preprocess_and_split', 'evaluate_model']