<template>
  <div class="festivals-container">
    <div class="festivals-header">
      <h1>🎉 축제 및 행사 정보</h1>
      <p>전국의 다양한 축제와 행사를 찾아보세요</p>
    </div>

    <!-- 필터 섹션 -->
    <div class="filters">
      <div class="filter-group">
        <label>년도</label>
        <select v-model="selectedYear" @change="applyFilters" class="filter-select">
          <option value="">전체</option>
          <option v-for="year in years" :key="year" :value="year">
            {{ year }}년
          </option>
        </select>
      </div>

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
    <div v-if="paginatedFestivals.length > 0" class="festivals-grid">
      <div v-for="festival in paginatedFestivals" :key="festival.id" class="festival-card" @click="goToDetail(festival.id)">
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

    <!-- 페이지네이션 -->
    <div v-if="filteredFestivals.length > 0" class="pagination">
      <button
        @click="goToPage(1)"
        :disabled="currentPage === 1"
        class="pagination-button"
      >
        처음
      </button>
      <button
        @click="goToPage(currentPage - 1)"
        :disabled="currentPage === 1"
        class="pagination-button"
      >
        이전
      </button>

      <div class="pagination-numbers">
        <button
          v-for="page in visiblePages"
          :key="page"
          @click="goToPage(page)"
          :class="['pagination-number', { active: currentPage === page }]"
        >
          {{ page }}
        </button>
      </div>

      <button
        @click="goToPage(currentPage + 1)"
        :disabled="currentPage === totalPages"
        class="pagination-button"
      >
        다음
      </button>
      <button
        @click="goToPage(totalPages)"
        :disabled="currentPage === totalPages"
        class="pagination-button"
      >
        마지막
      </button>
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

const selectedYear = ref('')
const selectedMonth = ref('')
const selectedRegion = ref('')
const festivals = ref([])
const loading = ref(false)
const currentPage = ref(1)
const itemsPerPage = 12

// 년도 목록 생성 (현재 년도부터 +2년까지)
const currentYear = new Date().getFullYear()
const years = [currentYear, currentYear + 1, currentYear + 2]

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
  // eventstartdate와 eventenddate도 확인 (JSON 파일의 필드명)
  const startDate = festival.event_start_date || festival.eventstartdate
  const endDate = festival.event_end_date || festival.eventenddate

  if (startDate && endDate) {
    const start = formatDate(startDate)
    const end = formatDate(endDate)
    if (start === end) {
      return start
    }
    return `${start} ~ ${end}`
  } else if (startDate) {
    return formatDate(startDate)
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

// 년도 필터링 함수
const isInSelectedYear = (festival, selectedYear) => {
  if (!selectedYear) return true // 전체 선택 시 모든 축제 표시

  const startDate = festival.event_start_date || festival.eventstartdate
  const endDate = festival.event_end_date || festival.eventenddate

  if (startDate && startDate.length >= 4) {
    const startYear = parseInt(startDate.substring(0, 4))

    if (endDate && endDate.length >= 4) {
      const endYear = parseInt(endDate.substring(0, 4))
      // 축제 기간이 선택된 년도를 포함하는지 확인
      return selectedYear >= startYear && selectedYear <= endYear
    }

    return selectedYear === startYear
  }

  // 날짜 정보가 없으면 모든 년도에 표시
  return true
}

// 월 필터링 함수 - event_start_date와 event_end_date를 파싱하여 월 범위 확인
const isInSelectedMonth = (festival, selectedMonth) => {
  if (!selectedMonth) return true // 전체 선택 시 모든 축제 표시

  // start_month가 있으면 기존 로직 사용
  if (festival.start_month) {
    // 시작월과 종료월 범위 확인
    if (festival.end_month) {
      // 연말-연초를 넘어가는 경우 처리 (예: 12월 ~ 2월)
      if (festival.start_month > festival.end_month) {
        return selectedMonth >= festival.start_month || selectedMonth <= festival.end_month
      }
      return selectedMonth >= festival.start_month && selectedMonth <= festival.end_month
    }
    return selectedMonth === festival.start_month
  }

  // start_month가 없으면 event_start_date/eventstartdate와 event_end_date/eventenddate를 파싱
  const startDate = festival.event_start_date || festival.eventstartdate
  const endDate = festival.event_end_date || festival.eventenddate

  if (startDate && startDate.length >= 6) {
    const startMonth = parseInt(startDate.substring(4, 6))
    const startDay = startDate.length >= 8 ? parseInt(startDate.substring(6, 8)) : 1

    if (endDate && endDate.length >= 6) {
      const endMonth = parseInt(endDate.substring(4, 6))
      const endDay = endDate.length >= 8 ? parseInt(endDate.substring(6, 8)) : 31

      const startYear = parseInt(startDate.substring(0, 4))
      const endYear = parseInt(endDate.substring(0, 4))

      // 다년도에 걸친 축제인 경우
      if (startYear !== endYear) {
        return true // 여러 해에 걸친 축제는 모든 월에 표시
      }

      // 연말-연초를 넘어가는 경우 처리
      if (startMonth > endMonth) {
        return selectedMonth >= startMonth || selectedMonth <= endMonth
      }
      return selectedMonth >= startMonth && selectedMonth <= endMonth
    }

    return selectedMonth === startMonth
  }

  // 날짜 정보가 없으면 모든 월에 표시
  return true
}

// Computed - 필터링된 축제 목록
const filteredFestivals = computed(() => {
  return festivals.value.filter(festival => {
    const matchYear = isInSelectedYear(festival, selectedYear.value)
    const matchMonth = isInSelectedMonth(festival, selectedMonth.value)
    const matchRegion = !selectedRegion.value || festival.region.includes(selectedRegion.value)
    return matchYear && matchMonth && matchRegion
  })
})

// 전체 페이지 수
const totalPages = computed(() => {
  return Math.ceil(filteredFestivals.value.length / itemsPerPage)
})

// 페이지네이션된 축제 목록
const paginatedFestivals = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredFestivals.value.slice(start, end)
})

// 표시할 페이지 번호들 (최대 5개)
const visiblePages = computed(() => {
  const pages = []
  const total = totalPages.value
  const current = currentPage.value

  if (total <= 5) {
    // 전체 페이지가 5개 이하면 모두 표시
    for (let i = 1; i <= total; i++) {
      pages.push(i)
    }
  } else {
    // 현재 페이지를 중심으로 5개 표시
    let start = Math.max(1, current - 2)
    let end = Math.min(total, start + 4)

    // 끝에 가까우면 start 조정
    if (end === total) {
      start = Math.max(1, end - 4)
    }

    for (let i = start; i <= end; i++) {
      pages.push(i)
    }
  }

  return pages
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
  // 필터 변경 시 첫 페이지로 이동
  currentPage.value = 1
}

const resetFilters = () => {
  selectedYear.value = ''
  selectedMonth.value = ''
  selectedRegion.value = ''
  currentPage.value = 1
}

const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    // 페이지 이동 시 스크롤을 맨 위로
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
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
  object-position: center;
  /* 이미지 부드러운 스케일링 */
  image-rendering: auto;
  image-rendering: -webkit-optimize-contrast;
  -ms-interpolation-mode: bicubic;
  /* 렌더링 최적화 */
  backface-visibility: hidden;
  -webkit-font-smoothing: antialiased;
  will-change: transform;
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

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  margin-top: 3rem;
  padding: 2rem 0;
}

.pagination-button {
  padding: 0.6rem 1.2rem;
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  color: #555;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.pagination-button:hover:not(:disabled) {
  background: #f5f5f5;
  border-color: #3498db;
  color: #3498db;
}

.pagination-button:disabled {
  background: #f5f5f5;
  color: #ccc;
  cursor: not-allowed;
  border-color: #f0f0f0;
}

.pagination-numbers {
  display: flex;
  gap: 0.3rem;
}

.pagination-number {
  min-width: 40px;
  height: 40px;
  padding: 0.5rem;
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  color: #555;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pagination-number:hover {
  background: #f5f5f5;
  border-color: #3498db;
  color: #3498db;
}

.pagination-number.active {
  background: #3498db;
  border-color: #3498db;
  color: white;
  font-weight: 600;
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

  .pagination {
    flex-wrap: wrap;
    gap: 0.3rem;
  }

  .pagination-button {
    padding: 0.5rem 0.8rem;
    font-size: 0.85rem;
  }

  .pagination-number {
    min-width: 35px;
    height: 35px;
    font-size: 0.85rem;
  }
}
</style>
