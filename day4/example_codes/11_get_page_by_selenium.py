from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

# Chrome 경로 설정
current_directory = os.path.dirname(os.path.abspath(__file__))
chrome_binary_path = f"{current_directory}\chrome-win64\chrome.exe"

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.binary_location = chrome_binary_path

# ChromeDriver 실행 파일의 경로 지정
chrome_driver_path = f"{current_directory}\chromedriver.exe"

# ChromeDriver 서비스 설정
service = Service(chrome_driver_path)

# 지정된 옵션으로 WebDriver 인스턴스 생성
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # URL 열기
    url = 'https://search.shopping.naver.com/catalog/5825766254?query=%ED%96%87%EB%B0%98+&NaPm=ct%3Dm0emslzs%7Cci%3D257e8e6fe1c7d4e0f5c6782288f1d02b8503ca58%7Ctr%3Dslsl%7Csn%3D95694%7Chk%3D94c8926eef4aef280f8a461fe2e96eeb9ab8d47b'
    driver.get(url)

    # 페이지 로딩 대기 (필요에 따라 조정)
    driver.implicitly_wait(10)  # 최대 10초 대기

    # 페이지의 HTML 소스 가져오기
    html = driver.page_source
    print(html)

finally:
    # WebDriver 종료
    driver.quit()
