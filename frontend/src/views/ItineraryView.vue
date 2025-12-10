<script setup>
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useTripStore } from '@/stores/trip'

const route = useRoute()
const tripStore = useTripStore()

onMounted(async () => {
  const id = route.params.id
  await tripStore.fetchPlan(id)
})
</script>

<template>
  <div class="itinerary-view">
    <div v-if="tripStore.loading" class="loading">로딩 중...</div>

    <div v-else-if="tripStore.currentPlan" class="itinerary-content">
      <h1>{{ tripStore.currentPlan.title }}</h1>

      <div class="trip-details">
        <p><strong>지역:</strong> {{ tripStore.currentPlan.region }}</p>
        <p><strong>기간:</strong> {{ tripStore.currentPlan.start_date }} ~ {{ tripStore.currentPlan.end_date }}</p>
        <p><strong>예산:</strong> {{ tripStore.currentPlan.budget.toLocaleString() }}원</p>
        <p><strong>스타일:</strong> {{ tripStore.currentPlan.travel_style }}</p>
        <p><strong>숙박:</strong> {{ tripStore.currentPlan.accommodation_type }}</p>
      </div>

      <div v-if="tripStore.currentPlan.itineraries && tripStore.currentPlan.itineraries.length > 0" class="itineraries">
        <h2>일정</h2>
        <div v-for="itinerary in tripStore.currentPlan.itineraries" :key="itinerary.id" class="itinerary-day">
          <h3>{{ itinerary.day_number }}일차 - {{ itinerary.date }}</h3>
          <p>{{ itinerary.description }}</p>
        </div>
      </div>

      <div v-else class="empty-itinerary">
        <p>아직 일정이 추가되지 않았습니다.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.loading {
  text-align: center;
  padding: 2rem;
}

h1 {
  margin-bottom: 2rem;
}

.trip-details {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.trip-details p {
  margin-bottom: 0.5rem;
}

.itineraries h2 {
  margin-bottom: 1rem;
}

.itinerary-day {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 1rem;
}

.itinerary-day h3 {
  margin-bottom: 0.5rem;
}

.empty-itinerary {
  text-align: center;
  padding: 2rem;
  color: #666;
}
</style>
