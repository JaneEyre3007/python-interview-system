import api from './index'

export function login(data) {
  return api.post('/users/login/', data)
}

export function register(data) {
  return api.post('/users/register/', data)
}

export function getProfile() {
  return api.get('/users/profile/')
}

export function getAIConfig() {
  return api.get('/users/ai-config/')
}

export function saveAIConfig(data) {
  return api.post('/users/ai-config/', data)
}

export function deleteAIConfig() {
  return api.delete('/users/ai-config/')
}
