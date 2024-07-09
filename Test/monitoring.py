import requests
import json
import os
import re
import time

# API 엔드포인트
url = "https://bigdata.kepco.co.kr/openapi/v1/powerUsage/industryType.do"

# 발급받은 API 인증키 입력
api_key = '7GJt0CMc6d9bl6fGx342QsfwtUVCnJL5pI0Iehtg'

# 연도 및 월 범위 설정
years = list(range(2010, 2011))  # 2010년부터 2023년까지
months = list(range(1, 3))      # 1월부터 12월까지

def convert_text_to_json(text):
    """
    응답 텍스트를 JSON 형식으로 수동으로 변환하는 함수.
    
    :param text: JSON 형식의 텍스트 데이터
    :return: 변환된 JSON 데이터
    """
    try:
        # "data" 배열 부분만 추출
        start = text.index('[')
        end = text.rindex(']') + 1
        data_part = text[start:end]

        # 항목들을 파싱하는 정규 표현식
        item_pattern = re.compile(r"""
            \{
            \s*"year":\s*"(?P<year>\d+)",\s*
            "month":\s*"(?P<month>\d+)",\s*
            "metro":\s*"(?P<metro>[^"]*)",\s*
            "city":\s*"(?P<city>[^"]*)",\s*
            "biz":\s*"(?P<biz>[^"]*)",\s*
            "custCnt":\s*(?P<custCnt>\d+),\s*
            "powerUsage":\s*(?P<powerUsage>\d+),\s*
            "bill":\s*(?P<bill>\d+),\s*
            "unitCost":\s*(?P<unitCost>[\d.]+)\s*
            \}
        """, re.VERBOSE)

        # JSON 배열 부분을 파싱하여 딕셔너리 리스트 생성
        data_list = []
        for match in item_pattern.finditer(data_part):
            item = match.groupdict()
            # 숫자형 데이터 형변환
            item['custCnt'] = int(item['custCnt'])
            item['powerUsage'] = int(item['powerUsage'])
            item['bill'] = int(item['bill'])
            item['unitCost'] = float(item['unitCost'])
            data_list.append(item)

        # 전체 JSON 형식으로 변환
        result = {"data": data_list}
        return result
    except (ValueError, json.JSONDecodeError, IndexError, re.error) as e:
        print(f"Error converting text to JSON: {e}")
        return None

def save_data_to_json_file(year, month, data):
    """
    데이터를 연도와 월에 따라 개별 JSON 파일에 저장하는 함수.
    
    :param year: 연도
    :param month: 월
    :param data: 저장할 데이터 (리스트 형식)
    """
    file_path = f"data_{year}_{month}.json"
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump({"data": data}, file, ensure_ascii=False, indent=4)

# 모든 연도와 월에 대해 데이터 수집
for year in years:
    for month in months:
        # 요청 파라미터 설정
        params = {
            'year': str(year),
            'month': str(month).zfill(2),
            'apiKey': api_key,
            'returnType': 'json'
        }
        
        # API 요청
        response = requests.get(url, params=params)    
        response_text = response.text

        json_result = convert_text_to_json(response_text)
        if json_result:
            # 연도와 월별로 개별 JSON 파일에 데이터 저장
            save_data_to_json_file(year, month, json_result["data"])
        
        # API 과부하를 피하기 위해 잠시 대기
        time.sleep(0.5)  # 0.5초 대기

print("Data collection and JSON saving completed.")
