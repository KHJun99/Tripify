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
    month: 'long',
    day: 'numeric'
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
    <div class="header">
      <h1>⭐ 추천된 여행지</h1>
      <p class="subtitle">다른 여행자들이 추천한 여행 계획을 확인해보세요!</p>
    </div>

    <div v-if="loading" class="loading">
      <p>로딩 중...</p>
    </div>

    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
    </div>

    <div v-else-if="recommendedPlans.length === 0" class="empty">
      <p>아직 추천된 여행 계획이 없습니다.</p>
    </div>

    <div v-else class="plans-grid">
      <div
        v-for="plan in recommendedPlans"
        :key="plan.id"
        class="plan-card"
        @click="goToPlan(plan.id)"
      >
        <div class="card-header">
          <h3>{{ plan.title }}</h3>
          <div class="rating-badge">
            <span class="star">⭐</span>
            <span class="rating-value">{{ plan.rating }}</span>
          </div>
        </div>

        <div class="card-info">
          <div class="info-item">
            <span class="info-label">📍 지역</span>
            <span class="info-value">{{ plan.region }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">📅 기간</span>
            <span class="info-value">
              {{ formatDate(plan.start_date) }} ~ {{ formatDate(plan.end_date) }}
              ({{ getDuration(plan.start_date, plan.end_date) }}일)
            </span>
          </div>
          <div class="info-item">
            <span class="info-label">👥 인원</span>
            <span class="info-value">{{ plan.people_count }}명</span>
          </div>
          <div class="info-item">
            <span class="info-label">💰 예산</span>
            <span class="info-value">{{ plan.budget.toLocaleString() }}원</span>
          </div>
        </div>

        <div v-if="plan.review" class="review-preview">
          <p class="review-text">{{ plan.review }}</p>
        </div>

        <div class="card-footer">
          <span class="author">작성자: {{ plan.user }}</span>
          <span class="date">{{ formatDate(plan.recommended_at) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.recommended-trips-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
  background: #f5f7fa;
  min-height: 100vh;
}

.header {
  text-align: center;
  margin-bottom: 3rem;
  padding: 2rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #6c757d;
  font-size: 1.1rem;
}

.loading,
.error,
.empty {
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 16px;
  color: #6c757d;
  font-size: 1.1rem;
}

.plans-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
}

.plan-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #e8ecef;
}

.plan-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e8ecef;
}

.card-header h3 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: #1a1a1a;
  flex: 1;
}

.rating-badge {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 600;
}

.star {
  font-size: 1.2rem;
}

.rating-value {
  font-size: 1rem;
}

.card-info {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
}

.info-label {
  font-weight: 600;
  color: #6c757d;
  font-size: 0.9rem;
}

.info-value {
  color: #2c3e50;
  font-weight: 500;
  text-align: right;
}

.review-preview {
  margin: 1.5rem 0;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.review-text {
  color: #495057;
  line-height: 1.6;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid #e8ecef;
  font-size: 0.85rem;
  color: #6c757d;
}

.author {
  font-weight: 500;
}

.date {
  color: #adb5bd;
}

@media (max-width: 768px) {
  .recommended-trips-view {
    padding: 1rem 0.5rem;
  }

  .header {
    padding: 1.5rem;
  }

  .header h1 {
    font-size: 2rem;
  }

  .plans-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .plan-card {
    padding: 1.5rem;
  }
}
</style>

