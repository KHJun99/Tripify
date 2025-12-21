<script setup>
import { ref, onMounted, watch, onBeforeUnmount } from 'vue'

const props = defineProps({
  attractions: {
    type: Array,
    default: () => []
  },
  region: {
    type: String,
    default: ''
  }
})

const mapContainer = ref(null)
const map = ref(null)
const markers = ref([])
const kakaoSdkLoaded = ref(false)
const mapError = ref('')

// 카카오맵 SDK 동적 로드
const loadKakaoMapSDK = () => {
  return new Promise((resolve, reject) => {
    // 이미 로드되었는지 확인
    if (window.kakao && window.kakao.maps) {
      kakaoSdkLoaded.value = true
      resolve()
      return
    }

    // 환경변수에서 API 키 가져오기
    const apiKey = import.meta.env.VITE_KAKAO_MAP_KEY

    if (!apiKey || apiKey === 'your_kakao_javascript_key_here') {
      mapError.value = '카카오맵 API 키가 설정되지 않았습니다.'
      reject(new Error('카카오맵 API 키를 .env 파일에 설정해주세요.'))
      return
    }

    // 스크립트 동적 로드
    const script = document.createElement('script')
    script.type = 'text/javascript'
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${apiKey}&libraries=services&autoload=false`

    script.onload = () => {
      if (window.kakao && window.kakao.maps) {
        window.kakao.maps.load(() => {
          kakaoSdkLoaded.value = true
          resolve()
        })
      } else {
        reject(new Error('카카오맵 SDK 로드 실패'))
      }
    }

    script.onerror = () => {
      mapError.value = '카카오맵 SDK를 불러올 수 없습니다.'
      reject(new Error('카카오맵 SDK 스크립트를 불러올 수 없습니다.'))
    }

    document.head.appendChild(script)
  })
}

// 지도 초기화
const initMap = () => {
  if (!mapContainer.value || !kakaoSdkLoaded.value) return

  try {
    // 기본 중심 좌표 (한국 중심)
    const defaultPosition = new window.kakao.maps.LatLng(37.5665, 126.9780)
    
    // 지도 옵션
    const mapOption = {
      center: defaultPosition,
      level: 6 // 확대 레벨
    }

    // 지도 생성
    map.value = new window.kakao.maps.Map(mapContainer.value, mapOption)

    // 지역으로 중심 설정 시도
    if (props.region) {
      searchPlace(props.region, (lat, lng) => {
        if (lat && lng) {
          const position = new window.kakao.maps.LatLng(lat, lng)
          map.value.setCenter(position)
          map.value.setLevel(7)
        }
      })
    }

    // 관광지 마커 추가
    addMarkers()
  } catch (error) {
    console.error('지도 초기화 오류:', error)
    mapError.value = '지도를 불러올 수 없습니다.'
  }
}

// 장소 검색
const searchPlace = (query, callback) => {
  if (!window.kakao || !window.kakao.maps || !window.kakao.maps.services) {
    callback(null, null)
    return
  }

  const geocoder = new window.kakao.maps.services.Geocoder()
  
  // 주소로 좌표 검색
  geocoder.addressSearch(query, (result, status) => {
    if (status === window.kakao.maps.services.Status.OK) {
      const lat = parseFloat(result[0].y)
      const lng = parseFloat(result[0].x)
      callback(lat, lng)
    } else {
      // 주소 검색 실패 시 키워드 검색 시도
      const places = new window.kakao.maps.services.Places()
      places.keywordSearch(query, (data, status) => {
        if (status === window.kakao.maps.services.Status.OK && data.length > 0) {
          const lat = parseFloat(data[0].y)
          const lng = parseFloat(data[0].x)
          callback(lat, lng)
        } else {
          callback(null, null)
        }
      })
    }
  })
}

// 관광지 마커 추가
const addMarkers = () => {
  if (!map.value || !props.attractions || props.attractions.length === 0) return

  // 기존 마커 제거
  markers.value.forEach(marker => marker.setMap(null))
  markers.value = []

  const places = new window.kakao.maps.services.Places()
  const bounds = new window.kakao.maps.LatLngBounds()

  let loadedCount = 0
  const totalCount = props.attractions.length

  props.attractions.forEach((attraction, index) => {
    if (!attraction.name) {
      loadedCount++
      if (loadedCount === totalCount && markers.value.length > 0) {
        map.value.setBounds(bounds)
      }
      return
    }

    // 지역명을 포함한 검색어 생성 (지역명이 관광지 이름에 없을 경우만 추가)
    let searchQuery = attraction.name
    if (props.region) {
      // 관광지 이름에 지역명이 포함되어 있지 않은 경우에만 추가
      const regionVariations = [
        props.region,
        props.region.replace('시', ''),
        props.region.replace('도', ''),
        props.region.replace('특별시', ''),
        props.region.replace('광역시', '')
      ]
      const hasRegion = regionVariations.some(region => 
        attraction.name.includes(region)
      )
      
      if (!hasRegion) {
        searchQuery = `${props.region} ${attraction.name}`
      }
    }

    // 키워드 검색
    places.keywordSearch(searchQuery, (data, status) => {
      loadedCount++

      if (status === window.kakao.maps.services.Status.OK && data.length > 0) {
        // 지역이 지정된 경우, 지역명이 포함된 결과를 우선 선택
        let selectedPlace = data[0]
        if (props.region) {
          // 지역명 변형 생성 (대구, 대구시, 대구광역시 등)
          const regionVariations = [
            props.region,
            props.region.replace('시', ''),
            props.region.replace('도', ''),
            props.region.replace('특별시', ''),
            props.region.replace('광역시', ''),
            props.region.replace('시', '시 '),
            props.region.replace('광역시', '광역시 ')
          ]
          
          // 지역명이 정확히 포함된 결과 찾기
          const regionMatch = data.find(place => {
            const address = place.address_name || ''
            const roadAddress = place.road_address_name || ''
            const placeName = place.place_name || ''
            const fullText = `${address} ${roadAddress} ${placeName}`
            
            // 지역명이 주소의 시작 부분에 있는지 확인 (더 정확한 매칭)
            return regionVariations.some(region => {
              const trimmedRegion = region.trim()
              return fullText.includes(trimmedRegion) && 
                     (address.startsWith(trimmedRegion) || 
                      roadAddress.startsWith(trimmedRegion) ||
                      address.includes(`${trimmedRegion} `) ||
                      roadAddress.includes(`${trimmedRegion} `))
            })
          })
          
          if (regionMatch) {
            selectedPlace = regionMatch
          } else {
            // 정확한 매칭이 없으면 첫 번째 결과 사용하지 않고 스킵
            console.warn(`지역 "${props.region}"에 해당하는 "${attraction.name}"을 찾을 수 없습니다.`)
            loadedCount++
            if (loadedCount === totalCount && markers.value.length > 0) {
              map.value.setBounds(bounds)
            }
            return
          }
        }

        const lat = parseFloat(selectedPlace.y)
        const lng = parseFloat(selectedPlace.x)
        const position = new window.kakao.maps.LatLng(lat, lng)

        // 마커 이미지 생성
        const imageSrc = 'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_number_blue.png'
        const imageSize = new window.kakao.maps.Size(36, 37)
        const imageOptions = {
          spriteSize: new window.kakao.maps.Size(36, 691),
          spriteOrigin: new window.kakao.maps.Point(0, (index % 10) * 46 + 10),
          offset: new window.kakao.maps.Point(13, 37)
        }
        const markerImage = new window.kakao.maps.MarkerImage(imageSrc, imageSize, imageOptions)

        // 마커 생성
        const marker = new window.kakao.maps.Marker({
          position: position,
          image: markerImage,
          map: map.value
        })

        // 인포윈도우 생성
        const infowindow = new window.kakao.maps.InfoWindow({
          content: `<div style="padding:5px;font-size:12px;min-width:100px;">${attraction.name}</div>`
        })

        // 마커 클릭 이벤트
        window.kakao.maps.event.addListener(marker, 'click', () => {
          infowindow.open(map.value, marker)
        })

        markers.value.push(marker)
        bounds.extend(position)
      }

      // 모든 검색 완료 후 지도 범위 조정
      if (loadedCount === totalCount && markers.value.length > 0) {
        map.value.setBounds(bounds)
      }
    })
  })
}

// 관광지 변경 시 마커 업데이트
watch(() => props.attractions, () => {
  if (map.value && kakaoSdkLoaded.value) {
    addMarkers()
  }
}, { deep: true })

onMounted(async () => {
  try {
    await loadKakaoMapSDK()
    initMap()
  } catch (error) {
    console.error('지도 로드 오류:', error)
  }
})

onBeforeUnmount(() => {
  // 마커 정리
  markers.value.forEach(marker => marker.setMap(null))
  markers.value = []
})
</script>

<template>
  <div class="itinerary-map-container">
    <div v-if="mapError" class="map-error">
      <p>{{ mapError }}</p>
      <small>카카오맵 API 키를 확인해주세요.</small>
    </div>
    <div v-else ref="mapContainer" class="map-container"></div>
    <div v-if="!kakaoSdkLoaded && !mapError" class="map-loading">
      <p>지도를 불러오는 중...</p>
    </div>
  </div>
</template>

<style scoped>
.itinerary-map-container {
  width: 100%;
  height: 400px;
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  margin-top: 1rem;
}

.map-container {
  width: 100%;
  height: 100%;
}

.map-error {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  color: #dc3545;
  padding: 2rem;
  text-align: center;
}

.map-error small {
  display: block;
  margin-top: 0.5rem;
  color: #6c757d;
  font-size: 0.85rem;
}

.map-loading {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  color: #6c757d;
}

@media (max-width: 768px) {
  .itinerary-map-container {
    height: 300px;
  }
}
</style>

