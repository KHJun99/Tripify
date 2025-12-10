import axios from './axios'

export const placeAPI = {
  getPlaces(params) {
    return axios.get('/places/', { params })
  },
  
  getPlace(id) {
    return axios.get(`/places/${id}/`)
  },
  
  getFestivals(params) {
    return axios.get('/places/festivals/', { params })
  },
  
  getBookmarks() {
    return axios.get('/bookmarks/')
  },
  
  createBookmark(placeId) {
    return axios.post('/bookmarks/', { place_id: placeId })
  },
  
  deleteBookmark(id) {
    return axios.delete(`/bookmarks/${id}/`)
  },
}
