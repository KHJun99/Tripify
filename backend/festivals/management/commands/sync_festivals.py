from django.core.management.base import BaseCommand
from festivals.models import Festival
from external_api.festival_api import FestivalAPI
from datetime import datetime
import time


class Command(BaseCommand):
    help = '한국관광공사 API에서 축제 데이터를 가져와 데이터베이스에 동기화합니다'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='기존 데이터를 모두 삭제하고 새로 가져옵니다',
        )
        parser.add_argument(
            '--month',
            type=int,
            help='특정 월의 축제만 가져옵니다 (1-12)',
        )
        parser.add_argument(
            '--year',
            type=int,
            help='특정 연도의 축제만 가져옵니다 (기본: 현재 연도)',
        )

    def handle(self, *args, **options):
        self.stdout.write('한국관광공사 API에서 축제 데이터를 가져오는 중...')

        festival_api = FestivalAPI()

        # API 키 확인
        if not festival_api.api_key or festival_api.api_key == 'your_tour_api_key_here':
            self.stdout.write(
                self.style.ERROR(
                    '\n❌ TOUR_API_KEY가 설정되지 않았습니다!\n'
                    '   .env 파일에 한국관광공사 API 키를 설정해주세요.\n'
                    '   자세한 내용은 TOUR_API_SETUP.md를 참고하세요.\n'
                )
            )
            return

        # 기존 데이터 삭제 옵션
        if options['clear']:
            Festival.objects.all().delete()
            self.stdout.write(self.style.WARNING('기존 축제 데이터를 모두 삭제했습니다.'))

        # 연도 설정
        year = options.get('year') or datetime.now().year
        self.stdout.write(f'대상 연도: {year}년')

        # 월별로 데이터 가져오기
        months = [options['month']] if options['month'] else range(1, 13)
        total_created = 0
        total_updated = 0
        total_errors = 0

        for month in months:
            self.stdout.write(f'\n{month}월 축제 데이터 가져오는 중...')

            # API 호출
            response = festival_api.search_festivals(month=month, year=year)

            if not response:
                self.stdout.write(self.style.ERROR(f'{month}월 데이터를 가져오는데 실패했습니다.'))
                total_errors += 1
                continue

            # 응답 파싱
            try:
                items = response.get('response', {}).get('body', {}).get('items', {}).get('item', [])

                # items가 딕셔너리인 경우 리스트로 변환
                if isinstance(items, dict):
                    items = [items]

                for item in items:
                    created, updated = self._save_festival(item, current_year)
                    if created:
                        total_created += 1
                    if updated:
                        total_updated += 1

                self.stdout.write(self.style.SUCCESS(f'{month}월: {len(items)}개 항목 처리 완료'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'{month}월 데이터 파싱 오류: {e}'))
                continue

            # API 호출 제한 방지를 위한 대기
            time.sleep(0.5)

        # 결과 요약
        self.stdout.write('\n' + '='*50)
        if total_errors > 0:
            self.stdout.write(
                self.style.WARNING(
                    f'\n⚠️  완료 (일부 오류 발생)\n'
                    f'   생성: {total_created}개\n'
                    f'   업데이트: {total_updated}개\n'
                    f'   오류: {total_errors}개월\n\n'
                    f'💡 API 오류가 발생했습니다. 다음을 확인하세요:\n'
                    f'   1. .env 파일의 TOUR_API_KEY가 올바른지 확인\n'
                    f'   2. 공공데이터포털에서 API가 활성화되었는지 확인\n'
                    f'   3. API 일일 호출 제한을 초과하지 않았는지 확인\n'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✅ 완료!\n'
                    f'   생성: {total_created}개\n'
                    f'   업데이트: {total_updated}개\n'
                )
            )

    def _save_festival(self, item, current_year):
        """API 응답 아이템을 Festival 모델로 저장"""
        try:
            # API 응답에서 필요한 데이터 추출
            title = item.get('title', '').strip()
            addr1 = item.get('addr1', '').strip()
            event_start = item.get('eventstartdate', '')
            event_end = item.get('eventenddate', '')

            # 시작일에서 월 추출
            month = 1
            if event_start and len(event_start) >= 6:
                try:
                    month = int(event_start[4:6])
                except:
                    month = 1

            # 지역 추출 (주소에서 첫 번째 단어)
            region = self._extract_region(addr1)

            # 기간 포맷팅
            period = self._format_period(event_start, event_end)

            # 이미지 URL
            image_url = item.get('firstimage', '') or item.get('firstimage2', '') or 'https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=800'

            # 전화번호
            tel = item.get('tel', '').strip()

            # content_id로 중복 체크 (외부 API ID 저장을 위해 모델에 필드 추가 필요)
            # 현재는 name + region으로 중복 체크
            festival, created = Festival.objects.update_or_create(
                name=title,
                region=region,
                defaults={
                    'location': addr1,
                    'period': period,
                    'month': month,
                    'description': item.get('overview', title)[:200],  # 간단 설명
                    'detailed_description': item.get('overview', ''),
                    'image': image_url,
                    'contact': tel,
                    'tags': self._generate_tags(title, month),
                    'is_active': True,
                }
            )

            if created:
                self.stdout.write(f'  ✓ 생성: {title} ({region})')
            else:
                self.stdout.write(f'  ↻ 업데이트: {title} ({region})')

            return created, not created

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ✗ 저장 오류: {e}'))
            return False, False

    def _extract_region(self, addr):
        """주소에서 지역 추출"""
        if not addr:
            return '기타'

        # 주소의 첫 단어 추출
        parts = addr.split()
        if not parts:
            return '기타'

        first_part = parts[0]

        # 지역명 매핑
        region_map = {
            '서울': '서울', '서울특별시': '서울',
            '부산': '부산', '부산광역시': '부산',
            '대구': '대구', '대구광역시': '대구',
            '인천': '인천', '인천광역시': '인천',
            '광주': '광주', '광주광역시': '광주',
            '대전': '대전', '대전광역시': '대전',
            '울산': '울산', '울산광역시': '울산',
            '세종': '세종', '세종특별자치시': '세종',
            '경기': '경기', '경기도': '경기',
            '강원': '강원', '강원도': '강원', '강원특별자치도': '강원',
            '충북': '충북', '충청북도': '충북',
            '충남': '충남', '충청남도': '충남',
            '전북': '전북', '전라북도': '전북', '전북특별자치도': '전북',
            '전남': '전남', '전라남도': '전남',
            '경북': '경북', '경상북도': '경북',
            '경남': '경남', '경상남도': '경남',
            '제주': '제주', '제주도': '제주', '제주특별자치도': '제주',
        }

        return region_map.get(first_part, '기타')

    def _format_period(self, start, end):
        """날짜 포맷팅"""
        if not start or not end:
            return '일정 미정'

        try:
            # YYYYMMDD 형식을 YYYY.MM.DD로 변환
            if len(start) == 8 and len(end) == 8:
                start_formatted = f'{start[:4]}.{start[4:6]}.{start[6:8]}'
                end_formatted = f'{end[:4]}.{end[4:6]}.{end[6:8]}'
                return f'{start_formatted} - {end_formatted}'
        except:
            pass

        return f'{start} - {end}'

    def _generate_tags(self, title, month):
        """제목과 월을 기반으로 태그 생성"""
        tags = []

        # 계절 태그
        if month in [12, 1, 2]:
            tags.append('겨울')
        elif month in [3, 4, 5]:
            tags.append('봄')
        elif month in [6, 7, 8]:
            tags.append('여름')
        else:
            tags.append('가을')

        # 제목 기반 태그
        keywords = {
            '축제': '축제',
            '벚꽃': '벚꽃',
            '불꽃': '불꽃놀이',
            '음악': '음악',
            '페스티벌': '페스티벌',
            '문화': '문화',
            '전통': '전통',
            '먹거리': '음식',
            '음식': '음식',
            '바다': '해변',
            '해변': '해변',
            '산': '자연',
            '꽃': '꽃',
            '등': '등축제',
        }

        for keyword, tag in keywords.items():
            if keyword in title and tag not in tags:
                tags.append(tag)

        # 기본 태그
        if not tags:
            tags.append('축제')

        return tags[:5]  # 최대 5개
