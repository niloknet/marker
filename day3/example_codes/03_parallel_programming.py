import threading
import time
import random


# 스레드에서 실행할 함수
def worker(barrier, thread_id):
    random_wait_time = random.randint(1, 6)  # 랜덤 대기 시간 (0.5초에서 3초 사이)
    print(f"스레드 {thread_id} 작업 중...")
    for i in range(random_wait_time):
        time.sleep(0.5)  # 랜덤 대기
        print(f"스레드 {thread_id}가 {(i+1)*0.5:.1f}초가 경과했습니다.")
    print(f"스레드 {thread_id}가 배리어에 도착했습니다.")
    barrier.wait()  # 배리어에서 대기
    print(f"스레드 {thread_id}가 배리어를 통과했습니다.")


def main():
    # 배리어 생성 (3개의 스레드가 도달할 때까지 대기)
    barrier = threading.Barrier(3)

    # 스레드 생성 및 시작

    thread_numbers = 3
    threads = []
    for i in range(thread_numbers):
        new_thread = threading.Thread(target=worker, args=(barrier, i))
        threads.append(new_thread)

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    print("모든 스레드가 배리어를 통과했습니다.")


if __name__ == "__main__":
    main()
