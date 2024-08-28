import threading
import os


# 각 파일에서 가장 큰 숫자를 찾는 함수
def find_max_in_file():
    pass


# 메인 함수
def main():
    # 파일들이 저장된 디렉토리 경로
    current_directory = os.path.dirname(os.path.abspath(__file__))
    directory = f"{current_directory}\sources"

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

    # find_max_in_file 에 적절한 인자와 내용을 넣고
    # 이곳 아래에 병렬 프로그래밍으로 스레드를 생성해
    # 각 파일에서 제일 큰 숫자를 찾고 그 중에서 제일 큰 숫자를 찾아보세요


if __name__ == "__main__":
    main()
