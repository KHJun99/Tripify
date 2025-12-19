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
      <div v-for="festival in filteredFestivals" :key="festival.id" class="festival-card" @click="goToDetail(festival.id)">
        <div class="festival-image">
          <img :src="festival.image_url || 'https://via.placeholder.com/400x200?text=Festival'" :alt="festival.title" />
          <div class="festival-badge">{{ festival.region }}</div>
        </div>
        <div class="festival-content">
          <h3>{{ festival.title }}</h3>
          <div class="festival-info">
            <div class="info-item">
              <span class="icon">📅</span>
              <span>{{ formatPeriod(festival) }}</span>
            </div>
            <div class="info-item">
              <span class="icon">📍</span>
              <span>{{ festival.address }}</span>
            </div>
          </div>
          <p class="festival-description" v-if="festival.category">{{ festival.category }}</p>
          <div class="festival-tags" v-if="festival.start_month">
            <span class="tag">{{ festival.start_month }}월</span>
            <span class="tag" v-if="festival.phone">{{ festival.phone }}</span>
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
import { useRouter } from 'vue-router'
import { getFestivals } from '@/api/festivals'

const router = useRouter()

const selectedMonth = ref('')
const selectedRegion = ref('')
const festivals = ref([])
const loading = ref(false)

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

// 날짜 포맷 함수
const formatPeriod = (festival) => {
  if (festival.event_start_date && festival.event_end_date) {
    const start = formatDate(festival.event_start_date)
    const end = formatDate(festival.event_end_date)
    return `${start} ~ ${end}`
  } else if (festival.event_start_date) {
    return formatDate(festival.event_start_date)
  } else if (festival.start_month) {
    return `${festival.start_month}월`
  }
  return '날짜 미정'
}

const formatDate = (dateStr) => {
  if (!dateStr || dateStr.length < 8) return dateStr
  const year = dateStr.substring(0, 4)
  const month = dateStr.substring(4, 6)
  const day = dateStr.substring(6, 8)
  return `${year}.${month}.${day}`
}

// Computed - 필터링된 축제 목록
const filteredFestivals = computed(() => {
  return festivals.value.filter(festival => {
    const matchMonth = !selectedMonth.value || festival.start_month === selectedMonth.value
    const matchRegion = !selectedRegion.value || festival.region.includes(selectedRegion.value)
    return matchMonth && matchRegion
  })
})

// API에서 축제 데이터 가져오기
const fetchFestivals = async () => {
  try {
    loading.value = true
    // 서버에서 모든 데이터를 가져옴 (필터링은 클라이언트에서 수행)
    const data = await getFestivals()
    festivals.value = data
  } catch (error) {
    console.error('축제 목록을 불러오는 데 실패했습니다:', error)
  } finally {
    loading.value = false
  }
}

const applyFilters = () => {
  // 클라이언트 측 필터링만 사용 (computed에서 자동 처리)
}

const resetFilters = () => {
  selectedMonth.value = ''
  selectedRegion.value = ''
}

const goToDetail = (festivalId) => {
  router.push({ name: 'festival-detail', params: { id: festivalId } })
}

onMounted(() => {
  fetchFestivals()
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
  cursor: pointer;
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
