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
  }
})
