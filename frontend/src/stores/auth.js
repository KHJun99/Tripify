import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authAPI } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token'))
  const isAuthenticated = ref(!!token.value)

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
      user.value = {
        username: response.data.username,
        id: response.data.user_id,
      }
      localStorage.setItem('token', response.data.token)
      isAuthenticated.value = true
      return response.data
    } catch (error) {
      throw error
    }
  }

  const logout = async () => {
    try {
      await authAPI.logout()
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
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
      user.value = {
        username: response.data.username,
        id: response.data.user_id,
        email: response.data.email,
        loginType: response.data.login_type,
      }
      localStorage.setItem('token', response.data.token)
      isAuthenticated.value = true
      return response.data
    } catch (error) {
      throw error
    }
  }

  const googleLogin = async (code) => {
    try {
      const response = await authAPI.googleLogin(code)
      token.value = response.data.token
      user.value = {
        username: response.data.username,
        id: response.data.user_id,
        email: response.data.email,
        loginType: response.data.login_type,
      }
      localStorage.setItem('token', response.data.token)
      isAuthenticated.value = true
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

  return {
    user,
    token,
    isAuthenticated,
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
