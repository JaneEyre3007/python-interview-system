import { defineStore } from 'pinia'
import api from '@/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    token: localStorage.getItem('access_token') || '',
  }),
  getters: {
    isLoggedIn: (state) => !!state.token,
  },
  actions: {
    async login(credentials: any) {
      const data: any = await api.post('/users/login/', credentials)
      this.token = data.tokens.access
      this.user = data.user
      localStorage.setItem('access_token', data.tokens.access)
      localStorage.setItem('refresh_token', data.tokens.refresh)
      localStorage.setItem('user', JSON.stringify(data.user))
    },
    async register(userData: any) {
      const data: any = await api.post('/users/register/', userData)
      this.token = data.tokens.access
      this.user = data.user
      localStorage.setItem('access_token', data.tokens.access)
      localStorage.setItem('refresh_token', data.tokens.refresh)
      localStorage.setItem('user', JSON.stringify(data.user))
    },
    logout() {
      this.token = ''
      this.user = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
    }
  }
})
