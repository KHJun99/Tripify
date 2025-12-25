<script setup>
  import { onMounted, ref, computed, watch } from 'vue'
  import { useTripStore } from '@/stores/trip'
  import { useAuthStore } from '@/stores/auth'
  import { useRouter } from 'vue-router'
  import { tripAPI } from '@/api/trip'
  import { placeAPI } from '@/api/place'
  import KakaoMapSearch from '@/components/KakaoMapSearch.vue'
  
  const tripStore = useTripStore()
  const authStore = useAuthStore()
  const router = useRouter()
  
  // --- 색상 팔레트 (확장) ---
  const colorPalette = [
    { bg: '#e3f2fd', text: '#1565c0' }, // Blue
    { bg: '#e8f5e9', text: '#2e7d32' }, // Green
    { bg: '#f3e5f5', text: '#7b1fa2' }, // Purple
    { bg: '#fff3e0', text: '#ef6c00' }, // Orange
    { bg: '#ffebee', text: '#c62828' }, // Red
    { bg: '#e0f7fa', text: '#006064' }, // Cyan
    { bg: '#fff8e1', text: '#ff8f00' }, // Amber
    { bg: '#fce4ec', text: '#c2185b' }, // Pink
    { bg: '#f9fbe7', text: '#827717' }, // Lime
    { bg: '#e8eaf6', text: '#283593' }, // Indigo
    { bg: '#efebe9', text: '#4e342e' }, // Brown
    { bg: '#eceff1', text: '#37474f' }, // Blue Grey
    { bg: '#f3e5f5', text: '#4a148c' }, // Deep Purple
    { bg: '#e0f2f1', text: '#004d40' }, // Teal
    { bg: '#fafafa', text: '#212121' }, // Dark Grey
    { bg: '#fbe9e7', text: '#bf360c' }, // Deep Orange
  ]
  
  // 겹치는 일정 그룹을 찾아서 각 그룹에 다른 색상 할당
  const planColorMap = computed(() => {
    if (!sortedPlans.value || sortedPlans.value.length === 0) {
      return new Map()
    }
    
    const colorMap = new Map() // plan.id -> color index
    // 시작일 순으로 정렬하여 순차적으로 색상 할당
    const sorted = [...sortedPlans.value]
      .filter(plan => plan && plan.id)
      .sort((a, b) => {
        const startA = new Date(a.start_date).getTime()
        const startB = new Date(b.start_date).getTime()
        if (startA !== startB) return startA - startB
        const endA = new Date(a.end_date).getTime()
        const endB = new Date(b.end_date).getTime()
        return endB - endA
      })
    
    // 각 일정에 대해 색상 할당
    sorted.forEach(plan => {
      // 현재 일정과 겹치는 일정들 찾기 (이미 색상이 할당된 것들만)
      const overlappingPlans = sorted.filter(p => 
        p.id !== plan.id && 
        colorMap.has(p.id) && 
        doPlansOverlap(p, plan)
      )
      
      // 겹치는 일정들이 사용 중인 색상들
      const usedColors = new Set()
      overlappingPlans.forEach(p => {
        usedColors.add(colorMap.get(p.id))
      })
      
      // 사용 가능한 가장 낮은 색상 인덱스 찾기
      let assignedColor = 0
      while (usedColors.has(assignedColor)) {
        assignedColor++
      }
      colorMap.set(plan.id, assignedColor)
    })
    
    return colorMap
  })
  
  const getPlanStyle = (id) => {
    const colorMap = planColorMap.value
    let colorIndex = 0
    
    if (colorMap && colorMap.has(id)) {
      colorIndex = colorMap.get(id)
    } else {
      // fallback: id 기반 색상
      const numId = typeof id === 'number' ? id : String(id).split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)
      colorIndex = numId % colorPalette.length
    }
    
    const color = colorPalette[colorIndex % colorPalette.length]
    return { '--plan-bg': color.bg, '--plan-text': color.text }
  }
  
  // --- 달력 상태 ---
  const currentDate = ref(new Date())
  const weekDays = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
  
  const currentYear = computed(() => currentDate.value.getFullYear())
  const currentMonth = computed(() => currentDate.value.getMonth())
  const daysInMonth = computed(() => new Date(currentYear.value, currentMonth.value + 1, 0).getDate())
  const startDay = computed(() => new Date(currentYear.value, currentMonth.value, 1).getDay())
  
  const changeMonth = (diff) => {
    currentDate.value = new Date(currentYear.value, currentMonth.value + diff, 1)
  }
  
  // 오늘 날짜 확인 함수
  const isToday = (day) => {
    const today = new Date()
    return today.getDate() === day &&
           today.getMonth() === currentMonth.value &&
           today.getFullYear() === currentYear.value
  }
  
  // --- 일정 정렬 ---
  const sortedPlans = computed(() => {
    return [...tripStore.plans].sort((a, b) => {
      const startA = new Date(a.start_date)
      const startB = new Date(b.start_date)
      if (startA - startB !== 0) return startA - startB
      const endA = new Date(a.end_date)
      const endB = new Date(b.end_date)
      return endB - endA
    })
  })
  
  // 특정 날짜에 계획이 포함되는지 여부
  const isPlanInDate = (plan, day) => {
    const targetDate = new Date(currentYear.value, currentMonth.value, day)
    targetDate.setHours(0, 0, 0, 0)
  
    const start = new Date(plan.start_date)
    const end = new Date(plan.end_date)
    start.setHours(0, 0, 0, 0)
    end.setHours(0, 0, 0, 0)
  
    return targetDate >= start && targetDate <= end
  }
  
  // 클래스 판별 로직
  const getPlanClass = (day, plan) => {
    const targetDate = new Date(currentYear.value, currentMonth.value, day)
    const targetTime = targetDate.setHours(0,0,0,0)
    const dayOfWeek = targetDate.getDay()
  
    const start = new Date(plan.start_date).setHours(0,0,0,0)
    const end = new Date(plan.end_date).setHours(0,0,0,0)
  
    const classes = []
    const isVisualStart = (targetTime === start) || (dayOfWeek === 0)
    const isVisualEnd = (targetTime === end) || (dayOfWeek === 6)
  
    if (isVisualStart) classes.push('is-start')
    if (isVisualEnd) classes.push('is-end')
    if (!isVisualStart && !isVisualEnd) classes.push('is-middle')
  
    return classes.join(' ')
  }
  
  // 텍스트 너비 계산
  const getSegmentWidth = (day, plan) => {
    const targetDate = new Date(currentYear.value, currentMonth.value, day)
    const dayOfWeek = targetDate.getDay()
  
    const endDate = new Date(plan.end_date)
    endDate.setHours(0,0,0,0)
  
    const daysLeftInWeek = 7 - dayOfWeek
    const msPerDay = 1000 * 60 * 60 * 24
    const daysLeftInPlan = Math.floor((endDate - targetDate) / msPerDay) + 1
  
    const span = Math.min(daysLeftInWeek, daysLeftInPlan)
    return `calc(100% * ${span} + ${span}px - 12px)`
  }
  
  // 일정이 겹치는지 확인
  const doPlansOverlap = (plan1, plan2) => {
    try {
      const start1 = new Date(plan1.start_date).setHours(0, 0, 0, 0)
      const end1 = new Date(plan1.end_date).setHours(0, 0, 0, 0)
      const start2 = new Date(plan2.start_date).setHours(0, 0, 0, 0)
      const end2 = new Date(plan2.end_date).setHours(0, 0, 0, 0)
      
      return !(end1 < start2 || end2 < start1)
    } catch (e) {
      console.error('doPlansOverlap error:', e)
      return false
    }
  }
  
  // 모든 일정의 행 번호를 미리 계산 (computed로 캐싱)
  // 같은 일정은 모든 날짜에서 같은 행에 배치되고, 겹치는 일정은 다른 행에 배치됨
  const planRowMap = computed(() => {
    if (!sortedPlans.value || sortedPlans.value.length === 0) {
      return new Map()
    }
    
    const rowMap = new Map() // plan.id -> row number
    
    // 시작일 순으로 정렬
    const sorted = [...sortedPlans.value]
      .filter(plan => plan && plan.id)
      .sort((a, b) => {
        const startA = new Date(a.start_date).getTime()
        const startB = new Date(b.start_date).getTime()
        if (startA !== startB) return startA - startB
        // 시작일이 같으면 종료일이 늦은 것부터 (긴 일정 우선)
        const endA = new Date(a.end_date).getTime()
        const endB = new Date(b.end_date).getTime()
        return endB - endA
      })
    
    // 각 일정에 대해 행 번호 할당
    sorted.forEach(plan => {
      // 현재 일정과 겹치는 일정들 찾기 (이미 행 번호가 할당된 것들만)
      // 일정 전체 기간에 대해 겹치는지 확인
      const overlappingPlans = sorted.filter(p => 
        p.id !== plan.id && 
        rowMap.has(p.id) && 
        doPlansOverlap(p, plan)
      )
      
      // 겹치는 일정들이 사용 중인 행 번호들
      const usedRows = new Set()
      overlappingPlans.forEach(p => {
        usedRows.add(rowMap.get(p.id))
      })
      
      // 사용 가능한 가장 낮은 행 번호 찾기
      let assignedRow = 0
      while (usedRows.has(assignedRow)) {
        assignedRow++
      }
      
      // 같은 일정은 항상 같은 행 번호를 가짐
      rowMap.set(plan.id, assignedRow)
    })
    
    return rowMap
  })
  
  // 특정 날짜에 포함되는 일정의 행 번호 반환
  // 같은 일정은 모든 날짜에 걸쳐 같은 행에 배치
  // 같은 plan.id는 항상 같은 행 번호를 반환하여 모든 날짜에서 일관된 위치에 표시됨
  const getPlanRow = (day, plan) => {
    try {
      if (!plan || !plan.id) {
        return 0
      }
      
      // 미리 계산된 행 번호 가져오기
      const rowMap = planRowMap.value
      if (!rowMap || !(rowMap instanceof Map)) {
        return 0
      }
      
      const row = rowMap.get(plan.id)
      if (row === undefined || row === null) {
        // 계산되지 않은 경우 기본값 0 반환
        return 0
      }
      
      // 같은 plan.id는 항상 같은 행 번호 반환
      // 이렇게 하면 같은 일정이 모든 날짜에서 같은 행에 표시됨
      return row
    } catch (e) {
      console.error('getPlanRow error:', e, plan)
      return 0
    }
  }
  
  // --- 위시리스트 기능 ---
  const newWish = ref('')
  const wishlist = ref([])
  const isLoadingWishlist = ref(false)
  
  // 위시리스트 조회
  const fetchWishlists = async () => {
    if (!authStore.isAuthenticated) {
      wishlist.value = []
      return
    }
    
    try {
      isLoadingWishlist.value = true
      const response = await tripAPI.getWishlists()
      wishlist.value = response.data
    } catch (error) {
      console.error('위시리스트 조회 실패:', error)
      wishlist.value = []
    } finally {
      isLoadingWishlist.value = false
    }
  }
  
  // 위시리스트 추가
  const addWish = async () => {
    if (!newWish.value.trim()) return
    
    if (!authStore.isAuthenticated) {
      alert('로그인이 필요합니다.')
      return
    }
    
    try {
      const response = await tripAPI.createWishlist({
        text: newWish.value.trim(),
        checked: false
      })
      wishlist.value.push(response.data)
      newWish.value = ''
    } catch (error) {
      console.error('위시리스트 추가 실패:', error)
      alert('위시리스트 추가에 실패했습니다.')
    }
  }
  
  // 위시리스트 체크 상태 변경
  const toggleWish = async (item) => {
    if (!authStore.isAuthenticated) return
    
    try {
      await tripAPI.updateWishlist(item.id, {
        checked: !item.checked
      })
      item.checked = !item.checked
    } catch (error) {
      console.error('위시리스트 업데이트 실패:', error)
    }
  }
  
  // 위시리스트 삭제
  const removeWish = async (id) => {
    if (!authStore.isAuthenticated) return
    
    try {
      await tripAPI.deleteWishlist(id)
      wishlist.value = wishlist.value.filter(item => item.id !== id)
    } catch (error) {
      console.error('위시리스트 삭제 실패:', error)
      alert('위시리스트 삭제에 실패했습니다.')
    }
  }
  
  // --- 북마크 기능 ---
  const bookmarks = ref([])
  const isLoadingBookmarks = ref(false)
  const showBookmarkModal = ref(false)
  const selectedBookmark = ref(null)
  const showAllBookmarksModal = ref(false)
  
  // 북마크 조회
  const fetchBookmarks = async () => {
    if (!authStore.isAuthenticated) {
      bookmarks.value = []
      return
    }
    
    try {
      isLoadingBookmarks.value = true
      const response = await placeAPI.getBookmarks()
      bookmarks.value = response.data
    } catch (error) {
      console.error('북마크 조회 실패:', error)
      bookmarks.value = []
    } finally {
      isLoadingBookmarks.value = false
    }
  }
  
  // 북마크 클릭 시 모달 열기
  const openBookmarkModal = (bookmark) => {
    selectedBookmark.value = bookmark
    showBookmarkModal.value = true
  }
  
  // 모든 북마크 보기 모달 열기
  const openAllBookmarksModal = () => {
    showAllBookmarksModal.value = true
  }
  
  // 북마크 삭제
  const removeBookmark = async (id, event) => {
    event.stopPropagation() // 클릭 이벤트 전파 방지
    if (!authStore.isAuthenticated) return
    
    try {
      await placeAPI.deleteBookmark(id)
      bookmarks.value = bookmarks.value.filter(item => item.id !== id)
    } catch (error) {
      console.error('북마크 삭제 실패:', error)
      alert('북마크 삭제에 실패했습니다.')
    }
  }
  
  
  onMounted(async () => {
    await tripStore.fetchPlans()
    await fetchWishlists()
    await fetchBookmarks()
  })
  
  const goToTrip = (id) => {
    router.push({ name: 'itinerary', params: { id } })
  }
  
  const goToCreate = () => {
    router.push('/trip/new')
  }
  </script>
  
  <template>
    <div class="my-trips-view">
      <!-- 고정 배경 -->
      <div class="static-bg-wrapper"></div>
  
      <div v-if="tripStore.loading" class="loading">로딩 중...</div>
  
      <div v-else class="content-wrapper">
        <!-- 달력 섹션 -->
        <div class="calendar-section glass-card">
          <div class="calendar-header">
            <div class="month-nav">
              <button class="nav-btn" @click="changeMonth(-1)">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
              </button>
              <div class="current-date-display">
                <span class="year-label">{{ currentYear }}</span>
                <span class="month-label">{{ currentMonth + 1 }}월</span>
              </div>
              <button class="nav-btn" @click="changeMonth(1)">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
              </button>
            </div>
            <button class="btn-create" @click="goToCreate">
              <span class="plus-icon">+</span> 새로운 여행
            </button>
          </div>
  
          <div class="calendar-board">
            <div class="week-header">
              <div v-for="day in weekDays" :key="day" class="weekday" :class="{ 'sunday': day === 'SUN', 'saturday': day === 'SAT' }">
                {{ day }}
              </div>
            </div>
            
            <div class="days-grid">
              <div v-for="n in startDay" :key="'blank-' + n" class="day blank"></div>
  
              <div v-for="day in daysInMonth" :key="day" class="day" :class="{ 'is-today': isToday(day) }">
                <div class="day-top">
                  <span class="day-number" :class="{ 'today-badge': isToday(day) }">{{ day }}</span>
                </div>
  
                <div class="plan-bars">
                  <div
                    v-for="plan in sortedPlans"
                    :key="`${day}-${plan.id}`"
                    class="plan-bar"
                    :class="[
                      getPlanClass(day, plan),
                      { 'is-inactive': !isPlanInDate(plan, day) }
                    ]"
                    :style="{
                      ...getPlanStyle(plan.id),
                      order: getPlanRow(day, plan)
                    }"
                    @click.stop="isPlanInDate(plan, day) && goToTrip(plan.id)"
                  >
                    <span
                      v-if="isPlanInDate(plan, day) && getPlanClass(day, plan).includes('is-start')"
                      class="plan-title"
                      :style="{ width: getSegmentWidth(day, plan) }"
                    >
                      {{ plan.title }}
                    </span>
                    <span v-else class="plan-title-hidden">&nbsp;</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <!-- 하단 섹션 -->
        <div class="bottom-section">
          
          <!-- 북마크 카드 -->
          <div class="card bookmark-card glass-card">
            <div class="card-header">
              <div class="header-content">
                <div>
                  <h3>
                    <svg 
                      xmlns="http://www.w3.org/2000/svg" 
                      width="28" 
                      height="28" 
                      viewBox="0 0 24 24" 
                      fill="none" 
                      stroke="#000000" 
                      stroke-width="2" 
                      stroke-linecap="round" 
                      stroke-linejoin="round"
                      style="vertical-align: sub; margin-right: 8px;"
                    >
                      <path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16z"></path>
                    </svg>
                    저장된 북마크
                  </h3>
                  <span class="subtitle">저장한 장소를 확인하세요</span>
                </div>
                <button 
                  v-if="bookmarks.length > 0"
                  class="view-all-bookmarks-btn" 
                  @click="openAllBookmarksModal"
                >
                  모든 북마크 보기
                </button>
              </div>
            </div>
            
            <div v-if="isLoadingBookmarks" class="loading-msg">로딩 중...</div>
            <ul v-else class="bookmark-list">
              <li 
                v-for="bookmark in bookmarks" 
                :key="bookmark.id" 
                class="bookmark-item"
                @click="openBookmarkModal(bookmark)"
              >
                <div class="bookmark-info">
                  <h4 class="bookmark-title">{{ bookmark.place?.title || '장소명 없음' }}</h4>
                  <p class="bookmark-address">{{ bookmark.place?.address || '주소 없음' }}</p>
                  <span v-if="bookmark.place?.category" class="bookmark-category">{{ bookmark.place.category }}</span>
                </div>
                <button @click="removeBookmark(bookmark.id, $event)" class="btn-del" title="북마크 삭제">×</button>
              </li>
              <li v-if="bookmarks.length === 0" class="empty-msg">저장된 북마크가 없습니다.</li>
            </ul>
          </div>
  
          <!-- 위시리스트 카드 -->
          <div class="card wishlist-card glass-card">
            <div class="card-header">
              <h3>여행 위시리스트</h3>
              <span class="subtitle">언젠가 떠나고 싶은 곳을 적어보세요</span>
            </div>
            
            <div class="wish-input-area">
              <input 
                v-model="newWish" 
                @keyup.enter="addWish" 
                placeholder="가고 싶은 곳 입력 (Enter)" 
                type="text"
              />
              <button @click="addWish" class="btn-add">+</button>
            </div>
  
            <ul class="wish-list">
              <li v-for="item in wishlist" :key="item.id" class="wish-item">
                <label :class="{ checked: item.checked }">
                  <input type="checkbox" :checked="item.checked" @change="toggleWish(item)" />
                  <span class="wish-text">{{ item.text }}</span>
                </label>
                <button @click="removeWish(item.id)" class="btn-del">×</button>
              </li>
              <li v-if="wishlist.length === 0" class="empty-msg">위시리스트가 비어있습니다.</li>
            </ul>
          </div>
        </div>
      </div>
  
      <!-- 북마크 모달 -->
      <div 
        v-if="showBookmarkModal" 
        class="modal-overlay" 
        :class="{ 'bookmark-overlay': selectedBookmark }"
        @click.self="!selectedBookmark && (showBookmarkModal = false)"
      >
        <KakaoMapSearch :bookmark="selectedBookmark" @close="showBookmarkModal = false" />
      </div>
  
      <!-- 모든 북마크 보기 모달 -->
      <div 
        v-if="showAllBookmarksModal" 
        class="modal-overlay bookmark-overlay"
        @click.self="showAllBookmarksModal = false"
      >
        <KakaoMapSearch :allBookmarks="bookmarks" @close="showAllBookmarksModal = false" />
      </div>
    </div>
  </template>
  
  <style scoped>
  /* --- 고정형 배경 스타일 --- */
  .my-trips-view {
    position: relative;
    min-height: 100vh;
    width: 100%;
    overflow-x: hidden;
    background-color: #f9f9f9; 
  }
  
  .static-bg-wrapper {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: -2;
    background-color: #f9f9f9;
    pointer-events: none;
  }
  
  /* --- 카드 스타일 --- */
  .glass-card {
    background: #ffffff !important;
    border: 1px solid rgba(0, 0, 0, 0.08) !important;
    box-shadow: 0 12px 28px rgba(0, 0, 0, 0.12), 0 2px 4px rgba(0, 0, 0, 0.08) !important;
  }
  
  /* --- 기본 레이아웃 --- */
  .content-wrapper {
    display: flex;
    flex-direction: column;
    gap: 24px;
    max-width: 1400px; 
    margin: 0 auto;
    padding: 3rem 2rem;
    position: relative;
    z-index: 1;
  }
  
  .loading {
    text-align: center;
    padding: 2rem;
    color: #555;
  }
  
  /* --- 달력 섹션 --- */
  .calendar-section {
    padding: 40px; 
    border-radius: 24px;
    width: 100%;
    box-sizing: border-box;
  }
  
  .calendar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
  }
  
  .month-nav {
    display: flex;
    align-items: center;
    gap: 24px;
  }
  
  .current-date-display {
    display: flex;
    flex-direction: column;
    align-items: center;
    line-height: 1.1;
  }
  
  .year-label {
    font-size: 1rem;
    color: #888;
    font-weight: 500;
  }
  
  .month-label {
    font-size: 2.2rem;
    font-weight: 800;
    color: #111;
  }
  
  .nav-btn {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: 1px solid #eee;
    background: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    color: #333;
    transition: all 0.2s;
  }
  
  .nav-btn:hover {
    background: #f5f5f5;
    transform: scale(1.05);
  }
  
  .btn-create {
    padding: 12px 24px;
    background-color: #111;
    color: white;
    border: none;
    border-radius: 30px; 
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    font-size: 1rem;
    display: flex;
    align-items: center;
    gap: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  }
  
  .plus-icon {
    font-size: 1.2rem;
    font-weight: 400;
  }
  
  .btn-create:hover {
    background-color: #333;
    transform: translateY(-2px);
  }
  
  .calendar-board {
    width: 100%;
  }
  
  .week-header {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    margin-bottom: 10px;
  }
  
  .weekday {
    text-align: left;
    padding-left: 12px;
    font-weight: 700;
    font-size: 0.85rem;
    color: #999;
    text-transform: uppercase;
    letter-spacing: 1px;
  }
  
  .weekday.sunday { color: #FF4757; }
  .weekday.saturday { color: #2F80ED; }
  
  .days-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    border-top: 1px solid #eee; 
    border-left: 1px solid #eee; 
  }
  
  .day {
    min-height: 160px;
    padding: 0;
    border-right: 1px solid #eee; 
    border-bottom: 1px solid #eee;
    position: relative;
    background-color: #fff;
    transition: background-color 0.2s;
  }
  
  .day:hover {
    background-color: #fafafa;
  }
  
  .day-top {
    padding: 12px 12px 6px 12px;
    display: flex;
    justify-content: flex-start;
  }
  
  .day-number {
    font-size: 1.1rem;
    font-weight: 500;
    color: #333;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
  }
  
  .today-badge {
    background-color: #2F80ED;
    color: white;
    font-weight: 700;
  }
  
  .blank {
    background: #fcfcfc;
  }
  
  .plan-bars {
    display: flex;
    flex-direction: column;
    gap: 0;
    width: 100%;
    padding-bottom: 6px;
  }
  
  .plan-bar {
    background-color: var(--plan-bg);
    color: var(--plan-text);
    font-size: 0.85rem;
    height: 28px;
    line-height: 28px;
    cursor: pointer;
    white-space: nowrap;
    position: relative;
    opacity: 1;
    border-radius: 0;
    margin: 0;
    flex-shrink: 0;
    /* order 속성이 항상 적용되도록 보장 */
    order: var(--plan-order, 0);
  }
  
  .plan-bar.is-inactive {
    height: 0 !important;
    min-height: 0 !important;
    max-height: 0 !important;
    line-height: 0 !important;
    overflow: hidden;
    margin: 0 !important;
    padding: 0 !important;
    border: none !important;
    pointer-events: none;
    opacity: 0;
    visibility: hidden;
    /* order는 유지하여 flex 레이아웃에서 같은 일정이 항상 같은 위치에 배치되도록 함 */
    /* height: 0이지만 flex order는 여전히 작동함 */
  }
  
  .plan-bar:hover {
    filter: brightness(0.95);
    z-index: 5;
  }
  
  .plan-bar.is-start {
    border-top-left-radius: 6px;
    border-bottom-left-radius: 6px;
    margin-left: 6px;
  }
  
  .plan-bar.is-end {
    border-top-right-radius: 6px;
    border-bottom-right-radius: 6px;
    margin-right: 6px;
  }
  
  .plan-title {
    display: block;
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    box-sizing: border-box;
    padding-left: 8px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-weight: 700;
    pointer-events: none;
    z-index: 10;
  }
  
  .plan-title-hidden {
    visibility: hidden;
  }
  
  /* --- 하단 섹션 --- */
  .bottom-section {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
  }
  
  .card {
    padding: 32px; 
    border-radius: 20px;
    display: flex;
    flex-direction: column;
  }
  
  .card-header .header-content {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .card-header {
    margin-bottom: 24px;
  }
  
  .card h3 {
    margin: 0 0 8px 0;
    font-size: 1.3rem;
    color: #111;
    font-weight: 800;
  }
  
  .subtitle {
    font-size: 0.9rem;
    color: #666;
  }
  
  /* --- 북마크 스타일 --- */
  .bookmark-list {
    list-style: none;
    padding: 0;
    margin: 0;
    max-height: 400px;
    overflow-y: auto;
  }
  
  .bookmark-item {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 12px;
    margin-bottom: 10px;
    background: rgba(255, 255, 255, 0.5);
    border-radius: 8px;
    border: 1px solid rgba(0, 0, 0, 0.05);
    transition: all 0.2s;
    cursor: pointer;
  }
  
  .bookmark-item:hover {
    background: rgba(255, 255, 255, 0.8);
    border-color: rgba(47, 128, 237, 0.3);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  }
  
  .bookmark-info {
    flex: 1;
    min-width: 0;
  }
  
  .bookmark-title {
    margin: 0 0 5px 0;
    font-size: 1rem;
    font-weight: 600;
    color: #333;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  
  .bookmark-address {
    margin: 0 0 5px 0;
    font-size: 0.85rem;
    color: #666;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  
  .bookmark-category {
    display: inline-block;
    padding: 2px 8px;
    font-size: 0.75rem;
    color: #2F80ED;
    background: rgba(47, 128, 237, 0.1);
    border-radius: 12px;
    font-weight: 500;
  }
  
  .loading-msg {
    text-align: center;
    padding: 2rem;
    color: #666;
    font-size: 0.9rem;
  }
  
  /* --- 위시리스트 스타일 --- */
  .wish-input-area {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
  }
  
  .wish-input-area input {
    flex: 1;
    padding: 14px;
    border: 1px solid #eee;
    background: #f8f9fa;
    border-radius: 12px;
    outline: none;
    transition: all 0.2s;
    font-size: 1rem;
  }
  
  .wish-input-area input:focus {
    border-color: #2F80ED;
    background: #fff;
    box-shadow: 0 0 0 3px rgba(47, 128, 237, 0.1);
  }
  
  .btn-add {
  padding: 12px 24px;
  background-color: #111;
  color: white;
  border: none;
  border-radius: 30px; 
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
  
.btn-add:hover {
  background-color: #333;
  transform: translateY(-2px);
}
  
  .wish-list {
    list-style: none;
    padding: 0;
    margin: 0;
    flex: 1;
    overflow-y: auto;
    max-height: 250px;
  }
  
  .wish-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 0;
    border-bottom: 1px solid #f1f1f1;
  }
  
  .wish-item label {
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
    flex: 1;
  }
  
  .wish-item input[type="checkbox"] {
    width: 18px;
    height: 18px;
    cursor: pointer;
    accent-color: #2F80ED;
  }
  
  .wish-text {
    transition: color 0.2s;
    font-size: 1rem;
    color: #333;
  }
  
  .checked .wish-text {
    text-decoration: line-through;
    color: #aaa;
  }
  
  .btn-del {
    border: none;
    background: none;
    color: #FF4757;
    cursor: pointer;
    font-size: 1.4rem;
    padding: 0 8px;
    opacity: 0.5;
    transition: opacity 0.2s;
  }
  
  .btn-del:hover {
    opacity: 1;
  }
  
  .view-all-bookmarks-btn {
    padding: 0.5rem 1.2rem;
    background-color: white;
    color: #2F80ED;
    border: 1px solid #2F80ED;
    border-radius: 50px;
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    white-space: nowrap;
    box-shadow: 0 2px 4px rgba(47, 128, 237, 0.1);
    flex-shrink: 0;
  }
  
  .view-all-bookmarks-btn:hover {
    background-color: #2F80ED;
    color: white;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(47, 128, 237, 0.3);
  }
  
  .empty-msg {
    text-align: center;
    color: #888;
    padding: 30px;
    font-size: 0.95rem;
  }
  
  /* --- 반응형 --- */
  @media (max-width: 900px) {
    .bottom-section {
      grid-template-columns: 1fr;
    }
  
    .day {
      min-height: 100px;
    }
    
    .content-wrapper {
      padding: 1.5rem;
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
    padding: 20px;
    transition: opacity 0.3s ease;
  }
  
  /* 북마크 모드일 때 오버레이 스타일 조정 */
  .modal-overlay.bookmark-overlay {
    justify-content: flex-start;
    align-items: stretch;
    padding: 0;
    background: transparent;
    pointer-events: none;
  }
  
  /* 북마크 모드일 때 사이드패널만 클릭 가능 */
  .modal-overlay.bookmark-overlay > * {
    pointer-events: auto;
  }
  </style>