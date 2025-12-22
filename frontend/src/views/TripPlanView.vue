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
  <div class="layout-container">
    <div class="static-bg-wrapper"></div>

    <div class="content-wrapper glass-card">
      
      <header class="header">
        <h1 class="title">New Trip</h1>
        <p class="desc">새로운 여행 계획을 생성합니다.</p>
      </header>

      <div v-if="error" class="error-message">{{ error }}</div>

      <form @submit.prevent="handleSubmit" class="form-grid">
        
        <div class="form-group">
          <label class="label">Schedule</label>
          <div class="row">
            <div class="input-wrap">
              <span class="sub-label">시작일</span>
              <input v-model="formData.start_date" type="date" required />
            </div>
            <div class="input-wrap">
              <span class="sub-label">종료일</span>
              <input v-model="formData.end_date" type="date" required />
            </div>
          </div>
        </div>

        <div class="form-group">
          <label class="label">Conditions</label>
          <div class="row">
            <div class="input-wrap">
              <span class="sub-label">인원</span>
              <input 
                v-model.number="formData.people_count" 
                type="number" 
                min="1" 
                max="20"
                required
                placeholder="2"
              />
            </div>
            <div class="input-wrap">
              <span class="sub-label">예산(KRW)</span>
              <input 
                v-model.number="formData.budget" 
                type="number"
                min="0"
                step="10000" 
                required
                placeholder="500000"
              />
            </div>
          </div>
        </div>

        <div class="form-group">
          <label class="label">Location</label>
          <div class="row">
            <div class="input-wrap">
              <span class="sub-label">출발</span>
              <select v-model="formData.departure_location" required>
                <option v-for="region in regions" :key="region" :value="region">{{ region }}</option>
              </select>
            </div>
            <div class="input-wrap">
              <span class="sub-label">도착</span>
              <select v-model="formData.region" required>
                <option v-for="region in regions" :key="region" :value="region">{{ region }}</option>
              </select>
            </div>
          </div>
        </div>

        <div class="form-group">
          <label class="label">Preferences</label>
          
          <div class="select-group">
            <span class="group-name">여행 스타일</span>
            <div class="button-grid">
              <button
                v-for="style in travelStyles"
                :key="style.value"
                type="button"
                class="select-btn"
                :class="{ active: formData.travel_style === style.value }"
                @click="formData.travel_style = style.value"
              >
                <span class="btn-emoji">{{ style.label.split(' ')[0] }}</span>
                <span class="btn-text">{{ style.label.split(' ')[1] }}</span>
              </button>
            </div>
          </div>

          <div class="select-group mt-4">
            <span class="group-name">숙소 유형</span>
            <div class="button-grid">
              <button
                v-for="type in accommodationTypes"
                :key="type.value"
                type="button"
                class="select-btn"
                :class="{ active: formData.accommodation_type === type.value }"
                @click="formData.accommodation_type = type.value"
              >
                <span class="btn-emoji">{{ type.label.split(' ')[0] }}</span>
                <span class="btn-text">{{ type.label.split(' ')[1] }}</span>
              </button>
            </div>
          </div>
        </div>

        <div class="action-area">
          <button type="submit" class="submit-btn" :disabled="loading">
            {{ loading ? 'Generating...' : '여행 계획 생성하기' }}
          </button>
        </div>

      </form>
    </div>
  </div>
</template>

<style scoped>
/* [폰트 적용] Pretendard CDN Import */
@import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css");

.layout-container {
  display: flex;
  justify-content: center;
  padding: 60px 20px;
  min-height: 100vh;
  color: #111;
  position: relative;
  
  /* [폰트 적용] Pretendard를 최우선으로 적용 */
  font-family: "Pretendard Variable", Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, "Helvetica Neue", "Segoe UI", "Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", sans-serif;
  letter-spacing: -0.02em;
}

.static-bg-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: -2;
  background-color: #f5f7fa;
  background-image: 
    radial-gradient(at 0% 0%, rgba(161, 196, 253, 0.5) 0px, transparent 50%),
    radial-gradient(at 100% 0%, rgba(255, 182, 193, 0.3) 0px, transparent 50%),
    radial-gradient(at 100% 100%, rgba(132, 250, 176, 0.4) 0px, transparent 50%),
    radial-gradient(at 0% 100%, rgba(194, 233, 251, 0.5) 0px, transparent 50%);
  background-attachment: fixed;
  background-size: cover;
  pointer-events: none;
}

.glass-card {
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.8);
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.04), 
    0 1px 2px rgba(0, 0, 0, 0.02);
  border-radius: 28px;
  padding: 48px;
}

.content-wrapper {
  width: 100%;
  max-width: 560px;
  position: relative;
  z-index: 1;
}

/* Header */
.header {
  margin-bottom: 40px;
  border-bottom: 1px solid rgba(0,0,0,0.06);
  padding-bottom: 24px;
}

.title {
  font-size: 36px;
  font-weight: 800;
  letter-spacing: -0.04em;
  margin: 0 0 6px 0;
  color: #1a1a1a;
  line-height: 1.1;
}

.desc {
  font-size: 16px;
  color: #6b7280;
  margin: 0;
  font-weight: 400;
  line-height: 1.5;
}

/* Form Layout */
.form-grid {
  display: flex;
  flex-direction: column;
  gap: 36px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* Section Label */
.label {
  font-size: 12px;
  font-weight: 700;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 4px;
}

/* Inputs Row */
.row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.input-wrap {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.sub-label {
  font-size: 13px;
  font-weight: 600;
  color: #4b5563;
  margin-left: 2px;
}

/* Input Styles */
input, select {
  width: 100%;
  height: 52px;
  padding: 0 16px;
  border: 1px solid transparent;
  border-radius: 12px; 
  font-size: 15px;
  font-weight: 500;
  font-family: inherit;
  color: #1f2937;
  background-color: rgba(255,255,255,0.6);
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  appearance: none;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}

input:hover, select:hover {
  background-color: rgba(255,255,255,0.9);
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

input:focus, select:focus {
  outline: none;
  background-color: #fff;
  border-color: #2563eb;
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1);
}

input::placeholder {
  color: #9ca3af;
  font-weight: 400;
}

/* Select preferences */
.select-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.mt-4 { margin-top: 12px; }

.group-name {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  margin-left: 2px;
}

.button-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

/* Button Styles */
.select-btn {
  padding: 10px 18px;
  font-size: 14px;
  font-weight: 500;
  font-family: inherit;
  color: #6b7280;
  background-color: rgba(255,255,255,0.5);
  border: 1px solid transparent;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}

.btn-emoji {
  font-size: 16px;
}

.btn-text {
  font-size: 14px;
}

.select-btn:hover {
  background-color: #fff;
  color: #111;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.select-btn.active {
  background-color: #111;
  color: #fff;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

/* Submit Button */
.action-area {
  margin-top: 12px;
  padding-top: 24px;
  border-top: 1px solid rgba(0,0,0,0.06);
}

.submit-btn {
  width: 100%;
  height: 60px;
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  color: #fff;
  font-size: 17px;
  font-weight: 700;
  font-family: inherit;
  letter-spacing: -0.01em;
  border: none;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(37, 99, 235, 0.35);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0);
}

.submit-btn:disabled {
  background: #cbd5e1;
  cursor: not-allowed;
  box-shadow: none;
  transform: none;
}

.error-message {
  color: #ef4444;
  font-size: 14px;
  margin-bottom: 24px;
  font-weight: 600;
  text-align: center;
  background-color: rgba(239, 68, 68, 0.1);
  padding: 12px;
  border-radius: 8px;
}

/* Mobile Responsive */
@media (max-width: 600px) {
  .layout-container {
    padding: 20px 16px;
  }
  
  .glass-card {
    padding: 32px 24px;
    border-radius: 24px;
  }

  .row {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .title {
    font-size: 28px;
  }
  
  .button-grid {
    grid-template-columns: 1fr 1fr;
  }
}
</style>