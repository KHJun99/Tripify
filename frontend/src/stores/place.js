import { defineStore } from 'pinia'
import { ref } from 'vue'
import { placeAPI } from '@/api/place'

export const usePlaceStore = defineStore('place', () => {
  const places = ref([])
  const festivals = ref([])
  const bookmarks = ref([])
  const currentPlace = ref(null)
  const loading = ref(false)

  const fetchPlaces = async (params = {}) => {
    loading.value = true
    try {
      const response = await placeAPI.getPlaces(params)
      places.value = response.data
      return response.data
    } catch (error) {
      console.error('Error fetching places:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const fetchPlace = async (id) => {
    loading.value = true
    try {
      const response = await placeAPI.getPlace(id)
      currentPlace.value = response.data
      return response.data
    } catch (error) {
      console.error('Error fetching place:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const fetchFestivals = async (params = {}) => {
    loading.value = true
    try {
      const response = await placeAPI.getFestivals(params)
      festivals.value = response.data
      return response.data
    } catch (error) {
      console.error('Error fetching festivals:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const fetchBookmarks = async () => {
    loading.value = true
    try {
      const response = await placeAPI.getBookmarks()
      bookmarks.value = response.data
      return response.data
    } catch (error) {
      console.error('Error fetching bookmarks:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const addBookmark = async (placeId) => {
    try {
      const response = await placeAPI.createBookmark(placeId)
      bookmarks.value.push(response.data)
      return response.data
    } catch (error) {
      console.error('Error adding bookmark:', error)
      throw error
    }
  }

  const removeBookmark = async (id) => {
    try {
      await placeAPI.deleteBookmark(id)
      bookmarks.value = bookmarks.value.filter((b) => b.id !== id)
    } catch (error) {
      console.error('Error removing bookmark:', error)
      throw error
    }
  }

  return {
    places,
    festivals,
    bookmarks,
    currentPlace,
    loading,
    fetchPlaces,
    fetchPlace,
    fetchFestivals,
    fetchBookmarks,
    addBookmark,
    removeBookmark,
  }
})
