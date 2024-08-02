import requests
import uuid
import time
import json
import re

api_url = 'https://rwkh9fz97v.apigw.ntruss.com/custom/v1/33170/69b22d27f15e92815b84163c252385db4ce3583d4645c4d27d967226c8dbe7de/general'
secret_key = 'YmJNenpDR1NCcVBJTk5iZFhScmZmb1JlVk5jeVhnaU4='
image_file = 'Test/testImage.jpg'

request_json = {
    'images': [
        {
            'format': 'jpg',
            'name': 'demo'
        }
    ],
    'requestId': str(uuid.uuid4()),
    'version': 'V2',
    'timestamp': int(round(time.time() * 1000))
}

payload = {'message': json.dumps(request_json).encode('UTF-8')}
files = [
  ('file', open(image_file,'rb'))
]
headers = {
  'X-OCR-SECRET': secret_key
}

response = requests.request("POST", api_url, headers=headers, data = payload, files = files)

if response.status_code == 200:
    result = response.json()
    with open('result.json', 'w', encoding='utf-8') as make_file:
        json.dump(result, make_file, indent="\t", ensure_ascii=False)
    
    text = ""
    for field in result['images'][0]['fields']:
        text += field['inferText']
    
    # Extract the amount between "청구금액:" and "원"
    amount_match = re.search(r'청구금액:\s*([\d,]+)\s*원', text)
    if amount_match:
        amount = amount_match.group(1)
        print(f"청구금액: {amount} 원")
    else:
        print("청구금액을 찾을 수 없습니다.")
    
    # Extract the due date between "납기일:" and "까지"
    due_date_match = re.search(r'납기일:\s*([\d년월일까지]+)', text)
    if due_date_match:
        due_date = due_date_match.group(1)
        print(f"납기일: {due_date}")
    else:
        print("납기일을 찾을 수 없습니다.")
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)