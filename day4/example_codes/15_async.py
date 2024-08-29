import asyncio

async def non_blocking_example(task_name):
    print(f'작업 {task_name} 시작')
    await asyncio.sleep(2)  # 비동기적으로 5초 대기
    print(f'작업 {task_name} 완료')
    return f'Task {task_name} finished'

async def main():
    results = await asyncio.gather(
        non_blocking_example('A'),
        non_blocking_example('B'),
        non_blocking_example('C')
    )
    print('비동기 결과:', results)

if __name__ == '__main__':
    asyncio.run(main())
