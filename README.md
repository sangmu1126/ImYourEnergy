<h3>24.07.09</h3>

LSTM 방식에서 데이터셋의 부족으로 model.predict가 안되어

많은 데이터셋을 얻기 위해 공공데이터 포털에서 오픈API를 활용함

1. 한국전력거래소_현재전력수급현황조회
https://www.data.go.kr/data/15056640/openapi.do

2. 기상청_지상기상월보 조회서비스
https://www.data.go.kr/data/15057260/openapi.do

Json 형식의 Response를 받지만, Decoding Error 이슈로 인해 text 파일로 받은 후, 다시 Json 형식으로 바꾸는 작업 진행
