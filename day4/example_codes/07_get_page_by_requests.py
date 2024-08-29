import requests

# 대상 웹 페이지 URL
url = 'https://search.shopping.naver.com/catalog/5825766254?query=%ED%96%87%EB%B0%98%20&NaPm=ct%3Dm0emslzs%7Cci%3D257e8e6fe1c7d4e0f5c6782288f1d02b8503ca58%7Ctr%3Dslsl%7Csn%3D95694%7Chk%3D94c8926eef4aef280f8a461fe2e96eeb9ab8d47b'

# 웹 페이지 요청 및 HTML 가져오기
response = requests.get(url)
html = response.text

print(html)
