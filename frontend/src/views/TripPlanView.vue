<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useTripStore } from '@/stores/trip'

const router = useRouter()
const tripStore = useTripStore()

const formData = ref({
  budget: 500000,
  people_count: 2,
  start_date: '',
  end_date: '',
  departure_location: '서울특별시',
  region: '서울특별시',
  travel_style: '관광',
  accommodation_type: 'hotel',
})

// 지역 옵션 (실제 tourism_data 기반)
const regions = [
  '서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시',
  '대전광역시', '울산광역시', '세종특별자치시',
  '경기도', '강원특별자치도', '충청북도', '충청남도',
  '전북특별자치도', '전라남도', '경상북도', '경상남도', '제주특별자치도'
]

// 여행 스타일 옵션
const travelStyles = [
  { value: '관광', label: '🏛️ 관광', desc: '명소 탐방' },
  { value: '힐링', label: '🌿 힐링', desc: '휴식과 재충전' },
  { value: '맛집투어', label: '🍴 맛집투어', desc: '음식 탐방' },
  { value: '문화체험', label: '🎭 문화체험', desc: '박물관, 공연' },
  { value: '자연탐방', label: '⛰️ 자연탐방', desc: '산, 바다, 계곡' },
  { value: '쇼핑', label: '🛍️ 쇼핑', desc: '쇼핑 중심' },
]

// 숙박 타입 옵션
const accommodationTypes = [
  { value: 'hotel', label: '🏨 호텔', desc: '고급 호텔' },
  { value: 'motel', label: '🏩 모텔', desc: '편안한 숙박' },
  { value: 'pension', label: '🏡 펜션', desc: '자연 속 휴식' },
  { value: 'guesthouse', label: '🏠 게스트하우스', desc: '저렴한 숙박' },
]

const loading = ref(false)
const error = ref('')

const handleSubmit = async () => {
  try {
    loading.value = true
    error.value = ''
    const result = await tripStore.generatePlan(formData.value)
    router.push({ name: 'itinerary', params: { id: result.id } })
  } catch (err) {
    error.value = err.response?.data?.error || '여행 계획 생성에 실패했습니다.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="trip-plan-view">
    <h1>AI 여행 계획 생성</h1>

    <div class="info-notice">
      <span class="notice-icon">ℹ️</span>
      <p>AI가 생성하는 예상 금액은 참고용이며 실제와 다를 수 있습니다. 실제 예약 전 반드시 확인해주세요.</p>
    </div>

    <div v-if="error" class="error-message">{{ error }}</div>

    <form @submit.prevent="handleSubmit" class="plan-form">
      <div class="form-row">
        <div class="form-group">
          <label>예산 (원)</label>
          <input v-model.number="formData.budget" type="number" min="0" step="10000" required />
          <span class="helper-text">총 예산을 입력하세요</span>
        </div>
        <div class="form-group">
          <label>인원 (명)</label>
          <input v-model.number="formData.people_count" type="number" min="1" max="20" required />
          <span class="helper-text">여행 인원수</span>
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label>시작일</label>
          <input v-model="formData.start_date" type="date" required />
        </div>
        <div class="form-group">
          <label>종료일</label>
          <input v-model="formData.end_date" type="date" required />
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label>출발지</label>
          <select v-model="formData.departure_location" required class="region-select">
            <option v-for="region in regions" :key="region" :value="region">
              {{ region }}
            </option>
          </select>
          <span class="helper-text">여행을 시작하는 지역</span>
        </div>
        <div class="form-group">
          <label>여행 지역</label>
          <select v-model="formData.region" required class="region-select">
            <option v-for="region in regions" :key="region" :value="region">
              {{ region }}
            </option>
          </select>
          <span class="helper-text">여행할 목적지</span>
        </div>
      </div>

      <div class="form-group">
        <label>여행 스타일</label>
        <div class="toggle-group">
          <button
            v-for="style in travelStyles"
            :key="style.value"
            type="button"
            class="toggle-btn"
            :class="{ active: formData.travel_style === style.value }"
            @click="formData.travel_style = style.value"
          >
            <div class="toggle-label">{{ style.label }}</div>
            <div class="toggle-desc">{{ style.desc }}</div>
          </button>
        </div>
      </div>

      <div class="form-group">
        <label>숙박 타입</label>
        <div class="toggle-group">
          <button
            v-for="type in accommodationTypes"
            :key="type.value"
            type="button"
            class="toggle-btn"
            :class="{ active: formData.accommodation_type === type.value }"
            @click="formData.accommodation_type = type.value"
          >
            <div class="toggle-label">{{ type.label }}</div>
            <div class="toggle-desc">{{ type.desc }}</div>
          </button>
        </div>
      </div>

      <button type="submit" class="btn-primary" :disabled="loading">
        {{ loading ? '생성 중...' : 'AI 여행 코스 생성' }}
      </button>
    </form>
  </div>
</template>

<style scoped>
.trip-plan-view {
  max-width: 700px;
  margin: 0 auto;
  padding: 1rem;
}

h1 {
  margin-bottom: 1.5rem;
  text-align: center;
}

.info-notice {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
  border-left: 4px solid #2196f3;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 4px rgba(33, 150, 243, 0.1);
}

.notice-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.info-notice p {
  margin: 0;
  color: #1565c0;
  font-size: 0.95rem;
  line-height: 1.5;
}

.error-message {
  padding: 1rem;
  background-color: #ffe6e6;
  color: #c00;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.plan-form {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.75rem;
  font-weight: 600;
  font-size: 1.05rem;
  color: #2c3e50;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #3498db;
}

.helper-text {
  display: block;
  margin-top: 0.25rem;
  font-size: 0.85rem;
  color: #666;
}

.region-select {
  cursor: pointer;
}

/* 토글 버튼 스타일 */
.toggle-group {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 0.75rem;
}

.toggle-btn {
  padding: 1rem;
  background: #f8f9fa;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
}

.toggle-btn:hover {
  background: #e9ecef;
  border-color: #3498db;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(52, 152, 219, 0.2);
}

.toggle-btn.active {
  background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
  border-color: #2980b9;
  color: white;
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.4);
}

.toggle-label {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.toggle-desc {
  font-size: 0.85rem;
  opacity: 0.8;
}

.toggle-btn.active .toggle-desc {
  opacity: 0.95;
}

.btn-primary {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 1.1rem;
  font-weight: bold;
  transition: all 0.3s;
  margin-top: 1rem;
}

.btn-primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #2980b9 0%, #21618c 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(52, 152, 219, 0.4);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* 반응형 */
@media (max-width: 768px) {
  .trip-plan-view {
    padding: 0.5rem;
  }

  .plan-form {
    padding: 1.5rem;
  }

  .toggle-group {
    grid-template-columns: 1fr 1fr;
  }

  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
