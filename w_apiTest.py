import requests
import json
import re
import time

# API 엔드포인트
url = "http://apis.data.go.kr/1360000/SfcMtlyInfoService/getMmSumry"

# 발급받은 API 인증키 입력
api_key = 'NpWQYBWBernbIhRAeWWRQx+Amef+hy8m+HDpfVbjbQzjZga2mjyJXKpn7C86fmyy4AaS0UlbG4BE8CPZnp+AvA=='

# 연도 및 월 범위 설정
years = list(range(2015, 2016))  # 2010년부터 2023년까지
months = list(range(3, 4))      # 1월부터 12월까지


# 모든 연도에 대해 데이터 수집
for year in years:
    year_data = []
    for month in months:
        # 요청 파라미터 설정
        params = {
            'serviceKey': api_key,
            'numOfRows': '100',
            'pageNo': '1',
            'dataType': 'JSON',
            'year': str(year),
            'month': str(month).zfill(2)
        }
        
        # API 요청
        response = requests.get(url, params=params)
        response_text = response.text
        
        print(response_text)
        
        # API 과부하를 피하기 위해 잠시 대기
        time.sleep(0.5)  # 0.5초 대기

    # 수집한 연도별 데이터를 JSON 파일에 저장
    

print("Data collection and JSON saving completed.")
