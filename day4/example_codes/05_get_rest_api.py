import urllib.request
import json

url = "https://api.thecatapi.com/v1/images/search"
with urllib.request.urlopen(url) as response:
    data = response.read()
text = data.decode("utf-8")

print(type(text), text)

json_data = json.loads(text)

print(type(json_data), json_data)

print(type(json_data[0]), json_data[0])

image_url = json_data[0]["url"]

print(type(image_url), image_url)
