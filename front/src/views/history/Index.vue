<template>
  <div class="space-y-5 animate-in">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
      <div>
        <h1 class="text-xl font-bold flex items-center gap-2.5" style="color: #111827;">
          <div class="w-8 h-8 rounded-lg flex items-center justify-center shrink-0" style="background: #EFF6FF; color: #2563EB;"><HistoryIcon class="w-4 h-4" /></div>
          考试历史
        </h1>
        <p class="text-xs mt-1 ml-[42px]" style="color: #9CA3AF;">查看历次考试记录和成绩</p>
      </div>
      <n-button type="primary" size="small" @click="$router.push('/exams')" class="!rounded-lg !font-medium"><template #icon><PlusIcon class="w-3.5 h-3.5" /></template>新建考试</n-button>
    </div>

    <div class="rounded-xl overflow-hidden" style="background: #FFFFFF; border: 1px solid #E5E7EB;">
      <n-data-table :columns="columns" :data="history" :loading="loading" :pagination="pagination" size="small" :bordered="false" :single-line="false" />
      <div v-if="!loading && history.length === 0" class="py-16 text-center">
        <div class="w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3" style="background: #F3F4F6;"><HistoryIcon class="w-5 h-5" style="color: #9CA3AF;" /></div>
        <p class="text-sm font-medium mb-1" style="color: #4B5563;">暂无考试记录</p>
        <p class="text-xs mb-4" style="color: #9CA3AF;">开始你的第一次考试吧</p>
        <n-button type="primary" size="small" @click="$router.push('/exams')" class="!rounded-lg">开始考试</n-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, h } from "vue"
import { useRouter } from "vue-router"
import { NTag, NButton } from "naive-ui"
import { PlusIcon, HistoryIcon } from "lucide-vue-next"
import api from "@/api"

const router = useRouter()
const loading = ref(false)
const history = ref<any[]>([])
const pagination = { pageSize: 10 }
const statusMap: Record<string, string> = { completed: "已完成", in_progress: "进行中", pending: "待开始" }
const statusColorMap: Record<string, "success" | "warning" | "default"> = { completed: "success", in_progress: "warning", pending: "default" }
const diffMap: Record<string, string> = { easy: "简单", medium: "中等", hard: "困难" }

const columns = [
  { title: "ID", key: "id", width: 60, render(row: any) { return h("span", { style: "color: #9CA3AF; font-family: 'JetBrains Mono', monospace; font-size: 12px;" }, `#${row.id}`) } },
  { title: "试卷标题", key: "title", ellipsis: { tooltip: true }, render(row: any) { return h("span", { style: "color: #111827; font-size: 14px; font-weight: 500;" }, row.title) } },
  { title: "题目数", key: "question_count", width: 80, render(row: any) { return h("span", { style: "color: #4B5563; font-variant-numeric: tabular-nums;" }, String(row.questions?.length ?? row.question_count ?? '—')) } },
  { title: "分数", key: "total_score", width: 70, render(row: any) { const score = row.total_score; if (score == null) { return h("span", { style: "#9CA3AF" }, "—") } const color = score >= 90 ? "#059669" : score >= 60 ? "#2563EB" : "#DC2626"; return h("span", { style: `font-weight: 700; color: ${color}; font-variant-numeric: tabular-nums;` }, String(score)) } },
  { title: "状态", key: "status", width: 80, render(row: any) { const type = statusColorMap[row.status] || "default"; return h(NTag, { type, round: true, size: "small", bordered: false }, { default: () => statusMap[row.status] || row.status }) } },
  { title: "难度", key: "difficulty", width: 80, render(row: any) { if (!row.difficulty || row.difficulty === "mixed") { return h("span", { style: "color: #9CA3AF; font-size: 12px;" }, "综合") } return h("span", { style: "color: #4B5563; font-size: 12px;" }, diffMap[row.difficulty] || row.difficulty) } },
  { title: "时间", key: "created_at", width: 150, render(row: any) { return h("span", { style: "color: #9CA3AF; font-size: 12px;" }, new Date(row.created_at).toLocaleString("zh-CN", { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" })) } },
  { title: "操作", key: "actions", width: 70, render(row: any) { return h(NButton, { size: "tiny", type: row.status === "completed" ? "primary" : "warning", quaternary: true, onClick: () => router.push(row.status === "completed" ? "/result/" + row.id : "/exam/" + row.id) }, { default: () => row.status === "completed" ? "查看" : "继续" }) } },
]

onMounted(async () => { loading.value = true; try { const d: any = await api.get("/exams/"); history.value = d.results || [] } catch (e) { console.error(e) } finally { loading.value = false } })
</script>
