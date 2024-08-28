import threading
import os


# 각 파일에서 가장 큰 숫자를 찾는 함수
def find_max_in_file(file_path, results, index, barrier):
    with open(file_path, "r") as file:
        numbers = [float(line.strip()) for line in file.readlines()]
    results[index] = max(numbers)
    barrier.wait()  # 배리어 대기


# 메인 함수
def main():
    # 파일들이 저장된 디렉토리 경로
    current_directory = os.path.dirname(os.path.abspath(__file__))
    directory = f"{current_directory}\..\sources"

    # 파일 경로 리스트 생성
    file_paths = [
        os.path.join(directory, file)
        for file in os.listdir(directory)
        if file.endswith(".txt")
    ]

    # 결과를 저장할 리스트 초기화
    results = [0] * len(file_paths)

    # 스레드 리스트와 배리어 생성
    threads = []
    barrier = threading.Barrier(len(file_paths))  # 파일 개수로 배리어 초기화

    # 각 파일에 대해 스레드를 생성하여 최대값 찾기
    for i, file_path in enumerate(file_paths):
        thread = threading.Thread(
            target=find_max_in_file, args=(file_path, results, i, barrier)
        )
        threads.append(thread)
        thread.start()

    # 모든 스레드가 완료될 때까지 대기
    for thread in threads:
        thread.join()

    # 전체 파일들 중 가장 큰 숫자 찾기
    overall_max = max(results)
    print(f"The largest number across all files is: {overall_max}")
    # The largest number across all files is: 45003.29624288437


if __name__ == "__main__":
    main()
