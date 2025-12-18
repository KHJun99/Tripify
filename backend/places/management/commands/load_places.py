import json
import os
from django.core.management.base import BaseCommand
from places.models import Place


class Command(BaseCommand):
    help = 'tourism_data 폴더의 JSON 파일들을 읽어 Place 모델에 로드합니다'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='기존 데이터를 삭제하고 새로 로드합니다',
        )

    def handle(self, *args, **options):
        # 기존 데이터 삭제 옵션
        if options['clear']:
            self.stdout.write('기존 Place 데이터를 삭제하는 중...')
            Place.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('기존 데이터 삭제 완료'))

        # tourism_data 폴더 경로
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        tourism_data_dir = os.path.join(base_dir, 'tourism_data')

        if not os.path.exists(tourism_data_dir):
            self.stdout.write(self.style.ERROR(f'tourism_data 폴더를 찾을 수 없습니다: {tourism_data_dir}'))
            return

        # 폴더와 place_type 매핑
        folder_mapping = {
            '관광지': 'tourist',
            '레포츠': 'tourist',
            '문화시설': 'tourist',
            '쇼핑': 'tourist',
            '숙박': 'accommodation',
            '음식점': 'restaurant',
            '축제공연행사': 'festival'
        }

        total_created = 0
        total_skipped = 0

        # 각 폴더 순회
        for folder_name, place_type in folder_mapping.items():
            folder_path = os.path.join(tourism_data_dir, folder_name)

            if not os.path.exists(folder_path):
                self.stdout.write(self.style.WARNING(f'폴더를 찾을 수 없습니다: {folder_name}'))
                continue

            self.stdout.write(f'\n[{folder_name}] 폴더 처리 중...')

            # 폴더 내 모든 JSON 파일 처리
            json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]

            for json_file in json_files:
                file_path = os.path.join(folder_path, json_file)
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
                        if Place.objects.filter(content_id=content_id).exists():
                            skipped_count += 1
                            continue

                        # 주소에서 지역 추출 (첫 번째 공백 전까지)
                        address = item.get('address', '')
                        region = address.split()[0] if address else ''

                        # Place 객체 생성
                        Place.objects.create(
                            title=item.get('title', ''),
                            place_type=place_type,
                            category=category,
                            address=address,
                            latitude=item.get('latitude'),
                            longitude=item.get('longitude'),
                            image_url=item.get('image', ''),
                            tel=item.get('phone', ''),
                            content_id=content_id,
                            region=region
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
