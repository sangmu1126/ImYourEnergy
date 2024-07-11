import requests
import json
import re
import time

# API 엔드포인트
url = "http://apis.data.go.kr/1360000/SfcMtlyInfoService/getMmSumry"

# 발급받은 API 인증키 입력
api_key = 'NpWQYBWBernbIhRAeWWRQx+Amef+hy8m+HDpfVbjbQzjZga2mjyJXKpn7C86fmyy4AaS0UlbG4BE8CPZnp+AvA=='

# 연도 및 월 범위 설정
years = list(range(2010, 2024))  # 2010년부터 2023년까지
months = list(range(1, 13))      # 1월부터 12월까지

def convert_text_to_json(text):
    """
    응답 텍스트를 JSON 형식으로 수동으로 변환하는 함수.
    
    :param text: JSON 형식의 텍스트 데이터
    :return: 변환된 JSON 데이터
    """
    try:
        # JSON 객체에서 필요한 항목만 추출하는 정규 표현식
        item_pattern = re.compile(r"""
            \{
            [^}]*?"avgtamax"\s*:\s*"(?P<avgtamax>[^"]*)",?
            [^}]*?"avgtamin"\s*:\s*"(?P<avgtamin>[^"]*)",?
            [^}]*?"taavg"\s*:\s*"(?P<taavg>[^"]*)",?
            [^}]*?"avghm"\s*:\s*"(?P<avghm>[^"]*)",?
            [^}]*?\}
        """, re.VERBOSE)

        # JSON 배열 부분을 파싱하여 딕셔너리 리스트 생성
        data_list = []
        for match in item_pattern.finditer(text):
            item = match.groupdict()
            data_list.append({
                "avgtamax": item.get("avgtamax"),
                "avgtamin": item.get("avgtamin"),
                "taavg": item.get("taavg"),
                "avghm": item.get("avghm")
            })

        # 전체 JSON 형식으로 변환
        result = {"data": data_list}
        return result
    except (ValueError, json.JSONDecodeError, IndexError, re.error) as e:
        print(f"Error converting text to JSON: {e}")
        return None

def save_data_to_json_file(year, data):
    """
    데이터를 연도별로 개별 JSON 파일에 저장하는 함수.
    
    :param year: 연도
    :param data: 저장할 데이터 (리스트 형식)
    """
    file_path = f"weather_{year}.json"
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

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
        
        # 텍스트에서 JSON 데이터 추출
        json_result = convert_text_to_json(response_text)
        if json_result:
            # 연도별 데이터를 수집
            year_data.extend(json_result["data"])
        
        # API 과부하를 피하기 위해 잠시 대기
        time.sleep(0.5)  # 0.5초 대기

    # 수집한 연도별 데이터를 JSON 파일에 저장
    save_data_to_json_file(year, {"data": year_data})

print("Data collection and JSON saving completed.")
