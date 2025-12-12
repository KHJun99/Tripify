import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import TripPlanView from '@/views/TripPlanView.vue'
import MyTripsView from '@/views/MyTripsView.vue'
import ItineraryView from '@/views/ItineraryView.vue'
import KakaoCallbackView from '@/views/KakaoCallbackView.vue'
import GoogleCallbackView from '@/views/GoogleCallbackView.vue'
import VerifyEmailView from '@/views/VerifyEmailView.vue'
import ResendVerificationView from '@/views/ResendVerificationView.vue'
import FindUsernameView from '@/views/FindUsernameView.vue'
import ResetPasswordRequestView from '@/views/ResetPasswordRequestView.vue'
import ResetPasswordConfirmView from '@/views/ResetPasswordConfirmView.vue'
import AccountSettingsView from '@/views/AccountSettingsView.vue'
import FestivalsView from '@/views/FestivalsView.vue'
import FestivalDetailView from '@/views/FestivalDetailView.vue'

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
      path: '/auth/kakao/callback',
      name: 'kakao-callback',
      component: KakaoCallbackView,
    },
    {
      path: '/auth/google/callback',
      name: 'google-callback',
      component: GoogleCallbackView,
    },
    {
      path: '/auth/verify-email',
      name: 'verify-email',
      component: VerifyEmailView,
    },
    {
      path: '/auth/resend-verification',
      name: 'resend-verification',
      component: ResendVerificationView,
    },
    {
      path: '/auth/find-username',
      name: 'find-username',
      component: FindUsernameView,
    },
    {
      path: '/auth/reset-password',
      name: 'reset-password-request',
      component: ResetPasswordRequestView,
    },
    {
      path: '/auth/reset-password/confirm',
      name: 'reset-password-confirm',
      component: ResetPasswordConfirmView,
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
    {
      path: '/settings',
      name: 'account-settings',
      component: AccountSettingsView,
      meta: { requiresAuth: true },
    },
    {
      path: '/festivals',
      name: 'festivals',
      component: FestivalsView,
    },
    {
      path: '/festivals/:id',
      name: 'festival-detail',
      component: FestivalDetailView,
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
