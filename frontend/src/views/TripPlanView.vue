<script setup>
  import { ref, onMounted } from 'vue'
  import { useRouter, useRoute } from 'vue-router'
  import { useTripStore } from '@/stores/trip'
  
  const router = useRouter()
  const route = useRoute()
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
  
  // URL query에서 검색어를 받아서 region에 설정
  onMounted(() => {
    if (route.query.search) {
      formData.value.region = route.query.search
    }
    // 예산 초기값 포맷팅
    budgetDisplay.value = formData.value.budget.toLocaleString('ko-KR')
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
    { value: '관광', label: '관광', desc: '명소 탐방' },
    { value: '힐링', label: '힐링', desc: '휴식과 재충전' },
    { value: '맛집투어', label: '맛집투어', desc: '음식 탐방' },
    { value: '문화체험', label: '문화체험', desc: '박물관, 공연' },
    { value: '자연탐방', label: '자연탐방', desc: '산, 바다, 계곡' },
    { value: '쇼핑', label: '쇼핑', desc: '쇼핑 중심' },
  ]
  
  // 숙박 타입 옵션
  const accommodationTypes = [
    { value: 'hotel', label: '호텔', desc: '고급 호텔' },
    { value: 'motel', label: '모텔', desc: '편안한 숙박' },
    { value: 'pension', label: '펜션', desc: '자연 속 휴식' },
    { value: 'guesthouse', label: '게스트하우스', desc: '저렴한 숙박' },
  ]
  
  const loading = ref(false)
  const error = ref('')
  
  // 예산 표시용 (쉼표 포함)
  const budgetDisplay = ref('500,000')
  
  // 예산 입력 처리 (쉼표 추가/제거)
  const handleBudgetInput = (event) => {
    const value = event.target.value.replace(/,/g, '') // 쉼표 제거
    if (!isNaN(value) && value !== '') {
      const numValue = parseInt(value)
      formData.value.budget = numValue
      budgetDisplay.value = numValue.toLocaleString('ko-KR')
    } else if (value === '') {
      formData.value.budget = 0
      budgetDisplay.value = '0'
    }
  }
  
  // 예산 포커스 아웃 시 포맷팅
  const handleBudgetBlur = () => {
    if (formData.value.budget > 0) {
      budgetDisplay.value = formData.value.budget.toLocaleString('ko-KR')
    }
  }
  
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
      <div class="content-wrapper form-card">
        
        <header class="header">
          <h1 class="title">New Trip</h1>
          <p class="desc">새로운 여행 계획을 생성합니다.</p>
        </header>
  
        <div v-if="error" class="error-message">{{ error }}</div>
  
        <form @submit.prevent="handleSubmit" class="form-grid">
          
          <div class="grid-row-2">
              <div class="form-group">
                <label class="label">Schedule</label>
                <div class="input-row">
                    <div class="input-wrap">
                    <span class="sub-label">시작일</span>
                    <input v-model="formData.start_date" type="date" placeholder="YYYY-MM-DD" required />
                    </div>
                    <div class="input-wrap">
                    <span class="sub-label">종료일</span>
                    <input v-model="formData.end_date" type="date" placeholder="YYYY-MM-DD" required />
                    </div>
                </div>
              </div>
  
              <div class="form-group">
                <label class="label">Conditions</label>
                <div class="input-row">
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
                        :value="budgetDisplay"
                        @input="handleBudgetInput"
                        @blur="handleBudgetBlur"
                        type="text"
                        required
                        placeholder="500,000"
                    />
                    </div>
                </div>
              </div>
          </div>
  
          <div class="form-group">
            <label class="label">Location</label>
            <div class="input-row">
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
            
            <div class="prefs-container">
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
  
              <div class="select-group">
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
          </div>
  
          <div class="action-area">
            <button type="submit" class="submit-btn" :disabled="loading">
              {{ loading ? '여행 계획 생성 중...' : '여행 계획 생성하기' }}
            </button>
          </div>
  
        </form>
      </div>
    </div>
  </template>
  
  <style scoped>
  @import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css");
  
  .layout-container {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding: 100px 40px;
    min-height: 100vh;
    color: #111;
    background-color: #ffffff;
    font-family: "Pretendard Variable", Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    letter-spacing: -0.02em;
  }
  
  .content-wrapper {
    width: 100%;
    max-width: 1300px; 
    position: relative;
    z-index: 1;
  }
  
  .form-card {
    background: #ffffff;
    border: 1px solid #e5e7eb; 
    box-shadow: 0 30px 60px -12px rgba(0, 0, 0, 0.25), 0 18px 36px -18px rgba(0, 0, 0, 0.15);
    border-radius: 24px;
    padding: 56px;
  }
  
  /* Header */
  .header {
    margin-bottom: 40px;
    border-bottom: 2px solid #f3f4f6;
    padding-bottom: 24px;
  }
  
  .title {
    font-size: 42px;
    font-weight: 800;
    letter-spacing: -0.04em;
    margin: 0 0 8px 0;
    color: #111;
    line-height: 1.1;
  }
  
  .desc {
    font-size: 17px;
    color: #6b7280;
    margin: 0;
    font-weight: 400;
  }
  
  /* Form Layout */
  .form-grid {
    display: flex;
    flex-direction: column;
    gap: 40px;
  }
  
  /* 상단 2열 그리드 */
  .grid-row-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 40px;
  }
  
  .input-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }
  
  .form-group {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  
  .label {
    font-size: 13px;
    font-weight: 700;
    color: #2F80ED;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 4px;
  }
  
  .input-wrap {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  
  .sub-label {
    font-size: 14px;
    font-weight: 600;
    color: #374151;
    margin-left: 2px;
  }
  
  /* Inputs */
  input, select {
    width: 100%;
    height: 56px; 
    padding: 0 18px;
    border: 1px solid #e5e7eb; 
    border-radius: 12px; 
    font-size: 16px;
    font-weight: 500;
    font-family: inherit;
    color: #111;
    background-color: #f9fafb; 
    transition: all 0.2s ease;
    appearance: none;
  }
  
  input:hover, select:hover {
    background-color: #f3f4f6;
    border-color: #d1d5db;
  }
  
  input:focus, select:focus {
    outline: none;
    background-color: #fff;
    border-color: #2F80ED;
    box-shadow: 0 0 0 4px rgba(47, 128, 237, 0.1);
  }
  
  input::placeholder {
    color: #9ca3af;
    font-weight: 400;
  }
  
  /* Date input placeholder styling */
  input[type="date"] {
    position: relative;
  }
  
  /* 날짜가 선택되지 않았을 때 (invalid) - placeholder 표시 */
  input[type="date"]:invalid::-webkit-datetime-edit-text {
    color: transparent;
  }
  
  input[type="date"]:invalid::-webkit-datetime-edit-month-field,
  input[type="date"]:invalid::-webkit-datetime-edit-day-field,
  input[type="date"]:invalid::-webkit-datetime-edit-year-field {
    color: transparent;
  }
  
  input[type="date"]:invalid::-webkit-datetime-edit {
    color: transparent;
  }
  
  input[type="date"]:invalid::before {
    content: attr(placeholder);
    position: absolute;
    left: 18px;
    top: 50%;
    transform: translateY(-50%);
    color: #9ca3af;
    font-weight: 400;
    pointer-events: none;
  }
  
  /* 날짜가 선택되었을 때 (valid) - 실제 날짜 텍스트 표시 */
  input[type="date"]:valid::-webkit-datetime-edit-text,
  input[type="date"]:valid::-webkit-datetime-edit-month-field,
  input[type="date"]:valid::-webkit-datetime-edit-day-field,
  input[type="date"]:valid::-webkit-datetime-edit-year-field {
    color: #111;
  }
  
  input[type="date"]:valid::before {
    display: none;
  }
  
  input[type="date"]::-webkit-calendar-picker-indicator {
    cursor: pointer;
    opacity: 0.6;
    position: relative;
    z-index: 1;
  }
  
  input[type="date"]::-webkit-calendar-picker-indicator:hover {
    opacity: 1;
  }
  
  /* Firefox */
  input[type="date"]:invalid {
    color: transparent;
  }
  
  input[type="date"]:valid {
    color: #111;
  }
  
  input[type="date"]:invalid::-moz-placeholder {
    color: #9ca3af;
    opacity: 1;
  }
  
  /* Preferences Layout */
  .prefs-container {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 40px;
  }
  
  .select-group {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  
  .group-name {
    font-size: 14px;
    font-weight: 600;
    color: #4b5563;
  }
  
  .button-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); 
    gap: 10px;
  }
  
  /* Select Buttons */
  .select-btn {
    padding: 14px 20px;
    font-size: 15px;
    font-weight: 500;
    font-family: inherit;
    color: #4b5563;
    background-color: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
  }
  
  .select-btn:hover {
    border-color: #2563eb;
    color: #2563eb;
    background-color: #eff6ff;
  }
  
  .select-btn.active {
    background-color: #111;
    color: #fff;
    border-color: #111;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  }
  
  .btn-emoji {
    font-size: 16px;
  }
  
  .btn-text {
    font-size: 14px;
  }
  
  /* Submit Button */
  .action-area {
    margin-top: 20px;
    padding-top: 32px;
    border-top: 1px solid #f3f4f6;
  }
  
  .submit-btn {
    width: 100%;
    height: 64px;
    background: #111; 
    color: #fff;
    font-size: 18px;
    font-weight: 700;
    font-family: inherit;
    letter-spacing: -0.01em;
    border: none;
    border-radius: 16px;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  
  .submit-btn:hover:not(:disabled) {
    transform: translateY(-2px);
    background: #333;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  }
  
  .submit-btn:active:not(:disabled) {
    transform: translateY(0);
  }
  
  .submit-btn:disabled {
    background: #e5e7eb;
    color: #9ca3af;
    cursor: not-allowed;
    transform: none;
  }
  
  .error-message {
    color: #dc2626;
    font-size: 14px;
    margin-bottom: 24px;
    font-weight: 600;
    text-align: center;
    background-color: #fef2f2;
    padding: 16px;
    border-radius: 12px;
  }
  
  /* Responsive */
  @media (max-width: 900px) {
    .layout-container {
      padding: 20px;
    }
    
    .form-card {
      padding: 32px 24px;
    }
  
    .grid-row-2, .prefs-container, .input-row {
      grid-template-columns: 1fr;
      gap: 24px;
    }
    
    .title {
      font-size: 32px;
    }
  }
  </style>