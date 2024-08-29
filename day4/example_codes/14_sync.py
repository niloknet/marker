import time

def blocking_example(task_name):
    print(f'작업 {task_name} 시작')
    time.sleep(2)  # 5초 동안 대기
    print(f'작업 {task_name} 완료')
    return f'Task {task_name} finished'

def main():
    results = []
    results.append(blocking_example('A'))
    results.append(blocking_example('B'))
    results.append(blocking_example('C'))
    return results

if __name__ == '__main__':
    final_results = main()
    print(final_results)
