import requests
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime, timedelta

def get_power_data(service_key, date):
    url = f"https://openapi.kpx.or.kr/openapi/sukub5mMaxDatetime/getSukub5mMaxDatetime?ServiceKey={service_key}&base_date={date}"
    response = requests.get(url)
    
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        result_code = root.find(".//resultCode").text
        result_msg = root.find(".//resultMsg").text
        
        if result_code == "00":
            data = {
                "resultCode": result_code,
                "resultMsg": result_msg,
                "baseDatetime": root.find(".//baseDatetime").text,
                "suppAbility": float(root.find(".//suppAbility").text),
                "currPwrTot": float(root.find(".//currPwrTot").text),
                "forecastLoad": float(root.find(".//forecastLoad").text),
                "suppReservePwr": float(root.find(".//suppReservePwr").text),
                "suppReserveRate": float(root.find(".//suppReserveRate").text),
                "operReservePwr": float(root.find(".//operReservePwr").text),
                "operReserveRate": float(root.find(".//operReserveRate").text)
            }
            return data
        else:
            return {"resultCode": result_code, "resultMsg": result_msg}
    else:
        return {"resultCode": str(response.status_code), "resultMsg": "HTTP request failed"}

def collect_data(service_key, start_date):
    all_data = []
    current_date = datetime.now()
    
    while start_date <= current_date:
        date_str = start_date.strftime("%Y%m%d")
        data = get_power_data(service_key, date_str)
        
        if data["resultCode"] == "00":
            all_data.append(data)
        
        start_date += timedelta(days=1)
    
    return all_data

# 서비스 키를 입력받아 호출
service_key = "NpWQYBWBernbIhRAeWWRQx%2BAmef%2Bhy8m%2BHDpfVbjbQzjZga2mjyJXKpn7C86fmyy4AaS0UlbG4BE8CPZnp%2BAvA%3D%3D"
start_date_str = input("Enter the start date (YYYYMMDD): ")
start_date = datetime.strptime(start_date_str, "%Y%m%d")

data = collect_data(service_key, start_date)

# 결과를 데이터프레임으로 변환
df = pd.DataFrame(data)
df.to_csv("power_data.csv", index=False)
print("Data collected and saved to power_data.csv")
