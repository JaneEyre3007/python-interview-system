import api from './index'

export function getQuestions(params) {
  return api.get('/questions/', { params })
}

export function getQuestion(id) {
  return api.get(`/questions/${id}/`)
}

export function createQuestion(data) {
  return api.post('/questions/', data)
}

export function deleteQuestion(id) {
  return api.delete(`/questions/${id}/`)
}

export function batchDeleteQuestions(ids) {
  return api.post('/questions/batch_delete/', { ids })
}

export function getRandomQuestions(count = 10) {
  return api.get('/questions/random/', { params: { count } })
}

export function getCategories() {
  return api.get('/questions/categories/')
}
