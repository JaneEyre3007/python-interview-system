import api from './index'

export function createExam(data) {
  return api.post('/exams/create_exam/', data)
}

export function startExam(id) {
  return api.post(`/exams/${id}/start/`)
}

export function submitAnswer(id, data) {
  return api.post(`/exams/${id}/submit_answer/`, data)
}

export function finishExam(id) {
  return api.post(`/exams/${id}/finish/`)
}

export function getExamResult(id) {
  return api.get(`/exams/${id}/result/`)
}

export function getExamList() {
  return api.get('/exams/')
}
