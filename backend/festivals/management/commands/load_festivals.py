import json
import os
from django.core.management.base import BaseCommand
from festivals.models import Festival


class Command(BaseCommand):
    help = 'tourism_data의 축제공연행사 폴더에서 JSON 파일들을 읽어 Festival 모델에 로드합니다'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='기존 데이터를 삭제하고 새로 로드합니다',
        )

    def handle(self, *args, **options):
        # 기존 데이터 삭제 옵션
        if options['clear']:
            self.stdout.write('기존 Festival 데이터를 삭제하는 중...')
            Festival.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('기존 데이터 삭제 완료'))

        # tourism_data 폴더 경로
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        tourism_data_dir = os.path.join(base_dir, 'tourism_data', '축제공연행사')

        if not os.path.exists(tourism_data_dir):
            self.stdout.write(self.style.ERROR(f'축제공연행사 폴더를 찾을 수 없습니다: {tourism_data_dir}'))
            return

        total_created = 0
        total_skipped = 0

        self.stdout.write('\n[축제공연행사] 폴더 처리 중...')

        # 폴더 내 모든 JSON 파일 처리
        json_files = [f for f in os.listdir(tourism_data_dir) if f.endswith('.json')]

        for json_file in json_files:
            file_path = os.path.join(tourism_data_dir, json_file)
            category = json_file.replace('.json', '')  # 파일명이 카테고리

            self.stdout.write(f'  - {json_file} 읽는 중...')

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data_list = json.load(f)

                created_count = 0
                skipped_count = 0

                for item in data_list:
                    # content_id는 id 필드를 사용
                    content_id = item.get('id', '')

                    # 이미 존재하는 데이터는 스킵
                    if Festival.objects.filter(content_id=content_id).exists():
                        skipped_count += 1
                        continue

                    # 주소에서 지역 추출 (첫 번째 공백 전까지)
                    address = item.get('address', '')
                    region = address.split()[0] if address else ''

                    # 날짜에서 월 추출 (YYYYMMDD 형식)
                    event_start_date = item.get('eventstartdate', '')
                    event_end_date = item.get('eventenddate', '')

                    start_month = None
                    end_month = None

                    if event_start_date and len(event_start_date) >= 6:
                        try:
                            start_month = int(event_start_date[4:6])
                        except ValueError:
                            pass

                    if event_end_date and len(event_end_date) >= 6:
                        try:
                            end_month = int(event_end_date[4:6])
                        except ValueError:
                            pass

                    # Festival 객체 생성
                    Festival.objects.create(
                        title=item.get('title', ''),
                        category=category,
                        address=address,
                        phone=item.get('phone', ''),
                        latitude=item.get('latitude'),
                        longitude=item.get('longitude'),
                        image_url=item.get('image', ''),
                        event_start_date=event_start_date,
                        event_end_date=event_end_date,
                        start_month=start_month,
                        end_month=end_month,
                        region=region,
                        content_id=content_id
                    )
                    created_count += 1

                total_created += created_count
                total_skipped += skipped_count

                self.stdout.write(f'    OK 생성: {created_count}개, 스킵: {skipped_count}개')

            except json.JSONDecodeError as e:
                self.stdout.write(self.style.ERROR(f'    ERROR JSON 파싱 오류: {e}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'    ERROR 오류: {e}'))

        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'완료! 총 {total_created}개 생성, {total_skipped}개 스킵'))
        self.stdout.write('='*60)
