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

    <!-- 결과 없음 -->
    <div v-else class="no-results">
      <div class="no-results-icon">🔍</div>
      <h3>검색 결과가 없습니다</h3>
      <p>다른 조건으로 검색해보세요</p>
    </div>

    <!-- 페이지네이션 -->
    <div v-if="totalPages > 1" class="pagination">
      <button 
        @click="goToPage(currentPage - 1)" 
        :disabled="currentPage === 1"
        class="pagination-btn"
      >
        이전
      </button>
      
      <div class="pagination-pages">
        <button
          v-for="page in visiblePages"
          :key="page"
          @click="goToPage(page)"
          :class="['pagination-page', { active: page === currentPage }]"
        >
          {{ page }}
        </button>
      </div>
      
      <button 
        @click="goToPage(currentPage + 1)" 
        :disabled="currentPage === totalPages"
        class="pagination-btn"
      >
        다음
      </button>
    </div>

    <!-- 페이지 정보 -->
    <div v-if="filteredFestivals.length > 0" class="page-info">
      전체 {{ filteredFestivals.length }}개 중 {{ startIndex + 1 }}-{{ endIndex }}개 표시
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
const currentPage = ref(1)
const itemsPerPage = 12

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
  // 디버깅: 첫 번째 항목만 출력
  if (process.env.NODE_ENV === 'development' && festivals.value.indexOf(festival) === 0) {
    console.log('🔍 첫 번째 축제 날짜 데이터:', {
      title: festival.title,
      event_start_date: festival.event_start_date,
      event_end_date: festival.event_end_date,
      start_month: festival.start_month,
      end_month: festival.end_month
    })
  }

  // event_start_date와 event_end_date가 있고 빈 문자열이 아닌 경우
  const startDate = festival.event_start_date
  const endDate = festival.event_end_date
  
  // null, undefined, 빈 문자열 체크
  const hasStartDate = startDate != null && startDate !== '' && String(startDate).trim() !== ''
  const hasEndDate = endDate != null && endDate !== '' && String(endDate).trim() !== ''
  
  if (hasStartDate && hasEndDate) {
    const startStr = String(startDate).trim()
    const endStr = String(endDate).trim()
    
    if (startStr.length >= 8 && endStr.length >= 8) {
      const start = formatDate(startStr)
      const end = formatDate(endStr)
      if (start && end) {
        return `${start} ~ ${end}`
      }
    }
  }
  
  // event_start_date만 있는 경우
  if (hasStartDate) {
    const startStr = String(startDate).trim()
    if (startStr.length >= 8) {
      const start = formatDate(startStr)
      if (start) {
        return start
      }
    }
  }
  
  // event_end_date만 있는 경우
  if (hasEndDate) {
    const endStr = String(endDate).trim()
    if (endStr.length >= 8) {
      const end = formatDate(endStr)
      if (end) {
        return end
      }
    }
  }
  
  // start_month와 end_month가 모두 있는 경우
  if (festival.start_month != null && festival.end_month != null) {
    const startMonth = Number(festival.start_month)
    const endMonth = Number(festival.end_month)
    if (!isNaN(startMonth) && !isNaN(endMonth)) {
      if (startMonth === endMonth) {
        return `${startMonth}월`
      } else {
        return `${startMonth}월 ~ ${endMonth}월`
      }
    }
  }
  
  // start_month만 있는 경우
  if (festival.start_month != null) {
    const startMonth = Number(festival.start_month)
    if (!isNaN(startMonth) && startMonth >= 1 && startMonth <= 12) {
      return `${startMonth}월`
    }
  }
  
  // end_month만 있는 경우
  if (festival.end_month != null) {
    const endMonth = Number(festival.end_month)
    if (!isNaN(endMonth) && endMonth >= 1 && endMonth <= 12) {
      return `${endMonth}월`
    }
  }
  
  return '날짜 미정'
}

const formatDate = (dateStr) => {
  if (!dateStr) return null
  
  // 문자열로 변환
  const str = String(dateStr).trim()
  
  // 최소 8자리 (YYYYMMDD) 확인
  if (str.length < 8) {
    return null
  }
  
  // 숫자만 있는지 확인
  if (!/^\d+$/.test(str)) {
    return null
  }
  
  const year = str.substring(0, 4)
  const month = str.substring(4, 6)
  const day = str.substring(6, 8)
  
  // 유효한 범위 확인
  const yearNum = parseInt(year, 10)
  const monthNum = parseInt(month, 10)
  const dayNum = parseInt(day, 10)
  
  if (isNaN(yearNum) || isNaN(monthNum) || isNaN(dayNum)) {
    return null
  }
  
  if (yearNum < 1900 || yearNum > 2100) return null
  if (monthNum < 1 || monthNum > 12) return null
  if (dayNum < 1 || dayNum > 31) return null
  
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

// Computed - 페이지네이션된 축제 목록
const paginatedFestivals = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredFestivals.value.slice(start, end)
})

// Computed - 전체 페이지 수
const totalPages = computed(() => {
  return Math.ceil(filteredFestivals.value.length / itemsPerPage)
})

// Computed - 현재 페이지의 시작/끝 인덱스
const startIndex = computed(() => {
  return (currentPage.value - 1) * itemsPerPage
})

const endIndex = computed(() => {
  const end = startIndex.value + itemsPerPage
  return Math.min(end, filteredFestivals.value.length)
})

// Computed - 표시할 페이지 번호들
const visiblePages = computed(() => {
  const pages = []
  const total = totalPages.value
  const current = currentPage.value
  
  // 최대 5개의 페이지 번호만 표시
  let start = Math.max(1, current - 2)
  let end = Math.min(total, start + 4)
  
  // 끝에서 5개 미만이면 시작점 조정
  if (end - start < 4) {
    start = Math.max(1, end - 4)
  }
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  
  return pages
})

// API에서 축제 데이터 가져오기
const fetchFestivals = async () => {
  try {
    loading.value = true
    // 서버에서 모든 데이터를 가져옴 (필터링은 클라이언트에서 수행)
    const data = await getFestivals()
    
    // 디버깅: 실제 API 응답 확인
    console.log('=== API 응답 데이터 ===')
    console.log('전체 데이터 타입:', Array.isArray(data) ? '배열' : typeof data)
    console.log('데이터 길이:', Array.isArray(data) ? data.length : 'N/A')
    
    if (Array.isArray(data) && data.length > 0) {
      console.log('첫 번째 축제 데이터:', data[0])
      console.log('첫 번째 축제 날짜 필드:', {
        event_start_date: data[0].event_start_date,
        event_end_date: data[0].event_end_date,
        start_month: data[0].start_month,
        end_month: data[0].end_month,
        title: data[0].title
      })
    }
    
    festivals.value = Array.isArray(data) ? data : (data.results || [])
  } catch (error) {
    console.error('축제 목록을 불러오는 데 실패했습니다:', error)
    console.error('에러 상세:', error.response?.data || error.message)
  } finally {
    loading.value = false
  }
}

const applyFilters = () => {
  // 필터 변경 시 첫 페이지로 이동
  currentPage.value = 1
}

const resetFilters = () => {
  selectedMonth.value = ''
  selectedRegion.value = ''
  currentPage.value = 1
}

const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    // 페이지 변경 시 스크롤을 맨 위로
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
  /* 이미지 렌더링 품질 향상 */
  image-rendering: -webkit-optimize-contrast;
  image-rendering: crisp-edges;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
  transform: translateZ(0);
  -webkit-transform: translateZ(0);
  /* 이미지 스무딩 개선 */
  -ms-interpolation-mode: bicubic;
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

/* 페이지네이션 스타일 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  margin: 3rem 0 1rem;
  padding: 1rem;
}

.pagination-btn {
  padding: 0.5rem 1rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.pagination-btn:hover:not(:disabled) {
  background-color: #2980b9;
}

.pagination-btn:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
  opacity: 0.6;
}

.pagination-pages {
  display: flex;
  gap: 0.25rem;
}

.pagination-page {
  min-width: 40px;
  height: 40px;
  padding: 0.5rem;
  background-color: white;
  color: #333;
  border: 2px solid #e0e0e0;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pagination-page:hover {
  background-color: #f0f0f0;
  border-color: #3498db;
}

.pagination-page.active {
  background-color: #3498db;
  color: white;
  border-color: #3498db;
  font-weight: bold;
}

.page-info {
  text-align: center;
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 2rem;
  padding: 0.5rem;
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
    gap: 0.25rem;
  }

  .pagination-pages {
    flex-wrap: wrap;
  }

  .pagination-page {
    min-width: 35px;
    height: 35px;
    font-size: 0.85rem;
  }

  .pagination-btn {
    padding: 0.4rem 0.8rem;
    font-size: 0.85rem;
  }
}
</style>
