import axios from './axios'

export const authAPI = {
  signup(data) {
    return axios.post('/auth/signup/', data)
  },
  
  login(data) {
    return axios.post('/auth/login/', data)
  },
  
  logout() {
    return axios.post('/auth/logout/')
  },
  
  getProfile() {
    return axios.get('/auth/profile/')
  },
  
  updateProfile(data) {
    return axios.patch('/auth/profile/', data)
  },

  kakaoLogin(code) {
    return axios.post('/auth/kakao/callback/', { code })
  },

  googleLogin(code) {
    return axios.post('/auth/google/callback/', { code })
  },

  deleteAccount(data) {
    return axios.delete('/auth/delete/', { data })
  },

  changePassword(data) {
    return axios.post('/auth/password-change/', data)
  },

  verifyPassword(password) {
    return axios.post('/auth/password-verify/', { password })
  },
}
