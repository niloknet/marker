import os
import matplotlib.pyplot as plt

# 파일에서 도수 분포표 읽기
bin_edges = []
counts = []

current_directory = os.path.dirname(os.path.abspath(__file__))
histogram_data_path = f"{current_directory}\histogram_data.txt"
with open(histogram_data_path, "r") as f:
    for line in f:
        edge, count = map(float, line.split())
        bin_edges.append(edge)
        counts.append(count)

# 마지막 bin edge 추가
bin_edges.append(bin_edges[-1] + 5000)

# 히스토그램 시각화
plt.bar(bin_edges[:-1], counts, width=5000, edgecolor="black", align="edge")
plt.title("Histogram of Scaled Float Values")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.grid(axis="y")

# 히스토그램 표시
plt.show()
