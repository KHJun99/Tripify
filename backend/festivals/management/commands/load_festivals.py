from django.core.management.base import BaseCommand
from festivals.models import Festival


class Command(BaseCommand):
    help = '초기 축제 데이터를 로드합니다'

    def handle(self, *args, **options):
        self.stdout.write('축제 데이터를 로드하는 중...')

        # 기존 데이터 삭제
        Festival.objects.all().delete()

        festivals_data = [
            {
                'name': '화천 산천어 축제',
                'region': '강원',
                'location': '강원 화천군 화천읍',
                'period': '2026.01.10 - 2026.02.01',
                'month': 1,
                'description': '얼음낚시로 유명한 겨울 대표 축제',
                'detailed_description': '화천 산천어 축제는 겨울철 대표 축제로, 청정 강원도에서 펼쳐지는 얼음낚시 체험을 중심으로 다양한 겨울 레저 활동을 즐길 수 있습니다. 얼음 위에서 직접 산천어를 낚고, 바로 구워먹는 특별한 경험을 할 수 있습니다. 가족 단위 방문객들에게 특히 인기가 높으며, 매년 100만 명 이상이 방문하는 세계적인 겨울 축제입니다.',
                'image': 'https://images.unsplash.com/photo-1551632811-561732d1e306?w=800',
                'tags': ['겨울', '얼음낚시', '가족'],
                'fee': '무료 (일부 체험 유료)',
                'contact': '033-440-2575',
                'programs': [
                    {'icon': '🎣', 'name': '얼음낚시', 'description': '얼음 구멍을 뚫고 산천어를 직접 낚는 체험'},
                    {'icon': '🏂', 'name': '눈썰매', 'description': '가족과 함께 즐기는 눈썰매장'},
                    {'icon': '🍖', 'name': '산천어 맨손잡기', 'description': '얼음 물속에서 산천어를 맨손으로 잡는 체험'},
                    {'icon': '🎪', 'name': '겨울 축제', 'description': '다양한 공연과 이벤트'}
                ],
                'transportation': {
                    'public': '서울 → 화천: 동서울터미널에서 화천행 시외버스 이용 (약 2시간 30분)',
                    'car': '서울 → 화천: 경춘국도 이용, 약 2시간 소요'
                }
            },
            {
                'name': '평창 송어축제',
                'region': '강원',
                'location': '강원 평창군 진부면',
                'period': '2025.12.20 - 2026.02.28',
                'month': 12,
                'description': '겨울철 대표 얼음낚시 축제',
                'detailed_description': '평창 송어축제는 청정 자연에서 펼쳐지는 겨울 체험 축제입니다. 송어 얼음낚시를 비롯하여 눈썰매, 스노우래프팅 등 다양한 겨울 레포츠를 즐길 수 있습니다. 가족 단위 방문객들이 안전하고 즐겁게 겨울을 만끽할 수 있는 프로그램들이 준비되어 있습니다.',
                'image': 'https://images.unsplash.com/photo-1551632811-561732d1e306?w=800',
                'tags': ['겨울', '얼음낚시', '송어'],
                'fee': '입장료 10,000원',
                'contact': '033-336-4000',
                'programs': [
                    {'icon': '🎣', 'name': '송어 얼음낚시', 'description': '얼음 위에서 송어를 낚는 체험'},
                    {'icon': '⛷️', 'name': '스노우래프팅', 'description': '눈 위를 달리는 스릴 넘치는 체험'},
                    {'icon': '🛷', 'name': '눈썰매', 'description': '어린이부터 어른까지 즐기는 눈썰매'}
                ],
                'transportation': {
                    'public': '서울 → 평창: 동서울터미널에서 진부행 버스 이용',
                    'car': '영동고속도로 진부IC 이용, 축제장까지 5분'
                }
            },
            {
                'name': '제주 들불축제',
                'region': '제주',
                'location': '제주 제주시 새별오름',
                'period': '2026.03.06 - 2026.03.08',
                'month': 3,
                'description': '제주 전통 목축문화 재현 축제',
                'detailed_description': '제주 들불축제는 제주의 전통 목축문화를 재현하는 독특한 축제입니다. 새별오름의 들판에 불을 놓아 해충을 없애고 새싹이 돋아나게 하는 전통 풍습을 현대적으로 재해석한 축제로, 거대한 불꽃이 밤하늘을 수놓는 장관을 볼 수 있습니다.',
                'image': 'https://images.unsplash.com/photo-1490730141103-6cac27aaab94?w=800',
                'tags': ['전통', '봄', '제주'],
                'fee': '무료',
                'contact': '064-728-3983',
                'programs': [
                    {'icon': '🔥', 'name': '들불놓기', 'description': '전통 방식의 들불놓기 재현'},
                    {'icon': '🎭', 'name': '전통공연', 'description': '제주 전통 문화 공연'},
                    {'icon': '🎆', 'name': '불꽃놀이', 'description': '밤하늘을 수놓는 화려한 불꽃쇼'}
                ],
                'transportation': {
                    'public': '제주공항에서 택시 또는 버스 이용 (약 30분)',
                    'car': '제주공항에서 1132번 도로 이용, 약 20분'
                }
            },
            {
                'name': '진해 군항제',
                'region': '경남',
                'location': '경남 창원시 진해구',
                'period': '2026.04.01 - 2026.04.10',
                'month': 4,
                'description': '벚꽃과 함께하는 대한민국 대표 봄 축제',
                'detailed_description': '진해 군항제는 대한민국 최대 벚꽃 축제로, 약 36만 그루의 벚나무가 만개하는 장관을 볼 수 있습니다. 진해 시가지 전체가 벚꽃으로 물들며, 여좌천 로망스 다리, 경화역 등 포토존이 가득합니다. 해군 함정 공개 행사와 함께 다채로운 문화 행사가 펼쳐집니다.',
                'image': 'https://images.unsplash.com/photo-1522383225653-ed111181a951?w=800',
                'tags': ['벚꽃', '봄', '가족'],
                'fee': '무료',
                'contact': '055-225-2341',
                'programs': [
                    {'icon': '🌸', 'name': '벚꽃 명소 탐방', 'description': '여좌천, 경화역 등 명소 투어'},
                    {'icon': '⚓', 'name': '해군 함정 공개', 'description': '해군 함정 승선 체험'},
                    {'icon': '🎭', 'name': '문화공연', 'description': '다양한 거리 공연과 이벤트'}
                ],
                'transportation': {
                    'public': '마산역에서 진해행 버스 이용 (약 30분)',
                    'car': '남해고속도로 진영IC 이용, 약 30분'
                }
            },
            {
                'name': '제주 유채꽃 축제',
                'region': '제주',
                'location': '제주 서귀포시',
                'period': '2026.04.03 - 2026.04.12',
                'month': 4,
                'description': '노란 유채꽃 물결이 아름다운 봄 축제',
                'detailed_description': '제주 유채꽃 축제는 제주도의 봄을 대표하는 축제입니다. 광활한 들판을 가득 메운 노란 유채꽃과 푸른 바다, 하늘이 어우러진 절경을 감상할 수 있습니다. 유채꽃밭 사이를 걸으며 사진을 찍고, 제주의 봄을 만끽할 수 있는 최고의 시기입니다.',
                'image': 'https://images.unsplash.com/photo-1490730141103-6cac27aaab94?w=800',
                'tags': ['유채꽃', '봄', '제주'],
                'fee': '무료',
                'contact': '064-760-2114',
                'programs': [
                    {'icon': '🌼', 'name': '유채꽃밭 산책', 'description': '광활한 유채꽃밭 탐방'},
                    {'icon': '📸', 'name': '포토존 투어', 'description': '인생샷 명소 투어'},
                    {'icon': '🎨', 'name': '체험 프로그램', 'description': '유채꽃 화관 만들기 등'}
                ],
                'transportation': {
                    'public': '제주공항에서 버스 이용 (약 1시간)',
                    'car': '제주공항에서 1132번 도로 이용, 약 40분'
                }
            },
            {
                'name': '전주 한옥마을 축제',
                'region': '전북',
                'location': '전북 전주시 한옥마을',
                'period': '2026.05.01 - 2026.05.05',
                'month': 5,
                'description': '전통과 현대가 어우러지는 문화축제',
                'detailed_description': '전주 한옥마을 축제는 700여 채의 한옥이 밀집한 전주 한옥마을에서 열리는 전통문화 축제입니다. 한복 체험, 전통 공예, 한식 체험 등 다양한 프로그램을 통해 한국의 전통문화를 경험할 수 있습니다.',
                'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800',
                'tags': ['한옥', '전통', '문화'],
                'fee': '무료 (일부 체험 유료)',
                'contact': '063-282-1330',
                'programs': [
                    {'icon': '👘', 'name': '한복 체험', 'description': '전통 한복 입고 한옥마을 산책'},
                    {'icon': '🎨', 'name': '전통 공예', 'description': '부채, 탈 만들기 등'},
                    {'icon': '🍜', 'name': '전주 비빔밥', 'description': '전주 10미 맛보기'}
                ],
                'transportation': {
                    'public': '전주역에서 버스 이용 (약 20분)',
                    'car': '호남고속도로 전주IC 이용, 약 15분'
                }
            },
            {
                'name': '보령 머드축제',
                'region': '충남',
                'location': '충남 보령시 대천해수욕장',
                'period': '2026.07.17 - 2026.07.26',
                'month': 7,
                'description': '세계적으로 유명한 머드 체험 축제',
                'detailed_description': '보령 머드축제는 세계 5대 축제 중 하나로, 보령의 청정 머드를 활용한 다양한 체험 프로그램을 즐길 수 있습니다. 머드 슬라이드, 머드 풀, 머드 마사지 등 온 가족이 함께 즐길 수 있는 여름 축제입니다.',
                'image': 'https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=800',
                'tags': ['여름', '체험', '해변'],
                'fee': '입장료 15,000원',
                'contact': '041-930-3882',
                'programs': [
                    {'icon': '🏖️', 'name': '머드 슬라이드', 'description': '거대한 머드 미끄럼틀'},
                    {'icon': '💆', 'name': '머드 마사지', 'description': '천연 머드 마사지 체험'},
                    {'icon': '🎪', 'name': '머드 레슬링', 'description': '머드 속에서 즐기는 레슬링'}
                ],
                'transportation': {
                    'public': '서울 남부터미널에서 대천행 버스 이용 (약 2시간 30분)',
                    'car': '서해안고속도로 대천IC 이용, 약 2시간'
                }
            },
            {
                'name': '대구 치맥 페스티벌',
                'region': '대구',
                'location': '대구 두류공원',
                'period': '2026.07.08 - 2026.07.12',
                'month': 7,
                'description': '치킨과 맥주의 완벽한 조합',
                'detailed_description': '대구 치맥 페스티벌은 치킨과 맥주를 주제로 한 독특한 축제입니다. 전국의 유명 치킨 브랜드와 수제 맥주를 한자리에서 맛볼 수 있으며, K-POP 공연과 다양한 이벤트가 함께 펼쳐집니다.',
                'image': 'https://images.unsplash.com/photo-1562967914-608f82629710?w=800',
                'tags': ['음식', '여름', '맥주'],
                'fee': '입장료 5,000원',
                'contact': '053-803-4000',
                'programs': [
                    {'icon': '🍗', 'name': '치킨 맛보기', 'description': '전국 유명 치킨 브랜드 시식'},
                    {'icon': '🍺', 'name': '맥주 페어링', 'description': '다양한 수제 맥주 체험'},
                    {'icon': '🎤', 'name': 'K-POP 공연', 'description': '유명 가수들의 라이브 공연'}
                ],
                'transportation': {
                    'public': '대구역에서 지하철 1호선 이용, 두류공원역 하차',
                    'car': '경부고속도로 대구IC 이용, 약 20분'
                }
            },
            {
                'name': '인천 펜타포트 록 페스티벌',
                'region': '인천',
                'location': '인천 송도 달빛축제공원',
                'period': '2026.08.07 - 2026.08.09',
                'month': 8,
                'description': '국내외 유명 뮤지션이 한자리에',
                'detailed_description': '인천 펜타포트 록 페스티벌은 국내 최대 규모의 록 페스티벌로, 국내외 유명 뮤지션들의 라이브 공연을 즐길 수 있습니다. 3일간 쉼 없이 이어지는 열정적인 무대와 음악을 사랑하는 이들의 축제입니다.',
                'image': 'https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=800',
                'tags': ['음악', '록', '페스티벌'],
                'fee': '3일권 150,000원',
                'contact': '1544-1555',
                'programs': [
                    {'icon': '🎸', 'name': '메인 스테이지', 'description': '헤드라이너 공연'},
                    {'icon': '🎵', 'name': '서브 스테이지', 'description': '신인 밴드 발굴 무대'},
                    {'icon': '🎪', 'name': '부대행사', 'description': '푸드트럭, 체험 부스 등'}
                ],
                'transportation': {
                    'public': '인천역에서 지하철 1호선 이용, 송도국제도시역 하차',
                    'car': '경인고속도로 인천IC 이용, 약 20분'
                }
            },
            {
                'name': '안동 국제탈춤페스티벌',
                'region': '경북',
                'location': '경북 안동시',
                'period': '2026.09.25 - 2026.10.04',
                'month': 9,
                'description': '세계의 탈춤과 민속공연을 한자리에',
                'detailed_description': '안동 국제탈춤페스티벌은 한국의 전통 탈춤과 세계 각국의 탈 문화를 한자리에서 볼 수 있는 국제 축제입니다. 하회별신굿탈놀이를 비롯한 다양한 전통 공연과 체험 프로그램이 준비되어 있습니다.',
                'image': 'https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=800',
                'tags': ['전통', '공연', '문화'],
                'fee': '무료',
                'contact': '054-841-6397',
                'programs': [
                    {'icon': '🎭', 'name': '하회별신굿탈놀이', 'description': 'UNESCO 무형문화유산 공연'},
                    {'icon': '🌏', 'name': '세계 탈춤 공연', 'description': '각국의 전통 탈춤 공연'},
                    {'icon': '🎨', 'name': '탈 만들기', 'description': '나만의 탈 만들기 체험'}
                ],
                'transportation': {
                    'public': '안동역에서 버스 이용 (약 30분)',
                    'car': '중앙고속도로 안동IC 이용, 약 15분'
                }
            },
            {
                'name': '서울 세계불꽃축제',
                'region': '서울',
                'location': '서울 여의도 한강공원',
                'period': '2026.10.10',
                'month': 10,
                'description': '화려한 불꽃으로 물드는 서울의 밤',
                'detailed_description': '서울 세계불꽃축제는 세계 최고 수준의 불꽃 업체들이 참가하여 화려한 불꽃쇼를 선보이는 축제입니다. 한강의 밤하늘을 수놓는 환상적인 불꽃과 음악이 어우러진 특별한 경험을 할 수 있습니다.',
                'image': 'https://images.unsplash.com/photo-1467810563316-b5476525c0f9?w=800',
                'tags': ['불꽃놀이', '가을', '데이트'],
                'fee': '무료',
                'contact': '02-3780-0561',
                'programs': [
                    {'icon': '🎆', 'name': '불꽃쇼', 'description': '세계 최고 수준의 불꽃 공연'},
                    {'icon': '🎵', 'name': '음악 콘서트', 'description': '유명 가수들의 공연'},
                    {'icon': '🍴', 'name': '푸드존', 'description': '다양한 음식과 먹거리'}
                ],
                'transportation': {
                    'public': '지하철 5호선 여의나루역 하차',
                    'car': '여의도 주변 주차장 이용 (교통 혼잡 예상)'
                }
            },
            {
                'name': '부산 불꽃축제',
                'region': '부산',
                'location': '부산 광안리해수욕장',
                'period': '2026.10.24',
                'month': 10,
                'description': '광안대교와 함께하는 화려한 불꽃쇼',
                'detailed_description': '부산 불꽃축제는 광안대교를 배경으로 펼쳐지는 국내 최대 규모의 불꽃 축제입니다. 바다 위에서 쏘아 올리는 불꽃과 광안대교의 조명이 어우러져 환상적인 야경을 만들어냅니다. 매년 100만 명 이상이 찾는 부산의 대표 축제입니다.',
                'image': 'https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=800',
                'tags': ['불꽃놀이', '해변', '야경'],
                'fee': '무료',
                'contact': '051-749-6221',
                'programs': [
                    {'icon': '🎇', 'name': '해상 불꽃쇼', 'description': '바다 위에서 펼쳐지는 불꽃 공연'},
                    {'icon': '🌉', 'name': '광안대교 조명쇼', 'description': '광안대교 LED 조명 연출'},
                    {'icon': '🎤', 'name': '축하 공연', 'description': '유명 가수들의 축하 공연'}
                ],
                'transportation': {
                    'public': '지하철 2호선 광안역 하차',
                    'car': '수영구 광안리 일대 (교통 혼잡 예상, 대중교통 이용 권장)'
                }
            },
            {
                'name': '광주 김치축제',
                'region': '광주',
                'location': '광주 김치타운',
                'period': '2026.10.16 - 2026.10.19',
                'month': 10,
                'description': '김치의 모든 것을 경험하는 축제',
                'detailed_description': '광주 김치축제는 한국의 대표 음식인 김치를 주제로 한 축제입니다. 김치 담그기 체험, 다양한 김치 요리 시식, 김치 관련 전시와 공연 등 김치의 모든 것을 경험할 수 있습니다.',
                'image': 'https://images.unsplash.com/photo-1505253758473-96b7015fcd40?w=800',
                'tags': ['음식', '김치', '전통'],
                'fee': '무료',
                'contact': '062-613-3990',
                'programs': [
                    {'icon': '🥬', 'name': '김치 담그기', 'description': '전통 방식의 김치 담그기 체험'},
                    {'icon': '🍽️', 'name': '김치 요리', 'description': '다양한 김치 요리 시식'},
                    {'icon': '🎭', 'name': '문화 공연', 'description': '전통 공연과 이벤트'}
                ],
                'transportation': {
                    'public': '광주송정역에서 버스 이용 (약 20분)',
                    'car': '호남고속도로 광주IC 이용, 약 20분'
                }
            },
            {
                'name': '빛초롱축제',
                'region': '경기',
                'location': '경기 가평군 청평면',
                'period': '2025.12.06 - 2026.03.08',
                'month': 12,
                'description': '겨울밤을 수놓는 화려한 빛의 향연',
                'detailed_description': '가평 빛초롱축제는 청평호반을 따라 펼쳐지는 대규모 빛 축제입니다. 수백만 개의 LED 조명으로 꾸며진 다양한 조형물과 빛 터널이 겨울밤을 환상적으로 물들입니다. 연인들의 데이트 명소로 인기가 높습니다.',
                'image': 'https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=800',
                'tags': ['겨울', '야경', '데이트'],
                'fee': '입장료 10,000원',
                'contact': '031-8008-6100',
                'programs': [
                    {'icon': '💡', 'name': '빛 터널', 'description': '화려한 LED 터널 산책'},
                    {'icon': '🎨', 'name': '빛 조형물', 'description': '대형 빛 조형물 감상'},
                    {'icon': '📸', 'name': '포토존', 'description': '인생샷 명소 투어'}
                ],
                'transportation': {
                    'public': '청평역에서 셔틀버스 이용',
                    'car': '경춘국도 이용, 약 1시간 30분'
                }
            },
            {
                'name': '태백 눈축제',
                'region': '강원',
                'location': '강원 태백시',
                'period': '2026.01.16 - 2026.01.25',
                'month': 1,
                'description': '눈과 얼음으로 만드는 겨울왕국',
                'detailed_description': '태백 눈축제는 산간 지역의 풍부한 적설량을 활용한 겨울 축제입니다. 대형 눈 조각 작품과 얼음 조각 전시, 눈썰매, 스노우래프팅 등 다양한 겨울 레포츠를 즐길 수 있습니다.',
                'image': 'https://images.unsplash.com/photo-1551632811-561732d1e306?w=800',
                'tags': ['겨울', '눈', '가족'],
                'fee': '무료',
                'contact': '033-550-2081',
                'programs': [
                    {'icon': '⛄', 'name': '눈 조각', 'description': '대형 눈 조각 작품 전시'},
                    {'icon': '🧊', 'name': '얼음 조각', 'description': '환상적인 얼음 조각 전시'},
                    {'icon': '🛷', 'name': '눈썰매', 'description': '가족과 함께 즐기는 눈썰매'}
                ],
                'transportation': {
                    'public': '태백역에서 도보 또는 택시 이용',
                    'car': '영동고속도로 제천IC 이용, 약 1시간'
                }
            }
        ]

        # 축제 데이터 생성
        created_count = 0
        for data in festivals_data:
            Festival.objects.create(**data)
            created_count += 1
            self.stdout.write(f'생성됨: {data["name"]}')

        self.stdout.write(
            self.style.SUCCESS(f'\n성공적으로 {created_count}개의 축제 데이터를 로드했습니다!')
        )
