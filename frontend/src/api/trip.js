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
    return axios.post('/travel/plans/generate/', data)
  },
  
  updatePlan(id, data) {
    return axios.patch(`/travel/plans/${id}/`, data)
  },
  
  deletePlan(id) {
    return axios.delete(`/travel/plans/${id}/`)
  },
}
