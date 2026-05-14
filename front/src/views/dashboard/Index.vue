<template>
  <div class="dashboard-root space-y-6 animate-in">
    <!-- Welcome -->
    <div>
      <h1 class="text-2xl font-bold" style="color: #111827; letter-spacing: -0.02em;">
        {{ greeting }}，<span style="color: #2563EB;">{{ authStore.user?.username }}</span>
      </h1>
      <p class="text-sm mt-1" style="color: #6B7280;">今天想练习什么？</p>
    </div>

    <!-- Quick Entry Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <button
        v-for="entry in quickEntries"
        :key="entry.label"
        @click="$router.push(entry.path)"
        class="quick-card group text-left"
      >
        <div class="flex items-start gap-3.5">
          <div class="p-2 rounded-lg shrink-0" :style="entry.iconBg">
            <component :is="entry.icon" class="w-5 h-5" :style="{ color: entry.iconColor }" />
          </div>
          <div class="min-w-0">
            <p class="text-sm font-semibold mb-0.5" style="color: #111827;">{{ entry.label }}</p>
            <p class="text-xs" style="color: #6B7280;">{{ entry.desc }}</p>
          </div>
        </div>
      </button>
    </div>

    <!-- Stats Grid -->
    <div class="grid-stats">
      <div v-for="(stat, idx) in stats" :key="idx" class="stat-card">
        <div class="flex items-center justify-between mb-3">
          <div class="stat-icon" :style="stat.iconBg">
            <component :is="stat.icon" class="w-4 h-4" :style="{ color: stat.iconColor }" />
          </div>
        </div>
        <p class="stat-value number-transition">{{ stat.value }}</p>
        <p class="stat-label">{{ stat.label }}</p>
      </div>
    </div>

    <!-- Recent Exams -->
    <div class="recent-exams-card rounded-xl overflow-hidden">
      <div class="px-5 py-4 flex items-center justify-between" style="border-bottom: 1px solid #E5E7EB;">
        <h2 class="text-sm font-bold" style="color: #111827;">最近考试</h2>
        <button
          @click="$router.push('/history')"
          class="view-all-btn text-xs font-medium flex items-center gap-1"
        >
          查看全部
          <ArrowRightIcon class="w-3.5 h-3.5" />
        </button>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="p-10 text-center">
        <div class="spinner-light mx-auto mb-3"></div>
        <p class="text-xs" style="color: #9CA3AF;">加载中...</p>
      </div>

      <!-- Empty -->
      <div v-else-if="recentExams.length === 0" class="p-10 text-center">
        <div class="w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3" style="background: #F3F4F6;">
          <ClipboardListIcon class="w-5 h-5" style="color: #9CA3AF;" />
        </div>
        <p class="text-sm font-medium mb-1" style="color: #4B5563;">暂无考试记录</p>
        <p class="text-xs mb-4" style="color: #9CA3AF;">开始你的第一次考试吧</p>
        <n-button type="primary" size="small" @click="$router.push('/exams')" class="!rounded-lg">
          开始考试
        </n-button>
      </div>

      <!-- Exam List -->
      <div v-else>
        <div
          v-for="(exam, i) in recentExams"
          :key="exam.id"
          class="exam-row px-5 py-3.5 flex items-center justify-between cursor-pointer"
          :style="i !== recentExams.length - 1 ? 'border-bottom: 1px solid #F3F4F6;' : ''"
          @click="router.push(exam.status === 'completed' ? '/result/' + exam.id : '/exam/' + exam.id)"
        >
          <div class="flex items-center gap-3 min-w-0">
            <div
              class="w-8 h-8 rounded-lg flex items-center justify-center shrink-0"
              :style="exam.status === 'completed'
                ? 'background: #ECFDF5; color: #059669;'
                : 'background: #F3F4F6; color: #9CA3AF;'"
            >
              <CheckIcon v-if="exam.status === 'completed'" class="w-4 h-4" />
              <ClockIcon v-else class="w-4 h-4" />
            </div>
            <div class="min-w-0">
              <p class="text-sm font-medium truncate" style="color: #111827;">{{ exam.title }}</p>
              <p class="text-[11px]" style="color: #9CA3AF;">{{ formatDate(exam.created_at) }}</p>
            </div>
          </div>
          <div class="flex items-center gap-3 shrink-0">
            <span class="text-[11px] font-medium" style="color: #9CA3AF;">{{ statusMap[exam.status] }}</span>
            <span v-if="exam.status === 'completed'" class="text-sm font-bold number-transition" style="color: #2563EB;">
              {{ exam.total_score }}分
            </span>
            <ChevronRightIcon class="w-4 h-4" style="color: #D1D5DB;" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, markRaw } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"
import {
  ClipboardListIcon, BookOpenIcon, SettingsIcon,
  LayoutDashboardIcon, CheckCircle2Icon, TargetIcon,
  BrainCircuitIcon, CheckIcon, ClockIcon,
  ArrowRightIcon, ChevronRightIcon
} from "lucide-vue-next"
import api from "@/api"

const router = useRouter()
const authStore = useAuthStore()
const loading = ref(false)
const recentExams = ref<any[]>([])

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 6) return "夜深了"
  if (h < 12) return "早上好"
  if (h < 18) return "下午好"
  return "晚上好"
})

const stats = ref([
  { label: "题库总数", value: "—", icon: markRaw(BookOpenIcon), iconBg: "background: #EFF6FF;", iconColor: "#3B82F6" },
  { label: "已完成考试", value: "—", icon: markRaw(CheckCircle2Icon), iconBg: "background: #ECFDF5;", iconColor: "#059669" },
  { label: "平均分", value: "—", icon: markRaw(TargetIcon), iconBg: "background: #FFFBEB;", iconColor: "#D97706" },
  { label: "总答题数", value: "—", icon: markRaw(BrainCircuitIcon), iconBg: "background: #F5F3FF;", iconColor: "#7C3AED" },
])

const quickEntries = [
  { label: "开始考试", desc: "随机抽题，模拟面试", path: "/exams", icon: markRaw(ClipboardListIcon), iconBg: "background: #EFF6FF;", iconColor: "#3B82F6" },
  { label: "题库管理", desc: "查看、导入、编辑题目", path: "/questions", icon: markRaw(BookOpenIcon), iconBg: "background: #F5F3FF;", iconColor: "#7C3AED" },
  { label: "AI 配置", desc: "设置 API 密钥和模型", path: "/ai-config", icon: markRaw(SettingsIcon), iconBg: "background: #FFFBEB;", iconColor: "#D97706" },
]

const statusMap: Record<string, string> = { completed: "已完成", in_progress: "进行中", pending: "待开始" }

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString('zh-CN', { month: 'long', day: 'numeric' })
}

onMounted(async () => {
  loading.value = true
  try {
    const data: any = await api.get("/exams/")
    recentExams.value = (data.results || []).slice(0, 5)
    const completed = (data.results || []).filter((e: any) => e.status === "completed")
    stats.value[1].value = String(completed.length)
    stats.value[3].value = String(data.results?.length || 0)
    if (completed.length > 0) {
      stats.value[2].value = Math.round(completed.reduce((s: number, e: any) => s + (e.total_score || 0), 0) / completed.length) + ""
    }
  } catch (e) { console.error(e) } finally { loading.value = false }
  try { const q: any = await api.get("/questions/", { params: { page_size: 1 } }); stats.value[0].value = String(q.count || 0) } catch (e) {}
})
</script>

<style scoped>
.dashboard-root {
  background: #F9FAFB;
  min-height: calc(100vh - 80px);
  padding: 24px;
  border-radius: 12px;
}

.quick-card {
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
}
.quick-card:hover {
  border-color: #D1D5DB;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
}

.stat-card {
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  padding: 20px;
  transition: border-color 0.15s cubic-bezier(0.4, 0, 0.2, 1);
}
.stat-card:hover {
  border-color: #D1D5DB;
}
.stat-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #111827;
  letter-spacing: -0.02em;
}
.stat-label {
  font-size: 12px;
  font-weight: 500;
  color: #9CA3AF;
  letter-spacing: 0.02em;
  margin-top: 4px;
}

.recent-exams-card {
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
}

.grid-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}
@media (max-width: 1024px) {
  .grid-stats { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 640px) {
  .grid-stats { grid-template-columns: 1fr; }
}

.view-all-btn {
  color: #9CA3AF;
  transition: color 0.15s cubic-bezier(0.4, 0, 0.2, 1);
}
.view-all-btn:hover {
  color: #2563EB;
}

.exam-row {
  transition: background 0.15s cubic-bezier(0.4, 0, 0.2, 1);
}
.exam-row:hover {
  background: #F9FAFB;
}

.spinner-light {
  width: 16px;
  height: 16px;
  border: 2px solid #E5E7EB;
  border-top-color: #2563EB;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
