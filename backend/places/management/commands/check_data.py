import os
from django.core.management.base import BaseCommand
from places.models import Place
from festivals.models import Festival


class Command(BaseCommand):
    help = '데이터베이스에 로드된 장소 및 축제 데이터 개수를 확인합니다'

    def handle(self, *args, **options):
        self.stdout.write('\n' + '='*60)
        self.stdout.write('데이터베이스 데이터 현황')
        self.stdout.write('='*60 + '\n')

        # Place 데이터 통계
        total_places = Place.objects.count()
        tourist_spots = Place.objects.filter(place_type='tourist').count()
        restaurants = Place.objects.filter(place_type='restaurant').count()
        accommodations = Place.objects.filter(place_type='accommodation').count()

        self.stdout.write('📍 장소 데이터 (Place):')
        self.stdout.write(f'  - 전체: {total_places:,}개')
        self.stdout.write(f'  - 관광지: {tourist_spots:,}개')
        self.stdout.write(f'  - 음식점: {restaurants:,}개')
        self.stdout.write(f'  - 숙박시설: {accommodations:,}개')

        # 지역별 통계 (상위 10개)
        from django.db.models import Count
        region_stats = Place.objects.values('region').annotate(
            count=Count('id')
        ).order_by('-count')[:10]

        self.stdout.write('\n  지역별 상위 10개:')
        for stat in region_stats:
            if stat['region']:
                self.stdout.write(f'    - {stat["region"]}: {stat["count"]:,}개')

        # Festival 데이터 통계
        total_festivals = Festival.objects.count()
        
        self.stdout.write(f'\n🎉 축제 데이터 (Festival):')
        self.stdout.write(f'  - 전체: {total_festivals:,}개')

        # 카테고리별 통계
        category_stats = Festival.objects.values('category').annotate(
            count=Count('id')
        ).order_by('-count')[:10]

        self.stdout.write('\n  카테고리별 상위 10개:')
        for stat in category_stats:
            if stat['category']:
                self.stdout.write(f'    - {stat["category"]}: {stat["count"]:,}개')

        # 지역별 통계
        festival_region_stats = Festival.objects.values('region').annotate(
            count=Count('id')
        ).order_by('-count')[:10]

        self.stdout.write('\n  지역별 상위 10개:')
        for stat in festival_region_stats:
            if stat['region']:
                self.stdout.write(f'    - {stat["region"]}: {stat["count"]:,}개')

        self.stdout.write('\n' + '='*60)
        self.stdout.write(f'총 데이터: {total_places + total_festivals:,}개')
        self.stdout.write('='*60 + '\n')

