<template>
  <div class="festival-detail-container">
    <div v-if="festival" class="festival-detail">
      <!-- 헤더 이미지 -->
      <div class="hero-image">
        <img :src="festival.image_url || 'https://via.placeholder.com/1200x400?text=Festival'" :alt="festival.title" />
        <div class="hero-overlay">
          <h1>{{ festival.title }}</h1>
          <div class="festival-badge">{{ festival.region }}</div>
        </div>
      </div>

      <!-- 기본 정보 -->
      <div class="content-wrapper">
        <div class="info-section">
          <h2>축제 정보</h2>
          <div class="info-grid">
            <div class="info-card">
              <div class="info-icon">📅</div>
              <div class="info-content">
                <h3>개최 기간</h3>
                <p>{{ formatPeriod() }}</p>
              </div>
            </div>
            <div class="info-card">
              <div class="info-icon">📍</div>
              <div class="info-content">
                <h3>장소</h3>
                <p>{{ festival.address }}</p>
              </div>
            </div>
            <div class="info-card">
              <div class="info-icon">🎭</div>
              <div class="info-content">
                <h3>카테고리</h3>
                <p>{{ festival.category || '일반축제' }}</p>
              </div>
            </div>
            <div class="info-card" v-if="festival.phone">
              <div class="info-icon">📞</div>
              <div class="info-content">
                <h3>문의</h3>
                <p>{{ festival.phone }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 위치 정보 및 카카오맵 -->
        <div class="location-section" v-if="festival.latitude && festival.longitude">
          <h2>위치 및 길찾기</h2>
          <div class="location-info">
            <p><strong>주소:</strong> {{ festival.address }}</p>
            <p><strong>좌표:</strong> {{ festival.latitude }}, {{ festival.longitude }}</p>
          </div>

          <!-- 카카오맵 표시 -->
          <div id="kakao-map" class="kakao-map"></div>

          <!-- 길찾기 버튼 -->
          <div class="map-buttons">
            <button @click="openKakaoNavi" class="map-button navi-btn">
              <span class="btn-icon">🧭</span>
              카카오내비로 길찾기
            </button>
            <button @click="copyAddress" class="map-button copy-btn">
              <span class="btn-icon">📋</span>
              주소 복사
            </button>
          </div>
        </div>

        <!-- 하단 액션 버튼 -->
        <div class="action-buttons">
          <button @click="goBack" class="back-button">
            목록으로 돌아가기
          </button>
        </div>
      </div>
    </div>

    <!-- 로딩 상태 -->
    <div v-else class="loading">
      <p>축제 정보를 불러오는 중...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getFestivalDetail } from '@/api/festivals'

const route = useRoute()
const router = useRouter()

const festival = ref(null)
const loading = ref(false)
const map = ref(null)
const endMarker = ref(null)
const kakaoSdkLoaded = ref(false)

const formatPeriod = () => {
  if (!festival.value) return ''

  if (festival.value.event_start_date && festival.value.event_end_date) {
    const start = formatDate(festival.value.event_start_date)
    const end = formatDate(festival.value.event_end_date)
    return `${start} ~ ${end}`
  } else if (festival.value.event_start_date) {
    return formatDate(festival.value.event_start_date)
  } else if (festival.value.start_month) {
    return `${festival.value.start_month}월`
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
      level: 5
    }

    console.log('지도 생성 중...')
    map.value = new window.kakao.maps.Map(container, options)
    console.log('✓ 지도 생성 완료!')

    // 목적지 마커 생성 (빨간색)
    const markerPosition = new window.kakao.maps.LatLng(festival.value.latitude, festival.value.longitude)
    const imageSrc = 'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_red.png'
    const imageSize = new window.kakao.maps.Size(40, 42)
    const markerImage = new window.kakao.maps.MarkerImage(imageSrc, imageSize)

    endMarker.value = new window.kakao.maps.Marker({
      position: markerPosition,
      image: markerImage
    })
    endMarker.value.setMap(map.value)

    // 인포윈도우 생성
    const infowindow = new window.kakao.maps.InfoWindow({
      content: `<div style="padding:10px;font-size:14px;font-weight:bold;">🎉 ${festival.value.title}</div>`
    })
    infowindow.open(map.value, endMarker.value)

    console.log('✓ 마커 및 인포윈도우 생성 완료!')
  } catch (error) {
    console.error('✗ 지도 생성 중 오류:', error)
    alert('지도를 표시하는 중 오류가 발생했습니다: ' + error.message)
  }
}

// 카카오내비 앱으로 길찾기
const openKakaoNavi = () => {
  if (!festival.value) return

  const lat = festival.value.latitude
  const lng = festival.value.longitude
  const name = encodeURIComponent(festival.value.title)

  // 카카오맵 웹 길찾기 URL
  window.open(`https://map.kakao.com/link/to/${name},${lat},${lng}`, '_blank')
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
.festival-detail-container {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.hero-image {
  position: relative;
  width: 100%;
  height: 400px;
  overflow: hidden;
}

.hero-image img {
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

.hero-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.8), transparent);
  padding: 3rem 2rem;
  color: white;
}

.hero-overlay h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.festival-badge {
  display: inline-block;
  background: rgba(52, 152, 219, 0.9);
  padding: 0.5rem 1rem;
  border-radius: 25px;
  font-weight: 600;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.info-section,
.location-section {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.info-section h2,
.location-section h2 {
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  color: #333;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.info-card {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.info-icon {
  font-size: 2rem;
}

.info-content h3 {
  font-size: 1rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.info-content p {
  font-size: 1.1rem;
  color: #333;
  font-weight: 500;
}

.location-info {
  margin-bottom: 1.5rem;
}

.location-info p {
  margin-bottom: 0.75rem;
  line-height: 1.6;
  color: #555;
}

/* 카카오맵 스타일 */
.kakao-map {
  width: 100%;
  height: 500px;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  overflow: hidden;
  border: 2px solid #e0e0e0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 지도 버튼 스타일 */
.map-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.map-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.map-button .btn-icon {
  font-size: 1.3rem;
}

.navi-btn {
  background: linear-gradient(135deg, #FEE500 0%, #FFEB3B 100%);
  color: #3c1e1e;
}

.navi-btn:hover {
  background: linear-gradient(135deg, #FFEB3B 0%, #FDD835 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(254, 229, 0, 0.4);
}

.copy-btn {
  background: linear-gradient(135deg, #95a5a6 0%, #7f8c8d 100%);
  color: white;
}

.copy-btn:hover {
  background: linear-gradient(135deg, #7f8c8d 0%, #6c7a7b 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(127, 140, 141, 0.4);
}

.action-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
}

.back-button {
  padding: 1rem 2rem;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.back-button:hover {
  background-color: #5a6268;
}

.loading {
  text-align: center;
  padding: 4rem 2rem;
  font-size: 1.2rem;
  color: #666;
}

@media (max-width: 768px) {
  .hero-image {
    height: 250px;
  }

  .hero-overlay h1 {
    font-size: 1.8rem;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .kakao-map {
    height: 350px;
  }

  .map-buttons {
    grid-template-columns: 1fr;
  }
}
</style>
