<template>
  <div class="festivals-container">
    <div class="festivals-header">
      <h1>🎉 축제 및 행사 정보</h1>
      <p>전국의 다양한 축제와 행사를 찾아보세요</p>
    </div>

    <!-- 필터 섹션 -->
    <div class="filters">
      <div class="filter-group">
        <label>월별</label>
        <select v-model="selectedMonth" @change="applyFilters" class="filter-select">
          <option value="">전체</option>
          <option v-for="month in months" :key="month.value" :value="month.value">
            {{ month.label }}
          </option>
        </select>
      </div>

      <div class="filter-group">
        <label>지역별</label>
        <select v-model="selectedRegion" @change="applyFilters" class="filter-select">
          <option value="">전국</option>
          <option v-for="region in regions" :key="region" :value="region">
            {{ region }}
          </option>
        </select>
      </div>

      <button @click="resetFilters" class="reset-button">
        필터 초기화
      </button>
    </div>

    <!-- 축제 목록 -->
    <div v-if="filteredFestivals.length > 0" class="festivals-grid">
      <div v-for="festival in filteredFestivals" :key="festival.id" class="festival-card">
        <div class="festival-image">
          <img :src="festival.image" :alt="festival.name" />
          <div class="festival-badge">{{ festival.region }}</div>
        </div>
        <div class="festival-content">
          <h3>{{ festival.name }}</h3>
          <div class="festival-info">
            <div class="info-item">
              <span class="icon">📅</span>
              <span>{{ festival.period }}</span>
            </div>
            <div class="info-item">
              <span class="icon">📍</span>
              <span>{{ festival.location }}</span>
            </div>
          </div>
          <p class="festival-description">{{ festival.description }}</p>
          <div class="festival-tags">
            <span v-for="tag in festival.tags" :key="tag" class="tag">
              {{ tag }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 결과 없음 -->
    <div v-else class="no-results">
      <div class="no-results-icon">🔍</div>
      <h3>검색 결과가 없습니다</h3>
      <p>다른 조건으로 검색해보세요</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const selectedMonth = ref('')
const selectedRegion = ref('')

const months = [
  { value: 1, label: '1월' },
  { value: 2, label: '2월' },
  { value: 3, label: '3월' },
  { value: 4, label: '4월' },
  { value: 5, label: '5월' },
  { value: 6, label: '6월' },
  { value: 7, label: '7월' },
  { value: 8, label: '8월' },
  { value: 9, label: '9월' },
  { value: 10, label: '10월' },
  { value: 11, label: '11월' },
  { value: 12, label: '12월' },
]

const regions = [
  '서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종',
  '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주'
]

// 2025-2026년 축제 데이터 (실제 예정 일정 기반)
const festivals = ref([
  {
    id: 1,
    name: '화천 산천어 축제',
    region: '강원',
    location: '강원 화천군 화천읍',
    period: '2026.01.10 - 2026.02.01',
    month: 1,
    description: '얼음낚시로 유명한 겨울 대표 축제',
    image: 'https://images.unsplash.com/photo-1551632811-561732d1e306?w=400',
    tags: ['겨울', '얼음낚시', '가족']
  },
  {
    id: 2,
    name: '평창 송어축제',
    region: '강원',
    location: '강원 평창군 진부면',
    period: '2025.12.20 - 2026.02.28',
    month: 12,
    description: '겨울철 대표 얼음낚시 축제',
    image: 'https://images.unsplash.com/photo-1551632811-561732d1e306?w=400',
    tags: ['겨울', '얼음낚시', '송어']
  },
  {
    id: 3,
    name: '제주 들불축제',
    region: '제주',
    location: '제주 제주시 새별오름',
    period: '2026.03.06 - 2026.03.08',
    month: 3,
    description: '제주 전통 목축문화 재현 축제',
    image: 'https://images.unsplash.com/photo-1490730141103-6cac27aaab94?w=400',
    tags: ['전통', '봄', '제주']
  },
  {
    id: 4,
    name: '진해 군항제',
    region: '경남',
    location: '경남 창원시 진해구',
    period: '2026.04.01 - 2026.04.10',
    month: 4,
    description: '벚꽃과 함께하는 대한민국 대표 봄 축제',
    image: 'https://images.unsplash.com/photo-1522383225653-ed111181a951?w=400',
    tags: ['벚꽃', '봄', '가족']
  },
  {
    id: 5,
    name: '제주 유채꽃 축제',
    region: '제주',
    location: '제주 서귀포시',
    period: '2026.04.03 - 2026.04.12',
    month: 4,
    description: '노란 유채꽃 물결이 아름다운 봄 축제',
    image: 'https://images.unsplash.com/photo-1490730141103-6cac27aaab94?w=400',
    tags: ['유채꽃', '봄', '제주']
  },
  {
    id: 6,
    name: '전주 한옥마을 축제',
    region: '전북',
    location: '전북 전주시 한옥마을',
    period: '2026.05.01 - 2026.05.05',
    month: 5,
    description: '전통과 현대가 어우러지는 문화축제',
    image: 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400',
    tags: ['한옥', '전통', '문화']
  },
  {
    id: 7,
    name: '보령 머드축제',
    region: '충남',
    location: '충남 보령시 대천해수욕장',
    period: '2026.07.17 - 2026.07.26',
    month: 7,
    description: '세계적으로 유명한 머드 체험 축제',
    image: 'https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=400',
    tags: ['여름', '체험', '해변']
  },
  {
    id: 8,
    name: '대구 치맥 페스티벌',
    region: '대구',
    location: '대구 두류공원',
    period: '2026.07.08 - 2026.07.12',
    month: 7,
    description: '치킨과 맥주의 완벽한 조합',
    image: 'https://images.unsplash.com/photo-1562967914-608f82629710?w=400',
    tags: ['음식', '여름', '맥주']
  },
  {
    id: 9,
    name: '인천 펜타포트 록 페스티벌',
    region: '인천',
    location: '인천 송도 달빛축제공원',
    period: '2026.08.07 - 2026.08.09',
    month: 8,
    description: '국내외 유명 뮤지션이 한자리에',
    image: 'https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=400',
    tags: ['음악', '록', '페스티벌']
  },
  {
    id: 10,
    name: '안동 국제탈춤페스티벌',
    region: '경북',
    location: '경북 안동시',
    period: '2026.09.25 - 2026.10.04',
    month: 9,
    description: '세계의 탈춤과 민속공연을 한자리에',
    image: 'https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=400',
    tags: ['전통', '공연', '문화']
  },
  {
    id: 11,
    name: '서울 세계불꽃축제',
    region: '서울',
    location: '서울 여의도 한강공원',
    period: '2026.10.10',
    month: 10,
    description: '화려한 불꽃으로 물드는 서울의 밤',
    image: 'https://images.unsplash.com/photo-1467810563316-b5476525c0f9?w=400',
    tags: ['불꽃놀이', '가을', '데이트']
  },
  {
    id: 12,
    name: '부산 불꽃축제',
    region: '부산',
    location: '부산 광안리해수욕장',
    period: '2026.10.24',
    month: 10,
    description: '광안대교와 함께하는 화려한 불꽃쇼',
    image: 'https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=400',
    tags: ['불꽃놀이', '해변', '야경']
  },
  {
    id: 13,
    name: '광주 김치축제',
    region: '광주',
    location: '광주 김치타운',
    period: '2026.10.16 - 2026.10.19',
    month: 10,
    description: '김치의 모든 것을 경험하는 축제',
    image: 'https://images.unsplash.com/photo-1505253758473-96b7015fcd40?w=400',
    tags: ['음식', '김치', '전통']
  },
  {
    id: 14,
    name: '빛초롱축제',
    region: '경기',
    location: '경기 가평군 청평면',
    period: '2025.12.06 - 2026.03.08',
    month: 12,
    description: '겨울밤을 수놓는 화려한 빛의 향연',
    image: 'https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=400',
    tags: ['겨울', '야경', '데이트']
  },
  {
    id: 15,
    name: '태백 눈축제',
    region: '강원',
    location: '강원 태백시',
    period: '2026.01.16 - 2026.01.25',
    month: 1,
    description: '눈과 얼음으로 만드는 겨울왕국',
    image: 'https://images.unsplash.com/photo-1551632811-561732d1e306?w=400',
    tags: ['겨울', '눈', '가족']
  },
])

const filteredFestivals = computed(() => {
  return festivals.value.filter(festival => {
    const matchMonth = !selectedMonth.value || festival.month === selectedMonth.value
    const matchRegion = !selectedRegion.value || festival.region === selectedRegion.value
    return matchMonth && matchRegion
  })
})

const applyFilters = () => {
  // 필터가 변경될 때 자동으로 computed가 업데이트됨
}

const resetFilters = () => {
  selectedMonth.value = ''
  selectedRegion.value = ''
}

onMounted(() => {
  // 추후 API에서 축제 데이터를 가져올 수 있음
  // fetchFestivals()
})
</script>

<style scoped>
.festivals-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.festivals-header {
  text-align: center;
  margin-bottom: 3rem;
}

.festivals-header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  color: #333;
}

.festivals-header p {
  font-size: 1.1rem;
  color: #666;
}

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  flex-wrap: wrap;
  align-items: end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex: 1;
  min-width: 150px;
}

.filter-group label {
  font-weight: 600;
  color: #555;
  font-size: 0.9rem;
}

.filter-select {
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: border-color 0.2s;
}

.filter-select:focus {
  outline: none;
  border-color: #3498db;
}

.reset-button {
  padding: 0.75rem 1.5rem;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s;
  align-self: end;
}

.reset-button:hover {
  background-color: #5a6268;
}

.festivals-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 2rem;
}

.festival-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.festival-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.festival-image {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.festival-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.festival-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(52, 152, 219, 0.9);
  color: white;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.festival-content {
  padding: 1.5rem;
}

.festival-content h3 {
  font-size: 1.3rem;
  margin-bottom: 1rem;
  color: #333;
}

.festival-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #666;
  font-size: 0.9rem;
}

.info-item .icon {
  font-size: 1rem;
}

.festival-description {
  color: #777;
  line-height: 1.6;
  margin-bottom: 1rem;
  font-size: 0.95rem;
}

.festival-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  background: #f0f0f0;
  color: #555;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.85rem;
}

.no-results {
  text-align: center;
  padding: 4rem 2rem;
}

.no-results-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.no-results h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: #333;
}

.no-results p {
  color: #666;
}

@media (max-width: 768px) {
  .festivals-header h1 {
    font-size: 2rem;
  }

  .filters {
    flex-direction: column;
  }

  .filter-group {
    min-width: 100%;
  }

  .reset-button {
    width: 100%;
  }

  .festivals-grid {
    grid-template-columns: 1fr;
  }
}
</style>
