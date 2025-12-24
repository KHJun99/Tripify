import { defineStore } from 'pinia'
import { ref } from 'vue'
import { tripAPI } from '@/api/trip'

export const useTripStore = defineStore('trip', () => {
  const plans = ref([])
  const currentPlan = ref(null)
  const loading = ref(false)

  const fetchPlans = async () => {
    loading.value = true
    try {
      const response = await tripAPI.getPlans()
      plans.value = response.data
      return response.data
    } catch (error) {
      console.error('Error fetching plans:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const fetchPlan = async (id) => {
    loading.value = true
    try {
      const response = await tripAPI.getPlan(id)
      currentPlan.value = response.data
      return response.data
    } catch (error) {
      console.error('Error fetching plan:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const createPlan = async (data) => {
    loading.value = true
    try {
      const response = await tripAPI.createPlan(data)
      plans.value.unshift(response.data)
      return response.data
    } catch (error) {
      console.error('Error creating plan:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const generatePlan = async (data) => {
    loading.value = true
    try {
      const response = await tripAPI.generatePlan(data)
      plans.value.unshift(response.data)
      return response.data
    } catch (error) {
      console.error('Error generating plan:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const updatePlan = async (id, data) => {
    loading.value = true
    try {
      const response = await tripAPI.updatePlan(id, data)
      const index = plans.value.findIndex((p) => p.id === id)
      if (index !== -1) {
        plans.value[index] = response.data
      }
      return response.data
    } catch (error) {
      console.error('Error updating plan:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const deletePlan = async (id) => {
    loading.value = true
    try {
      await tripAPI.deletePlan(id)
      plans.value = plans.value.filter((p) => p.id !== id)
    } catch (error) {
      console.error('Error deleting plan:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const recommendPlan = async (id, data) => {
    try {
      const response = await tripAPI.recommendPlan(id, data)
      // 현재 계획 업데이트
      if (currentPlan.value && currentPlan.value.id === id) {
        currentPlan.value = response.data
      }
      // 목록 업데이트
      const index = plans.value.findIndex((p) => p.id === id)
      if (index !== -1) {
        plans.value[index] = response.data
      }
      return response.data
    } catch (error) {
      console.error('Error recommending plan:', error)
      throw error
    }
  }

  const unrecommendPlan = async (id) => {
    try {
      const response = await tripAPI.unrecommendPlan(id)
      
      // 현재 계획 업데이트
      if (currentPlan.value && currentPlan.value.id === id) {
        currentPlan.value = response.data
      }
      
      // 목록 업데이트
      const index = plans.value.findIndex((p) => p.id === id)
      if (index !== -1) {
        plans.value[index] = response.data
      }
      
      return response.data
    } catch (error) {
      console.error('[Store] 추천 취소 오류 상세:', {
        message: error.message,
        response: error.response,
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data,
        config: error.config
      })
      throw error
    }
  }

  const fetchRecommendedPlans = async () => {
    loading.value = true
    try {
      const response = await tripAPI.getRecommendedPlans()
      return response.data
    } catch (error) {
      console.error('Error fetching recommended plans:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const modifyPlan = async (id, requirements) => {
    loading.value = true
    try {
      const response = await tripAPI.modifyPlan(id, { requirements })
      
      // 현재 계획 업데이트
      if (currentPlan.value && currentPlan.value.id === id) {
        currentPlan.value = response.data
      }
      
      // 목록 업데이트
      const index = plans.value.findIndex((p) => p.id === id)
      if (index !== -1) {
        plans.value[index] = response.data
      }
      
      return response.data
    } catch (error) {
      console.error('[Store] 계획 수정 오류 상세:', {
        message: error.message,
        response: error.response,
        status: error.response?.status,
        data: error.response?.data
      })
      throw error
    } finally {
      loading.value = false
    }
  }

  return {
    plans,
    currentPlan,
    loading,
    fetchPlans,
    fetchPlan,
    createPlan,
    generatePlan,
    updatePlan,
    deletePlan,
    recommendPlan,
    unrecommendPlan,
    fetchRecommendedPlans,
    modifyPlan,
  }
})
