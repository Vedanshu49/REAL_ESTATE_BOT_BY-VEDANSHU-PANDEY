import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const queryAnalysis = (query) => {
  return api.post('/queries/analyze/', { query })
}

export const getAllProperties = () => {
  return api.get('/properties/')
}

export const downloadData = (query) => {
  return api.post('/queries/download_data/', { query }, { responseType: 'blob' })
}

export const getLocations = () => {
  return api.get('/properties/locations_list/')
}

export const getQueryHistory = () => {
  return api.get('/queries/history/')
}

export default api
