<template>
  <div class="page-container">
    <div v-if="festival" class="content-wrap">
      
      <!-- 히어로 섹션 -->
      <section class="hero-section">
        <div class="image-container">
          <div class="bg-image-blur" :style="`background-image: url(${imageUrl})`"></div>
          <img class="main-image" :src="imageUrl" :alt="festival.title" />
        </div>
      </section>

      <!-- 메인 컨텐츠 -->
      <main class="main-container">
        
        <!-- 축제 헤더 -->
        <header class="festival-header">
          <div class="tags">
            <span class="tag region">{{ festival.region }}</span>
            <span class="tag category">{{ festival.category || '축제' }}</span>
          </div>
          <h1 class="title">{{ festival.title }}</h1>
          <p class="date-range">{{ formatPeriod() }}</p>
        </header>

        <div class="divider"></div>

        <!-- 상세 정보 그리드 -->
        <div class="detail-grid">
          
          <!-- 좌측 패널 -->
          <div class="left-panel">
            <!-- 위치 정보 -->
            <div class="info-group">
              <h3 class="group-label">위치</h3>
              <p class="group-value">{{ festival.address }}</p>
              <button @click="copyAddress" class="btn-text-action">
                주소 복사
              </button>
            </div>

            <!-- 연락처 -->
            <div class="info-group" v-if="festival.phone">
              <h3 class="group-label">문의</h3>
              <p class="group-value">{{ festival.phone }}</p>
            </div>

            <!-- 액션 버튼 -->
            <div class="action-area">
              <button @click="goBack" class="btn-back">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="19" y1="12" x2="5" y2="12"></line>
                  <polyline points="12 19 5 12 12 5"></polyline>
                </svg>
                목록으로
              </button>
            </div>
          </div>

          <!-- 우측 패널 (지도) -->
          <div class="right-panel" v-if="festival.latitude && festival.longitude">
            <div class="map-card">
              <div class="map-header">
                <span class="map-label">지도 보기</span>
                <button @click="openKakaoNavi" class="btn-kakao-official">
                  <svg class="kakao-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#000000">
                    <path d="M12 3c-5.52 0-10 3.68-10 8.21 0 2.89 1.92 5.45 4.89 6.94-.24.88-.87 3.18-.99 3.64-.05.19-.03.37.08.49.1.12.28.18.45.18.1 0 .2-.03.29-.09l4.77-3.23c.17.01.33.03.51.03 5.52 0 10-3.68 10-8.21C22 6.68 17.52 3 12 3z"/>
                  </svg>
                  카카오맵에서 경로 보러가기
                </button>
              </div>
              <div id="kakao-map" class="kakao-map"></div>
            </div>
          </div>

        </div>
      </main>
    </div>

    <!-- 로딩 상태 -->
    <div v-else class="loading-container">
      <div class="loader"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getFestivalDetail } from '@/api/festivals'

const route = useRoute()
const router = useRouter()

const festival = ref(null)
const loading = ref(false)
const map = ref(null)
const endMarker = ref(null)
const kakaoSdkLoaded = ref(false)
const userLocation = ref(null)

// 이미지 URL 계산
const imageUrl = computed(() => {
  return festival.value?.image_url || 'https://via.placeholder.com/1920x800?text=No+Image'
})

const formatPeriod = () => {
  if (!festival.value) return ''

  // 디버깅: 실제 데이터 확인
  if (process.env.NODE_ENV === 'development') {
    console.log('Festival detail data:', {
      title: festival.value.title,
      event_start_date: festival.value.event_start_date,
      event_end_date: festival.value.event_end_date,
      start_month: festival.value.start_month,
      end_month: festival.value.end_month
    })
  }

  // event_start_date와 event_end_date가 있고 빈 문자열이 아닌 경우
  const startDate = festival.value.event_start_date
  const endDate = festival.value.event_end_date
  
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
  if (festival.value.start_month != null && festival.value.end_month != null) {
    const startMonth = Number(festival.value.start_month)
    const endMonth = Number(festival.value.end_month)
    if (!isNaN(startMonth) && !isNaN(endMonth)) {
      if (startMonth === endMonth) {
        return `${startMonth}월`
      } else {
        return `${startMonth}월 - ${endMonth}월`
      }
    }
  }
  
  // start_month만 있는 경우
  if (festival.value.start_month != null) {
    const startMonth = Number(festival.value.start_month)
    if (!isNaN(startMonth) && startMonth >= 1 && startMonth <= 12) {
      return `${startMonth}월 예정`
    }
  }
  
  // end_month만 있는 경우
  if (festival.value.end_month != null) {
    const endMonth = Number(festival.value.end_month)
    if (!isNaN(endMonth) && endMonth >= 1 && endMonth <= 12) {
      return `${endMonth}월 예정`
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

// 카카오맵 SDK 동적 로드
const loadKakaoMapSDK = () => {
  return new Promise((resolve, reject) => {
    // 이미 로드되었는지 확인
    if (window.kakao && window.kakao.maps) {
      console.log('✓ 카카오맵 SDK 이미 로드됨')
      kakaoSdkLoaded.value = true
      resolve()
      return
    }

    // 환경변수에서 API 키 가져오기
    const apiKey = import.meta.env.VITE_KAKAO_MAP_KEY

    // 디버깅: 환경변수 값 확인
    console.log('🔍 환경변수 체크:')
    console.log('  - VITE_KAKAO_MAP_KEY:', apiKey)
    console.log('  - 타입:', typeof apiKey)
    console.log('  - 길이:', apiKey?.length)

    if (!apiKey || apiKey === 'your_kakao_javascript_key_here') {
      console.error('✗ 카카오맵 API 키가 설정되지 않았습니다.')
      reject(new Error('카카오맵 API 키를 .env 파일에 설정해주세요.\nVITE_KAKAO_MAP_KEY=your_actual_key'))
      return
    }

    console.log('카카오맵 SDK 로딩 시작...')

    // 스크립트 동적 로드
    const script = document.createElement('script')
    script.type = 'text/javascript'
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${apiKey}&libraries=services,clusterer,drawing&autoload=false`

    script.onload = () => {
      console.log('카카오맵 SDK 스크립트 로드 완료, 초기화 중...')

      // SDK 초기화 대기
      if (window.kakao && window.kakao.maps) {
        window.kakao.maps.load(() => {
          console.log('✓ 카카오맵 SDK 초기화 완료!')
          kakaoSdkLoaded.value = true
          resolve()
        })
      } else {
        reject(new Error('카카오맵 SDK 로드 실패'))
      }
    }

    script.onerror = () => {
      console.error('✗ 카카오맵 SDK 스크립트 로드 실패')
      reject(new Error('카카오맵 SDK 스크립트를 불러올 수 없습니다. API 키를 확인해주세요.'))
    }

    document.head.appendChild(script)
  })
}

const fetchFestivalDetail = async () => {
  try {
    loading.value = true
    const festivalId = route.params.id
    festival.value = await getFestivalDetail(festivalId)

    // 축제 정보 로드 후 지도 초기화
    await nextTick()
    if (festival.value && festival.value.latitude && festival.value.longitude) {
      try {
        // 카카오맵 SDK 동적 로드
        await loadKakaoMapSDK()
        // SDK 로드 완료 후 지도 초기화
        initKakaoMap()
      } catch (error) {
        console.error('카카오맵 초기화 실패:', error)
        alert(`카카오맵을 로드하는데 실패했습니다.\n\n${error.message}\n\n다음을 확인하세요:\n1. frontend/.env 파일에 VITE_KAKAO_MAP_KEY 설정\n2. 카카오 개발자 콘솔에서 http://localhost:5173 도메인 등록\n3. 프론트엔드 서버 재시작`)
      }
    }
  } catch (error) {
    console.error('축제 상세 정보를 불러오는 데 실패했습니다:', error)
  } finally {
    loading.value = false
  }
}

// 카카오맵 초기화
const initKakaoMap = () => {
  console.log('🗺️ initKakaoMap 호출됨')
  console.log('📍 festival 좌표:', festival.value?.latitude, festival.value?.longitude)

  if (!kakaoSdkLoaded.value || !window.kakao || !window.kakao.maps) {
    console.error('✗ 카카오맵 SDK가 로드되지 않았습니다.')
    return
  }

  const container = document.getElementById('kakao-map')
  if (!container) {
    console.error('✗ kakao-map 요소를 찾을 수 없습니다.')
    return
  }

  console.log('✓ 지도 컨테이너 발견')

  try {
    const options = {
      center: new window.kakao.maps.LatLng(festival.value.latitude, festival.value.longitude),
      level: 4
    }

    console.log('지도 생성 중...')
    map.value = new window.kakao.maps.Map(container, options)
    console.log('✓ 지도 생성 완료!')

    // 목적지 마커 생성
    const markerPosition = new window.kakao.maps.LatLng(festival.value.latitude, festival.value.longitude)
    
    endMarker.value = new window.kakao.maps.Marker({
      position: markerPosition
    })
    endMarker.value.setMap(map.value)

    console.log('✓ 마커 생성 완료!')
  } catch (error) {
    console.error('✗ 지도 생성 중 오류:', error)
    alert('지도를 표시하는 중 오류가 발생했습니다: ' + error.message)
  }
}

// 좌표를 주소로 변환 (카카오맵 Geocoder 사용)
const coordToAddress = (lat, lng) => {
  return new Promise((resolve) => {
    if (!window.kakao || !window.kakao.maps || !window.kakao.maps.services) {
      console.log('카카오맵 SDK가 로드되지 않았습니다.')
      resolve(null)
      return
    }

    const geocoder = new window.kakao.maps.services.Geocoder()
    const coord = new window.kakao.maps.LatLng(lat, lng)

    geocoder.coord2Address(coord.getLng(), coord.getLat(), (result, status) => {
      if (status === window.kakao.maps.services.Status.OK) {
        // 도로명 주소 우선, 없으면 지번 주소
        const address = result[0].road_address 
          ? result[0].road_address.address_name 
          : (result[0].address ? result[0].address.address_name : null)
        
        console.log('좌표 변환 결과:', address)
        resolve(address)
      } else {
        console.log('좌표 변환 실패:', status)
        resolve(null)
      }
    })
  })
}

// 사용자 현재 위치 가져오기 (브라우저 Geolocation API)
const getUserCurrentLocation = () => {
  return new Promise((resolve) => {
    if (!navigator.geolocation) {
      console.log('Geolocation API를 지원하지 않습니다.')
      resolve(null)
      return
    }

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const lat = position.coords.latitude
        const lng = position.coords.longitude
        
        // 좌표를 주소로 변환
        const address = await coordToAddress(lat, lng)
        
        const location = {
          lat: lat,
          lng: lng,
          address: address || '현재 위치'
        }
        console.log('현재 위치:', location)
        userLocation.value = location
        resolve(location)
      },
      (error) => {
        console.log('위치 정보 가져오기 실패:', error.message)
        resolve(null)
      },
      {
        timeout: 5000,
        maximumAge: 60000,
        enableHighAccuracy: false
      }
    )
  })
}

// 카카오내비 앱으로 길찾기
const openKakaoNavi = async () => {
  if (!festival.value) return

  // 도착지 좌표를 숫자로 변환
  const endLat = parseFloat(festival.value.latitude)
  const endLng = parseFloat(festival.value.longitude)
  let endAddress = festival.value.address || festival.value.title

  // 좌표 유효성 검사
  if (isNaN(endLat) || isNaN(endLng)) {
    console.error('도착지 좌표가 유효하지 않습니다:', { latitude: festival.value.latitude, longitude: festival.value.longitude })
    alert('축제 위치 정보를 불러올 수 없습니다.')
    return
  }

  // 도착지 좌표가 있지만 주소가 정확하지 않은 경우, 좌표로 주소 변환 시도
  if (endLat && endLng && (!endAddress || endAddress === festival.value.title)) {
    const convertedAddress = await coordToAddress(endLat, endLng)
    if (convertedAddress) {
      endAddress = convertedAddress
    }
  }

  // 사용자 현재 위치 가져오기
  let startLocation = userLocation.value
  if (!startLocation) {
    // 위치 정보가 없으면 가져오기 시도
    startLocation = await getUserCurrentLocation()
  }

  // 출발지 좌표 유효성 검사
  if (!startLocation || !startLocation.lat || !startLocation.lng) {
    console.warn('출발지 정보를 가져올 수 없습니다. 도착지만 자동 입력됩니다.')
  }

  // 카카오맵 길찾기 URL 생성
  let naviUrl = ''
  
  if (startLocation && startLocation.lat && startLocation.lng && endLat && endLng) {
    // 출발지와 도착지 모두 좌표가 있는 경우
    try {
      const startLat = parseFloat(startLocation.lat)
      const startLng = parseFloat(startLocation.lng)
      const endLatNum = parseFloat(endLat)
      const endLngNum = parseFloat(endLng)
      
      naviUrl = `https://map.kakao.com/link/from/현재위치,${startLat},${startLng}/to/${encodeURIComponent(endAddress)},${endLatNum},${endLngNum}`
      
      console.log('카카오맵 길찾기 URL (출발지+도착지 자동 입력):', naviUrl)
      console.log('출발지:', { lat: startLat, lng: startLng, address: startLocation.address })
      console.log('도착지:', { name: endAddress, lat: endLatNum, lng: endLngNum })
    } catch (error) {
      console.error('URL 생성 오류:', error)
      // 폴백: 도착지만 포함
      const endLatNum = parseFloat(endLat)
      const endLngNum = parseFloat(endLng)
      const endParam = `${encodeURIComponent(endAddress)},${endLatNum},${endLngNum}`
      naviUrl = `https://map.kakao.com/link/to/${endParam}`
      console.log('카카오맵 URL (도착지만 자동 입력 - 폴백):', naviUrl)
    }
  } else if (endLat && endLng) {
    // 출발지 정보가 없는 경우 (도착지만)
    try {
      const endLatNum = parseFloat(endLat)
      const endLngNum = parseFloat(endLng)
      const endParam = `${encodeURIComponent(endAddress)},${endLatNum},${endLngNum}`
      naviUrl = `https://map.kakao.com/link/to/${endParam}`
      console.log('카카오맵 URL (도착지만 자동 입력):', naviUrl)
    } catch (error) {
      console.error('URL 생성 오류:', error)
      const endLatNum = parseFloat(endLat)
      const endLngNum = parseFloat(endLng)
      naviUrl = `https://map.kakao.com/link/to/${endLatNum},${endLngNum}`
      console.log('카카오맵 URL (도착지만 자동 입력 - 좌표만):', naviUrl)
    }
    console.log('도착지:', { name: endAddress, lat: endLat, lng: endLng })
    console.log('⚠️ 출발지 정보를 가져올 수 없어 도착지만 자동 입력됩니다.')
  } else {
    // 좌표가 없는 경우 검색 URL 사용
    const searchQuery = encodeURIComponent(endAddress)
    naviUrl = `https://map.kakao.com/?q=${searchQuery}`
    console.log('카카오맵 검색 URL:', naviUrl)
  }
  
  // 새 창에서 카카오맵 열기
  try {
    const newWindow = window.open(naviUrl, '_blank')
    if (!newWindow || newWindow.closed || typeof newWindow.closed === 'undefined') {
      window.location.href = naviUrl
    }
  } catch (error) {
    console.error('카카오맵 열기 실패:', error)
    window.location.href = naviUrl
  }
}

// 주소 복사
const copyAddress = async () => {
  if (!festival.value || !festival.value.address) return

  try {
    await navigator.clipboard.writeText(festival.value.address)
    alert('주소가 클립보드에 복사되었습니다!')
  } catch (err) {
    console.error('주소 복사 실패:', err)
    // 폴백: 수동 복사
    const textArea = document.createElement('textarea')
    textArea.value = festival.value.address
    document.body.appendChild(textArea)
    textArea.select()
    document.execCommand('copy')
    document.body.removeChild(textArea)
    alert('주소가 복사되었습니다!')
  }
}

const goBack = () => {
  router.push({ name: 'festivals' })
}

onMounted(() => {
  fetchFestivalDetail()
})
</script>

<style scoped>
/* 기본 설정 */
* {
  box-sizing: border-box;
}

.page-container {
  min-height: 100vh;
  background-color: #ffffff;
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
  color: #191f28;
}

/* 1. 히어로 섹션 (이미지 품질 개선) */
.hero-section {
  width: 100%;
  height: 50vh;
  min-height: 400px;
  background-color: #111;
}

.image-container {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}

.bg-image-blur {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-size: cover;
  background-position: center;
  filter: blur(30px) brightness(0.7);
  transform: scale(1.1);
  z-index: 1;
}

.main-image {
  position: relative;
  z-index: 2;
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  image-rendering: auto;
  image-rendering: -webkit-optimize-contrast;
  -ms-interpolation-mode: bicubic;
  backface-visibility: hidden;
  -webkit-font-smoothing: antialiased;
}

/* 2. 메인 컨테이너 */
.main-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 4rem 1.5rem 6rem;
}

/* 헤더 스타일 */
.festival-header {
  margin-bottom: 2rem;
}

.tags {
  display: flex;
  gap: 8px;
  margin-bottom: 1rem;
}

.tag {
  font-size: 0.85rem;
  font-weight: 700;
  padding: 6px 10px;
  border-radius: 6px;
}

.tag.region {
  color: #3182f6;
  background-color: rgba(49, 130, 246, 0.1);
}

.tag.category {
  color: #4e5968;
  background-color: #f2f4f6;
}

.title {
  font-size: 2.8rem;
  font-weight: 800;
  line-height: 1.25;
  margin: 0 0 1rem;
  letter-spacing: -0.02em;
  word-break: keep-all;
}

.date-range {
  font-size: 1.25rem;
  color: #4e5968;
  font-weight: 500;
}

.divider {
  width: 100%;
  height: 1px;
  background-color: #e5e8eb;
  margin-bottom: 3rem;
}

/* 3. 그리드 레이아웃 */
.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 5rem;
}

/* 좌측 패널 */
.left-panel {
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.info-group {
  display: flex;
  flex-direction: column;
}

.info-group .group-label {
  font-size: 0.95rem;
  color: #8b95a1;
  font-weight: 600;
  margin-bottom: 0.8rem;
}

.info-group .group-value {
  font-size: 1.2rem;
  font-weight: 500;
  color: #191f28;
  line-height: 1.5;
}

.info-group .group-text {
  font-size: 1.05rem;
  line-height: 1.75;
  color: #333;
  white-space: pre-wrap;
}

.btn-text-action {
  margin-top: 0.8rem;
  font-size: 0.9rem;
  color: #8b95a1;
  background: none;
  border: none;
  text-decoration: underline;
  cursor: pointer;
  padding: 0;
  align-self: flex-start;
}

.btn-text-action:hover {
  color: #333;
}

.action-area {
  margin-top: 1rem;
}

.btn-back {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 14px 28px;
  border-radius: 10px;
  border: 1px solid #d1d6db;
  background-color: white;
  font-size: 1rem;
  font-weight: 600;
  color: #333;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-back:hover {
  background-color: #f9fafb;
  border-color: #b0b8c1;
}

/* 우측 패널 (Sticky 지도) */
.right-panel {
  position: sticky;
  top: 2rem;
  height: fit-content;
}

.map-card {
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.08);
}

.map-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.2rem 1.5rem;
  background-color: white;
  border-bottom: 1px solid #f2f4f6;
}

.map-label {
  font-size: 1rem;
  font-weight: 800;
  color: #191f28;
}

/* 카카오내비 버튼 스타일 */
.btn-kakao-official {
  display: flex;
  align-items: center;
  gap: 8px;
  background-color: #FEE500;
  border: none;
  padding: 8px 16px 8px 12px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 700;
  color: #000000;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.btn-kakao-official:hover {
  background-color: #fdd835;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.btn-kakao-official:active {
  transform: translateY(0);
}

.kakao-svg {
  width: 18px;
  height: 18px;
}

.kakao-map {
  width: 100%;
  height: 420px;
  background-color: #f2f4f6;
}

/* 로딩 */
.loading-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.loader {
  width: 36px;
  height: 36px;
  border: 4px solid #e5e8eb;
  border-top-color: #3182f6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 반응형 */
@media (max-width: 960px) {
  .detail-grid {
    grid-template-columns: 1fr;
    gap: 4rem;
  }

  .right-panel {
    position: static;
  }

  .title {
    font-size: 2.2rem;
  }

  .hero-section {
    height: 40vh;
  }

  .main-container {
    padding: 3rem 1rem 4rem;
  }
}

@media (max-width: 768px) {
  .hero-section {
    height: 35vh;
    min-height: 300px;
  }

  .title {
    font-size: 1.8rem;
  }

  .date-range {
    font-size: 1.1rem;
  }

  .detail-grid {
    gap: 3rem;
  }

  .kakao-map {
    height: 350px;
  }

  .main-container {
    padding: 2rem 1rem 3rem;
  }
}
</style>