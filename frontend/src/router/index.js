import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import TripPlanView from '@/views/TripPlanView.vue'
import MyTripsView from '@/views/MyTripsView.vue'
import ItineraryView from '@/views/ItineraryView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView,
    },
    {
      path: '/trip/new',
      name: 'trip-plan',
      component: TripPlanView,
      meta: { requiresAuth: true },
    },
    {
      path: '/trips',
      name: 'my-trips',
      component: MyTripsView,
      meta: { requiresAuth: true },
    },
    {
      path: '/trip/:id',
      name: 'itinerary',
      component: ItineraryView,
      meta: { requiresAuth: true },
    },
  ],
})

// 네비게이션 가드
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  if (to.meta.requiresAuth && !token) {
    next({ name: 'login' })
  } else if ((to.name === 'login' || to.name === 'signup') && token) {
    next({ name: 'home' })
  } else {
    next()
  }
})

export default router
