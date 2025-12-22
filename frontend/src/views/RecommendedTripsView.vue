<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useTripStore } from '@/stores/trip'

const router = useRouter()
const tripStore = useTripStore()

const recommendedPlans = ref([])
const loading = ref(false)
const error = ref('')

const fetchRecommendedPlans = async () => {
  loading.value = true
  error.value = ''
  try {
    const plans = await tripStore.fetchRecommendedPlans()
    recommendedPlans.value = plans
  } catch (err) {
    error.value = '추천된 여행 계획을 불러오는 중 오류가 발생했습니다.'
    console.error('Error fetching recommended plans:', err)
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

const getDuration = (startDate, endDate) => {
  const start = new Date(startDate)
  const end = new Date(endDate)
  const diffTime = Math.abs(end - start)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  return diffDays
}

const goToPlan = (id) => {
  router.push(`/trip/${id}`)
}

onMounted(() => {
  fetchRecommendedPlans()
})
</script>

<template>
  <div class="recommended-trips-view">
    <div class="page-header">
      <h1>추천 여행지</h1>
      <p>다른 여행자들이 검증한 알짜배기 여행 코스를 확인하세요.</p>
    </div>

    <div v-if="loading" class="status-box">
      <p>데이터를 불러오고 있습니다...</p>
    </div>

    <div v-else-if="error" class="status-box">
      <p>{{ error }}</p>
    </div>

    <div v-else-if="recommendedPlans.length === 0" class="status-box">
      <p>등록된 추천 여행이 없습니다.</p>
    </div>

    <div v-else class="plans-list">
      <div
        v-for="plan in recommendedPlans"
        :key="plan.id"
        class="plan-card"
        @click="goToPlan(plan.id)"
      >
        <div class="card-header">
          <div class="title-section">
            <span class="region-label">{{ plan.region }}</span>
            <h3>{{ plan.title }}</h3>
          </div>
          <div class="rating-badge">
            <span class="star">★</span>
            <span class="score">{{ plan.rating }}</span>
          </div>
        </div>

        <div class="info-grid">
          <div class="info-item">
            <span class="label">여행 기간</span>
            <span class="value date-value">
              {{ formatDate(plan.start_date) }} ~ {{ formatDate(plan.end_date) }}
              <span class="duration">({{ getDuration(plan.start_date, plan.end_date) }}일)</span>
            </span>
          </div>
          
          <div class="info-item">
            <span class="label">인원</span>
            <span class="value">{{ plan.people_count }}명</span>
          </div>

          <div class="info-item budget-item">
            <span class="label">총 예산</span>
            <span class="value price">{{ plan.budget.toLocaleString() }}원</span>
          </div>
        </div>

        <div class="card-footer-content">
          <div v-if="plan.review" class="review-section">
            <span class="review-label">Traveler's Note</span>
            <p class="review-text">{{ plan.review }}</p>
          </div>
          
          <div class="meta-info">
            <span class="author">By. <b>{{ plan.user }}</b></span>
            <span class="separator">|</span>
            <span class="date">{{ formatDate(plan.recommended_at) }} 작성</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.recommended-trips-view {
  max-width: 1000px;
  margin: 0 auto;
  padding: 3rem 1rem;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 2rem;
  border-bottom: 2px solid #e9ecef;
  padding-bottom: 1rem;
}

.page-header h1 {
  font-size: 2rem;
  color: #111;
  margin-bottom: 0.5rem;
  font-weight: 800;
}

.page-header p {
  color: #666;
  font-size: 1rem;
}

.status-box {
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 8px;
  border: 1px solid #ddd;
  color: #888;
}

.plans-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.plan-card {
  background: white;
  border: 1px solid #e1e4e8;
  border-radius: 12px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  position: relative;
  box-shadow: 0 2px 4px rgba(0,0,0,0.03);
}

.plan-card:hover {
  border-color: #667eea;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.2rem;
  border-bottom: 1px solid #f1f3f5;
  padding-bottom: 1rem;
}

.title-section {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.region-label {
  font-size: 0.8rem;
  font-weight: 700;
  color: #667eea;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.card-header h3 {
  margin: 0;
  font-size: 1.35rem;
  font-weight: 700;
  color: #2d3748;
}

.rating-badge {
  background: #fff9db;
  color: #f08c00;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 4px;
}

.info-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.label {
  font-size: 0.75rem;
  color: #868e96;
  font-weight: 600;
}

.value {
  font-size: 1rem;
  color: #343a40;
  font-weight: 500;
}

.date-value {
  font-family: 'Roboto', sans-serif;
}

.duration {
  color: #667eea;
  font-weight: 600;
  margin-left: 4px;
  font-size: 0.9rem;
}

.budget-item .price {
  font-size: 1.1rem;
  font-weight: 800;
  color: #111;
}

.card-footer-content {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
}

.review-section {
  margin-bottom: 0.8rem;
}

.review-label {
  display: block;
  font-size: 0.7rem;
  font-weight: 700;
  color: #adb5bd;
  margin-bottom: 0.3rem;
}

.review-text {
  font-size: 0.95rem;
  color: #495057;
  line-height: 1.5;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden; 
}

.meta-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: #868e96;
  justify-content: flex-end;
  margin-top: 0.5rem;
}

.separator {
  color: #dee2e6;
  font-size: 0.7rem;
}

@media (max-width: 600px) {
  .info-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .card-header {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .rating-badge {
    align-self: flex-start;
  }
}
</style>