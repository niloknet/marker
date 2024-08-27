# 한글 문자열을 파일에 쓰기
with open("korean_text.txt", "w", encoding="utf-8") as file:
    file.write("안녕하세요, 세계!\n")
