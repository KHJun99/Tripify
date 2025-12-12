import axios from './axios'

export const tripAPI = {
  getPlans() {
    return axios.get('/travel/plans/')
  },
  
  getPlan(id) {
    return axios.get(`/travel/plans/${id}/`)
  },
  
  createPlan(data) {
    return axios.post('/travel/plans/', data)
  },
  
  generatePlan(data) {
    // AI 일정 생성은 시간이 걸리므로 60초 타임아웃 설정
    return axios.post('/travel/plans/generate/', data, {
      timeout: 60000, // 60초
    })
  },
  
  updatePlan(id, data) {
    return axios.patch(`/travel/plans/${id}/`, data)
  },
  
  deletePlan(id) {
    return axios.delete(`/travel/plans/${id}/`)
  },
}
