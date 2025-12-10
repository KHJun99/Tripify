<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useTripStore } from '@/stores/trip'

const router = useRouter()
const tripStore = useTripStore()

const formData = ref({
  budget: 500000,
  start_date: '',
  end_date: '',
  region: '서울',
  travel_style: '관광',
  accommodation_type: 'motel',
})

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

    <div v-if="error" class="error-message">{{ error }}</div>

    <form @submit.prevent="handleSubmit" class="plan-form">
      <div class="form-group">
        <label>예산 (원)</label>
        <input v-model.number="formData.budget" type="number" min="0" required />
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

      <div class="form-group">
        <label>지역</label>
        <select v-model="formData.region" required>
          <option value="서울">서울</option>
          <option value="부산">부산</option>
          <option value="제주">제주</option>
          <option value="강원">강원</option>
          <option value="경기">경기</option>
        </select>
      </div>

      <div class="form-group">
        <label>여행 스타일</label>
        <input v-model="formData.travel_style" type="text" placeholder="예: 관광, 힐링, 맛집투어" required />
      </div>

      <div class="form-group">
        <label>숙박 타입</label>
        <select v-model="formData.accommodation_type" required>
          <option value="hotel">호텔</option>
          <option value="motel">모텔</option>
          <option value="pension">펜션</option>
          <option value="guesthouse">게스트하우스</option>
        </select>
      </div>

      <button type="submit" class="btn-primary" :disabled="loading">
        {{ loading ? '생성 중...' : 'AI 여행 코스 생성' }}
      </button>
    </form>
  </div>
</template>

<style scoped>
.trip-plan-view {
  max-width: 600px;
  margin: 0 auto;
}

h1 {
  margin-bottom: 2rem;
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
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
}

.btn-primary {
  width: 100%;
  padding: 1rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;
  transition: background-color 0.3s;
}

.btn-primary:hover:not(:disabled) {
  background-color: #2980b9;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
