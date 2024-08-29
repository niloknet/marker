from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os

# ChromeDriver 경로 설정
current_directory = os.path.dirname(os.path.abspath(__file__))
chrome_driver_path = f"{current_directory}\chromedriver.exe"

# ChromeDriver 서비스 시작
service = Service(chrome_driver_path)
service.start()

# WebDriver 인스턴스 생성
driver = webdriver.Chrome(service=service)

try:
    # Google 홈페이지 열기
    driver.get("https://www.google.com")

    # 페이지 제목 출력
    print("Page title is:", driver.title)

finally:
    # WebDriver 종료
    driver.quit()
