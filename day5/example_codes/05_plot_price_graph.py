import pandas as pd
import matplotlib.pyplot as plt

# CSV 파일에서 데이터를 읽어옵니다.
df = pd.read_csv('hatban_prices_by_datetime.csv')

# 'date' 열이 이미 존재하고 datetime 형식인지 확인합니다.
if 'date' not in df.columns:
    # 'date' 열이 존재하지 않으면, 개별 구성 요소에서 생성합니다.
    # 이 예제에서는 'date' 열이 이미 존재한다고 가정합니다.
    pass
else:
    # 'date' 열이 이미 존재한다면, datetime 형식으로 변환합니다.
    df['date'] = pd.to_datetime(df['date'])

# 'price' 열에 null 값이 있는 행을 제거합니다.
df.dropna(subset=['price'], inplace=True)

# 가격을 시간에 따라 플롯합니다.
plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['price'], marker='o', linestyle='-')
plt.title('Hatban Price Graph')
plt.xlabel('Date')
plt.ylabel('Price')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()