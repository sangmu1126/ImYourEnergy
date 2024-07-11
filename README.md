<h3>24.07.09</h3>

LSTM 방식에서 데이터셋의 부족으로 model.predict가 안되어

많은 데이터셋을 얻기 위해 공공데이터 포털에서 오픈API를 활용함

1. 한국전력거래소_현재전력수급현황조회
https://www.data.go.kr/data/15056640/openapi.do

2. 기상청_지상기상월보 조회서비스
https://www.data.go.kr/data/15057260/openapi.do

Json 형식의 Response를 받지만, Decoding Error 이슈로 인해 text 파일로 받은 후, 다시 Json 형식으로 바꾸는 작업 진행



<h3>24.07.11</h3>
weather의 API에서 json 방식으로 바로 가공하려 했으나, 데이터 형식을 조절하는데에 문제가 있어

XML 방식으로 리턴받아 텍스트로 변환 후, 다시 json 형식으로 변환하는 방식을 채택함

weather_{year}.json과 data_{year}.json으로 데이터를 가공하였으나, 년.월 까지 일치시킨 후 도시(city 와 stnko) 일치 시에 메모리 이슈 및 Key Error가 있어 데이터를 전처리하는 데에 문제가 생김

방대한 데이터 양에서 시간복잡도를 최소화하는 데에 초점을 두고 논문이나 기존의 코드들을 서치함
