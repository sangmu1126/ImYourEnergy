import requests
import uuid
import time
import json

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

print(response.text.encode('utf8'))

# with open('result.json', 'w', encoding='utf-8') as make_file:
#     json.dump(result, make_file, indent="\t", ensure_ascii=False)
    
# text = ""
# for field in result['images'][0]['fields']:
#     text += field['inferText']
# print(text)
