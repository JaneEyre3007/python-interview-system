import { ref, onMounted, onUnmounted } from "vue"
import { useAuthStore } from "@/stores/auth"
import api from "@/api"

function parseJwt(token: string): { exp: number } | null {
  try {
    const base64 = token.split(".")[1].replace(/-/g, "+").replace(/_/g, "/")
    return JSON.parse(atob(base64))
  } catch {
    return null
  }
}

export function useTokenRefresh() {
  const authStore = useAuthStore()
  const lastActivity = ref(Date.now())
  const REFRESH_BEFORE_EXPIRY = 10 * 60 * 1000 // 10 minutes in ms
  const CHECK_INTERVAL = 30 * 1000 // 30 seconds
  const IDLE_TIMEOUT = 5 * 60 * 1000 // 5 minutes idle = stop refreshing
  let timerId: ReturnType<typeof setInterval> | null = null

  function recordActivity() {
    lastActivity.value = Date.now()
  }

  async function tryRefresh() {
    const token = localStorage.getItem("access_token")
    if (!token) return

    const payload = parseJwt(token)
    if (!payload?.exp) return

    const expiresAt = payload.exp * 1000
    const now = Date.now()
    const idle = now - lastActivity.value

    if (idle > IDLE_TIMEOUT) return

    if (expiresAt - now < REFRESH_BEFORE_EXPIRY) {
      const refresh = localStorage.getItem("refresh_token")
      if (!refresh) return

      try {
        const data: any = await api.post("/users/token/refresh/", { refresh })
        const newAccess = data.access
        authStore.token = newAccess
        localStorage.setItem("access_token", newAccess)
      } catch {
        authStore.logout()
        window.location.href = "/login"
      }
    }
  }

  function start() {
    document.addEventListener("mousemove", recordActivity, { passive: true })
    document.addEventListener("keydown", recordActivity, { passive: true })
    document.addEventListener("click", recordActivity, { passive: true })
    timerId = setInterval(tryRefresh, CHECK_INTERVAL)
  }

  function stop() {
    document.removeEventListener("mousemove", recordActivity)
    document.removeEventListener("keydown", recordActivity)
    document.removeEventListener("click", recordActivity)
    if (timerId) {
      clearInterval(timerId)
      timerId = null
    }
  }

  onMounted(start)
  onUnmounted(stop)
}
