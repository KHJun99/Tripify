<template>
  <div class="page-wrapper">
    <div class="festivals-container">
      <!-- 헤더 -->
      <div class="festivals-header">
        <span class="sub-title">Travel & Culture</span>
        <h1>축제 및 행사</h1>
        <p>전국의 다채로운 경험, 여행의 즐거움을 발견하세요.</p>
      </div>

      <!-- 필터 섹션 -->
      <div class="filters-wrapper">
        <div class="filters">
          <div class="filter-group">
            <label>기간 선택</label>
            <div class="select-wrapper">
              <select v-model="selectedMonth" @change="applyFilters" class="filter-select">
                <option value="">전체 기간</option>
                <option v-for="month in months" :key="month.value" :value="month.value">
                  {{ month.label }}
                </option>
              </select>
              <svg class="select-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </div>
          </div>

          <div class="filter-group">
            <label>지역 선택</label>
            <div class="select-wrapper">
              <select v-model="selectedRegion" @change="applyFilters" class="filter-select">
                <option value="">전국 전체</option>
                <option v-for="region in regions" :key="region" :value="region">
                  {{ region }}
                </option>
              </select>
              <svg class="select-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </div>
          </div>

          <button @click="resetFilters" class="reset-button" aria-label="필터 초기화">
            <div class="icon-box">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 12"/>
                <path d="M3 3l0 9l9 0"/>
              </svg>
            </div>
            <span>초기화</span>
          </button>
        </div>
      </div>

      <!-- 축제 목록 -->
      <div v-if="paginatedFestivals.length > 0" class="festivals-grid">
        <div v-for="festival in paginatedFestivals" :key="festival.id" class="festival-card" @click="goToDetail(festival.id)">
          <div class="card-image-wrapper">
            <img :src="festival.image_url || 'https://via.placeholder.com/400x250/e0e0e0/888888?text=No+Image'" :alt="festival.title" />
            <div class="location-badge">{{ festival.region }}</div>
          </div>
          
          <div class="card-content">
            <div class="card-meta-top">
              <span class="category-text" v-if="festival.category">{{ festival.category }}</span>
            </div>
            
            <h3 class="card-title">{{ festival.title }}</h3>
            
            <div class="card-info-list">
              <div class="info-item">
                <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                  <line x1="16" y1="2" x2="16" y2="6"></line>
                  <line x1="8" y1="2" x2="8" y2="6"></line>
                  <line x1="3" y1="10" x2="21" y2="10"></line>
                </svg>
                <span>{{ formatPeriod(festival) }}</span>
              </div>
              <div class="info-item address">
                <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                  <circle cx="12" cy="10" r="3"></circle>
                </svg>
                <span>{{ festival.address }}</span>
              </div>
            </div>

            <div class="card-tags" v-if="festival.start_month">
              <span class="tag">{{ festival.start_month }}월 행사</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 결과 없음 -->
      <div v-else class="no-results">
        <div class="empty-state-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#e0e0e0" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </div>
        <h3>조건에 맞는 축제가 없습니다</h3>
        <p>검색 필터를 변경하여 다른 행사를 찾아보세요.</p>
        <button @click="resetFilters" class="btn-retry">모든 축제 보기</button>
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
        return `${start} - ${end}`
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
        return `${startMonth}월 - ${endMonth}월`
      }
    }
  }
  
  // start_month만 있는 경우
  if (festival.start_month != null) {
    const startMonth = Number(festival.start_month)
    if (!isNaN(startMonth) && startMonth >= 1 && startMonth <= 12) {
      return `${startMonth}월 예정`
    }
  }
  
  // end_month만 있는 경우
  if (festival.end_month != null) {
    const endMonth = Number(festival.end_month)
    if (!isNaN(endMonth) && endMonth >= 1 && endMonth <= 12) {
      return `${endMonth}월 예정`
    }
  }
  
  return '일정 미정'
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
@import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;500;600;700;800&display=swap');

* {
  box-sizing: border-box;
}

.page-wrapper {
  min-height: 100vh;
  background-color: #f8f9fa;
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
  color: #111;
}

.festivals-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 4rem 2rem;
}

/* Header Section */
.festivals-header {
  text-align: center;
  margin-bottom: 3.5rem;
}

.sub-title {
  display: block;
  font-size: 0.85rem;
  font-weight: 600;
  color: #6a11cb;
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}

.festivals-header h1 {
  font-size: 2.8rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color: #1a1a1a;
  letter-spacing: -0.02em;
}

.festivals-header p {
  font-size: 1.15rem;
  color: #666;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
}

/* Filters Section */
.filters-wrapper {
  position: sticky;
  top: 1rem;
  z-index: 10;
  margin-bottom: 3rem;
}

.filters {
  display: flex;
  gap: 1.5rem;
  padding: 1.25rem 2rem;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
  align-items: flex-end;
  max-width: 1000px;
  margin: 0 auto;
}

.filter-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.filter-group label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #888;
  margin-left: 0.2rem;
}

.select-wrapper {
  position: relative;
}

.filter-select {
  width: 100%;
  appearance: none;
  background-color: #fff;
  border: 1px solid #e1e4e8;
  border-radius: 12px;
  padding: 0.9rem 1rem;
  font-size: 1rem;
  color: #333;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
  height: 52px;
}

.filter-select:hover {
  border-color: #b0b8c1;
}

.filter-select:focus {
  outline: none;
  border-color: #6a11cb;
  box-shadow: 0 0 0 3px rgba(106, 17, 203, 0.1);
}

.select-icon {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
  color: #888;
  width: 18px;
  height: 18px;
}

/* 초기화 버튼 */
.reset-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  padding: 0 1.5rem;
  height: 52px;
  background-color: #ffffff;
  border: 1px solid #e1e4e8;
  border-radius: 12px;
  color: #555;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  white-space: nowrap;
}

.reset-button .icon-box {
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.5s ease;
}

.reset-button:hover {
  border-color: #6a11cb;
  color: #6a11cb;
  background-color: #fcfaff;
  box-shadow: 0 4px 12px rgba(106, 17, 203, 0.1);
  transform: translateY(-1px);
}

.reset-button:hover .icon-box {
  transform: rotate(-180deg);
}

.reset-button:active {
  transform: translateY(1px);
}

/* Grid Layout */
.festivals-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 2.5rem;
  margin-bottom: 3rem;
}

/* Card Design */
.festival-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
  border: 1px solid rgba(0, 0, 0, 0.02);
  display: flex;
  flex-direction: column;
  height: 100%;
}

.festival-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
}

.festival-card:hover .card-image-wrapper img {
  transform: scale(1.05);
}

.card-image-wrapper {
  position: relative;
  width: 100%;
  padding-top: 60%;
  overflow: hidden;
}

.card-image-wrapper img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
  image-rendering: -webkit-optimize-contrast;
  image-rendering: crisp-edges;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
  transform: translateZ(0);
  -webkit-transform: translateZ(0);
  -ms-interpolation-mode: bicubic;
}

.location-badge {
  position: absolute;
  top: 1.2rem;
  right: 1.2rem;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  color: white;
  padding: 0.4rem 0.9rem;
  border-radius: 50px;
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 0.5px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.card-content {
  padding: 1.8rem;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.card-meta-top {
  margin-bottom: 0.8rem;
}

.category-text {
  font-size: 0.8rem;
  color: #6a11cb;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.card-title {
  font-size: 1.4rem;
  font-weight: 700;
  margin: 0 0 1.2rem 0;
  color: #212529;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-info-list {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  margin-bottom: 1.5rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  color: #555;
  font-size: 0.95rem;
}

.info-item .icon {
  color: #adb5bd;
  flex-shrink: 0;
}

.info-item.address span {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-tags {
  margin-top: auto;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  background: #f8f9fa;
  color: #495057;
  padding: 0.4rem 0.8rem;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 500;
  border: 1px solid #e9ecef;
}

/* No Results */
.no-results {
  text-align: center;
  padding: 6rem 2rem;
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
  margin-bottom: 3rem;
}

.empty-state-icon {
  margin-bottom: 1.5rem;
  opacity: 0.5;
}

.no-results h3 {
  font-size: 1.5rem;
  margin-bottom: 0.8rem;
  color: #333;
}

.no-results p {
  color: #888;
  margin-bottom: 2rem;
}

.btn-retry {
  padding: 0.8rem 2rem;
  background-color: #212529;
  color: white;
  border: none;
  border-radius: 50px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-retry:hover {
  background-color: #000;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
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
  padding: 0.6rem 1.2rem;
  background-color: #6a11cb;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.2s;
}

.pagination-btn:hover:not(:disabled) {
  background-color: #5a0db8;
  transform: translateY(-1px);
}

.pagination-btn:disabled {
  background-color: #d1d6db;
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
  border: 1px solid #e1e4e8;
  border-radius: 10px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pagination-page:hover {
  background-color: #f8f9fa;
  border-color: #6a11cb;
}

.pagination-page.active {
  background-color: #6a11cb;
  color: white;
  border-color: #6a11cb;
  font-weight: 700;
}

.page-info {
  text-align: center;
  color: #888;
  font-size: 0.9rem;
  margin-bottom: 2rem;
  padding: 0.5rem;
}

/* Responsive */
@media (max-width: 768px) {
  .festivals-container {
    padding: 2rem 1rem;
  }

  .festivals-header h1 {
    font-size: 2rem;
  }

  .festivals-header p {
    font-size: 1rem;
  }

  .filters {
    flex-direction: column;
    align-items: stretch;
    padding: 1.5rem;
  }

  .reset-button {
    margin-top: 0.5rem;
    width: 100%;
  }

  .festivals-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .card-title {
    font-size: 1.25rem;
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
    padding: 0.5rem 1rem;
    font-size: 0.85rem;
  }
}
</style>