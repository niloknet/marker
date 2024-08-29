import urllib.request
import json

def fetch_random_cat_image():
    # 랜덤 고양이 이미지를 가져오기 위한 URL
    url = "https://api.thecatapi.com/v1/images/search"

    try:
        # URL을 열고 데이터를 가져옴
        with urllib.request.urlopen(url) as response:
            # 응답 데이터를 읽음
            data = response.read()
            # 데이터를 문자열로 디코딩
            text = data.decode("utf-8")
            # JSON 데이터를 파싱
            json_data = json.loads(text)
            return json_data
    except urllib.error.URLError as e:
        print(f"데이터를 가져오지 못했습니다: {e.reason}")
        return None

def main():
    # 랜덤 고양이 이미지 가져오기
    cat_data = fetch_random_cat_image()
    if cat_data:
        # 이미지 URL을 추출하고 출력
        image_url = cat_data[0]["url"]
        print(f"랜덤 고양이 이미지 URL: {image_url}")

if __name__ == "__main__":
    main()