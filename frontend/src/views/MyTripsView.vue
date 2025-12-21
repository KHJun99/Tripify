<script setup>
import { onMounted, ref, computed } from 'vue'
import { useTripStore } from '@/stores/trip'
import { useRouter } from 'vue-router'

const tripStore = useTripStore()
const router = useRouter()

// --- 색상 팔레트 ---
const colorPalette = [
  { bg: '#e3f2fd', text: '#1565c0' }, // 파랑
  { bg: '#e8f5e9', text: '#2e7d32' }, // 초록
  { bg: '#f3e5f5', text: '#7b1fa2' }, // 보라
  { bg: '#fff3e0', text: '#ef6c00' }, // 주황
  { bg: '#ffebee', text: '#c62828' }, // 빨강
  { bg: '#e0f7fa', text: '#006064' }, // 하늘
  { bg: '#fff8e1', text: '#ff8f00' }, // 노랑
  { bg: '#fce4ec', text: '#c2185b' }, // 분홍
]

const getPlanStyle = (id) => {
  const numId = typeof id === 'number' ? id : String(id).split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)
  const color = colorPalette[numId % colorPalette.length]
  return { '--plan-bg': color.bg, '--plan-text': color.text }
}

// --- 달력 상태 ---
const currentDate = ref(new Date())
const weekDays = ['일', '월', '화', '수', '목', '금', '토']

const currentYear = computed(() => currentDate.value.getFullYear())
const currentMonth = computed(() => currentDate.value.getMonth())
const daysInMonth = computed(() => new Date(currentYear.value, currentMonth.value + 1, 0).getDate())
const startDay = computed(() => new Date(currentYear.value, currentMonth.value, 1).getDay())

const changeMonth = (diff) => {
  currentDate.value = new Date(currentYear.value, currentMonth.value + diff, 1)
}

// --- 일정 정렬 ---
const sortedPlans = computed(() => {
  return [...tripStore.plans].sort((a, b) => {
    const startA = new Date(a.start_date)
    const startB = new Date(b.start_date)
    if (startA - startB !== 0) return startA - startB
    const endA = new Date(a.end_date)
    const endB = new Date(b.end_date)
    return endB - endA
  })
})

const getPlansForDate = (day) => {
  if (!sortedPlans.value.length) return []
  const targetDate = new Date(currentYear.value, currentMonth.value, day)
  targetDate.setHours(0, 0, 0, 0)

  return sortedPlans.value.filter(plan => {
    const start = new Date(plan.start_date)
    const end = new Date(plan.end_date)
    start.setHours(0, 0, 0, 0)
    end.setHours(0, 0, 0, 0)
    return targetDate >= start && targetDate <= end
  })
}

// 클래스 판별 로직
const getPlanClass = (day, plan) => {
  const targetDate = new Date(currentYear.value, currentMonth.value, day)
  const targetTime = targetDate.setHours(0,0,0,0)
  const dayOfWeek = targetDate.getDay()

  const start = new Date(plan.start_date).setHours(0,0,0,0)
  const end = new Date(plan.end_date).setHours(0,0,0,0)

  const classes = []
  const isVisualStart = (targetTime === start) || (dayOfWeek === 0)
  const isVisualEnd = (targetTime === end) || (dayOfWeek === 6)

  if (isVisualStart) classes.push('is-start')
  if (isVisualEnd) classes.push('is-end')
  if (!isVisualStart && !isVisualEnd) classes.push('is-middle')

  return classes.join(' ')
}

// 텍스트 너비 계산 (연속된 일정 표시용)
const getSegmentWidth = (day, plan) => {
  const targetDate = new Date(currentYear.value, currentMonth.value, day)
  const dayOfWeek = targetDate.getDay()

  const endDate = new Date(plan.end_date)
  endDate.setHours(0,0,0,0)

  const daysLeftInWeek = 7 - dayOfWeek
  const msPerDay = 1000 * 60 * 60 * 24
  const daysLeftInPlan = Math.floor((endDate - targetDate) / msPerDay) + 1

  const span = Math.min(daysLeftInWeek, daysLeftInPlan)
  return `calc(100% * ${span} + ${span - 1}px)`
}

onMounted(async () => {
  await tripStore.fetchPlans()
})

const goToTrip = (id) => {
  router.push({ name: 'itinerary', params: { id } })
}

const goToCreate = () => {
  router.push('/trip/new')
}
</script>

<template>
  <div class="my-trips-view">
    <h1></h1>
    <div v-if="tripStore.loading" class="loading">로딩 중...</div>

    <div v-else>
      <div class="calendar-section">
        <div class="calendar-header">
          <div class="month-nav">
            <button @click="changeMonth(-1)">&lt;</button>
            <h2>{{ currentYear }}. {{ currentMonth + 1 }}</h2>
            <button @click="changeMonth(1)">&gt;</button>
          </div>
          <button class="btn-create" @click="goToCreate">여행 추가 +</button>
        </div>

        <div class="calendar-board">
          <div v-for="day in weekDays" :key="day" class="weekday">{{ day }}</div>
          <div v-for="n in startDay" :key="'blank-' + n" class="day blank"></div>

          <div v-for="day in daysInMonth" :key="day" class="day">
            <span class="day-number">{{ day }}</span>

            <div class="plan-bars">
              <div
                v-for="plan in getPlansForDate(day)"
                :key="plan.id"
                class="plan-bar"
                :class="getPlanClass(day, plan)"
                :style="getPlanStyle(plan.id)"
                @click.stop="goToTrip(plan.id)"
              >
                <span
                  v-if="getPlanClass(day, plan).includes('is-start')"
                  class="plan-title"
                  :style="{ width: getSegmentWidth(day, plan) }"
                >
                  {{ plan.title }}
                </span>
                <span v-else class="plan-title-hidden">&nbsp;</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      </div>
  </div>
</template>

<style scoped>
/* 기본 레이아웃 */
h1 { margin-bottom: 2rem; color: #333; }
.loading { text-align: center; padding: 2rem; }

/* 달력 스타일 */
.calendar-section {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  margin-bottom: 0;
  width: 100%;
  box-sizing: border-box;
}

/* 헤더 스타일 개선 */
.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.month-nav {
  display: flex;
  align-items: center;
  gap: 20px;
  flex: 1;
  justify-content: center;
  margin-left: 100px;
}

.month-nav h2 { margin: 0; font-size: 1.5rem; }
.month-nav button { padding: 5px 15px; border: 1px solid #ddd; background: white; border-radius: 4px; cursor: pointer; }

/* 여행 추가 버튼 스타일 */
.btn-create {
  padding: 8px 16px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
  font-size: 0.9rem;
}
.btn-create:hover {
  background-color: #2980b9;
}

.calendar-board {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  width: 100%;
  border-top: 1px solid #eee;
  border-left: 1px solid #eee;
  table-layout: fixed;
}

.weekday {
  text-align: center;
  font-weight: bold;
  padding: 10px 0;
  background: #f9f9f9;
  border-right: 1px solid #eee;
  border-bottom: 1px solid #eee;
  font-size: 0.9rem;
  color: #555;
}

.day {
  min-height: 100px;
  padding: 30px 0 0 0;
  border-right: 1px solid #eee;
  border-bottom: 1px solid #eee;
  position: relative;
  min-width: 0;
  background-color: #fff;
  overflow: visible;
  z-index: 1;
}

.day-number {
  position: absolute;
  top: 8px; left: 8px;
  font-size: 0.9rem; font-weight: bold; color: #333;
}

.blank { background: #fdfdfd; }

.plan-bars {
  display: flex;
  flex-direction: column;
  gap: 2px;
  width: 100%;
  position: relative;
}

.plan-bar {
  background-color: var(--plan-bg);
  color: var(--plan-text);
  font-size: 0.8rem;
  height: 24px;
  line-height: 24px;
  cursor: pointer;
  margin: 0;
  padding: 0;
  border-radius: 0;
  white-space: nowrap;
  text-align: left;
  position: relative;
}

.plan-bar:hover {
  filter: brightness(0.95);
}

.plan-bar.is-start {
  border-top-left-radius: 4px;
  border-bottom-left-radius: 4px;
  margin-left: 4px;
  border-left: 3px solid var(--plan-text);
  z-index: 10;
}

.plan-bar.is-end {
  border-top-right-radius: 4px;
  border-bottom-right-radius: 4px;
  margin-right: 4px;
}

.plan-title {
  display: block;
  position: absolute;
  top: 0; left: 0; height: 100%;
  padding-left: 6px;
  box-sizing: border-box;
  font-weight: 600;
  overflow: hidden;
  text-overflow: ellipsis;
  pointer-events: none;
}

.plan-title-hidden { visibility: hidden; }

@media (max-width: 768px) {
  .calendar-section { padding: 10px; }
  .month-nav { margin-left: 0; } /* 모바일에서는 중앙 정렬 보정 해제 */
  .day { min-height: 70px; padding-top: 25px; }
  .plan-bar { font-size: 10px; height: 18px; line-height: 18px; }
  .day-number { font-size: 0.8rem; top: 4px; left: 4px; }
  .btn-create { padding: 6px 12px; font-size: 0.8rem; }
}
</style>
