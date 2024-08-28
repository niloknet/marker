import matplotlib.pyplot as plt

# 데이터 생성
x = [1, 2, 3, 4, 5]
y = [2, 3, 5, 7, 11]

# 선 그래프 그리기
plt.plot(x, y, marker="o")

# 그래프 제목과 레이블 설정
plt.title("Simple Line Graph")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")

# 그래프 표시
plt.grid(True)
plt.show()
