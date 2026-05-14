import api from './index'

export function generateQuestions(data) {
  return api.post('/ai/generate/', data)
}

export function evaluateAnswer(data) {
  return api.post('/ai/evaluate/', data)
}

export function getTokenStats(days = 30) {
  return api.get('/ai/token-stats/', { params: { days } })
}
