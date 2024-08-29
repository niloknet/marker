from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

# ChromeDriver 경로 설정
current_directory = os.path.dirname(os.path.abspath(__file__))
chrome_binary_path = f"{current_directory}\chrome-headless-shell-win64\chrome-headless-shell.exe"

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
    # 웹 페이지로 이동
    driver.get("https://www.google.com")

    # 페이지 제목 출력
    print("Page title is:", driver.title)

finally:
    # WebDriver 종료
    driver.quit()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

# ChromeDriver 경로 설정
current_directory = os.path.dirname(os.path.abspath(__file__))

# Set up Chrome options
chrome_options = Options()
chrome_options.binary_location = chrome_binary_path

# Specify the path to the ChromeDriver executable
chrome_driver_path = f"{current_directory}\chromedriver.exe"

# Set up the ChromeDriver service
service = Service(chrome_driver_path)

# Create a WebDriver instance with the specified options
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Navigate to a web page
    driver.get("https://www.google.com")

    # Print the page title
    print("Page title is:", driver.title)

finally:
    # Quit the WebDriver
    driver.quit()
