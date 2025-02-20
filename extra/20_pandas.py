import pandas as pd
import matplotlib.pyplot as plt

# 예제 1: 리스트로부터 Series 생성
print("예제 1: 리스트로부터 Series 생성")
print("-------------------------------")
s = pd.Series([1, 3, 5, 7, 9])
print(s)
print("\n")

# 예제 2: 딕셔너리로부터 DataFrame 생성
print("예제 2: 딕셔너리로부터 DataFrame 생성")
print("-----------------------------------")
data = {'Name': ['Tom', 'Jerry', 'Mickey'],
        'Age': [20, 21, 19]}
df = pd.DataFrame(data)
print(df)
print("\n")

# 예제 3: 중첩 리스트를 DataFrame으로 변환
print("예제 3: 중첩 리스트를 DataFrame으로 변환")
print("--------------------------------------")
nested_list = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
df_nested = pd.DataFrame(nested_list, columns=['Col1', 'Col2'])
print(df_nested)
print("\n")

# 예제 4: 열 선택
print("예제 4: 열 선택")
print("----------------")
ages = df['Age']
print(ages)
print("\n")

# 예제 5: 행 선택
print("예제 5: 행 선택")
print("----------------")
first_row = df.loc[0]
print(first_row)
print("\n")

# 예제 6: 조건 필터링
print("예제 6: 조건 필터링")
print("-------------------")
adults = df[df['Age'] > 30]
print(adults)
print("\n")

# 예제 7: CSV 파일로부터 DataFrame 생성
print("예제 7: CSV 파일로부터 DataFrame 생성")
print("-------------------------------------")
df = pd.read_csv('data.csv')
print(df)
print("\n")

# 예제 8: DataFrame을 CSV 파일로 저장
print("예제 8: DataFrame을 CSV 파일로 저장")
print("------------------------------------")
df.to_csv('output.csv', index=False)
print("\n")

# 예제 9: 데이터 확인 - 상위 5개 행 출력
print("예제 9: 데이터 확인 - 상위 5개 행 출력")
print("-----------------------------------")
print(df.head())
print("\n")

# 예제 10: 데이터 확인 - 데이터프레임 정보 출력
print("예제 10: 데이터 확인 - 데이터프레임 정보 출력")
print("-----------------------------------------")
print(df.info())
print("\n")

# 예제 11: 데이터 확인 - 기술 통계 출력
print("예제 11: 데이터 확인 - 기술 통계 출력")
print("-----------------------------------")
print(df.describe())
print("\n")

# 예제 12: 열 추가
print("예제 12: 열 추가")
print("----------------")
df['City'] = ['New York', 'Los Angeles', 'Chicago']
print(df)
print("\n")

# 예제 13: 행 삭제
print("예제 13: 행 삭제")
print("----------------")
df = df.drop(0)
print(df)
print("\n")

# 예제 14: 열 삭제
print("예제 14: 열 삭제")
print("----------------")
df = df.drop('City', axis=1)
print(df)
print("\n")

# 예제 15: 데이터프레임 병합
print("예제 15: 데이터프레임 병합")
print("--------------------------")
df1 = pd.DataFrame({'Name': ['Alice', 'Bob'], 'Age': [25, 30]})
df2 = pd.DataFrame({'Name': ['Charlie', 'David'], 'Age': [35, 40]})
result = pd.concat([df1, df2])
print(result)
print("\n")


# 데이터프레임 병합 시 인덱스 무시
print("병합하면서 줄 인덱스를 다시 설정")
result = pd.concat([df1, df2], ignore_index=True)
print(result)
print("\n")

# 예제 16: 데이터프레임 조인
print("예제 16: 데이터프레임 조인")
print("--------------------------")
left = pd.DataFrame({'key': ['A', 'B'], 'value': [1, 2]})
right = pd.DataFrame({'key': ['A', 'B'], 'value': [3, 4]})
merged = pd.merge(left, right, on='key')
print(merged)
print("\n")

# 예제 17: 데이터 시각화
df.plot(kind='bar', x='Name', y='Age')
plt.show()