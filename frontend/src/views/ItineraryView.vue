<script setup>
import { onMounted, computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useTripStore } from '@/stores/trip'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const tripStore = useTripStore()
const authStore = useAuthStore()

const showReviewModal = ref(false)
const review = ref('')
const rating = ref(5)
const isSubmitting = ref(false)
const reviewError = ref('')

// 계획 수정 관련
const showModifyModal = ref(false)
const requirements = ref('')
const isModifying = ref(false)
const modifyError = ref('')

// 숙박 타입 한글 변환
const getAccommodationTypeLabel = (type) => {
  const labels = {
    'hotel': '호텔',
    'motel': '모텔',
    'pension': '펜션',
    'guesthouse': '게스트하우스'
  }
  return labels[type] || type
}

// 총 예상 비용 계산
const totalEstimatedCost = computed(() => {
  if (!tripStore.currentPlan?.itineraries) return 0
  return tripStore.currentPlan.itineraries.reduce((sum, itinerary) => {
    return sum + (itinerary.estimated_cost || 0)
  }, 0)
})


const isOwner = computed(() => {
  if (!tripStore.currentPlan || !authStore.user) {
    return false
  }
  
  // user_id로 비교 (가장 정확한 방법)
  if (tripStore.currentPlan.user_id && authStore.user.id) {
    return tripStore.currentPlan.user_id === authStore.user.id
  }
  
  // user_id가 없으면 username으로 fallback
  const planUser = typeof tripStore.currentPlan.user === 'string' 
    ? tripStore.currentPlan.user 
    : tripStore.currentPlan.user?.username || tripStore.currentPlan.user
  
  const currentUser = authStore.user.username || authStore.user
  
  return planUser === currentUser
})

const handleRecommend = () => {
  if (!tripStore.currentPlan.is_recommended) {
    showReviewModal.value = true
    review.value = tripStore.currentPlan.review || ''
    rating.value = tripStore.currentPlan.rating || 5
  } else {
    handleUnrecommend()
  }
}

const handleUnrecommend = async () => {
  if (!confirm('추천을 취소하시겠습니까?')) return
  
  try {
    console.log('추천 취소 시작 - Plan ID:', tripStore.currentPlan.id)
    const result = await tripStore.unrecommendPlan(tripStore.currentPlan.id)
    console.log('추천 취소 성공:', result)
    // 성공 메시지
    alert('추천이 취소되었습니다.')
  } catch (error) {
    console.error('추천 취소 오류 상세:', {
      message: error.message,
      response: error.response,
      status: error.response?.status,
      data: error.response?.data
    })
    const errorMessage = error.response?.data?.error || error.message || '추천 취소 중 오류가 발생했습니다.'
    alert(errorMessage)
  }
}

const submitReview = async () => {
  if (!review.value.trim()) {
    reviewError.value = '후기를 입력해주세요.'
    return
  }
  
  if (review.value.trim().length > 2000) {
    reviewError.value = '후기는 2000자 이하여야 합니다.'
    return
  }
  
  isSubmitting.value = true
  reviewError.value = ''
  
  try {
    await tripStore.recommendPlan(tripStore.currentPlan.id, {
      review: review.value.trim(),
      rating: rating.value
    })
    showReviewModal.value = false
    review.value = ''
    rating.value = 5
  } catch (error) {
    reviewError.value = error.response?.data?.error || '후기 작성 중 오류가 발생했습니다.'
  } finally {
    isSubmitting.value = false
  }
}

const closeReviewModal = () => {
  showReviewModal.value = false
  review.value = ''
  rating.value = 5
  reviewError.value = ''
}

const handleModify = () => {
  showModifyModal.value = true
  requirements.value = ''
  modifyError.value = ''
}

const closeModifyModal = () => {
  showModifyModal.value = false
  requirements.value = ''
  modifyError.value = ''
}

const submitModify = async () => {
  if (!requirements.value.trim()) {
    modifyError.value = '수정 요구사항을 입력해주세요.'
    return
  }
  
  if (requirements.value.trim().length > 2000) {
    modifyError.value = '요구사항은 2000자 이하여야 합니다.'
    return
  }
  
  if (!confirm('계획을 수정하시겠습니까? 기존 일정이 삭제되고 새로운 일정으로 대체됩니다.')) {
    return
  }
  
  isModifying.value = true
  modifyError.value = ''
  
  try {
    console.log('계획 수정 시작 - Plan ID:', tripStore.currentPlan.id)
    await tripStore.modifyPlan(tripStore.currentPlan.id, requirements.value.trim())
    console.log('계획 수정 성공')
    showModifyModal.value = false
    requirements.value = ''
    alert('계획이 성공적으로 수정되었습니다!')
  } catch (error) {
    console.error('계획 수정 오류 상세:', {
      message: error.message,
      response: error.response,
      status: error.response?.status,
      data: error.response?.data
    })
    modifyError.value = error.response?.data?.error || error.message || '계획 수정 중 오류가 발생했습니다.'
  } finally {
    isModifying.value = false
  }
}

const error = ref('')

onMounted(async () => {
  const id = route.params.id
  
  // 사용자 정보가 없으면 로드
  if (!authStore.user && authStore.isAuthenticated) {
    try {
      await authStore.getProfile()
    } catch (error) {
      console.error('프로필 로드 실패:', error)
    }
  }
  
  try {
    await tripStore.fetchPlan(id)
  } catch (err) {
    console.error('여행 계획 로드 실패:', err)
    if (err.response?.status === 404) {
      error.value = '여행 계획을 찾을 수 없습니다.'
    } else if (err.response?.status === 403) {
      error.value = '이 여행 계획에 접근할 수 없습니다.'
    } else {
      error.value = '여행 계획을 불러오는 중 오류가 발생했습니다.'
    }
  }
})
</script>

<template>
  <div class="itinerary-view">
    <div v-if="tripStore.loading" class="loading">로딩 중...</div>

    <div v-else-if="error" class="error-message-container">
      <div class="error-message-box">
        <h2>⚠️ 오류</h2>
        <p>{{ error }}</p>
        <button @click="$router.push('/recommended')" class="btn-back">추천된 여행지로 돌아가기</button>
      </div>
    </div>

    <div v-else-if="tripStore.currentPlan" class="itinerary-content">
      <div class="header-section">
        <h1>{{ tripStore.currentPlan.title }}</h1>
        <div v-if="isOwner" class="action-buttons">
          <button 
            @click="handleModify" 
            class="btn-modify"
            :disabled="tripStore.loading || isModifying"
          >
            ✏️ 계획 수정
          </button>
          <div class="recommend-section">
            <button 
              v-if="!tripStore.currentPlan.is_recommended"
              @click="handleRecommend" 
              class="btn-recommend"
            >
              ⭐ 추천하기
            </button>
            <button 
              v-else
              @click="handleUnrecommend" 
              class="btn-recommended"
            >
              ⭐ 추천됨
            </button>
          </div>
        </div>
      </div>

      <div class="price-notice">
        <span class="notice-icon">💡</span>
        <p>표시된 예상 금액은 AI가 추정한 참고 가격입니다. 실제 예약 전 반드시 정확한 가격을 확인해주세요.</p>
      </div>

      <div class="trip-details">
        <div class="detail-grid">
          <div class="detail-item">
            <span class="detail-label">📍 출발지</span>
            <span class="detail-value">{{ tripStore.currentPlan.departure_location }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">🎯 여행 지역</span>
            <span class="detail-value">{{ tripStore.currentPlan.region }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">📅 기간</span>
            <span class="detail-value">{{ tripStore.currentPlan.start_date }} ~ {{ tripStore.currentPlan.end_date }}</span>
          </div>
          <div class="detail-item highlight">
            <span class="detail-label">💰 총 예산</span>
            <span class="detail-value">{{ tripStore.currentPlan.budget.toLocaleString() }}원</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">👥 인원</span>
            <span class="detail-value">{{ tripStore.currentPlan.people_count }}명 (1인당 약 {{ Math.floor(tripStore.currentPlan.budget / tripStore.currentPlan.people_count).toLocaleString() }}원)</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">🎨 스타일</span>
            <span class="detail-value">{{ tripStore.currentPlan.travel_style }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">🏨 숙박</span>
            <span class="detail-value">{{ getAccommodationTypeLabel(tripStore.currentPlan.accommodation_type) }}</span>
          </div>
        </div>
      </div>

      <div v-if="tripStore.currentPlan.itineraries && tripStore.currentPlan.itineraries.length > 0" class="itineraries">
        <h2 class="section-title">📋 여행 일정</h2>
        <div v-for="itinerary in tripStore.currentPlan.itineraries" :key="itinerary.id" class="itinerary-day">
          <div class="day-header">
            <div class="day-badge">Day {{ itinerary.day_number }}</div>
            <h3>{{ itinerary.day_number }}일차 - {{ itinerary.date }}</h3>
          </div>
          <p class="day-description">{{ itinerary.description }}</p>

          <!-- 관광지 정보 -->
          <div v-if="itinerary.attractions && itinerary.attractions.length > 0" class="section">
            <h4>🏛️ 관광지</h4>
            <div v-for="(attraction, index) in itinerary.attractions" :key="index" class="attraction-item">
              <p class="attraction-name">{{ attraction.name }}</p>
              <p class="attraction-details">
                <span v-if="attraction.time">⏰ {{ attraction.time }}</span>
                <span v-if="attraction.duration">⏱️ {{ attraction.duration }}</span>
              </p>
              <p v-if="attraction.description" class="attraction-description">{{ attraction.description }}</p>
            </div>
          </div>

          <!-- 교통수단 정보 -->
          <div v-if="itinerary.transportation_info && Object.keys(itinerary.transportation_info).length > 0" class="section">
            <h4>🚌 교통수단</h4>
            <div v-for="(info, time) in itinerary.transportation_info" :key="time" class="info-item">
              <p><strong>{{ time }}:</strong> {{ info }}</p>
            </div>
          </div>

          <!-- 숙소 정보 -->
          <div v-if="itinerary.accommodation_info && Object.keys(itinerary.accommodation_info).length > 0" class="section">
            <h4>🏨 숙소</h4>
            <p v-if="itinerary.accommodation_info.name" class="info-item">
              <strong>숙소:</strong> {{ itinerary.accommodation_info.name }}
            </p>
            <p v-if="itinerary.accommodation_info.cost" class="info-item">
              <strong>비용:</strong> {{ itinerary.accommodation_info.cost.toLocaleString() }}원
            </p>
            <p v-if="itinerary.accommodation_info.check_in" class="info-item">
              <strong>체크인:</strong> {{ itinerary.accommodation_info.check_in }} /
              <strong>체크아웃:</strong> {{ itinerary.accommodation_info.check_out }}
            </p>
          </div>

          <!-- 식사 정보 -->
          <div v-if="itinerary.meals_info && Object.keys(itinerary.meals_info).length > 0" class="section">
            <h4>🍽️ 식사</h4>
            <div v-for="(meal, time) in itinerary.meals_info" :key="time" class="meal-item">
              <p>
                <strong>{{ time }}:</strong>
                {{ typeof meal === 'string' ? meal : meal.restaurant }}
                <span v-if="typeof meal === 'object' && meal.cost">
                  ({{ meal.cost.toLocaleString() }}원)
                </span>
              </p>
            </div>
          </div>

          <!-- 축제/행사 정보 -->
          <div v-if="itinerary.events_info && itinerary.events_info.length > 0" class="section">
            <h4>🎉 축제/행사</h4>
            <div v-for="(event, index) in itinerary.events_info" :key="index" class="event-item">
              <p class="event-name">{{ event.name }}</p>
              <p v-if="event.time" class="event-details">⏰ {{ event.time }}</p>
              <p v-if="event.location" class="event-details">📍 {{ event.location }}</p>
              <p v-if="event.description" class="event-description">{{ event.description }}</p>
            </div>
          </div>

          <!-- 예상 비용 -->
          <div v-if="itinerary.estimated_cost" class="estimated-cost">
            <p><strong>💰 예상 비용:</strong> {{ itinerary.estimated_cost.toLocaleString() }}원</p>
          </div>
        </div>

        <!-- 총 예상 비용 -->
        <div v-if="totalEstimatedCost > 0" class="total-cost-summary">
          <div class="total-cost-content">
            <h3>💰 총 예상 비용</h3>
            <p class="total-cost-amount">{{ totalEstimatedCost.toLocaleString() }}원</p>
            <p class="total-cost-budget">
              예산: {{ tripStore.currentPlan.budget.toLocaleString() }}원
              <span class="cost-difference" :class="totalEstimatedCost > tripStore.currentPlan.budget ? 'over-budget' : 'within-budget'">
                ({{ totalEstimatedCost > tripStore.currentPlan.budget ? '+' : '' }}{{ (totalEstimatedCost - tripStore.currentPlan.budget).toLocaleString() }}원)
              </span>
            </p>
          </div>
        </div>
      </div>

      <div v-else class="empty-itinerary">
        <p>아직 일정이 추가되지 않았습니다.</p>
      </div>
    </div>

    <!-- 계획 수정 모달 -->
    <div v-if="showModifyModal" class="modal-overlay" @click.self="closeModifyModal">
      <div class="modal-content modify-modal">
        <h2>여행 계획 수정</h2>
        <p class="modal-subtitle">수정하고 싶은 요구사항을 자세히 작성해주세요. AI가 요구사항에 맞게 계획을 수정해드립니다.</p>
        
        <div class="modify-form">
          <div class="form-group">
            <label>수정 요구사항</label>
            <textarea
              v-model="requirements"
              placeholder="예: 2일차에 해변 관광지를 추가하고 싶어요. 저녁 식사는 해산물 요리로 변경해주세요. 예산을 조금 더 절약할 수 있도록 저렴한 숙소로 변경해주세요."
              rows="10"
              maxlength="2000"
              class="requirements-textarea"
            ></textarea>
            <div class="char-count">{{ requirements.length }} / 2000</div>
          </div>
          
          <div v-if="modifyError" class="error-message">{{ modifyError }}</div>
          
          <div class="modal-buttons">
            <button @click="closeModifyModal" class="btn-cancel" :disabled="isModifying">
              취소
            </button>
            <button @click="submitModify" class="btn-submit" :disabled="isModifying">
              {{ isModifying ? '수정 중...' : '수정하기' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 후기 작성 모달 -->
    <div v-if="showReviewModal" class="modal-overlay" @click.self="closeReviewModal">
      <div class="modal-content review-modal">
        <h2>여행 계획 추천하기</h2>
        <p class="modal-subtitle">다른 사용자들과 여행 경험을 공유해주세요!</p>
        
        <div class="review-form">
          <div class="form-group">
            <label>평점</label>
            <div class="rating-input">
              <button
                v-for="i in 5"
                :key="i"
                @click="rating = i"
                class="star-btn"
                :class="{ active: i <= rating }"
              >
                ⭐
              </button>
              <span class="rating-text">{{ rating }}점</span>
            </div>
          </div>
          
          <div class="form-group">
            <label>후기</label>
            <textarea
              v-model="review"
              placeholder="여행 경험을 자유롭게 작성해주세요..."
              rows="8"
              maxlength="2000"
              class="review-textarea"
            ></textarea>
            <div class="char-count">{{ review.length }} / 2000</div>
          </div>
          
          <div v-if="reviewError" class="error-message">{{ reviewError }}</div>
          
          <div class="modal-buttons">
            <button @click="closeReviewModal" class="btn-cancel" :disabled="isSubmitting">
              취소
            </button>
            <button @click="submitReview" class="btn-submit" :disabled="isSubmitting">
              {{ isSubmitting ? '제출 중...' : '추천하기' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.itinerary-view {
  background: #f5f7fa;
  min-height: 100vh;
  padding: 2rem 1rem;
}

.itinerary-content {
  max-width: 1200px;
  margin: 0 auto;
}

.loading {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
  color: #666;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  gap: 1rem;
}

.action-buttons {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

h1 {
  margin: 0;
  font-size: 2rem;
  font-weight: 700;
  color: #1a1a1a;
  flex: 1;
}

.recommend-section {
  display: flex;
  gap: 0.5rem;
}

.btn-modify {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #1e90ff 0%, #00bfff 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
  box-shadow: 0 4px 12px rgba(30, 144, 255, 0.3);
}

.btn-modify:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(30, 144, 255, 0.4);
}

.btn-modify:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-recommend,
.btn-recommended {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.btn-recommend {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.btn-recommend:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

.btn-recommended {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(245, 87, 108, 0.3);
}

.btn-recommended:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(245, 87, 108, 0.4);
}

.price-notice {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  background: linear-gradient(135deg, #fff9e6 0%, #ffecb3 100%);
  border-left: 4px solid #ffa726;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 4px rgba(255, 167, 38, 0.1);
}

.notice-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.price-notice p {
  margin: 0;
  color: #e65100;
  font-size: 0.95rem;
  line-height: 1.5;
  font-weight: 500;
}

.trip-details {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  margin-bottom: 2rem;
  border: 1px solid #e8ecef;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 10px;
  border-left: 4px solid #3498db;
  transition: all 0.3s ease;
}

.detail-item:hover {
  background: #e9ecef;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.detail-item.highlight {
  background: linear-gradient(135deg, #fff5e6 0%, #ffe8cc 100%);
  border-left-color: #ff9800;
}

.detail-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #6c757d;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-value {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
}

.detail-item.highlight .detail-value {
  color: #e65100;
  font-size: 1.2rem;
}

.section-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 2rem;
  padding-bottom: 0.75rem;
  border-bottom: 3px solid #3498db;
}

.itinerary-day {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  margin-bottom: 2rem;
  border: 1px solid #e8ecef;
  transition: all 0.3s ease;
}

.itinerary-day:hover {
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

.day-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e8ecef;
}

.day-badge {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 700;
  font-size: 0.9rem;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.itinerary-day h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.6rem;
  font-weight: 700;
}

.day-description {
  color: #555;
  font-size: 1.05rem;
  line-height: 1.6;
  margin-bottom: 2rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 10px;
  border-left: 4px solid #3498db;
}

.section {
  margin-top: 1.5rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 12px;
  border: 1px solid #e8ecef;
}

.section h4 {
  margin-bottom: 1rem;
  color: #2c3e50;
  font-size: 1.3rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.attraction-item,
.event-item {
  margin-bottom: 1rem;
  padding: 1rem 1.25rem;
  background: white;
  border-radius: 10px;
  border-left: 4px solid #3498db;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
}

.attraction-item:hover,
.event-item:hover {
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.15);
  transform: translateX(4px);
}

.attraction-name,
.event-name {
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.attraction-details,
.event-details {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}

.attraction-details span {
  margin-right: 1rem;
}

.attraction-description,
.event-description {
  color: #555;
  font-size: 0.95rem;
  margin-top: 0.5rem;
}

.info-item,
.meal-item {
  margin-bottom: 0.75rem;
  padding: 0.75rem 1rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
}

.info-item strong,
.meal-item strong {
  color: #495057;
  font-weight: 600;
  margin-right: 0.5rem;
}

.estimated-cost {
  margin-top: 1.5rem;
  padding: 1.25rem;
  background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
  border-radius: 12px;
  text-align: right;
  border: 2px solid #4caf50;
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.2);
}

.estimated-cost p {
  color: #1b5e20;
  font-size: 1.2rem;
  font-weight: 700;
  margin: 0;
}

.empty-itinerary {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error-message-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
  padding: 2rem;
}

.error-message-box {
  background: white;
  padding: 3rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  text-align: center;
  max-width: 500px;
}

.error-message-box h2 {
  color: #dc3545;
  margin-bottom: 1rem;
  font-size: 1.8rem;
}

.error-message-box p {
  color: #6c757d;
  margin-bottom: 2rem;
  font-size: 1.1rem;
}

.btn-back {
  padding: 0.75rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-back:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

.total-cost-summary {
  margin-top: 2rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.total-cost-content {
  text-align: center;
  color: white;
}

.total-cost-content h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: white;
}

.total-cost-amount {
  margin: 0.5rem 0;
  font-size: 2rem;
  font-weight: bold;
  color: white;
}

.total-cost-budget {
  margin: 0.75rem 0 0 0;
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.9);
}

.cost-difference {
  font-weight: 600;
  margin-left: 0.5rem;
}

.cost-difference.within-budget {
  color: #a5d6a7;
}

.cost-difference.over-budget {
  color: #ffcdd2;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .itinerary-view {
    padding: 1rem 0.5rem;
  }

  h1 {
    font-size: 1.5rem;
  }

  .trip-details {
    padding: 1.5rem;
  }

  .detail-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .itinerary-day {
    padding: 1.5rem;
  }

  .day-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .section-title {
    font-size: 1.5rem;
  }

  .section {
    padding: 1rem;
  }

  .section h4 {
    font-size: 1.1rem;
  }
}

/* 스크롤 애니메이션 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.itinerary-day {
  animation: fadeInUp 0.5s ease-out;
}

.itinerary-day:nth-child(1) { animation-delay: 0.1s; }
.itinerary-day:nth-child(2) { animation-delay: 0.2s; }
.itinerary-day:nth-child(3) { animation-delay: 0.3s; }
.itinerary-day:nth-child(4) { animation-delay: 0.4s; }
.itinerary-day:nth-child(5) { animation-delay: 0.5s; }

/* 후기 작성 모달 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.review-modal {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  max-width: 600px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.review-modal h2 {
  margin: 0 0 0.5rem 0;
  color: #1a1a1a;
  font-size: 1.8rem;
}

.modal-subtitle {
  color: #6c757d;
  margin-bottom: 2rem;
  font-size: 0.95rem;
}

.review-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.form-group label {
  font-weight: 600;
  color: #2c3e50;
  font-size: 1rem;
}

.rating-input {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.star-btn {
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  padding: 0;
  transition: transform 0.2s ease;
  filter: grayscale(100%);
  opacity: 0.3;
}

.star-btn:hover {
  transform: scale(1.2);
}

.star-btn.active {
  filter: none;
  opacity: 1;
}

.rating-text {
  margin-left: 0.5rem;
  font-weight: 600;
  color: #667eea;
  font-size: 1.1rem;
}

.review-textarea,
.requirements-textarea {
  width: 100%;
  padding: 1rem;
  border: 2px solid #e8ecef;
  border-radius: 8px;
  font-size: 1rem;
  font-family: inherit;
  resize: vertical;
  transition: border-color 0.3s ease;
}

.review-textarea:focus,
.requirements-textarea:focus {
  outline: none;
  border-color: #1e90ff;
}

.char-count {
  text-align: right;
  color: #6c757d;
  font-size: 0.85rem;
}

.error-message {
  padding: 0.75rem;
  background: #ffebee;
  color: #c62828;
  border-radius: 8px;
  font-size: 0.9rem;
}

.modal-buttons {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1rem;
}

.btn-cancel,
.btn-submit {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-cancel {
  background: #e8ecef;
  color: #495057;
}

.btn-cancel:hover:not(:disabled) {
  background: #dee2e6;
}

.btn-submit {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

.btn-cancel:disabled,
.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.modify-modal {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  max-width: 700px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  animation: slideUp 0.3s ease;
}

.modify-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

@media (max-width: 768px) {
  .header-section {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .action-buttons {
    flex-direction: column;
    width: 100%;
    gap: 0.5rem;
  }
  
  .btn-modify,
  .btn-recommend,
  .btn-recommended {
    width: 100%;
  }
  
  h1 {
    font-size: 1.5rem;
  }
  
  .review-modal,
  .modify-modal {
    padding: 1.5rem;
  }
}
</style>
