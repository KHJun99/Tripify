import axios from 'axios'

const API_URL = 'http://localhost:8000/api/festivals'

/**
 * 축제 목록 조회
 * @param {Object} params - 필터 파라미터 (month, region, search 등)
 * @returns {Promise} 축제 목록
 */
export const getFestivals = async (params = {}) => {
  try {
    const response = await axios.get(`${API_URL}/`, { params })
    return response.data
  } catch (error) {
    console.error('축제 목록 조회 실패:', error)
    throw error
  }
}

/**
 * 축제 상세 정보 조회
 * @param {number} id - 축제 ID
 * @returns {Promise} 축제 상세 정보
 */
export const getFestivalDetail = async (id) => {
  try {
    const response = await axios.get(`${API_URL}/${id}/`)
    return response.data
  } catch (error) {
    console.error('축제 상세 정보 조회 실패:', error)
    throw error
  }
}
