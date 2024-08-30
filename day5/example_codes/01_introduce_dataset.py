from data_utils import load_breast_cancer_dataset, load_titanic_dataset, load_digits_dataset
import pandas as pd

def get_dataset_info(X, y):
    # 입력 수와 종류
    input_count = X.shape[1]
    input_types = X.dtypes.apply(lambda x: x.name).unique().tolist()
    
    # 출력 수와 종류
    output_count = 1
    output_type = y.dtype.name
    
    # 상위 2개 데이터
    top_data = X.head(2)
    
    return {
        'Input Count': input_count,
        'Input Types': input_types,
        'Output Count': output_count,
        'Output Type': output_type,
        'Top Data': top_data
    }

# 데이터셋 로드
datasets = {
    'Breast Cancer': load_breast_cancer_dataset(),
    'Titanic': load_titanic_dataset(),
    'Digits': load_digits_dataset()
}

# 각 데이터셋에 대한 정보 출력
for dataset_name, (X, y) in datasets.items():
    # DataFrame으로 변환 (필요한 경우)
    if not isinstance(X, pd.DataFrame):
        X = pd.DataFrame(X)
    if not isinstance(y, pd.Series):
        y = pd.Series(y)
    
    # 데이터셋 정보 가져오기
    info = get_dataset_info(X, y)
    
    # 정보 출력
    print(f"\n{dataset_name} Dataset:")
    print(f"입력 수: {info['Input Count']}")
    print(f"입력 종류: {info['Input Types']}")
    print(f"출력 수: {info['Output Count']}")
    print(f"출력 종류: {info['Output Type']}")
    print(f"상위 2개 데이터:\n{info['Top Data']}")