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
                <strong>{{ time === 'breakfast' ? '아침' : time === 'lunch' ? '점심' : '저녁' }}:</strong>
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
  margin-bottom: 1.5rem;
}

.itinerary-day h3 {
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-size: 1.5rem;
}

.day-description {
  color: #666;
  font-style: italic;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f0f0f0;
}

.section {
  margin-top: 1.5rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.section h4 {
  margin-bottom: 0.75rem;
  color: #495057;
  font-size: 1.1rem;
}

.attraction-item,
.event-item {
  margin-bottom: 1rem;
  padding: 0.75rem;
  background: white;
  border-radius: 6px;
  border-left: 3px solid #3498db;
}

.attraction-name,
.event-name {
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 0.25rem;
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
  margin-bottom: 0.5rem;
  padding: 0.5rem;
  background: white;
  border-radius: 4px;
}

.estimated-cost {
  margin-top: 1.5rem;
  padding: 1rem;
  background: #e8f5e9;
  border-radius: 8px;
  text-align: right;
}

.estimated-cost p {
  color: #2e7d32;
  font-size: 1.1rem;
  margin: 0;
}

.empty-itinerary {
  text-align: center;
  padding: 2rem;
  color: #666;
}
</style>
