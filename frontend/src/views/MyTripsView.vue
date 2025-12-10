<script setup>
import { onMounted } from 'vue'
import { useTripStore } from '@/stores/trip'
import { useRouter } from 'vue-router'

const tripStore = useTripStore()
const router = useRouter()

onMounted(async () => {
  await tripStore.fetchPlans()
})

const goToTrip = (id) => {
  router.push({ name: 'itinerary', params: { id } })
}
</script>

<template>
  <div class="my-trips-view">
    <h1>내 여행 계획</h1>

    <div v-if="tripStore.loading" class="loading">로딩 중...</div>

    <div v-else-if="tripStore.plans.length === 0" class="empty-state">
      <p>아직 여행 계획이 없습니다.</p>
      <router-link to="/trip/new" class="btn-primary">여행 계획 만들기</router-link>
    </div>

    <div v-else class="trips-grid">
      <div v-for="plan in tripStore.plans" :key="plan.id" class="trip-card" @click="goToTrip(plan.id)">
        <h3>{{ plan.title }}</h3>
        <p class="trip-info">{{ plan.region }} | {{ plan.travel_style }}</p>
        <p class="trip-dates">{{ plan.start_date }} ~ {{ plan.end_date }}</p>
        <p class="trip-budget">예산: {{ plan.budget.toLocaleString() }}원</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
h1 {
  margin-bottom: 2rem;
}

.loading {
  text-align: center;
  padding: 2rem;
}

.empty-state {
  text-align: center;
  padding: 3rem;
}

.empty-state p {
  margin-bottom: 1rem;
  color: #666;
}

.btn-primary {
  display: inline-block;
  padding: 1rem 2rem;
  background-color: #3498db;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: bold;
}

.trips-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.trip-card {
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s;
}

.trip-card:hover {
  transform: translateY(-5px);
}

.trip-card h3 {
  margin-bottom: 1rem;
  font-size: 1.25rem;
}

.trip-info,
.trip-dates,
.trip-budget {
  margin-bottom: 0.5rem;
  color: #666;
}
</style>
