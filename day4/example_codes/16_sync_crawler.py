import requests
import time

def fetch(url):
    response = requests.get(url)
    return response.text

def main(urls):
    results = []
    for url in urls:
        results.append(fetch(url))
    return results

if __name__ == '__main__':
    urls = ['https://www.google.com/', 'https://www.naver.com/', 'https://www.bing.com/']
    start_time = time.time()  # Record start time
    results = main(urls)
    end_time = time.time()  # Record end time
    print([len(result) for result in results])
    print(f'총 실행 시간: {end_time - start_time} 초')
