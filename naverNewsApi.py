import urllib.request
import datetime
import json
from turtledemo.penrose import start

client_id = "BwMHvFEybzQOOyZ7qgT1"  # 네이버에서 발급 받은 client-id
client_secret = "kE2qceih0M"  # 네이버에서 발급 받은 client-secret

jsonResult = []  # 변환된 검색 결과가 전부 저장될 리스트

def getRequestUrl(url):  # url에 대한 접속 요청 후 네이버에서 응답 받은 결과 반환 함수
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", client_id)  # 네이버에서 발급 받은 client-id를 url의 헤더에 추가
    req.add_header("X-Naver-Client-Secret", client_secret)  # 네이버에서 발급 받은 client-secret를 url의 헤더에 추가
    try:  # 예외처리
        response = urllib.request.urlopen(req)  # api key가 포함된 요청을 네이버에 전송
        if response.getcode() == 200:  # 요청에 대한 응답코드가 200(정상코드)인지 확인
            print(f"요청에 대한 응답 성공 [{datetime.datetime.now()}]")
            return response.read().decode("utf-8")
    except Exception as e:
        print(e)  # 에러의 내용을 출력
        print(f"에러 발생 url : {url} [{datetime.datetime.now()}]")
        return None

# urlTest = "https://openapi.naver.com/v1/search/news.json?query=mlb&display=5"
# print(getRequestUrl(urlTest))

def getNaverSearch(node, srcText, start, display):
    base = "https://openapi.naver.com/v1/search"
    node =f"/{node}.json"
    parameters = f"?query={urllib.parse.quote(srcText)}&start={start}&display={display}"
    url = base + node + parameters
    responseDecode = getRequestUrl(url)  # 네이버의 뉴스 검색 결과

    if responseDecode == None:  # 에러 발생 검색 실패
        return None
    else:  # 응답 성공
        return json.loads(responseDecode)  # 파이썬에서 처리 가능한 객체로 변환하여 반환

# print(getNaverSearch("news", "프로야구", "1", "5"))

def getPostData(post, jsonResult, cnt):
    title = post["title"]  # 기사제목
    description = post["description"]  # 기사요약
    org_link = post["originallink"]  # 기사링크원본url
    link = post["link"]  # 네이버기사url
    pDate = datetime.datetime.strptime(post["pubDate"], "%a, %d %b %Y %H:%M:%S +0900")
    pDate = pDate.strftime("%Y-%m-%d %H:%M:%S")  # 날짜 형식을 2024-10-07 11:29:00 변환->기사 게시일
    jsonResult.append({"cnt":cnt, "title":title, "description":description,
                       "org_link":org_link, "link":link, "pDate":pDate})

    return jsonResult

srcText = "아파트"
node = "news"
jsonResponse = getNaverSearch(node, srcText, "1", "100")
total = jsonResponse["total"]  # 검색된 뉴스 기사의 총 개수
resultList = []
cnt = 0

while (jsonResponse != None) and (jsonResponse["display"] != 0):
    for post in jsonResponse["items"]:
        cnt = cnt + 1
        getPostData(post, resultList, cnt)
    start = jsonResponse["start"] + jsonResponse["display"]
    jsonResponse = getNaverSearch(node, srcText, start, "100")

print(f"검색된 총 뉴스기사 수 : {total}건")
# print(resultList)

with open(f"{srcText}_naver_{node}.json", "w", encoding="utf-8") as outfile:
    jsonFile = json.dumps(resultList, indent=4, sort_keys=True, ensure_ascii=False)
    outfile.write(jsonFile)

print(f"가져온 총 뉴스 데이터 수 : {cnt}건")





