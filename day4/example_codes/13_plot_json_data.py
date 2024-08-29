import os
import json
import matplotlib.pyplot as plt

current_directory = os.path.dirname(os.path.abspath(__file__))
json_path = f"{current_directory}\\rice_price.json"

# rice_price.json 파일에서 데이터 로드
with open(json_path, 'r') as file:
    rice_data = json.load(file)


# 날짜와 최소 가격 추출
dates = [entry['date'] for entry in rice_data['result']]
min_prices = [entry['minPrice'] for entry in rice_data['result']]

# 데이터 플롯
plt.figure(figsize=(10, 5))
plt.plot(dates, min_prices, marker='o')
plt.title('Minimum Rice Prices Over Dates')
plt.xlabel('Date')
plt.ylabel('Minimum Price')
plt.xticks(rotation=45)  # x축 레이블 회전
plt.grid()
plt.tight_layout()  # 레이블이 잘리지 않도록 레이아웃 조정
plt.show()
