import os
import threading
import numpy as np


# 파일에서 숫자를 읽고 도수 계산하는 함수
def count_frequencies(file_path, all_numbers, lock):
    with open(file_path, "r") as file:
        numbers = [float(line.strip()) for line in file]
    with lock:
        all_numbers.extend(numbers)


def main():
    # 파일들이 저장된 디렉토리 경로
    current_directory = os.path.dirname(os.path.abspath(__file__))
    directory = f"{current_directory}\..\practices\sources"
    histogram_file_path = f"{current_directory}\histogram_data.txt"

    # 텍스트 파일 경로 리스트 생성
    text_files = [
        os.path.join(directory, file)
        for file in os.listdir(directory)
        if file.endswith(".txt")
    ]

    # 빈도 저장을 위한 리스트와 락 생성
    all_numbers = []
    lock = threading.Lock()

    # 스레드 리스트 생성
    threads = []

    # 각 파일에 대해 스레드를 생성하여 빈도 계산
    for file_path in text_files:
        thread = threading.Thread(
            target=count_frequencies, args=(file_path, all_numbers, lock)
        )
        threads.append(thread)
        thread.start()

    # 모든 스레드가 완료될 때까지 대기
    for thread in threads:
        thread.join()

    # 히스토그램 범위 설정
    bins = np.arange(-50000, 50001, 5000)  # -50000부터 50000까지 5000 간격

    # 히스토그램 계산
    counts, bin_edges = np.histogram(all_numbers, bins)

    # 도수 분포표를 표준 출력
    print("도수 분포표:")
    for count, edge in zip(counts, bin_edges[:-1]):
        print(f"범위 {edge} - {edge + 5000}: {count}")

    # 도수 분포표를 파일에 저장
    with open(histogram_file_path, "w") as f:
        for count, edge in zip(counts, bin_edges[:-1]):
            f.write(f"{edge} {count}\n")

    print(f"도수 분포표가 '{histogram_file_path}' 파일에 저장되었습니다.")


if __name__ == "__main__":
    main()
