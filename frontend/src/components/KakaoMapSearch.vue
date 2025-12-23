<template>
  <div class="kakao-map-search" :class="{ 'bookmark-mode': bookmark, 'show': bookmark }">
    <!-- 헤더는 북마크 모드가 아닐 때만 표시 -->
    <div v-if="!bookmark" class="search-header">
      <h2>장소 검색 및 북마크</h2>
      <button class="close-btn" @click="$emit('close')">✕</button>
    </div>
    
    <!-- 북마크 모드일 때는 간단한 헤더 -->
    <div v-if="bookmark" class="bookmark-header">
      <h2>북마크 위치</h2>
      <button class="close-btn" @click="$emit('close')">✕</button>
    </div>

    <!-- 북마크 모드일 때는 정보 카드와 지도만 표시 -->
    <template v-if="bookmark && bookmark.place">
      <div class="bookmark-info-card">
        <h3>{{ bookmark.place.title }}</h3>
        <p class="address">{{ bookmark.place.address }}</p>
        <p v-if="bookmark.place.category" class="category">{{ bookmark.place.category }}</p>
      </div>
      <div class="map-container">
        <div id="map" style="width:100%;height:400px;"></div>
      </div>
    </template>

    <!-- 일반 모드일 때는 전체 기능 표시 -->
    <template v-else>
      <!-- 검색 기능 -->
      <div class="search-container">
        <div class="search-box">
          <input
            v-model="searchKeyword"
            type="text"
            placeholder="장소를 검색하세요"
            @keyup.enter="searchPlaces"
            class="search-input"
          />
          <button @click="searchPlaces" class="search-btn">검색</button>
        </div>
      </div>

      <div class="map-container">
        <div id="map" style="width:100%;height:400px;"></div>
      </div>
    </template>

    <!-- 검색 결과는 북마크 모드가 아닐 때만 표시 -->
    <div v-if="!bookmark && places.length > 0" class="results-container">
      <h3>검색 결과</h3>
      <div class="places-list">
        <div
          v-for="place in places"
          :key="place.id"
          class="place-item"
        >
          <div class="place-info">
            <h4>{{ place.place_name }}</h4>
            <p class="address">{{ place.road_address_name || place.address_name }}</p>
            <p class="category" v-if="place.category_name">{{ place.category_name }}</p>
            <p class="phone" v-if="place.phone">{{ place.phone }}</p>
          </div>
          <button
            @click="bookmarkPlace(place)"
            class="bookmark-btn"
            :disabled="isBookmarking"
          >
            {{ isBookmarking ? '저장 중...' : '북마크 저장' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 에러/성공 메시지는 북마크 모드가 아닐 때만 표시 -->
    <div v-if="!bookmark && error" class="error-message">{{ error }}</div>
    <div v-if="!bookmark && success" class="success-message">{{ success }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { placeAPI } from '@/api/place'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  bookmark: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close'])

const authStore = useAuthStore()
const searchKeyword = ref('')
const places = ref([])
const map = ref(null)
const markers = ref([])
const error = ref('')
const success = ref('')
const isBookmarking = ref(false)

// 카카오맵 SDK 로드
const loadKakaoMap = () => {
  return new Promise((resolve, reject) => {
    // 이미 로드되었는지 확인
    if (window.kakao && window.kakao.maps) {
      resolve()
      return
    }

    // 환경변수에서 API 키 가져오기
    const apiKey = import.meta.env.VITE_KAKAO_MAP_KEY

    if (!apiKey || apiKey === 'your_kakao_javascript_key_here') {
      error.value = '카카오맵 API 키가 설정되지 않았습니다.'
      reject(new Error('카카오맵 API 키를 .env 파일에 설정해주세요.'))
      return
    }

    // 스크립트 동적 로드
    const script = document.createElement('script')
    script.type = 'text/javascript'
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${apiKey}&libraries=services,clusterer&autoload=false`

    script.onload = () => {
      // SDK 초기화 대기
      if (window.kakao && window.kakao.maps) {
        window.kakao.maps.load(() => {
          resolve()
        })
      } else {
        error.value = '카카오맵 SDK 로드 실패'
        reject(new Error('카카오맵 SDK 로드 실패'))
      }
    }

    script.onerror = () => {
      error.value = '카카오맵 SDK를 불러올 수 없습니다.'
      reject(new Error('카카오맵 SDK 스크립트를 불러올 수 없습니다. API 키를 확인해주세요.'))
    }

    document.head.appendChild(script)
  })
}

// 지도 초기화
const initMap = () => {
  const container = document.getElementById('map')
  
  // 북마크 모드인 경우 해당 위치로 초기화
  if (props.bookmark && props.bookmark.place && props.bookmark.place.latitude && props.bookmark.place.longitude) {
    const place = props.bookmark.place
    const options = {
      center: new window.kakao.maps.LatLng(parseFloat(place.latitude), parseFloat(place.longitude)),
      level: 3
    }
    map.value = new window.kakao.maps.Map(container, options)
  } else {
    // 일반 검색 모드
    const options = {
      center: new window.kakao.maps.LatLng(37.5665, 126.9780), // 서울시청
      level: 3
    }
    map.value = new window.kakao.maps.Map(container, options)
  }
}

// 마커 제거
const clearMarkers = () => {
  markers.value.forEach(marker => marker.setMap(null))
  markers.value = []
}

// 검색
const searchPlaces = () => {
  if (!searchKeyword.value.trim()) {
    error.value = '검색어를 입력해주세요.'
    return
  }

  if (!window.kakao || !window.kakao.maps || !window.kakao.maps.services) {
    error.value = '카카오맵 SDK가 로드되지 않았습니다.'
    return
  }

  error.value = ''
  const ps = new window.kakao.maps.services.Places()

  ps.keywordSearch(searchKeyword.value, (data, status) => {
    if (status === window.kakao.maps.services.Status.OK) {
      places.value = data
      clearMarkers()

      // 지도 중심 이동
      const bounds = new window.kakao.maps.LatLngBounds()
      data.forEach(place => {
        const position = new window.kakao.maps.LatLng(place.y, place.x)
        bounds.extend(position)

        // 마커 생성
        const marker = new window.kakao.maps.Marker({
          position: position,
          map: map.value
        })
        markers.value.push(marker)

        // 인포윈도우
        const infowindow = new window.kakao.maps.InfoWindow({
          content: `<div style="padding:5px;font-size:12px;">${place.place_name}</div>`
        })
        window.kakao.maps.event.addListener(marker, 'click', () => {
          infowindow.open(map.value, marker)
        })
      })

      map.value.setBounds(bounds)
    } else if (status === window.kakao.maps.services.Status.ZERO_RESULT) {
      error.value = '검색 결과가 없습니다.'
      places.value = []
    } else {
      error.value = '검색 중 오류가 발생했습니다.'
      places.value = []
    }
  })
}

// 북마크 정보가 변경되면 지도 업데이트
watch(() => props.bookmark, (newBookmark) => {
  if (newBookmark && newBookmark.place && map.value && window.kakao && window.kakao.maps) {
    const place = newBookmark.place
    if (place.latitude && place.longitude) {
      clearMarkers()
      const position = new window.kakao.maps.LatLng(parseFloat(place.latitude), parseFloat(place.longitude))
      map.value.setCenter(position)
      map.value.setLevel(3)
      
      // 마커 생성
      const marker = new window.kakao.maps.Marker({
        position: position,
        map: map.value
      })
      markers.value.push(marker)
      
      // 인포윈도우
      const infowindow = new window.kakao.maps.InfoWindow({
        content: `<div style="padding:10px;font-size:14px;min-width:150px;">
          <strong>${place.title || '장소명 없음'}</strong><br/>
          <span style="font-size:12px;color:#666;">${place.address || '주소 없음'}</span>
        </div>`
      })
      infowindow.open(map.value, marker)
    }
  }
}, { immediate: false })

// 북마크 저장
const bookmarkPlace = async (place) => {
  if (!authStore.isAuthenticated) {
    error.value = '로그인이 필요합니다.'
    return
  }

  isBookmarking.value = true
  error.value = ''
  success.value = ''

  try {
    // 1. 카카오맵 장소를 Place로 저장
    const placeData = {
      id: place.id,
      place_name: place.place_name,
      address_name: place.address_name,
      road_address_name: place.road_address_name || '',
      x: place.x,
      y: place.y,
      category_name: place.category_name || '',
      phone: place.phone || '',
      place_url: place.place_url || ''
    }

    console.log('장소 데이터:', placeData)
    const placeResponse = await placeAPI.createPlaceFromKakao(placeData)
    console.log('장소 저장 응답:', placeResponse.data)
    const savedPlace = placeResponse.data

    if (!savedPlace || !savedPlace.id) {
      throw new Error('장소 저장 응답에 ID가 없습니다.')
    }

    // 2. 북마크 생성
    console.log('북마크 생성 시도, place_id:', savedPlace.id)
    await placeAPI.createBookmark(savedPlace.id)
    console.log('북마크 생성 성공')

    success.value = '북마크가 저장되었습니다!'
    setTimeout(() => {
      success.value = ''
    }, 3000)
  } catch (err) {
    console.error('북마크 저장 실패:', err)
    console.error('에러 상세:', err.response?.data)
    
    if (err.response?.data) {
      const errorData = err.response.data
      
      // 백엔드에서 반환하는 에러 메시지 처리
      if (errorData.error) {
        error.value = errorData.error
      } else if (errorData.place_id) {
        // Serializer ValidationError는 배열로 반환될 수 있음
        const placeIdError = Array.isArray(errorData.place_id) 
          ? errorData.place_id[0] 
          : errorData.place_id
        error.value = placeIdError || '이미 북마크된 장소입니다.'
      } else if (errorData.non_field_errors) {
        const nonFieldError = Array.isArray(errorData.non_field_errors)
          ? errorData.non_field_errors[0]
          : errorData.non_field_errors
        error.value = nonFieldError
      } else {
        // 첫 번째 필드 에러 사용
        const firstError = Object.values(errorData)[0]
        error.value = Array.isArray(firstError) ? firstError[0] : firstError
      }
    } else if (err.message) {
      error.value = err.message
    } else {
      error.value = '북마크 저장 중 오류가 발생했습니다.'
    }
  } finally {
    isBookmarking.value = false
  }
}

onMounted(async () => {
  try {
    await loadKakaoMap()
    await nextTick()
    initMap()
    
    // 북마크 모드인 경우 마커 표시
    if (props.bookmark && props.bookmark.place && map.value && window.kakao && window.kakao.maps) {
      const place = props.bookmark.place
      if (place.latitude && place.longitude) {
        const position = new window.kakao.maps.LatLng(parseFloat(place.latitude), parseFloat(place.longitude))
        
        // 지도 중심 이동
        map.value.setCenter(position)
        map.value.setLevel(3)
        
        // 기존 마커 제거
        clearMarkers()
        
        // 마커 생성
        const marker = new window.kakao.maps.Marker({
          position: position,
          map: map.value
        })
        markers.value.push(marker)
        
        // 인포윈도우
        const infowindow = new window.kakao.maps.InfoWindow({
          content: `<div style="padding:10px;font-size:14px;min-width:150px;">
            <strong>${place.title || '장소명 없음'}</strong><br/>
            <span style="font-size:12px;color:#666;">${place.address || '주소 없음'}</span>
          </div>`
        })
        infowindow.open(map.value, marker)
      }
    }
  } catch (err) {
    console.error('카카오맵 로드 실패:', err)
    error.value = err.message || '카카오맵을 불러올 수 없습니다.'
  }
})

onUnmounted(() => {
  clearMarkers()
})
</script>

<style scoped>
/* 북마크 정보 카드 */
.bookmark-info-card {
  background: rgba(255, 255, 255, 0.9);
  padding: 1.5rem;
  margin: 0;
  border-bottom: 1px solid #e5e7eb;
  border-radius: 0;
}

.bookmark-info-card h3 {
  margin: 0 0 10px 0;
  font-size: 1.2rem;
  color: #333;
  font-weight: 600;
}

.bookmark-info-card .address {
  margin: 5px 0;
  font-size: 0.9rem;
  color: #666;
}

.bookmark-info-card .category {
  margin: 5px 0 0 0;
  font-size: 0.85rem;
  color: #4285f4;
  display: inline-block;
  padding: 4px 10px;
  background: rgba(66, 133, 244, 0.1);
  border-radius: 12px;
}
.kakao-map-search {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 90%;
  max-width: 900px;
  max-height: 90vh;
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  z-index: 1000;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: all 0.3s ease;
}

/* 북마크 모드일 때 사이드패널로 변경 */
.kakao-map-search.bookmark-mode {
  top: 50%;
  left: 0;
  transform: translate(-100%, -50%);
  width: 450px;
  max-width: 90vw;
  max-height: 90vh;
  height: auto;
  border-radius: 0;
  border-top-right-radius: 20px;
  border-bottom-right-radius: 20px;
  box-shadow: 4px 0 20px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease;
}

/* 북마크 모드일 때 표시 */
.kakao-map-search.bookmark-mode.show {
  transform: translate(0, -50%);
}

@media (max-width: 768px) {
  .kakao-map-search.bookmark-mode {
    width: 85vw;
    max-width: 400px;
  }
}

.search-header,
.bookmark-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e5e7eb;
}

.bookmark-header {
  padding: 1rem 1.5rem;
}

.search-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #1f2937;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
  padding: 0.5rem;
  line-height: 1;
}

.close-btn:hover {
  color: #1f2937;
}

.search-container {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e5e7eb;
}

.search-box {
  display: flex;
  gap: 0.5rem;
}

.search-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 1rem;
  outline: none;
}

.search-input:focus {
  border-color: #4285f4;
  box-shadow: 0 0 0 3px rgba(66, 133, 244, 0.1);
}

.search-btn {
  padding: 0.75rem 1.5rem;
  background: #4285f4;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.search-btn:hover {
  background: #357ae8;
}

.map-container {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e5e7eb;
}

/* 북마크 모드일 때 지도 컨테이너 패딩 조정 */
.kakao-map-search.bookmark-mode .map-container {
  padding: 0;
  border-bottom: none;
}

.results-container {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem 2rem;
}

.results-container h3 {
  margin: 0 0 1rem 0;
  font-size: 1.2rem;
  color: #1f2937;
}

.places-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.place-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  transition: all 0.2s;
}

.place-item:hover {
  border-color: #4285f4;
  box-shadow: 0 4px 12px rgba(66, 133, 244, 0.1);
}

.place-info {
  flex: 1;
}

.place-info h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
  color: #1f2937;
}

.place-info .address {
  margin: 0.25rem 0;
  color: #6b7280;
  font-size: 0.9rem;
}

.place-info .category {
  margin: 0.25rem 0;
  color: #4285f4;
  font-size: 0.85rem;
  font-weight: 500;
}

.place-info .phone {
  margin: 0.25rem 0 0 0;
  color: #9ca3af;
  font-size: 0.85rem;
}

.bookmark-btn {
  padding: 0.75rem 1.5rem;
  background: #10b981;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  white-space: nowrap;
}

.bookmark-btn:hover:not(:disabled) {
  background: #059669;
}

.bookmark-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.error-message {
  padding: 1rem 2rem;
  background: #fef2f2;
  color: #dc2626;
  border-top: 1px solid #fecaca;
}

.success-message {
  padding: 1rem 2rem;
  background: #d1fae5;
  color: #059669;
  border-top: 1px solid #a7f3d0;
}
</style>

