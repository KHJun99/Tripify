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
    <!-- 헤더 섹션 -->
    <div class="header-section">
      <div class="header-background"></div>
      <div class="header-overlay"></div>
      <div class="header-content">
        <h1>
          <span class="header-icon">✈️</span>
          AI 여행 계획 생성
        </h1>
        <p class="header-subtitle">원하는 조건을 입력하면 AI가 맞춤 여행 코스를 만들어드립니다</p>
        <div class="header-decoration">
          <div class="decoration-item"></div>
          <div class="decoration-item"></div>
          <div class="decoration-item"></div>
        </div>
      </div>
    </div>

    <!-- 안내 메시지 -->
    <div class="info-notice">
      <span class="notice-icon">💡</span>
      <p>AI가 생성하는 예상 금액은 참고용이며 실제와 다를 수 있습니다. 실제 예약 전 반드시 확인해주세요.</p>
    </div>

    <!-- 에러 메시지 -->
    <div v-if="error" class="error-message">
      <span class="error-icon">⚠️</span>
      {{ error }}
    </div>

    <!-- 폼 섹션 -->
    <form @submit.prevent="handleSubmit" class="plan-form">
      <!-- 기본 정보 카드 -->
      <div class="form-card card-basic">
        <div class="card-background"></div>
        <div class="card-content">
          <div class="card-header">
            <span class="card-icon">💰</span>
            <h2>기본 정보</h2>
          </div>
        <div class="form-row">
          <div class="form-group">
            <label>
              <span class="label-icon">💰</span>
              예산 (원)
            </label>
            <div class="input-wrapper">
              <input 
                v-model.number="formData.budget" 
                type="number" 
                min="0" 
                step="10000" 
                required 
                placeholder="예: 500000"
              />
              <span class="input-suffix">원</span>
            </div>
            <span class="helper-text">총 예산을 입력하세요</span>
          </div>
          <div class="form-group">
            <label>
              <span class="label-icon">👥</span>
              인원 (명)
            </label>
            <div class="input-wrapper">
              <input 
                v-model.number="formData.people_count" 
                type="number" 
                min="1" 
                max="20" 
                required 
                placeholder="예: 2"
              />
              <span class="input-suffix">명</span>
            </div>
            <span class="helper-text">여행 인원수</span>
          </div>
        </div>
        </div>
      </div>

      <!-- 날짜 정보 카드 -->
      <div class="form-card card-date">
        <div class="card-background"></div>
        <div class="card-content">
          <div class="card-header">
            <span class="card-icon">📅</span>
            <h2>여행 기간</h2>
          </div>
        <div class="form-row">
          <div class="form-group">
            <label>
              <span class="label-icon">🛫</span>
              시작일
            </label>
            <input v-model="formData.start_date" type="date" required />
          </div>
          <div class="form-group">
            <label>
              <span class="label-icon">🛬</span>
              종료일
            </label>
            <input v-model="formData.end_date" type="date" required />
          </div>
        </div>
        </div>
      </div>

      <!-- 지역 정보 카드 -->
      <div class="form-card card-location">
        <div class="card-background"></div>
        <div class="card-content">
          <div class="card-header">
            <span class="card-icon">🗺️</span>
            <h2>여행 지역</h2>
          </div>
        <div class="form-row">
          <div class="form-group">
            <label>
              <span class="label-icon">📍</span>
              출발지
            </label>
            <div class="select-wrapper">
              <select v-model="formData.departure_location" required>
                <option v-for="region in regions" :key="region" :value="region">
                  {{ region }}
                </option>
              </select>
            </div>
            <span class="helper-text">여행을 시작하는 지역</span>
          </div>
          <div class="form-group">
            <label>
              <span class="label-icon">🎯</span>
              여행 지역
            </label>
            <div class="select-wrapper">
              <select v-model="formData.region" required>
                <option v-for="region in regions" :key="region" :value="region">
                  {{ region }}
                </option>
              </select>
            </div>
            <span class="helper-text">여행할 목적지</span>
          </div>
        </div>
        </div>
      </div>

      <!-- 여행 스타일 카드 -->
      <div class="form-card card-style">
        <div class="card-background"></div>
        <div class="card-content">
          <div class="card-header">
            <span class="card-icon">🎨</span>
            <h2>여행 스타일</h2>
          </div>
        <div class="toggle-group">
          <button
            v-for="style in travelStyles"
            :key="style.value"
            type="button"
            class="toggle-btn"
            :class="{ active: formData.travel_style === style.value }"
            @click="formData.travel_style = style.value"
          >
            <div class="toggle-icon">{{ style.label.split(' ')[0] }}</div>
            <div class="toggle-label">{{ style.label.split(' ')[1] }}</div>
            <div class="toggle-desc">{{ style.desc }}</div>
          </button>
        </div>
        </div>
      </div>

      <!-- 숙박 타입 카드 -->
      <div class="form-card card-accommodation">
        <div class="card-background"></div>
        <div class="card-content">
          <div class="card-header">
            <span class="card-icon">🏨</span>
            <h2>숙박 타입</h2>
          </div>
        <div class="toggle-group">
          <button
            v-for="type in accommodationTypes"
            :key="type.value"
            type="button"
            class="toggle-btn accommodation-btn"
            :class="{ active: formData.accommodation_type === type.value }"
            @click="formData.accommodation_type = type.value"
          >
            <div class="toggle-icon">{{ type.label.split(' ')[0] }}</div>
            <div class="toggle-label">{{ type.label.split(' ')[1] }}</div>
            <div class="toggle-desc">{{ type.desc }}</div>
          </button>
        </div>
        </div>
      </div>

      <!-- 제출 버튼 -->
      <button type="submit" class="btn-primary" :disabled="loading">
        <span v-if="loading" class="btn-loading">
          <span class="spinner"></span>
          생성 중...
        </span>
        <span v-else class="btn-content">
          <span class="btn-icon">✨</span>
          AI 여행 코스 생성하기
        </span>
      </button>
    </form>
  </div>
</template>

<style scoped>
.trip-plan-view {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem 1rem;
  background: linear-gradient(to bottom, #e8f4f8 0%, #f0f8ff 50%, #ffffff 100%);
  min-height: 100vh;
  position: relative;
}

.trip-plan-view::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    radial-gradient(circle at 20% 50%, rgba(30, 144, 255, 0.05) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(0, 191, 255, 0.05) 0%, transparent 50%);
  pointer-events: none;
  z-index: 0;
}

/* 헤더 섹션 */
.header-section {
  border-radius: 24px;
  padding: 4rem 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  position: relative;
  overflow: hidden;
  min-height: 280px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.header-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    url('https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=1200&q=80'),
    linear-gradient(135deg, rgba(30, 144, 255, 0.9) 0%, rgba(0, 191, 255, 0.9) 100%);
  background-size: cover;
  background-position: center;
  background-blend-mode: overlay;
  opacity: 0.95;
}

.header-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(30, 144, 255, 0.85) 0%, rgba(0, 191, 255, 0.85) 100%);
  z-index: 1;
}

.header-section::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.15) 0%, transparent 70%);
  animation: pulse 4s ease-in-out infinite;
  z-index: 2;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.1); opacity: 0.8; }
}

.header-content {
  position: relative;
  z-index: 3;
  text-align: center;
  color: white;
}

.header-icon {
  font-size: 4rem;
  display: block;
  margin-bottom: 0.5rem;
  animation: float 3s ease-in-out infinite;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
}

.header-decoration {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 2rem;
}

.decoration-item {
  width: 8px;
  height: 8px;
  background: white;
  border-radius: 50%;
  opacity: 0.7;
  animation: blink 2s ease-in-out infinite;
}

.decoration-item:nth-child(2) {
  animation-delay: 0.3s;
}

.decoration-item:nth-child(3) {
  animation-delay: 0.6s;
}

@keyframes blink {
  0%, 100% { opacity: 0.3; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.2); }
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

h1 {
  font-size: 2.5rem;
  font-weight: 800;
  margin: 0 0 0.5rem 0;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.header-subtitle {
  font-size: 1.1rem;
  opacity: 0.95;
  margin: 0;
  font-weight: 300;
}

/* 안내 메시지 */
.info-notice {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1.25rem 1.5rem;
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
  border-left: 4px solid #2196f3;
  border-radius: 12px;
  margin-bottom: 2rem;
  box-shadow: 0 4px 12px rgba(33, 150, 243, 0.15);
  animation: slideIn 0.5s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.notice-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
  margin-top: 0.1rem;
}

.info-notice p {
  margin: 0;
  color: #1565c0;
  font-size: 0.95rem;
  line-height: 1.6;
  font-weight: 500;
}

/* 에러 메시지 */
.error-message {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1.25rem 1.5rem;
  background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
  color: #c62828;
  border-radius: 12px;
  margin-bottom: 2rem;
  border-left: 4px solid #c62828;
  box-shadow: 0 4px 12px rgba(198, 40, 40, 0.15);
  font-weight: 500;
}

.error-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

/* 폼 스타일 */
.plan-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-card {
  background: white;
  padding: 0;
  border-radius: 20px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.8);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(10px);
}

.form-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, #1e90ff 0%, #00bfff 50%, #1e90ff 100%);
  background-size: 200% 100%;
  animation: shimmer 3s linear infinite;
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

.card-background {
  position: absolute;
  top: 0;
  right: 0;
  width: 40%;
  height: 100%;
  opacity: 0.05;
  background-size: cover;
  background-position: center;
  pointer-events: none;
}

.card-basic .card-background {
  background-image: url('https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=800&q=80');
}

.card-date .card-background {
  background-image: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80');
}

.card-location .card-background {
  background-image: url('https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=800&q=80');
}

.card-style .card-background {
  background-image: url('https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=800&q=80');
}

.card-accommodation .card-background {
  background-image: url('https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80');
}

.card-content {
  position: relative;
  z-index: 1;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
}

.form-card:hover {
  box-shadow: 0 12px 40px rgba(30, 144, 255, 0.2);
  transform: translateY(-4px) scale(1.01);
}

.form-card:hover .card-background {
  opacity: 0.08;
  transform: scale(1.1);
  transition: all 0.4s ease;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid rgba(102, 126, 234, 0.1);
  position: relative;
}

.card-header::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 60px;
  height: 2px;
  background: linear-gradient(90deg, #1e90ff 0%, #00bfff 100%);
  border-radius: 2px;
}

.card-icon {
  font-size: 1.8rem;
  filter: drop-shadow(0 2px 4px rgba(30, 144, 255, 0.2));
}

.card-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #1e90ff 0%, #00bfff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group:last-child {
  margin-bottom: 0;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.form-group label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  font-weight: 600;
  font-size: 1rem;
  color: #2c3e50;
}

.label-icon {
  font-size: 1.2rem;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-wrapper input {
  flex: 1;
  padding-right: 3rem;
}

.input-suffix {
  position: absolute;
  right: 1rem;
  color: #6c757d;
  font-size: 0.9rem;
  font-weight: 500;
  pointer-events: none;
}

.form-group input,
.select-wrapper select {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: white;
  color: #2c3e50;
}

.select-wrapper {
  position: relative;
}

.select-wrapper::after {
  content: '▼';
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #6c757d;
  pointer-events: none;
  font-size: 0.75rem;
}

.select-wrapper select {
  appearance: none;
  cursor: pointer;
  padding-right: 2.5rem;
}

.form-group input:focus,
.select-wrapper select:focus {
  outline: none;
  border-color: #1e90ff;
  box-shadow: 0 0 0 3px rgba(30, 144, 255, 0.1);
  transform: translateY(-1px);
}

.helper-text {
  display: block;
  margin-top: 0.5rem;
  font-size: 0.85rem;
  color: #6c757d;
  font-weight: 400;
}

/* 토글 버튼 스타일 */
.toggle-group {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 1rem;
}

.toggle-btn {
  padding: 1.25rem 1rem;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  border: 2px solid #e0e0e0;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  text-align: center;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(10px);
}

.toggle-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s;
}

.toggle-btn:hover::before {
  left: 100%;
}

.toggle-btn:hover {
  border-color: #1e90ff;
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(30, 144, 255, 0.2);
}

.toggle-btn.active {
  background: linear-gradient(135deg, #1e90ff 0%, #00bfff 100%);
  border-color: #1e90ff;
  color: white;
  box-shadow: 
    0 8px 25px rgba(30, 144, 255, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  transform: translateY(-3px) scale(1.05);
}

.toggle-btn.active::after {
  content: '✓';
  position: absolute;
  top: 8px;
  right: 8px;
  width: 24px;
  height: 24px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: bold;
  animation: checkIn 0.3s ease-out;
}

@keyframes checkIn {
  from {
    transform: scale(0) rotate(-180deg);
    opacity: 0;
  }
  to {
    transform: scale(1) rotate(0deg);
    opacity: 1;
  }
}

.toggle-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  display: block;
}

.toggle-label {
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
  display: block;
}

.toggle-desc {
  font-size: 0.8rem;
  opacity: 0.7;
  font-weight: 400;
}

.toggle-btn.active .toggle-desc {
  opacity: 0.9;
}

/* 제출 버튼 */
.btn-primary {
  width: 100%;
  padding: 1.5rem 2rem;
  background: linear-gradient(135deg, #1e90ff 0%, #00bfff 100%);
  color: white;
  border: none;
  border-radius: 16px;
  cursor: pointer;
  font-size: 1.3rem;
  font-weight: 700;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  margin-top: 2rem;
  box-shadow: 
    0 10px 30px rgba(30, 144, 255, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  position: relative;
  overflow: hidden;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.btn-primary::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.btn-primary:hover:not(:disabled)::before {
  width: 300px;
  height: 300px;
}

.btn-primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #00bfff 0%, #1e90ff 100%);
  transform: translateY(-3px);
  box-shadow: 0 12px 35px rgba(30, 144, 255, 0.4);
}

.btn-primary:active:not(:disabled) {
  transform: translateY(-1px);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.btn-content,
.btn-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  position: relative;
  z-index: 1;
}

.btn-icon {
  font-size: 1.3rem;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 반응형 */
@media (max-width: 768px) {
  .trip-plan-view {
    padding: 1rem 0.5rem;
  }

  .header-section {
    padding: 2rem 1.5rem;
    border-radius: 16px;
  }

  h1 {
    font-size: 2rem;
  }

  .header-subtitle {
    font-size: 0.95rem;
  }

  .form-card {
    padding: 1.5rem;
  }

  .card-header h2 {
    font-size: 1.2rem;
  }

  .toggle-group {
    grid-template-columns: 1fr 1fr;
    gap: 0.75rem;
  }

  .toggle-btn {
    padding: 1rem 0.75rem;
  }

  .toggle-icon {
    font-size: 1.5rem;
  }

  .form-row {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .btn-primary {
    padding: 1rem 1.5rem;
    font-size: 1.1rem;
  }
}

@media (max-width: 480px) {
  .toggle-group {
    grid-template-columns: 1fr;
  }
}
</style>
