import requests
import json
import time
import xml.etree.ElementTree as ET

# API 엔드포인트
url = "http://apis.data.go.kr/1360000/SfcMtlyInfoService/getMmSumry"

# 발급받은 API 인증키 입력
api_key = 'NpWQYBWBernbIhRAeWWRQx+Amef+hy8m+HDpfVbjbQzjZga2mjyJXKpn7C86fmyy4AaS0UlbG4BE8CPZnp+AvA=='

# 연도 및 월 범위 설정
years = list(range(2015, 2024))  # 2015년부터 2023년까지
months = list(range(1, 13))      # 1월부터 12월까지

def parse_xml_response(response_text):
    """
    XML 응답에서 필요한 데이터를 파싱하여 JSON 형식으로 변환하는 함수.
    
    :param response_text: XML 형식의 응답 메시지
    :return: JSON 형식으로 변환된 데이터
    """
    root = ET.fromstring(response_text)
    info_list = []
    
    for info in root.findall('.//info'):
        data = {
            "stnid": info.findtext('stnid'),
            "stnko": info.findtext('stnko'),
            "pa": info.findtext('pa'),
            "avgtamax": info.findtext('avgtamax'),
            "avgtamin": info.findtext('avgtamin'),
            "taavg": info.findtext('taavg'),
            "avghm": info.findtext('avghm')
        }
        info_list.append(data)
    
    return info_list

def save_data_to_json_file(year, month, data):
    """
    데이터를 연도 및 월별로 개별 JSON 파일에 저장하는 함수.
    
    :param year: 연도
    :param month: 월
    :param data: 저장할 데이터 (리스트 형식)
    """
    file_path = f"weather/weather_{year}_{month:02d}.json"
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump({"data": data}, file, ensure_ascii=False, indent=4)

# 모든 연도에 대해 데이터 수집
for year in years:
    for month in months:
        # 요청 파라미터 설정
        params = {
            'serviceKey': api_key,
            'numOfRows': '100',
            'pageNo': '1',
            'dataType': 'XML',
            'year': str(year),
            'month': str(month).zfill(2)
        }
        
        # API 요청
        response = requests.get(url, params=params)
        if response.status_code == 200:
            response_text = response.text
            monthly_data = parse_xml_response(response_text)
            # 수집한 월별 데이터를 JSON 파일에 저장
            save_data_to_json_file(year, month, monthly_data)
        
        # API 과부하를 피하기 위해 잠시 대기
        time.sleep(0.5)  # 0.5초 대기

print("Data collection and JSON saving completed.")
