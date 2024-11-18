import requests

url = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo'
params ={'serviceKey' : '', 'pageNo' : '1', 'numOfRows' : '30', 'solYear' : '2024'}

response = requests.get(url, params=params)
print(response.text)