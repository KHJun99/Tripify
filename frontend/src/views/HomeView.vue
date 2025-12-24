<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { getFestivals } from '@/api/festivals'
import KakaoMapSearch from '@/components/KakaoMapSearch.vue'
import tripifyLogo from '@/assets/img/logo1.png'

const router = useRouter()
const searchQuery = ref('')
const festivals = ref([]) 
const festivalsMap = ref({}) 
const showBookmarkModal = ref(false)

// 북마크 카드 클릭 핸들러 - 카카오맵 검색 모달 열기
const handleBookmarkClick = () => {
  showBookmarkModal.value = true
}

// --- 1. 여행지 데이터 및 랜덤 추천 로직 ---
const allDestinations = [
  { 
    id: 101, 
    name: '서울의 찬란한 야경', 
    image: 'https://images.pexels.com/photos/237211/pexels-photo-237211.jpeg?auto=compress&cs=tinysrgb&w=800' 
  },
  { 
    id: 102, 
    name: '부산의 시원한 바다', 
    image: 'https://images.pexels.com/photos/1005417/pexels-photo-1005417.jpeg?auto=compress&cs=tinysrgb&w=800' 
  },
  { 
    id: 103, 
    name: '제주 유채꽃 필 무렵', 
    image: 'https://images.pexels.com/photos/1083822/pexels-photo-1083822.jpeg?auto=compress&cs=tinysrgb&w=800' 
  },
  { 
    id: 104, 
    name: '동해의 푸른 파도', 
    image: 'https://images.pexels.com/photos/994605/pexels-photo-994605.jpeg?auto=compress&cs=tinysrgb&w=800' 
  },
  { 
    id: 105, 
    name: '청량한 숲속 힐링',
    image: 'https://images.pexels.com/photos/1320684/pexels-photo-1320684.jpeg?auto=compress&cs=tinysrgb&w=800' 
  },
]

const randomPicks = ref([])
const activeBgIndex = ref(0)
let slideInterval = null
const isHovering = ref(false)

const shuffleAndPick = () => {
  randomPicks.value = [...allDestinations]
    .sort(() => 0.5 - Math.random())
    .slice(0, 3)
}

const startSlideShow = () => {
  slideInterval = setInterval(() => {
    if (!isHovering.value && randomPicks.value.length > 0) {
      activeBgIndex.value = (activeBgIndex.value + 1) % randomPicks.value.length
    }
  }, 5000)
}

const stopSlideShow = () => {
  if (slideInterval) clearInterval(slideInterval)
}

const onCardHover = (index) => {
  isHovering.value = true
  activeBgIndex.value = index
}

const onCardLeave = () => {
  isHovering.value = false
}

const goToDetail = (id) => {
  router.push({ name: 'festivals' })
}

const currentBgImage = computed(() => {
  return randomPicks.value[activeBgIndex.value]?.image || ''
})

// --- 2. 달력 및 기타 로직 ---
const today = new Date()
const selectedDate = ref(today)
const dateList = ref([])
const scrollContainer = ref(null)
const displayYear = computed(() => selectedDate.value.getFullYear())
const displayMonth = computed(() => selectedDate.value.getMonth() + 1)

const generateMonths = () => {
  const months = []
  const start = new Date(today.getFullYear(), today.getMonth() - 12, 1)
  for (let i = 0; i < 25; i++) {
    const d = new Date(start)
    d.setMonth(start.getMonth() + i)
    months.push(d)
  }
  dateList.value = months
}

const selectDate = (date) => { 
  selectedDate.value = date 
}

const isSelected = (date) => {
  return date.getFullYear() === selectedDate.value.getFullYear() &&
         date.getMonth() === selectedDate.value.getMonth()
}

const isCurrentMonth = (date) => {
  return date.getFullYear() === today.getFullYear() &&
         date.getMonth() === today.getMonth()
}

// 선택된 월의 축제 목록 (Map 방식 사용)
const monthFestivals = computed(() => {
  const year = selectedDate.value.getFullYear()
  const month = selectedDate.value.getMonth() + 1
  const key = `${year}-${month}` 
  return festivalsMap.value[key] || [] 
})


const scrollToCurrentDate = () => {
  if (scrollContainer.value) {
    const currentIndex = dateList.value.findIndex(d =>
      d.getFullYear() === today.getFullYear() &&
      d.getMonth() === today.getMonth()
    )
    if (currentIndex !== -1) {
      // 실제 DOM 요소의 너비 측정
      const dateItems = scrollContainer.value.querySelectorAll('.date-item')
      if (dateItems.length > 0) {
        const firstItem = dateItems[0]
        const itemRect = firstItem.getBoundingClientRect()
        const itemWidth = itemRect.width + 12 // gap 12px 포함
        
        const containerWidth = scrollContainer.value.clientWidth
        // 현재 달을 가운데로 위치시키기
        const scrollPos = (currentIndex * itemWidth) - (containerWidth / 2) + (itemWidth / 2)
        scrollContainer.value.scrollLeft = Math.max(0, scrollPos)
      }
    }
  }
}

const scroll = (direction) => {
  if (!scrollContainer.value || dateList.value.length === 0) return
  
  // 현재 선택된 날짜의 인덱스 찾기
  const currentIndex = dateList.value.findIndex(d =>
    d.getFullYear() === selectedDate.value.getFullYear() &&
    d.getMonth() === selectedDate.value.getMonth()
  )
  
  if (currentIndex === -1) return
  
  // 다음/이전 달 인덱스 계산
  let targetIndex
  if (direction === 'left') {
    targetIndex = Math.max(0, currentIndex - 1)
  } else {
    targetIndex = Math.min(dateList.value.length - 1, currentIndex + 1)
  }
  
  // 날짜 선택 변경
  selectDate(dateList.value[targetIndex])
  
  // 해당 달을 가운데로 스크롤 (즉시 실행, setTimeout 제거)
  scrollToDate(dateList.value[targetIndex])
}

// 특정 날짜로 스크롤 (가운데 정렬)
const scrollToDate = (targetDate) => {
  if (!scrollContainer.value) return
  
  const targetIndex = dateList.value.findIndex(d =>
    d.getFullYear() === targetDate.getFullYear() &&
    d.getMonth() === targetDate.getMonth()
  )
  
  if (targetIndex !== -1) {
    const dateItems = scrollContainer.value.querySelectorAll('.date-item')
    if (dateItems.length > 0) {
      const firstItem = dateItems[0]
      const itemRect = firstItem.getBoundingClientRect()
      const itemWidth = itemRect.width + 12 // gap 12px 포함
      
      const containerWidth = scrollContainer.value.clientWidth
      // 해당 달을 가운데로 위치시키기
      const scrollPos = (targetIndex * itemWidth) - (containerWidth / 2) + (itemWidth / 2)
      
      // requestAnimationFrame을 사용하여 더 부드러운 애니메이션
      requestAnimationFrame(() => {
        scrollContainer.value.scrollTo({
          left: Math.max(0, scrollPos),
          behavior: 'smooth'
        })
      })
    }
  }
}

// 지역명 정규화 함수 (예: '대구' -> '대구광역시')
const normalizeRegion = (input) => {
  const regionMap = {
    '서울': '서울특별시',
    '부산': '부산광역시',
    '대구': '대구광역시',
    '인천': '인천광역시',
    '광주': '광주광역시',
    '대전': '대전광역시',
    '울산': '울산광역시',
    '세종': '세종특별자치시',
    '경기': '경기도',
    '강원': '강원특별자치도',
    '충북': '충청북도',
    '충남': '충청남도',
    '전북': '전북특별자치도',
    '전남': '전라남도',
    '경북': '경상북도',
    '경남': '경상남도',
    '제주': '제주특별자치도',
  }
  
  // 입력값에서 공백 제거 및 정규화
  const normalized = input.trim()
  
  // 매핑에 있는 경우 변환
  for (const [key, value] of Object.entries(regionMap)) {
    if (normalized.includes(key)) {
      return value
    }
  }
  
  // 매핑에 없는 경우 원본 반환
  return normalized
}

const handleSearch = () => {
  if (searchQuery.value) {
    const normalizedRegion = normalizeRegion(searchQuery.value)
    router.push({ name: 'trip-plan', query: { search: normalizedRegion } })
  }
}

const goToFestivals = () => {
  router.push({ name: 'festivals' })
}

const goToFestivalsWithMonth = (year, month) => {
  router.push({ name: 'festivals', query: { month: month } })
}

// 축제 데이터를 Map으로 가공
const processFestivalsData = (data) => {
  const map = {}
  data.forEach(festival => {
    if (!festival.event_start_date) return
    const yearStr = festival.event_start_date.substring(0, 4)
    const monthStr = festival.event_start_date.substring(4, 6)
    const key = `${parseInt(yearStr)}-${parseInt(monthStr)}`
    if (!map[key]) { 
      map[key] = [] 
    }
    if (map[key].length < 6) { 
      map[key].push(festival) 
    }
  })
  festivalsMap.value = map
}

// 축제 데이터 로드
const loadFestivals = async () => {
  try {
    const data = await getFestivals()
    festivals.value = data
    processFestivalsData(data) 
  } catch (error) {
    console.error('축제 데이터 로드 실패:', error)
  }
}

onMounted(async () => {
  shuffleAndPick()
  startSlideShow()
  generateMonths()
  await loadFestivals()
  await nextTick()
  // DOM이 완전히 렌더링된 후 스크롤 (현재 달을 가운데로)
  setTimeout(() => {
    scrollToCurrentDate()
  }, 100)
})

onUnmounted(() => {
  stopSlideShow()
})
</script>

<template>
  <div class="home">
    <!-- 고정 배경 (배경색 제거됨) -->
    <div class="static-bg-wrapper"></div>

    <!-- Hero 섹션 -->
    <section class="hero-container">
      <transition name="fade" mode="out-in">
         <div 
          :key="currentBgImage" 
          class="hero-bg" 
          :style="{ backgroundImage: `url(${currentBgImage})` }"
        ></div>
      </transition>
      <div class="hero-overlay"></div>

      <div class="hero-content-wrapper">
        <div class="hero-text-area animate-slide-up">
          <h1 class="logo-title">
            <img :src="tripifyLogo" alt="Tripify" class="hero-logo" />
          </h1>
          <p class="hero-subtitle">
            한국에서 만나는,<br>
            마법 같은 여행의 시작
          </p>
          
          <div class="search-box">
            <span class="search-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
              </svg>
            </span>
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="어디로 떠나고 싶으세요?" 
              @keyup.enter="handleSearch" 
            />
          </div>
        </div>

        <div class="hero-visual-area animate-slide-up-delay">
          <div 
            v-for="(place, index) in randomPicks" 
            :key="place.id" 
            class="polaroid-card"
            :class="[`pos-${index}`, { 'active-card': index === activeBgIndex }]"
            @mouseover="onCardHover(index)"
            @mouseleave="onCardLeave"
            @click="goToDetail(place.id)"
          >
            <div class="active-indicator" v-if="index === activeBgIndex">Viewing</div>
            <div class="img-box">
              <img :src="place.image" :alt="place.name" />
            </div>
            <div class="img-caption">
              <span>{{ place.name }}</span>
              <span class="click-hint">자세히 보기 &rarr;</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features 섹션 -->
    <section class="features">
       <div class="section-header">
        <h2>Tripify 주요 기능</h2>
        <p class="section-desc">여행의 시작부터 끝까지, 스마트하게 도와드립니다.</p>
      </div>

      <div class="feature-grid">
        <div class="feature-card glass-card clickable" @click="router.push({ name: 'trip-plan' })">
          <div class="icon-circle">
            <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"></polygon>
                <line x1="8" y1="2" x2="8" y2="18"></line>
                <line x1="16" y1="6" x2="16" y2="22"></line>
              </svg>
          </div>
          <div class="card-content">
            <h3>Tripify 맞춤 추천</h3>
            <p>예산과 여행 스타일에 딱 맞는 최적의 코스를 AI가 자동으로 생성해드립니다.</p>
            <span class="link-text">여행 계획 만들기 &rarr;</span>
          </div>
        </div>
        
        <div class="feature-card glass-card clickable" @click="goToFestivals">
          <div class="icon-circle">
            <span class="icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M2 9a3 3 0 0 1 0 6v2a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-2a3 3 0 0 1 0-6V7a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"></path>
                <path d="M13 5v2"></path>
                <path d="M13 17v2"></path>
                <path d="M13 11v2"></path>
              </svg>
            </span>
          </div>
          <div class="card-content">
            <h3>지역 축제 정보</h3>
            <p>여행지에서 열리는 다양한 축제와 행사 정보를 한눈에 확인하세요.</p>
            <span class="link-text">축제 보러가기 &rarr;</span>
          </div>
        </div>
        
        <div class="feature-card glass-card clickable" @click="handleBookmarkClick">
          <div class="icon-circle">
            <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16z"></path>
            </svg>
          </div>
          <div class="card-content">
            <h3>나만의 북마크</h3>
            <p>마음에 드는 장소를 발견하셨나요? 저장해두고 언제든 확인하세요.</p>
            <span class="link-text">장소 북마크하기 &rarr;</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Calendar 섹션 -->
    <section class="calendar-section">
      <div class="calendar-header-wrapper">
        <h2 class="calendar-title">월별 축제 일정</h2>
        <p class="section-desc">떠나고 싶은 달을 선택하여 축제를 확인해보세요.</p>
      </div>
      
      <div class="calendar-wrapper glass-card">
        <div class="calendar-left">
          <span class="year-text">{{ displayYear }}</span>
          <span class="month-text">{{ displayMonth }}월</span>
        </div>
        <div class="divider"></div>
        
        <button class="nav-btn prev" @click="scroll('left')">
          <span class="arrow-icon"></span>
        </button>
        
        <div class="date-scroll-area" ref="scrollContainer">
          <div
            v-for="date in dateList"
            :key="date"
            class="date-item"
            :class="{ active: isSelected(date), current: isCurrentMonth(date) }"
            @click="selectDate(date)"
          >
            <span class="day-num">{{ date.getMonth() + 1 }}</span>
            <span class="day-name">월</span>
          </div>
        </div>
        
        <button class="nav-btn next" @click="scroll('right')">
          <span class="arrow-icon right"></span>
        </button>
      </div>

      <!-- 축제 목록 -->
      <div class="festival-list-wrapper">
        <transition name="fade" mode="out-in">
          <div v-if="monthFestivals.length > 0" class="month-festivals" :key="selectedDate.toString()">
            <div class="list-header">
              <h4>{{ selectedDate.getFullYear() }}년 {{ selectedDate.getMonth() + 1 }}월의 축제</h4>
              <button 
                class="view-all-btn" 
                @click="goToFestivalsWithMonth(selectedDate.getFullYear(), selectedDate.getMonth() + 1)"
              >
                {{ selectedDate.getMonth() + 1 }}월 축제 모두보기
              </button>
            </div>
            <div class="festival-grid">
              <div
                v-for="festival in monthFestivals"
                :key="festival.id"
                class="festival-card-modern glass-card"
                @click="router.push({ name: 'festival-detail', params: { id: festival.id } })"
              >
                <div class="festival-content">
                  <div class="festival-category">Festival</div>
                  <div class="festival-title">{{ festival.title }}</div>
                  <div class="festival-location">{{ festival.region }}</div>
                </div>
                <div class="arrow-indicator">&rarr;</div>
              </div>
            </div>
          </div>
          <div v-else class="no-festivals glass-card" :key="'no-data'">
            <p>해당 월에 예정된 축제 정보가 없습니다.</p>
          </div>
        </transition>
      </div>
    </section>

    <!-- 카카오맵 검색 모달 -->
    <div v-if="showBookmarkModal" class="modal-overlay" @click.self="showBookmarkModal = false">
      <KakaoMapSearch @close="showBookmarkModal = false" />
    </div>
  </div>
</template>

<style scoped>
.home {
  width: 100%;
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
}

/* --- 고정형 배경 스타일 (배경색 제거됨) --- */
.static-bg-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: -2;
  /* background-color 및 background-image 제거됨 */
  background-attachment: fixed;
  background-size: cover;
  pointer-events: none;
}

/* --- Glassmorphism 효과 (그림자 강화) --- */
.glass-card {
  background: rgba(255, 255, 255, 0.75) !important; 
  border: 1px solid rgba(255, 255, 255, 0.6) !important;
  /* 기존보다 조금 더 진하고 명확한 이중 그림자 적용 */
  box-shadow: 
    0 2px 4px rgba(0, 0, 0, 0.05), /* 가까운 그림자 (윤곽) */
    0 8px 16px rgba(0, 0, 0, 0.08) !important; /* 먼 그림자 (깊이감) */
}

/* --- Hero Section --- */
.hero-container { 
  position: relative; 
  width: 100vw; 
  height: 600px; 
  overflow: hidden; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  margin-bottom: 2rem; 
  color: #fff; 
  /* background-color 제거됨 */
}

.hero-bg { 
  position: absolute; 
  top: 0; 
  left: 0; 
  width: 100%; 
  height: 100%; 
  background-size: cover; 
  background-position: center; 
  filter: blur(3px) brightness(0.8); 
  z-index: 0; 
  transform: scale(1.05); 
  transition: transform 6s linear; 
}

.fade-enter-active, .fade-leave-active { 
  transition: opacity 0.8s ease-in-out; 
}

.fade-enter-from, .fade-leave-to { 
  opacity: 0; 
}

.hero-overlay { 
  position: absolute; 
  top: 0; 
  left: 0; 
  width: 100%; 
  height: 100%; 
  background: linear-gradient(to right, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0.3) 100%); 
  z-index: 1; 
}

.hero-content-wrapper { 
  position: relative; 
  z-index: 2; 
  width: 100%; 
  max-width: 1200px; 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  padding: 0 2rem; 
}

.animate-slide-up { 
  animation: slideUp 1s ease-out forwards; 
  opacity: 0; 
}

.animate-slide-up-delay { 
  animation: slideUp 1s ease-out 0.3s forwards; 
  opacity: 0; 
}

@keyframes slideUp { 
  from { opacity: 0; transform: translateY(30px); } 
  to { opacity: 1; transform: translateY(0); } 
}

.hero-text-area { 
  flex: 1; 
  text-align: left; 
}

.logo-title { 
  font-size: 4.5rem; 
  font-weight: 900; 
  margin-bottom: 1rem; 
  text-shadow: 2px 2px 4px rgba(0,0,0,0.5); 
}

.trip { 
  color: #4285f4; 
}

.ify { 
  color: #fff; 
}

.hero-logo {
  width: 450px; 
  height: auto;
  display: block;
  mix-blend-mode: multiply;
  margin-left: -40px; 
  margin-bottom: -70px; 
}

.hero-subtitle { 
  font-size: 2rem; 
  margin-bottom: 2.5rem; 
  font-weight: 700; 
  color: #f3f4f6; 
  line-height: 1.3; 
  text-shadow: 1px 1px 3px rgba(0,0,0,0.5); 
}


.search-box { 
  display: flex; 
  align-items: center; 
  background-color: rgba(255, 255, 255, 0.95); 
  padding: 1.2rem 1.5rem; 
  border-radius: 50px; 
  box-shadow: 0 8px 20px rgba(0,0,0,0.3); 
  max-width: 500px; 
  transition: transform 0.3s ease, box-shadow 0.3s ease; 
}

.search-box:focus-within { 
  transform: translateY(-3px); 
  box-shadow: 0 12px 25px rgba(66, 133, 244, 0.4); 
}

.search-icon { 
  margin-right: 15px; 
  font-size: 1.3rem; 
  color: #2F80ED;
  align-items: center;
  margin-top: 2px;
}

.search-box input { 
  flex: 1; 
  border: none; 
  font-size: 1.1rem; 
  outline: none; 
  color: #333; 
  background: transparent; 
}

.hero-visual-area { 
  flex: 1; 
  position: relative; 
  height: 450px; 
  display: flex; 
  justify-content: center; 
  align-items: center; 
}

.polaroid-card { 
  position: absolute; 
  background: #fff; 
  padding: 12px 12px 35px 12px; 
  box-shadow: 0 15px 35px rgba(0,0,0,0.4); 
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); 
  width: 260px; 
  cursor: pointer; 
  border-radius: 4px; 
}

.polaroid-card:hover, .polaroid-card.active-card { 
  z-index: 20 !important; 
  transform: scale(1.1) rotate(0deg) !important; 
  box-shadow: 0 25px 50px rgba(0,0,0,0.5); 
}

.active-indicator { 
  position: absolute; 
  top: -10px; 
  right: -10px; 
  background: #4285f4; 
  color: white; 
  padding: 4px 10px; 
  border-radius: 20px; 
  font-size: 0.8rem; 
  font-weight: bold; 
  box-shadow: 0 4px 10px rgba(0,0,0,0.2); 
  z-index: 2; 
}

.img-box { 
  width: 100%; 
  height: 220px; 
  overflow: hidden; 
  background: #eee; 
  border-radius: 2px; 
}

.img-box img { 
  width: 100%; 
  height: 100%; 
  object-fit: cover; 
  transition: transform 0.5s ease; 
}

.polaroid-card:hover .img-box img { 
  transform: scale(1.1); 
}

.img-caption { 
  margin-top: 15px; 
  text-align: center; 
  color: #333; 
  font-weight: bold; 
  font-size: 1.2rem; 
  display: flex; 
  flex-direction: column; 
  align-items: center; 
}

.click-hint { 
  font-size: 0.9rem; 
  color: #4285f4; 
  margin-top: 5px; 
  opacity: 0; 
  transition: opacity 0.3s ease; 
}

.polaroid-card:hover .click-hint { 
  opacity: 1; 
}

.pos-0 { 
  transform: rotate(-6deg) translateX(-100px) translateY(-30px); 
  z-index: 5; 
}

.pos-1 { 
  transform: rotate(4deg) translateX(0px) translateY(40px); 
  z-index: 4; 
}

.pos-2 { 
  transform: rotate(9deg) translateX(100px) translateY(-20px); 
  z-index: 3; 
}

/* --- Features Section --- */
.features { 
  padding: 4rem 2rem; 
  max-width: 1200px; 
  margin: 0 auto; 
  width: 100%; 
}

.section-header { 
  text-align: center; 
  margin-bottom: 3rem; 
}

.features h2 { 
  font-size: 2.2rem; 
  color: #1f2937; 
  font-weight: 800; 
  margin-bottom: 0.5rem; 
}

.section-desc { 
  color: #6b7280; 
  font-size: 1.1rem; 
}

.feature-grid { 
  display: grid; 
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
  gap: 2.5rem; 
}

.feature-card { 
  border-radius: 20px; 
  padding: 2.5rem 2rem; 
  transition: all 0.3s ease; 
  display: flex; 
  flex-direction: column; 
  align-items: flex-start; 
  position: relative; 
  overflow: hidden; 
}

.feature-card:hover { 
  transform: translateY(-10px); 
  box-shadow: 0 20px 40px rgba(66, 133, 244, 0.1) !important; 
  border-color: #bfdbfe !important; 
}

.icon-circle { 
  width: 60px; 
  height: 60px; 
  background-color: #eff6ff; 
  border-radius: 50%; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  margin-bottom: 1.5rem; 
  transition: transform 0.3s ease; 
}

.feature-card:hover .icon-circle { 
  transform: scale(1.1) rotate(5deg); 
  background-color: #dbeafe; 
}

.icon { 
  font-size: 1.8rem; 
}

.card-content h3 { 
  font-size: 1.4rem; 
  font-weight: 700; 
  color: #111827; 
  margin-bottom: 0.8rem; 
}

.card-content p { 
  color: #4b5563; 
  line-height: 1.6; 
  font-size: 1rem; 
  margin-bottom: 1rem; 
}

.feature-card.clickable { 
  cursor: pointer; 
}

.link-text { 
  font-size: 0.95rem; 
  font-weight: 600; 
  color: #4285f4; 
  opacity: 0; 
  transform: translateX(-10px); 
  transition: all 0.3s ease; 
  display: inline-block; 
}

.feature-card.clickable:hover .link-text { 
  opacity: 1; 
  transform: translateX(0); 
}

/* --- Calendar Section --- */
.calendar-section {
  max-width: 1000px;
  margin: 0 auto 6rem;
  padding: 0 2rem;
  width: 100%;
}

.calendar-header-wrapper { 
  text-align: center; 
  margin-bottom: 3rem; 
}

.calendar-title { 
  font-size: 2rem; 
  color: #1f2937; 
  font-weight: 800; 
  margin-bottom: 0.5rem; 
}

/* 캘린더 컨테이너 */
.calendar-wrapper {
  display: flex;
  align-items: center;
  padding: 20px 30px;
  border-radius: 24px;
  height: 120px;
  position: relative;
  z-index: 10;
}

.calendar-left { 
  display: flex; 
  flex-direction: column; 
  align-items: flex-start; 
  justify-content: center; 
  min-width: 110px; 
  padding-right: 20px; 
}

.year-text { 
  font-size: 0.95rem; 
  color: #94a3b8; 
  font-weight: 600; 
  letter-spacing: -0.02em; 
  transition: color 0.3s ease; 
}

.month-text { 
  font-size: 2.2rem; 
  font-weight: 900; 
  color: #1f2937; 
  line-height: 1.1; 
  letter-spacing: -0.03em; 
  transition: all 0.3s ease; 
}

.divider { 
  width: 2px; 
  height: 50px; 
  background-color: #f1f5f9; 
  margin: 0 15px; 
  border-radius: 2px; 
}

.nav-btn { 
  background: #f8fafc; 
  border: none; 
  width: 40px; 
  height: 40px; 
  border-radius: 50%; 
  cursor: pointer; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  transition: all 0.2s ease; 
  flex-shrink: 0; 
}

.nav-btn:hover { 
  background: #eff6ff; 
  transform: scale(1.1); 
}

.arrow-icon { 
  width: 8px; 
  height: 8px; 
  border-top: 2px solid #64748b; 
  border-left: 2px solid #64748b; 
  transform: rotate(-45deg); 
  margin-left: 2px; 
}

.arrow-icon.right { 
  transform: rotate(135deg); 
  margin-left: -2px; 
}

.date-scroll-area { 
  flex: 1; 
  display: flex; 
  overflow-x: auto; 
  gap: 12px; 
  padding: 10px 15px; 
  scrollbar-width: none; 
  margin: 0 10px; 
  scroll-behavior: smooth; 
  -webkit-overflow-scrolling: touch; 
}

.date-scroll-area::-webkit-scrollbar { 
  display: none; 
}

.date-item { 
  display: flex; 
  flex-direction: column; 
  align-items: center; 
  justify-content: center; 
  min-width: 60px; 
  height: 80px; 
  cursor: pointer; 
  border-radius: 16px; 
  color: #94a3b8; 
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1); 
  background: transparent; 
}

.date-item:hover { 
  background-color: #f8fafc; 
  color: #64748b; 
}

.day-num { 
  font-size: 1.2rem; 
  font-weight: 700; 
  margin-bottom: 4px; 
}

.day-name { 
  font-size: 0.85rem; 
  font-weight: 500; 
}

.date-item.current { 
  position: relative; 
}

.date-item.current .day-num { 
  color: #e11d48; 
}

.date-item.active { 
  background-color: #4285f4; 
  color: #ffffff !important; 
  box-shadow: 0 8px 16px rgba(66, 133, 244, 0.3); 
  transform: translateY(-2px); 
}

.date-item.active .day-num, 
.date-item.active .day-name { 
  color: #ffffff; 
}

.date-item.active::after { 
  display: none; 
}

/* --- 축제 리스트 스타일 --- */
.festival-list-wrapper { 
  min-height: 500px; 
  margin-top: 3rem; 
  position: relative; 
}

.list-header { 
  display: flex; 
  align-items: center; 
  gap: 10px; 
  margin-bottom: 1.5rem; 
  padding-left: 5px; 
  justify-content: space-between;
}

.month-festivals h4 { 
  font-size: 1.3rem; 
  font-weight: 700; 
  color: #1f2937; 
  margin: 0; 
}

.view-all-btn {
  margin-left: auto;
  padding: 0.5rem 1.2rem;
  background-color: white;
  color: #4285f4;
  border: 1px solid #4285f4;
  border-radius: 50px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  box-shadow: 0 2px 4px rgba(66, 133, 244, 0.1);
}

.view-all-btn:hover {
  background-color: #4285f4;
  color: white;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(66, 133, 244, 0.3);
}

.festival-grid { 
  display: grid; 
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); 
  gap: 1.5rem; 
}

.festival-card-modern {
  border-radius: 16px; 
  padding: 1.5rem; 
  cursor: pointer; 
  transition: all 0.3s ease; 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  position: relative; 
  overflow: hidden;
}

.festival-card-modern::before { 
  content: ''; 
  position: absolute; 
  left: 0; 
  top: 0; 
  bottom: 0; 
  width: 4px; 
  background-color: #4285f4; 
  opacity: 0; 
  transition: opacity 0.3s ease; 
}

.festival-card-modern:hover { 
  transform: translateY(-5px); 
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1) !important; 
  border-color: #bfdbfe !important; 
}

.festival-card-modern:hover::before { 
  opacity: 1; 
}

.festival-content { 
  flex: 1; 
}

.festival-category { 
  font-size: 0.75rem; 
  font-weight: 700; 
  color: #4285f4; 
  text-transform: uppercase; 
  letter-spacing: 0.05em; 
  margin-bottom: 0.5rem; 
}

.festival-title { 
  font-size: 1.1rem; 
  font-weight: 700; 
  color: #1e293b; 
  margin-bottom: 0.3rem; 
  line-height: 1.4; 
}

.festival-location { 
  font-size: 0.9rem; 
  color: #64748b; 
  display: flex; 
  align-items: center; 
}

.festival-location::before { 
  content: ''; 
  display: inline-block; 
  width: 6px; 
  height: 6px; 
  background-color: #cbd5e1; 
  border-radius: 50%; 
  margin-right: 6px; 
}

.arrow-indicator { 
  font-size: 1.2rem; 
  color: #cbd5e1; 
  font-weight: bold; 
  transform: translateX(0); 
  transition: all 0.3s ease; 
  margin-left: 1rem; 
}

.festival-card-modern:hover .arrow-indicator { 
  color: #4285f4; 
  transform: translateX(5px); 
}

.no-festivals {
  width: 100%;
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  border-radius: 16px;
  color: #64748b;
}

/* 반응형 */
@media (max-width: 768px) {
  .hero-container { 
    height: auto; 
    padding: 4rem 0; 
  }
  
  .hero-content-wrapper { 
    flex-direction: column; 
    text-align: center; 
  }
  
  .hero-text-area { 
    text-align: center; 
    margin-bottom: 3rem; 
    padding: 0 1rem; 
  }
  
  .logo-title { 
    font-size: 3rem; 
  }
  
  .hero-subtitle { 
    font-size: 1.5rem; 
  }
  
  .hero-visual-area { 
    height: 350px; 
    width: 100%; 
  }
  
  .polaroid-card { 
    width: 200px; 
    padding: 8px 8px 25px 8px; 
  }
  
  .img-box { 
    height: 160px; 
  }
  
  .pos-0 { 
    transform: rotate(-6deg) translateX(-60px) translateY(-20px); 
  }
  
  .pos-2 { 
    transform: rotate(9deg) translateX(60px) translateY(-10px); 
  }
  
  .calendar-wrapper { 
    flex-direction: column; 
    height: auto; 
    padding: 15px; 
  }
  
  .calendar-left { 
    width: 100%; 
    align-items: center; 
    margin-bottom: 15px; 
    padding-right: 0; 
  }
  
  .divider { 
    width: 100%; 
    height: 1px; 
    margin: 10px 0; 
  }
  
  .festival-grid {
    grid-template-columns: 1fr;
  }
}

/* 모달 오버레이 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>