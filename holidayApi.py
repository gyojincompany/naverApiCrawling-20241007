import requests

url = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo'
params ={'serviceKey' : 'cTWUGiJR/GRNsWP1Zvpr6EfojgF2NzRo6pzKHUXZplHewa1M8A9dkuiqnqsbVFTvix8hc8GWw4abmLFx7YB5tA==', 'pageNo' : '1', 'numOfRows' : '30', 'solYear' : '2024'}

response = requests.get(url, params=params)
print(response.text)