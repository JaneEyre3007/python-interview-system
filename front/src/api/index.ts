import axios from "axios"
import { createDiscreteApi } from "naive-ui"

const { message } = createDiscreteApi(["message"])

const api = axios.create({
  baseURL: "/api",
  timeout: 10000,
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token")
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    if (error.response) {
      const { status, data } = error.response
      if (status === 401) {
        localStorage.removeItem("access_token")
        localStorage.removeItem("refresh_token")
        window.location.href = "/login"
      }
      message.error(data.error || data.message || data.detail || "网络错误")
    } else {
      message.error("网络连接失败")
    }
    return Promise.reject(error)
  }
)

export default api