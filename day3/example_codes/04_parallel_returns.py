import threading
import time
import random


# 스레드에서 실행할 함수
def worker(barrier, thread_id, results):
    print(f"스레드 {thread_id} 작업 중...")
    print(f"스레드 {thread_id}는 메인 스레드로부터 {results[thread_id]}를 받았습니다.")
    print(f"스레드 {thread_id}는 {results[thread_id]/2.0}초 뒤에 베리어에 도착합니다")
    for i in range(results[thread_id]):
        time.sleep(0.5)  # 랜덤 대기
        print(f"스레드 {thread_id}가 {(i+1)*0.5:.1f}초가 경과했습니다.")
    results[thread_id] = random.randint(10, 20)  # 새로운 값을 메인 스레드로 넘겨주기
    print(f"스레드 {thread_id}가 메인 스레드에 {results[thread_id]}를 전달하였습니다.")
    print(f"스레드 {thread_id}가 배리어에 도착했습니다.")
    barrier.wait()  # 배리어에서 대기
    print(f"스레드 {thread_id}가 배리어를 통과했습니다.")


def main():
    thread_numbers = 5
    # 배리어 생성 (3개의 스레드가 도달할 때까지 대기)
    barrier = threading.Barrier(thread_numbers)

    # 스레드 생성 및 시작
    # 1부터 6사이의 5개의 랜덤한 정수 리스트 생성
    results = [random.randint(1, 6) for _ in range(thread_numbers)]
    print(f"스레드로 보낼 배열 값들: {results}")

    threads = []
    for i in range(thread_numbers):
        new_thread = threading.Thread(target=worker, args=(barrier, i, results))
        threads.append(new_thread)

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    print("모든 스레드가 배리어를 통과했습니다.")
    print(f"스레드로부터 받은 새로운 배열: {results}")


if __name__ == "__main__":
    main()
