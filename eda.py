import json
import pandas as pd
import glob
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# JSON 파일 로드 함수
def load_json_files(pattern):
    files = glob.glob(pattern)
    data_list = []
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for record in data['data']:
                year = int(record['year'])
                month = int(record['month'])
                record['year'] = year
                record['month'] = month
                data_list.append(record)
    return pd.DataFrame(data_list)

# 한글 도시명과 비즈니스 유형을 영어로 번역하는 딕셔너리
city_translation = {
    "서울": "Seoul", "부산": "Busan", "대구": "Daegu", "인천": "Incheon",
    "광주": "Gwangju", "대전": "Daejeon", "울산": "Ulsan", "세종": "Sejong",
    "수원": "Suwon", "고양": "Goyang", "용인": "Yongin", "성남": "Seongnam",
    "부천": "Bucheon", "화성": "Hwaseong", "남양주": "Namyangju", "안산": "Ansan",
    "안양": "Anyang", "평택": "Pyeongtaek", "의정부": "Uijeongbu", "파주": "Paju",
    "시흥": "Siheung", "김포": "Gimpo", "광명": "Gwangmyeong", "군포": "Gunpo",
    "이천": "Icheon", "오산": "Osan", "하남": "Hanam", "양주": "Yangju",
    "구리": "Guri", "안성": "Anseong", "포천": "Pocheon", "의왕": "Uiwang",
    "여주": "Yeoju", "양평": "Yangpyeong", "동두천": "Dongducheon", "가평": "Gapyeong",
    "춘천": "Chuncheon", "원주": "Wonju", "강릉": "Gangneung", "동해": "Donghae",
    "태백": "Taebaek", "속초": "Sokcho", "삼척": "Samcheok", "홍천": "Hongcheon",
    "횡성": "Hoengseong", "영월": "Yeongwol", "평창": "Pyeongchang", "정선": "Jeongseon",
    "철원": "Cheorwon", "화천": "Hwacheon", "양구": "Yanggu", "인제": "Inje",
    "고성": "Goseong", "양양": "Yangyang", "청주": "Cheongju", "충주": "Chungju",
    "제천": "Jecheon", "보은": "Boeun", "옥천": "Okcheon", "영동": "Yeongdong",
    "진천": "Jincheon", "괴산": "Goesan", "음성": "Eumseong", "단양": "Danyang",
    "천안": "Cheonan", "공주": "Gongju", "보령": "Boryeong", "아산": "Asan",
    "서산": "Seosan", "논산": "Nonsan", "계룡": "Gyeryong", "당진": "Dangjin",
    "금산": "Geumsan", "부여": "Buyeo", "서천": "Seocheon", "청양": "Cheongyang",
    "홍성": "Hongseong", "예산": "Yesan", "태안": "Taean", "전주": "Jeonju",
    "군산": "Gunsan", "익산": "Iksan", "정읍": "Jeongeup", "남원": "Namwon",
    "김제": "Gimje", "완주": "Wanju", "진안": "Jinan", "무주": "Muju",
    "장수": "Jangsu", "임실": "Imsil", "순창": "Sunchang", "고창": "Gochang",
    "부안": "Buan", "목포": "Mokpo", "여수": "Yeosu", "순천": "Suncheon",
    "나주": "Naju", "광양": "Gwangyang", "담양": "Damyang", "곡성": "Gokseong",
    "구례": "Gurye", "고흥": "Goheung", "보성": "Boseong", "화순": "Hwasun",
    "장흥": "Jangheung", "강진": "Gangjin", "해남": "Haenam", "영암": "Yeongam",
    "무안": "Muan", "함평": "Hampyeong", "영광": "Yeonggwang", "장성": "Jangseong",
    "완도": "Wando", "진도": "Jindo", "신안": "Shinan", "포항": "Pohang",
    "경주": "Gyeongju", "김천": "Gimcheon", "안동": "Andong", "구미": "Gumi",
    "영주": "Yeongju", "영천": "Yeongcheon", "상주": "Sangju", "문경": "Mungyeong",
    "경산": "Gyeongsan", "군위": "Gunwi", "의성": "Uiseong", "청송": "Cheongsong",
    "영양": "Yeongyang", "영덕": "Yeongdeok", "청도": "Cheongdo", "고령": "Goryeong",
    "성주": "Seongju", "칠곡": "Chilgok", "예천": "Yecheon", "봉화": "Bonghwa",
    "울진": "Uljin", "울릉": "Ulleung", "창원": "Changwon", "진주": "Jinju",
    "통영": "Tongyeong", "사천": "Sacheon", "김해": "Gimhae", "밀양": "Miryang",
    "거제": "Geoje", "양산": "Yangsan", "의령": "Uiryeong", "함안": "Haman",
    "창녕": "Changnyeong", "고성": "Goseong", "남해": "Namhae", "하동": "Hadong",
    "산청": "Sancheong", "함양": "Hamyang", "거창": "Geochang", "합천": "Hapcheon",
    "제주": "Jeju", "서귀포": "Seogwipo"
}

biz_translation = {
    "농업, 임업 및 어업 ": "Agriculture, Forestry, and Fishing",
    "광업": "Mining",
    "제조업": "Manufacturing",
    "전기, 가스, 증기 및 공기 조절 공급업": "Electricity, Gas, Steam, and Air Conditioning Supply",
    "수도, 하수 및 폐기물 처리, 원료 재생업": "Water Supply, Sewerage, Waste Management, and Remediation Activities",
    "건설업": "Construction",
    "도매 및 소매업": "Wholesale and Retail Trade",
    "운수 및 창고업": "Transportation and Storage",
    "숙박 및 음식점업": "Accommodation and Food Service Activities",
    "정보통신업": "Information and Communication",
    "금융 및 보험업": "Financial and Insurance Activities",
    "부동산업 및 임대업": "Real Estate Activities and Rental and Leasing",
    "전문, 과학 및 기술 서비스업": "Professional, Scientific, and Technical Activities",
    "사업시설 관리, 사업 지원 및 임대 서비스업": "Business Facilities Management, Business Support, and Rental Services",
    "공공 행정, 국방 및 사회 보장 행정": "Public Administration, Defense, and Social Security Administration",
    "교육 서비스업": "Education",
    "보건업 및 사회복지 서비스업": "Human Health and Social Work Activities",
    "예술, 스포츠 및 여가관련 서비스업": "Arts, Sports, and Recreation Related Services",
    "기타 서비스업": "Other Services"
}


# 한글 도시명과 비즈니스 유형을 영어로 번역하는 함수
def translate_columns(df, column_name, translation_dict):
    df[column_name] = df[column_name].map(translation_dict)
    return df

# data 파일에서 city값에서 뒤의 한글자를 제거하는 함수
def preprocess_city_name(city_name):
    if city_name != '전체':
        return city_name[:-1]
    return city_name

# 전력 사용량 데이터 로드
power_df = load_json_files("data_*.json")

# 전력 사용량 데이터에서 city 값 전처리
power_df['city'] = power_df['city'].apply(preprocess_city_name)

# 한글을 영어로 번역
power_df = translate_columns(power_df, 'city', city_translation)
power_df = translate_columns(power_df, 'biz', biz_translation)

# 데이터 전처리
power_df['year'] = power_df['year'].astype(int)
power_df['month'] = power_df['month'].astype(int)
power_df['date'] = pd.to_datetime(power_df[['year', 'month']].assign(day=1))

# 도시별 데이터 제한 (20개 도시만 선택)
selected_cities = power_df['city'].unique()[:20]

# 도시별로 데이터 분리 및 그래프 저장
plt.figure(figsize=(20, len(selected_cities) * 5))
for i, city in enumerate(selected_cities):
    city_df = power_df[power_df['city'] == city]
    plt.subplot(len(selected_cities), 1, i+1)
    sns.lineplot(data=city_df, x='date', y='powerUsage', hue='biz', palette='tab20')
    plt.title(f'Power Usage in {city}')
    plt.xlabel('Time')
    plt.ylabel('Power Usage')
    plt.legend(loc='upper right')

plt.tight_layout()
plt.show()
