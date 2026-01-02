import axios from 'axios'

/**
 * API client for PyHammer backend
 */
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Calculator API
export const calculator = {
  calculate: async (weapons, target, assumeCover = false, assumeHalfRange = false) => {
    const response = await client.post('/api/calculator/calculate', {
      weapons,
      target,
      assume_cover: assumeCover,
      assume_half_range: assumeHalfRange,
      deduplicate_exclusive: true,
    })
    return response.data
  },

  calculateMultiTarget: async (weapons, targets, assumeCover = false, assumeHalfRange = false) => {
    const response = await client.post('/api/calculator/calculate-multi-target', {
      weapons,
      targets,
      assume_cover: assumeCover,
      assume_half_range: assumeHalfRange,
    })
    return response.data
  },
}

// Roster API
export const rosters = {
  list: async () => {
    const response = await client.get('/api/rosters/list')
    return response.data
  },

  load: async (filename) => {
    const response = await client.get(`/api/rosters/load/${filename}`)
    return response.data
  },

  save: async (filename, weapons) => {
    const response = await client.post('/api/rosters/save', {
      filename,
      weapons,
    })
    return response.data
  },

  delete: async (filename) => {
    const response = await client.delete(`/api/rosters/delete/${filename}`)
    return response.data
  },
}

// Target API
export const targets = {
  list: async () => {
    const response = await client.get('/api/targets/list')
    return response.data
  },

  load: async (filename) => {
    const response = await client.get(`/api/targets/load/${filename}`)
    return response.data
  },

  save: async (filename, targets) => {
    const response = await client.post('/api/targets/save', {
      filename,
      targets,
    })
    return response.data
  },

  delete: async (filename) => {
    const response = await client.delete(`/api/targets/delete/${filename}`)
    return response.data
  },
}

// Visualizations API
export const visualizations = {
  generateChart: async (chartType, weapons, targets, assumeCover = false, assumeHalfRange = false, theme = 'plotly') => {
    const response = await client.post('/api/visualizations/chart', {
      chart_type: chartType,
      weapons,
      targets,
      assume_cover: assumeCover,
      assume_half_range: assumeHalfRange,
      theme,
    })
    return response.data
  },

  getThemes: async () => {
    const response = await client.get('/api/visualizations/themes')
    return response.data
  },
}

export default client
