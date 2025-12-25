import requests
import json
import time
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()
API_KEY = os.getenv('API_KEY')

if not API_KEY:
    print("❌ API_KEY를 찾을 수 없습니다. .env 파일을 확인해주세요!")
    exit()

url = "http://apis.data.go.kr/B551011/KorService2/areaBasedList2"

# ============================================================================
# 음식점 카테고리 검증 키워드
# ============================================================================
food_validation_keywords = {
    '일식': ['일식', '초밥', '스시', '사시미', '회', '우동', '라멘', '소바', '덮밥', '돈까스', '가츠', '야키', '이자카야', '오코노미야키', '규동', '텐동', '오뎅', '사케'],
    '중식': ['중식', '중국', '짜장', '짬뽕', '탕수육', '마라', '양꼬치', '만두', '딤섬', '깐풍', '유산슬', '팔보채'],
    '한식': ['한식', '한정식', '비빔밥', '불고기', '갈비', '삼겹살', '김치', '된장', '국밥', '찌개', '전골', '보쌈', '족발', '순대', '떡볶이', '순두부', '냉면', '칼국수'],
    '서양식': ['서양식', '양식', '스테이크', '파스타', '피자', '햄버거', '리조또', '그라탕', '샐러드', '브런치', '베이글', '샌드위치', '이탈리안', '프렌치', '경양식'],
    '카페디저트': ['카페', '커피', '베이커리', '디저트', '와플', '빵', '케이크', '마카롱', '아이스크림', '젤라또'],
    '이색음식점': ['퓨전', '이색', '월드', '에스닉', '베트남', '태국', '인도', '멕시칸', '타코', '쌀국수', '분짜', '팟타이', '카레', '터키'],
}

# ============================================================================
# 관광지 카테고리 검증 키워드 (우선순위 순)
# ============================================================================
tourism_validation_keywords = {
    # 공원 (가장 우선)
    '국립공원': ['국립공원'],
    '도립공원': ['도립공원', '도립'],
    '군립공원': ['군립공원', '군립'],
    '시립공원': ['시립공원', '시립'],
    
    # 자연
    '폭포': ['폭포'],
    '동굴': ['동굴'],
    '호수': ['호수', '저수지', '댐'],
    '약수터': ['약수', '샘'],
    
    # 해안 관련
    '해수욕장': ['해수욕장', '비치'],
    '해안절경': ['해안', '해변'],
    '항구포구': ['항구', '포구', '항'],
    
    # 시설
    '자연휴양림': ['휴양림', '자연휴양'],
    '자연생태관광지': ['생태', '습지', '생태공원'],
    
    # 문화
    '종교성지': ['성지', '성당', '교회', '성모', '순교'],
    '문': ['문', '문루', '아문'],
}

# ============================================================================
# 레포츠 카테고리 검증 키워드 (우선순위 순)
# ============================================================================
sports_validation_keywords = {
    # 겨울/빙상 스포츠 (우선순위 높음)
    '스키스노보드': ['스키', '스노보드', '스노우파크', '슬로프'],
    '스케이트': ['스케이트', '빙상', '아이스링크', '롤러'],
    '썰매장': ['썰매'],
    
    # 수상 스포츠
    '래프팅': ['래프팅'],
    '카약카누': ['카약', '카누'],
    '요트': ['요트', '마리나'],
    '윈드서핑제트스키': ['윈드서핑', '제트스키', '웨이크보드'],
    '스노쿨링스킨스쿠버': ['스쿠버', '다이빙', '스노쿨링'],
    
    # 낚시 (민물 우선)
    '민물낚시': ['낚시터'],
    '바다낚시': ['바다낚시', '선상낚시', '어선'],
    
    # 기타
    '골프': ['골프', 'cc', '컨트리클럽'],
    '경기장': ['경기장', '체육관', '경륜', '경마', '운동장'],
    '야영장오토캠핑장': ['캠핑', '야영', '글램핑'],
    '수련시설': ['수련원', '수련관', '연수원'],
}

# ============================================================================
# 문화시설 카테고리 검증 키워드 (우선순위 순)
# ============================================================================
culture_validation_keywords = {
    # 박물관/미술관 (가장 구체적)
    '박물관': ['박물관', '뮤지엄'],
    '미술관화랑': ['미술관', '갤러리', '화랑', '아트센터'],
    
    # 공연/영화
    '영화관': ['영화관', '시네마'],
    '공연장': ['공연장', '콘서트홀', '아트홀', '문예회관'],
    
    # 전시/기념
    '기념관': ['기념관'],
    '전시관': ['전시관', '전시장', '전시실'],
    
    # 도서/서적
    '도서관': ['도서관', '열람실'],
    '대형서점': ['서점', '북카페'],
    
    # 문화시설
    '외국문화원': ['외국문화원', '대사관', '주한'],
    '문화전수시설': ['전수관', '전수소', '전승관'],
    '문화원': ['문화원', '문화의집'],
    
    # 컨벤션
    '컨벤션센터': ['컨벤션', 'expo', 'exco', 'bexco', 'coex', 'setec', 'kintext'],
}

# ============================================================================
# 쇼핑 카테고리 검증 키워드 (우선순위 순)
# ============================================================================
shopping_validation_keywords = {
    # 면세/백화점 (가장 우선)
    '면세점': ['면세점', 'duty free'],
    '백화점': ['백화점', '갤러리아', '신세계', '현대백화점'],
    
    # 대형매장
    '아울렛': ['아울렛', 'outlet', '프리미엄아울렛'],
    '대형마트': ['마트', '이마트', '홈플러스', '롯데마트'],
    
    # 쇼핑몰
    '복합쇼핑몰': ['쇼핑몰', '몰', 'mall'],
    
    # 시장/특산물
    '전통시장': ['시장', '전통시장', '재래시장', '공설시장'],
    '특산물판매점': ['특산물', '로컬푸드', '직판장', '판매장'],
    
    # 공예
    '공예공방': ['공방', '공예', '핸드메이드', '수제'],
}

# ============================================================================
# 숙박 카테고리 검증 키워드 (우선순위 순)
# ============================================================================
accommodation_validation_keywords = {
    # 호텔/리조트 (가장 우선)
    '관광호텔': ['호텔', '리조트'],
    '콘도미니엄': ['콘도'],
    
    # 소형숙박
    '모텔': ['모텔'],
    '펜션': ['펜션'],
    '민박': ['민박'],
    '여관': ['여관'],
    
    # 공유숙박
    '호스텔': ['호스텔', '유스호스텔'],
    '게스트하우스': ['게스트하우스', '게하'],
}

# ============================================================================
# 음식점 카테고리 자동 재분류 함수
# ============================================================================
def detect_food_category(title, original_category):
    """음식점 제목을 기반으로 올바른 카테고리 감지"""
    title_lower = title.lower()
    
    food_categories = ['한식', '서양식', '중식', '일식', '이색음식점', '카페디저트']
    
    if original_category not in food_categories:
        return original_category, False
    
    # 우선순위대로 체크
    for category, keywords in food_validation_keywords.items():
        if category == original_category:
            continue
        for keyword in keywords:
            if keyword in title_lower:
                return category, True
    
    return original_category, False

# ============================================================================
# 관광지 카테고리 자동 재분류 함수
# ============================================================================
def detect_tourism_category(title, original_category):
    """관광지 제목을 기반으로 올바른 카테고리 감지"""
    title_lower = title.lower()
    
    # 우선순위대로 체크 (공원 먼저, 그 다음 구체적 키워드)
    for category, keywords in tourism_validation_keywords.items():
        if category == original_category:
            continue
        for keyword in keywords:
            if keyword in title_lower:
                return category, True
    
    return original_category, False

# ============================================================================
# 레포츠 카테고리 자동 재분류 함수
# ============================================================================
def detect_sports_category(title, original_category):
    """레포츠 제목을 기반으로 올바른 카테고리 감지"""
    title_lower = title.lower()
    
    # 우선순위대로 체크
    for category, keywords in sports_validation_keywords.items():
        if category == original_category:
            continue
        for keyword in keywords:
            if keyword in title_lower:
                return category, True
    
    return original_category, False

# ============================================================================
# 문화시설 카테고리 자동 재분류 함수
# ============================================================================
def detect_culture_category(title, original_category):
    """문화시설 제목을 기반으로 올바른 카테고리 감지"""
    title_lower = title.lower()
    
    # 우선순위대로 체크
    for category, keywords in culture_validation_keywords.items():
        if category == original_category:
            continue
        for keyword in keywords:
            if keyword in title_lower:
                return category, True
    
    return original_category, False

# ============================================================================
# 쇼핑 카테고리 자동 재분류 함수
# ============================================================================
def detect_shopping_category(title, original_category):
    """쇼핑 제목을 기반으로 올바른 카테고리 감지"""
    title_lower = title.lower()
    
    # 우선순위대로 체크
    for category, keywords in shopping_validation_keywords.items():
        if category == original_category:
            continue
        for keyword in keywords:
            if keyword in title_lower:
                return category, True
    
    return original_category, False

# ============================================================================
# 숙박 카테고리 자동 재분류 함수
# ============================================================================
def detect_accommodation_category(title, original_category):
    """숙박 제목을 기반으로 올바른 카테고리 감지"""
    title_lower = title.lower()
    
    # 우선순위대로 체크
    for category, keywords in accommodation_validation_keywords.items():
        if category == original_category:
            continue
        for keyword in keywords:
            if keyword in title_lower:
                return category, True
    
    return original_category, False

# ============================================================================
# 수집할 데이터 정의
# ============================================================================
data_to_collect = {
    '관광지': {
        'contentTypeId': '12',
        'validation_func': detect_tourism_category,
        'subcategories': {
            'A01010100': '국립공원',
            'A01010200': '도립공원',
            'A01010300': '군립공원',
            'A01010400': '산',
            'A01010500': '자연생태관광지',
            'A01010600': '자연휴양림',
            'A01010700': '수목원',
            'A01010800': '폭포',
            'A01010900': '계곡',
            'A01011000': '약수터',
            'A01011100': '해안절경',
            'A01011200': '해수욕장',
            'A01011300': '섬',
            'A01011400': '항구포구',
            'A01011600': '등대',
            'A01011700': '호수',
            'A01011800': '강',
            'A01011900': '동굴',
            'A02010100': '고궁',
            'A02010200': '성',
            'A02010300': '문',
            'A02010400': '고택',
            'A02010500': '생가',
            'A02010600': '민속마을',
            'A02010700': '유적지사적지',
            'A02010800': '사찰',
            'A02010900': '종교성지',
            'A02011000': '안보관광지',
        }
    },
    '문화시설': {
        'contentTypeId': '14',
        'validation_func': detect_culture_category,
        'subcategories': {
            'A02060100': '박물관',
            'A02060200': '기념관',
            'A02060300': '전시관',
            'A02060400': '컨벤션센터',
            'A02060500': '미술관화랑',
            'A02060600': '공연장',
            'A02060700': '문화원',
            'A02060800': '외국문화원',
            'A02060900': '도서관',
            'A02061000': '대형서점',
            'A02061100': '문화전수시설',
            'A02061200': '영화관',
        }
    },
    '축제공연행사': {
        'contentTypeId': '15',
        'validation_func': None,
        'subcategories': {
            'A02070100': '문화관광축제',
            'A02070200': '일반축제',
            'A02080100': '전통공연',
            'A02080200': '연극',
            'A02080300': '뮤지컬',
            'A02080400': '오페라',
            'A02080500': '전시회',
            'A02080600': '박람회',
            'A02080800': '무용',
            'A02080900': '클래식음악회',
            'A02081000': '대중콘서트',
            'A02081100': '영화',
            'A02081200': '스포츠경기',
            'A02081300': '기타행사',
        }
    },
    '레포츠': {
        'contentTypeId': '28',
        'validation_func': detect_sports_category,
        'subcategories': {
            'A03020200': '수련시설',
            'A03020300': '경기장',
            'A03020700': '골프',
            'A03021200': '스키스노보드',
            'A03021300': '스케이트',
            'A03021400': '썰매장',
            'A03021700': '야영장오토캠핑장',
            'A03030100': '윈드서핑제트스키',
            'A03030200': '카약카누',
            'A03030300': '요트',
            'A03030400': '스노쿨링스킨스쿠버',
            'A03030500': '민물낚시',
            'A03030600': '바다낚시',
            'A03030800': '래프팅',
        }
    },
    '숙박': {
        'contentTypeId': '32',
        'validation_func': detect_accommodation_category,
        'subcategories': {
            'B02010100': '관광호텔',
            'B02010500': '호스텔',
            'B02010900': '콘도미니엄',
            'B02011000': '유스호스텔',
            'B02011100': '펜션',
            'B02011200': '여관',
            'B02011300': '모텔',
            'B02011400': '민박',
            'B02011500': '게스트하우스',
            'B02011600': '홈스테이',
        }
    },
    '쇼핑': {
        'contentTypeId': '38',
        'validation_func': detect_shopping_category,
        'subcategories': {
            'A04010100': '공예공방',
            'A04010200': '특산물판매점',
            'A04010300': '상설시장',
            'A04010400': '백화점',
            'A04010500': '면세점',
            'A04010600': '대형마트',
            'A04010700': '전통시장',
            'A04010900': '한국관광명품점',
            'A04011100': '종합쇼핑몰',
            'A04011200': '복합쇼핑몰',
            'A04011300': '아울렛',
        }
    },
    '음식점': {
        'contentTypeId': '39',
        'validation_func': detect_food_category,
        'subcategories': {
            'A05020100': '한식',
            'A05020200': '서양식',
            'A05020300': '중식',
            'A05020400': '일식',
            'A05020700': '이색음식점',
            'A05020900': '카페디저트',
        }
    },
}

# ============================================================================
# 데이터 수집 및 검증
# ============================================================================
main_folder = 'tourism_data'
if not os.path.exists(main_folder):
    os.makedirs(main_folder)
    print(f"📁 메인 폴더 생성: {main_folder}\n")

validation_stats = {
    'total': 0,
    'corrected': 0,
    'corrections': {}
}

print("=" * 80)
print("🚀 전체 관광 데이터 수집 및 자동 검증 시작")
print("=" * 80)

# ============================================================================
# 축제공연행사 날짜 정보 수집 (searchFestival API)
# ============================================================================
festival_date_info = {}

def collect_festival_dates():
    """searchFestival API로 축제 날짜 정보 수집"""
    print("\n" + "="*80)
    print("📅 축제공연행사 날짜 정보 수집 중... (searchFestival API)")
    print("="*80)
    
    festival_api_url = "http://apis.data.go.kr/B551011/KorService2/searchFestival2"
    page = 1
    total_collected = 0
    
    while True:
        params = {
            'serviceKey': API_KEY,
            'numOfRows': 100,
            'pageNo': page,
            'MobileOS': 'ETC',
            'MobileApp': 'AppTest',
            '_type': 'json',
            'listYN': 'Y',
            'arrange': 'A',
            'eventStartDate': '20240101',  # 2024년 이후 모든 축제
        }
        
        try:
            response = requests.get(festival_api_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                # 응답 구조 확인
                if 'response' not in data:
                    print(f"  ⚠️ API 응답에 'response' 키가 없습니다.")
                    print(f"  📋 실제 응답 키: {list(data.keys())}")
                    if 'OpenAPI_ServiceResponse' in data:
                        print(f"  💡 OpenAPI 에러: {data.get('OpenAPI_ServiceResponse', {}).get('cmmMsgHeader', {}).get('returnReasonCode', 'Unknown')}")
                    break
                
                if data['response']['header']['resultCode'] == '0000':
                    items_data = data['response']['body']['items']
                    
                    if not isinstance(items_data, dict) or 'item' not in items_data:
                        break
                    
                    items = items_data['item']
                    
                    if not items or items == '':
                        break
                    
                    if isinstance(items, dict):
                        items = [items]
                    
                    # contentid를 키로 날짜 정보 저장
                    for item in items:
                        contentid = item.get('contentid')
                        if contentid:
                            festival_date_info[contentid] = {
                                'eventstartdate': item.get('eventstartdate', ''),
                                'eventenddate': item.get('eventenddate', '')
                            }
                            total_collected += 1
                    
                    print(f"  페이지 {page}: {len(items)}개 수집 (누적: {total_collected}개)")
                    page += 1
                else:
                    result_msg = data['response']['header'].get('resultMsg', 'Unknown Error')
                    print(f"  ⚠️ API 오류: {result_msg}")
                    break
            else:
                print(f"  ⚠️ HTTP 오류: {response.status_code}")
                break
                
        except Exception as e:
            print(f"  ⚠️ 오류 발생: {str(e)}")
            import traceback
            print(f"  📋 상세 오류:")
            traceback.print_exc()
            break
        
        time.sleep(0.2)
    
    print(f"✅ 총 {total_collected}개 축제의 날짜 정보 수집 완료\n")
    return festival_date_info

# 축제 날짜 정보 먼저 수집
festival_date_info = collect_festival_dates()

for main_category, config in data_to_collect.items():
    print(f"\n{'='*80}")
    print(f"📂 [{main_category}] 카테고리 수집 중...")
    print(f"{'='*80}")
    
    category_folder = os.path.join(main_folder, main_category)
    if not os.path.exists(category_folder):
        os.makedirs(category_folder)
        print(f"📁 폴더 생성: {category_folder}\n")
    
    categorized_data = {}
    validation_func = config.get('validation_func')
    
    for cat3_code, cat3_name in config['subcategories'].items():
        print(f"  🔹 [{cat3_name}] 수집 중...", end=" ")
        
        all_items = []
        page = 1
        
        while True:
            params = {
                'serviceKey': API_KEY,
                'numOfRows': 100,
                'pageNo': page,
                'MobileOS': 'ETC',
                'MobileApp': 'AppTest',
                '_type': 'json',
                'contentTypeId': config['contentTypeId'],
                'cat3': cat3_code,
            }
            
            try:
                response = requests.get(url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data['response']['header']['resultCode'] == '0000':
                        items_data = data['response']['body']['items']
                        
                        if not isinstance(items_data, dict) or 'item' not in items_data:
                            break
                        
                        items = items_data['item']
                        
                        if not items or items == '':
                            break
                        
                        if isinstance(items, dict):
                            items = [items]
                        
                        all_items.extend(items)
                        page += 1
                    else:
                        break
                else:
                    break
                    
            except Exception as e:
                break
            
            time.sleep(0.2)
        
        if len(all_items) == 0:
            print("⚠️ 데이터 없음")
            continue
        
        # 데이터 검증 및 재분류
        corrected_count = 0
        for item in all_items:
            validation_stats['total'] += 1
            title = item.get('title', '')
            
            # 검증 함수가 있으면 실행
            correct_category = cat3_name
            was_corrected = False
            
            if validation_func:
                correct_category, was_corrected = validation_func(title, cat3_name)
                
                if was_corrected:
                    corrected_count += 1
                    validation_stats['corrected'] += 1
                    correction_key = f"{cat3_name} → {correct_category}"
                    validation_stats['corrections'][correction_key] = validation_stats['corrections'].get(correction_key, 0) + 1
            
            # 카테고리별로 분류
            if correct_category not in categorized_data:
                categorized_data[correct_category] = []
            
            simplified_item = {
                'id': item.get('contentid'),
                'title': item.get('title'),
                'address': item.get('addr1'),
                'phone': item.get('tel', ''),
                'latitude': item.get('mapy'),
                'longitude': item.get('mapx'),
                'image': item.get('firstimage', ''),
                'category': correct_category,
            }
            
            # 축제공연행사인 경우 날짜 정보 병합
            if main_category == '축제공연행사':
                contentid = item.get('contentid')
                if contentid and contentid in festival_date_info:
                    # searchFestival API에서 수집한 날짜 정보 병합
                    simplified_item['eventstartdate'] = festival_date_info[contentid].get('eventstartdate', '')
                    simplified_item['eventenddate'] = festival_date_info[contentid].get('eventenddate', '')
                else:
                    # 날짜 정보 없는 경우 빈 문자열
                    simplified_item['eventstartdate'] = ''
                    simplified_item['eventenddate'] = ''
            
            if was_corrected:
                simplified_item['original_category'] = cat3_name
            
            categorized_data[correct_category].append(simplified_item)
        
        print(f"✅ {len(all_items)}개 수집" + (f" (재분류: {corrected_count}개)" if corrected_count > 0 else ""))
    
    # 카테고리별 파일 저장
    print(f"\n  💾 파일 저장 중...")
    
    # 축제공연행사인 경우 날짜 매칭 통계 출력
    if main_category == '축제공연행사':
        total_festivals = sum(len(items) for items in categorized_data.values())
        
        if total_festivals > 0:  # 0으로 나누기 방지
            matched_festivals = sum(
                1 for items in categorized_data.values() 
                for item in items 
                if item.get('eventstartdate')
            )
            print(f"\n  📅 날짜 정보 매칭 결과:")
            print(f"    ✅ 매칭 성공: {matched_festivals}개 ({matched_festivals/total_festivals*100:.1f}%)")
            print(f"    ⚠️ 매칭 실패: {total_festivals - matched_festivals}개 ({(total_festivals - matched_festivals)/total_festivals*100:.1f}%)")
            print()
        else:
            print(f"\n  ⚠️ 축제 데이터가 없어서 날짜 매칭을 수행하지 않았습니다.\n")
    
    for category, items in categorized_data.items():
        file_path = os.path.join(category_folder, f'{category}.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        print(f"    ✅ {category}: {len(items)}개 → {file_path}")

# 결과 요약
print("\n" + "=" * 80)
print("📊 전체 검증 결과 요약")
print("=" * 80)
print(f"총 수집: {validation_stats['total']:,}개")
print(f"재분류: {validation_stats['corrected']:,}개 ({validation_stats['corrected']/validation_stats['total']*100:.1f}%)")

if validation_stats['corrections']:
    print("\n⚠️ 재분류 상세:")
    for correction, count in sorted(validation_stats['corrections'].items(), key=lambda x: x[1], reverse=True)[:15]:
        print(f"  - {correction}: {count}개")

print(f"\n✅ 전체 데이터 수집 및 검증 완료!")
print(f"📁 저장 경로: {main_folder}/")
print("=" * 80)

