import json

# Python 딕셔너리
python_dict = {
    "name": "Alice",
    "age": 30,
    "is_student": False,
    "courses": ["Math", "Science"],
    "address": {
        "city": "New York",
        "zipcode": "10001"
    }
}

# 딕셔너리를 JSON 문자열로 변환
json_string = json.dumps(python_dict, indent=4)
print(f"json_string 타입: {type(json_string)}")
print(f"JSON 문자열: {json_string}")

# JSON 문자열을 Python 딕셔너리로 변환
python_dict = json.loads(json_string)
print(f"python_dict의 타입: {type(python_dict)}")
print(f"Python 딕셔너리: {python_dict}")
