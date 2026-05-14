<template>
  <div class="space-y-6 animate-in">
    <div>
      <h1 class="text-xl font-bold" style="color: #111827; letter-spacing: -0.02em;">开始考试</h1>
      <p class="text-xs mt-0.5" style="color: #9CA3AF;">自定义考试参数或快速开始练习</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-5 gap-6">
      <div class="lg:col-span-3 p-6 rounded-xl" style="background: #FFFFFF; border: 1px solid #E5E7EB;">
        <div class="flex items-center gap-2.5 mb-5">
          <div class="p-1.5 rounded-lg" style="background: #EFF6FF;"><SettingsIcon class="w-4 h-4" style="color: #2563EB;" /></div>
          <h2 class="text-sm font-bold" style="color: #111827;">自定义组卷</h2>
        </div>
        <n-form :model="examForm" label-placement="top" size="small">
          <n-form-item label="试卷标题"><n-input v-model:value="examForm.title" placeholder="例如：Python 进阶练习" maxlength="50" show-count /></n-form-item>
          <div class="grid grid-cols-2 gap-3">
            <n-form-item label="题目数量"><n-input-number v-model:value="examForm.question_count" :min="1" :max="50" class="w-full" /></n-form-item>
            <n-form-item label="难度"><n-select v-model:value="examForm.difficulty" :options="difficultyOptions" /></n-form-item>
          </div>
          <n-form-item label="题目类型"><n-select v-model:value="examForm.question_type" :options="typeOptions" /></n-form-item>
          <n-button type="primary" block :loading="loading" @click="handleCreateExam" class="!rounded-lg !font-semibold !h-10">
            <template #icon><SparklesIcon class="w-4 h-4" /></template>生成试卷
          </n-button>
        </n-form>
      </div>

      <div class="lg:col-span-2 space-y-3">
        <h2 class="text-sm font-bold px-1" style="color: #111827;">快速开始</h2>
        <div v-for="opt in quickOptions" :key="opt.title" @click="startQuick(opt)" class="quick-card cursor-pointer" style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 12px; padding: 16px;">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="p-2 rounded-lg shrink-0" :style="opt.bgStyle"><component :is="opt.icon" class="w-4 h-4" :style="{ color: opt.iconColor }" /></div>
              <div>
                <p class="font-semibold text-sm" style="color: #111827;">{{ opt.title }}</p>
                <p class="text-[11px]" style="color: #9CA3AF;">{{ opt.desc }}</p>
              </div>
            </div>
            <ChevronRightIcon class="w-4 h-4 shrink-0" style="color: #9CA3AF;" />
          </div>
        </div>
      </div>
    </div>

    <div v-if="recentExams.length > 0" class="p-6 rounded-xl" style="background: #FFFFFF; border: 1px solid #E5E7EB;">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-sm font-bold" style="color: #111827;">最近的考试</h2>
        <n-button quaternary type="primary" size="small" @click="$router.push('/history')">查看全部<template #icon><ChevronRightIcon class="w-3.5 h-3.5" /></template></n-button>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        <div v-for="exam in recentExams" :key="exam.id" class="recent-exam-card rounded-lg p-4">
          <div class="flex justify-between items-start mb-2">
            <n-tag :type="exam.status === 'completed' ? 'success' : 'warning'" round size="small">{{ statusMap[exam.status] || exam.status }}</n-tag>
            <p class="text-[11px]" style="color: #9CA3AF;">{{ formatDate(exam.created_at) }}</p>
          </div>
          <h3 class="font-medium text-sm mb-2 line-clamp-1" style="color: #111827;">{{ exam.title }}</h3>
          <div class="flex items-center justify-between">
            <p class="text-[11px]" style="color: #9CA3AF;">{{ exam.questions?.length || 0 }} 道题</p>
            <n-button v-if="exam.status === 'completed'" quaternary size="tiny" type="primary" @click="$router.push('/result/' + exam.id)">查看结果</n-button>
            <n-button v-else type="primary" size="tiny" @click="$router.push('/exam/' + exam.id)">继续</n-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, markRaw } from "vue"
import { useRouter } from "vue-router"
import { SettingsIcon, ChevronRightIcon, SparklesIcon, ZapIcon, TargetIcon, LayersIcon } from "lucide-vue-next"
import { useMessage } from "naive-ui"
import api from "@/api"

const router = useRouter()
const message = useMessage()
const loading = ref(false)
const recentExams = ref<any[]>([])
const statusMap: Record<string, string> = { completed: "已完成", in_progress: "进行中", pending: "待开始" }
const examForm = reactive({ title: "Python 练习", question_count: 10, question_type: "mixed", difficulty: "mixed" })
const difficultyOptions = [{ label: "综合", value: "mixed" }, { label: "简单", value: "easy" }, { label: "中等", value: "medium" }, { label: "困难", value: "hard" }]
const typeOptions = [{ label: "综合", value: "mixed" }, { label: "选择题", value: "choice" }, { label: "填空题", value: "fill" }, { label: "编程题", value: "code" }, { label: "简答题", value: "short" }]
const quickOptions = [
  { title: "快速热身", desc: "5 道简单题 · 快速上手", icon: markRaw(ZapIcon), bgStyle: "background: #FFFBEB;", iconColor: "#D97706", data: { title: "快速热身", question_count: 5, difficulty: "easy", question_type: "mixed" } },
  { title: "标准练习", desc: "10 道中等题 · 系统练习", icon: markRaw(TargetIcon), bgStyle: "background: #EFF6FF;", iconColor: "#2563EB", data: { title: "标准练习", question_count: 10, difficulty: "medium", question_type: "mixed" } },
  { title: "挑战模式", desc: "15 道困难题 · 深度挑战", icon: markRaw(LayersIcon), bgStyle: "background: #FEF2F2;", iconColor: "#DC2626", data: { title: "挑战模式", question_count: 15, difficulty: "hard", question_type: "mixed" } },
]
function formatDate(dateStr: string): string { const d = new Date(dateStr); const now = new Date(); const diff = now.getTime() - d.getTime(); const days = Math.floor(diff / (1000 * 60 * 60 * 24)); if (days === 0) return "今天"; if (days === 1) return "昨天"; if (days < 7) return `${days} 天前`; return d.toLocaleDateString("zh-CN", { month: "short", day: "numeric" }) }
const handleCreateExam = async () => { if (!examForm.title.trim()) { message.warning("请输入试卷标题"); return } loading.value = true; try { const d: any = await api.post("/exams/create_exam/", examForm); message.success("试卷已生成"); router.push("/exam/" + d.id) } catch (e) { console.error(e) } finally { loading.value = false } }
const startQuick = async (opt: any) => { loading.value = true; try { const d: any = await api.post("/exams/create_exam/", opt.data); router.push("/exam/" + d.id) } catch (e) { console.error(e) } finally { loading.value = false } }
onMounted(async () => { try { const d: any = await api.get("/exams/"); recentExams.value = (d.results || []).slice(0, 6) } catch (e) { console.error(e) } })
</script>

<style scoped>
.quick-card { transition: border-color 0.15s cubic-bezier(0.4, 0, 0.2, 1); }
.quick-card:hover { border-color: #D1D5DB; }
.recent-exam-card { border: 1px solid #E5E7EB; transition: border-color 0.15s cubic-bezier(0.4, 0, 0.2, 1); }
.recent-exam-card:hover { border-color: #D1D5DB; }
</style>
