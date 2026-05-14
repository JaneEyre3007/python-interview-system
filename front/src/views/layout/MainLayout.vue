<template>
  <div class="layout-root" style="min-height: 100vh;">
    <nav class="navbar">
      <div class="navbar__inner">
        <router-link to="/" class="flex items-center gap-2.5 shrink-0">
          <div class="navbar__logo">
            <CodeIcon class="w-3.5 h-3.5" />
          </div>
          <span class="text-sm font-bold hidden sm:inline" style="color: #111827; letter-spacing: -0.02em;">PyInterview</span>
        </router-link>

        <div class="nav-center">
          <router-link
            v-for="item in menuOptions"
            :key="item.key"
            :to="item.path"
            class="navbar__link"
            :class="{ 'navbar__link--active': isActive(item.path) }"
          >
            <component :is="item.icon" class="w-3.5 h-3.5 shrink-0" />
            <span class="hidden lg:inline">{{ item.label }}</span>
          </router-link>
        </div>

        <router-link to="/profile" class="navbar__link">
          <SettingsIcon class="w-3.5 h-3.5 shrink-0" />
          <span class="hidden lg:inline">{{ authStore.user?.username }}</span>
        </router-link>
      </div>
    </nav>

    <main class="main-content">
      <div class="main-content__inner">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, markRaw } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"
import {
  LayoutDashboardIcon,
  BookOpenIcon,
  ClipboardListIcon,
  HistoryIcon,
  BarChart3Icon,
  CodeIcon,
  SettingsIcon,
} from "lucide-vue-next"

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const menuOptions = [
  { label: "工作台", key: "dashboard", path: "/", icon: markRaw(LayoutDashboardIcon) },
  { label: "题库", key: "questions", path: "/questions", icon: markRaw(BookOpenIcon) },
  { label: "考试", key: "exams", path: "/exams", icon: markRaw(ClipboardListIcon) },
  { label: "历史", key: "history", path: "/history", icon: markRaw(HistoryIcon) },
  { label: "统计", key: "stats", path: "/token-stats", icon: markRaw(BarChart3Icon) },
]

const isActive = (path: string) => path === "/" ? route.path === "/" : route.path.startsWith(path)
</script>

<style scoped>
.layout-root {
  background: #F9FAFB;
}

.main-content {
  margin-top: 42px;
  margin-bottom: 32px;
  padding-left: 16px;
  padding-right: 16px;
}
@media (min-width: 640px) {
  .main-content {
    padding-left: 24px;
    padding-right: 24px;
  }
}

.main-content__inner {
  max-width: 1152px;
  margin: 0 auto;
}

.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
  padding: 4px 16px;
}

.navbar__inner {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  padding: 3px 12px;
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 20px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
}

.nav-center {
  display: flex;
  align-items: center;
  gap: 1px;
  flex: 1;
  justify-content: center;
}

.navbar__link {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 3px 8px;
  border-radius: 16px;
  font-size: 11px;
  font-weight: 500;
  color: #9CA3AF;
  transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
  text-decoration: none;
}

.navbar__link:hover {
  color: #4B5563;
  background: #F3F4F6;
}

.navbar__link--active {
  color: #2563EB;
  background: #EFF6FF;
}

.navbar__logo {
  width: 20px;
  height: 20px;
  border-radius: 6px;
  background: linear-gradient(135deg, #2563EB, #7C3AED);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s cubic-bezier(0.4, 0, 0.2, 1);
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
