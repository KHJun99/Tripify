import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authAPI } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token'))
  const isAuthenticated = ref(!!token.value)
  let autoLogoutTimer = null // 자동 로그아웃 타이머
  const remainingTime = ref(null) // 남은 시간 (밀리초)
  let timeUpdateInterval = null // 시간 업데이트 인터벌

  // 남은 시간 계산 및 업데이트
  const updateRemainingTime = () => {
    const loginTime = localStorage.getItem('loginTime')
    if (loginTime && token.value) {
      const elapsed = Date.now() - parseInt(loginTime)
      const sixHours = 6 * 60 * 60 * 1000 // 6시간
      const remaining = sixHours - elapsed
      
      if (remaining > 0) {
        remainingTime.value = remaining
      } else {
        remainingTime.value = 0
      }
    } else {
      remainingTime.value = null
    }
  }

  // 남은 시간을 읽기 쉬운 형식으로 변환
  const formattedRemainingTime = computed(() => {
    if (!remainingTime.value || remainingTime.value <= 0) {
      return null
    }
    
    const hours = Math.floor(remainingTime.value / (60 * 60 * 1000))
    const minutes = Math.floor((remainingTime.value % (60 * 60 * 1000)) / (60 * 1000))
    const seconds = Math.floor((remainingTime.value % (60 * 1000)) / 1000)
    
    if (hours > 0) {
      return `${hours}시간 ${minutes}분`
    } else if (minutes > 0) {
      return `${minutes}분 ${seconds}초`
    } else {
      return `${seconds}초`
    }
  })

  // 시간 업데이트 인터벌 시작
  const startTimeUpdateInterval = () => {
    // 기존 인터벌이 있으면 제거
    if (timeUpdateInterval) {
      clearInterval(timeUpdateInterval)
    }
    
    // 즉시 한 번 업데이트
    updateRemainingTime()
    
    // 1초마다 업데이트
    timeUpdateInterval = setInterval(() => {
      updateRemainingTime()
    }, 1000)
  }

  // 시간 업데이트 인터벌 중지
  const stopTimeUpdateInterval = () => {
    if (timeUpdateInterval) {
      clearInterval(timeUpdateInterval)
      timeUpdateInterval = null
    }
    remainingTime.value = null
  }

  // 자동 로그아웃 타이머 설정 (6시간)
  const setAutoLogoutTimer = () => {
    // 기존 타이머가 있으면 제거
    if (autoLogoutTimer) {
      clearTimeout(autoLogoutTimer)
    }

    // 로그인 시간 저장
    const loginTime = Date.now()
    localStorage.setItem('loginTime', loginTime.toString())

    // 시간 업데이트 인터벌 시작
    startTimeUpdateInterval()

    // 6시간 후 자동 로그아웃
    autoLogoutTimer = setTimeout(async () => {
      alert('6시간이 경과하여 자동으로 로그아웃됩니다.')
      await logout()
      // 로그인 페이지로 리다이렉트
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }, 6 * 60 * 60 * 1000) // 6시간 = 21,600,000ms
  }

  // 자동 로그아웃 타이머 제거
  const clearAutoLogoutTimer = () => {
    if (autoLogoutTimer) {
      clearTimeout(autoLogoutTimer)
      autoLogoutTimer = null
    }
    stopTimeUpdateInterval()
    localStorage.removeItem('loginTime')
  }

  // 페이지 로드 시 로그인 시간 확인 및 타이머 설정
  // logout 함수가 정의된 후에 호출되도록 함수 내부에서 정의
  const checkLoginTime = () => {
    const loginTime = localStorage.getItem('loginTime')
    if (loginTime && token.value) {
      const elapsed = Date.now() - parseInt(loginTime)
      const sixHours = 6 * 60 * 60 * 1000 // 6시간

      if (elapsed >= sixHours) {
        // 이미 6시간이 경과한 경우 즉시 로그아웃
        logout()
        if (window.location.pathname !== '/login') {
          window.location.href = '/login'
        }
      } else {
        // 시간 업데이트 인터벌 시작
        startTimeUpdateInterval()
        
        // 남은 시간만큼 타이머 설정
        const remaining = sixHours - elapsed
        autoLogoutTimer = setTimeout(async () => {
          alert('6시간이 경과하여 자동으로 로그아웃됩니다.')
          await logout()
          if (window.location.pathname !== '/login') {
            window.location.href = '/login'
          }
        }, remaining)
      }
    }
  }

  const signup = async (data) => {
    try {
      const response = await authAPI.signup(data)
      return response.data
    } catch (error) {
      throw error
    }
  }

  const login = async (credentials) => {
    try {
      const response = await authAPI.login(credentials)
      token.value = response.data.token
      localStorage.setItem('token', response.data.token)
      isAuthenticated.value = true
      
      // 프로필 정보 가져오기
      try {
        const profile = await getProfile()
        user.value = profile
      } catch (error) {
        // 프로필 가져오기 실패 시 기본 정보만 저장
        user.value = {
          username: response.data.username,
          id: response.data.user_id,
        }
      }
      
      // 자동 로그아웃 타이머 설정
      setAutoLogoutTimer()
      
      return response.data
    } catch (error) {
      throw error
    }
  }

  const logout = async () => {
    try {
      await authAPI.logout()
    } catch (error) {
      // 에러는 조용히 처리
    } finally {
      // 자동 로그아웃 타이머 제거
      clearAutoLogoutTimer()
      
      token.value = null
      user.value = null
      isAuthenticated.value = false
      localStorage.removeItem('token')
    }
  }

  const getProfile = async () => {
    try {
      const response = await authAPI.getProfile()
      user.value = response.data
      return response.data
    } catch (error) {
      throw error
    }
  }

  const updateProfile = async (data) => {
    try {
      const response = await authAPI.updateProfile(data)
      user.value = response.data
      return response.data
    } catch (error) {
      throw error
    }
  }

  const kakaoLogin = async (code) => {
    try {
      const response = await authAPI.kakaoLogin(code)
      token.value = response.data.token
      localStorage.setItem('token', response.data.token)
      isAuthenticated.value = true
      
      // 프로필 정보 가져오기
      try {
        const profile = await getProfile()
        user.value = profile
      } catch (error) {
        // 프로필 가져오기 실패 시 기본 정보만 저장
        user.value = {
          username: response.data.username,
          id: response.data.user_id,
          email: response.data.email,
          loginType: response.data.login_type,
        }
      }
      
      // 자동 로그아웃 타이머 설정
      setAutoLogoutTimer()
      
      return response.data
    } catch (error) {
      throw error
    }
  }

  const googleLogin = async (code) => {
    try {
      const response = await authAPI.googleLogin(code)
      token.value = response.data.token
      localStorage.setItem('token', response.data.token)
      isAuthenticated.value = true
      
      // 프로필 정보 가져오기
      try {
        const profile = await getProfile()
        user.value = profile
      } catch (error) {
        // 프로필 가져오기 실패 시 기본 정보만 저장
        user.value = {
          username: response.data.username,
          id: response.data.user_id,
          email: response.data.email,
          loginType: response.data.login_type,
        }
      }
      
      // 자동 로그아웃 타이머 설정
      setAutoLogoutTimer()
      
      return response.data
    } catch (error) {
      throw error
    }
  }

  const deleteAccount = async (password = null) => {
    try {
      const data = password ? { password } : {}
      const response = await authAPI.deleteAccount(data)

      // 계정 삭제 성공 시 로그아웃 처리
      clearAutoLogoutTimer()
      token.value = null
      user.value = null
      isAuthenticated.value = false
      localStorage.removeItem('token')

      return response.data
    } catch (error) {
      throw error
    }
  }

  const changePassword = async (currentPassword, newPassword, newPasswordConfirm) => {
    try {
      const response = await authAPI.changePassword({
        current_password: currentPassword,
        new_password: newPassword,
        new_password_confirm: newPasswordConfirm,
      })

      // 비밀번호 변경 성공 시 새 토큰으로 업데이트
      if (response.data.token) {
        token.value = response.data.token
        localStorage.setItem('token', response.data.token)
      }

      return response.data
    } catch (error) {
      throw error
    }
  }

  // 초기화 시 로그인 시간 확인 (logout 함수가 정의된 후에 호출)
  if (token.value) {
    // 다음 틱에서 실행하여 모든 함수가 정의된 후에 호출되도록 함
    setTimeout(() => {
      checkLoginTime()
    }, 0)
  }

  return {
    user,
    token,
    isAuthenticated,
    remainingTime,
    formattedRemainingTime,
    signup,
    login,
    logout,
    getProfile,
    updateProfile,
    kakaoLogin,
    googleLogin,
    deleteAccount,
    changePassword,
  }
})
