import asyncio
import aiohttp
import time


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.text()

async def main(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(url, session) for url in urls]
        return await asyncio.gather(*tasks)
    
if __name__ == '__main__':
    urls = ['https://www.google.com/', 'https://www.naver.com/', 'https://www.bing.com/']
    start_time = time.time()  # Record start time
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(main(urls))
    end_time = time.time()  # Record end time
    print([len(result) for result in results])
    print(f'총 실행 시간: {end_time - start_time} 초')
    