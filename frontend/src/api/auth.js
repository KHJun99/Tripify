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
}
