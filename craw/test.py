import requests

q = requests.get("https://static.packt-cdn.com/downloads/9781801075541_ColorImages.pdf")


print(q.text)