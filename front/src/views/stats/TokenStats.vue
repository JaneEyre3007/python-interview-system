<template>
  <div class="space-y-5 animate-in">
    <div>
      <h1 class="text-xl font-bold flex items-center gap-2.5" style="color: #111827;">
        <div class="w-8 h-8 rounded-lg flex items-center justify-center shrink-0" style="background: #EFF6FF; color: #2563EB;"><BarChart3Icon class="w-4 h-4" /></div>
        Token 用量统计
      </h1>
      <p class="text-xs mt-1 ml-[42px]" style="color: #9CA3AF;">监控 AI 调用消耗与历史记录</p>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <div v-for="item in summary" :key="item.label" class="stat-card">
        <p class="text-[11px] font-semibold mb-1 uppercase tracking-wider" style="color: #9CA3AF;">{{ item.label }}</p>
        <p class="text-xl sm:text-2xl font-bold number-transition" style="color: #111827; font-variant-numeric: tabular-nums;">{{ item.value.toLocaleString() }}</p>
        <div class="mt-2"><n-progress type="line" :percentage="item.percentage" :show-indicator="false" :status="item.status" :height="4" :border-radius="2" /></div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
      <div class="p-5 rounded-xl" style="background: #FFFFFF; border: 1px solid #E5E7EB;">
        <h2 class="text-xs font-bold mb-4 uppercase tracking-wider" style="color: #4B5563;">每日 Token 用量</h2>
        <div v-if="!hasData" class="h-64 flex items-center justify-center"><p class="text-sm" style="color: #9CA3AF;">暂无数据</p></div>
        <v-chart v-else class="h-64" :option="lineOption" autoresize />
      </div>
      <div class="p-5 rounded-xl" style="background: #FFFFFF; border: 1px solid #E5E7EB;">
        <h2 class="text-xs font-bold mb-4 uppercase tracking-wider" style="color: #4B5563;">调用类型分布</h2>
        <div v-if="!hasData" class="h-64 flex items-center justify-center"><p class="text-sm" style="color: #9CA3AF;">暂无数据</p></div>
        <v-chart v-else class="h-64" :option="pieOption" autoresize />
      </div>
    </div>

    <div class="rounded-xl overflow-hidden" style="background: #FFFFFF; border: 1px solid #E5E7EB;">
      <div class="p-5 pb-3"><h2 class="text-xs font-bold uppercase tracking-wider" style="color: #4B5563;">最近调用记录</h2></div>
      <n-data-table :columns="columns" :data="recentCalls" :loading="loading" size="small" :bordered="false" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue"
import { use } from "echarts/core"
import { CanvasRenderer } from "echarts/renderers"
import { LineChart, PieChart } from "echarts/charts"
import { GridComponent, TooltipComponent, LegendComponent } from "echarts/components"
import VChart from "vue-echarts"
import { BarChart3Icon } from "lucide-vue-next"
import api from "@/api"

use([CanvasRenderer, LineChart, PieChart, GridComponent, TooltipComponent, LegendComponent])

const loading = ref(false)
const statsData = ref<any>(null)
const hasData = computed(() => { const d = statsData.value; return d && (d.total?.total_tokens > 0 || d.daily?.length > 0) })
const typeMap: Record<string, string> = { generate: "生成题目", evaluate: "评判答案" }

const summary = computed(() => {
  const total = statsData.value?.total?.total_tokens || 0
  const prompt = statsData.value?.total?.prompt_tokens || 0
  const completion = statsData.value?.total?.completion_tokens || 0
  const max = Math.max(total, 1)
  return [
    { label: "总 Token 数", value: total, percentage: Math.round((total / max) * 70), status: "success" as const },
    { label: "Prompt Token", value: prompt, percentage: Math.round((prompt / max) * 60), status: "info" as const },
    { label: "Completion Token", value: completion, percentage: Math.round((completion / max) * 40), status: "warning" as const },
  ]
})

const recentCalls = computed(() => (statsData.value?.recent || []).slice(0, 20))

const lineOption = computed(() => ({
  backgroundColor: "transparent",
  tooltip: { trigger: "axis", backgroundColor: "#FFFFFF", borderColor: "#E5E7EB", textStyle: { color: "#111827", fontSize: 12 } },
  grid: { left: "3%", right: "4%", bottom: "3%", top: "8%", containLabel: true },
  xAxis: { type: "category", data: statsData.value?.daily?.map((d: any) => d.date) || [], axisLabel: { fontSize: 10, color: "#9CA3AF" }, axisLine: { lineStyle: { color: "#E5E7EB" } }, axisTick: { show: false } },
  yAxis: { type: "value", axisLabel: { fontSize: 10, color: "#9CA3AF" }, axisLine: { lineStyle: { color: "#E5E7EB" } }, splitLine: { lineStyle: { color: "#F3F4F6", type: "dashed" } } },
  series: [{ name: "Token", type: "line", smooth: true, symbol: "circle", symbolSize: 4, lineStyle: { width: 2, color: "#2563EB" }, itemStyle: { color: "#2563EB" }, areaStyle: { color: { type: "linear", x: 0, y: 0, x2: 0, y2: 1, colorStops: [{ offset: 0, color: "rgba(37, 99, 235, 0.15)" }, { offset: 1, color: "rgba(37, 99, 235, 0)" }] } }, data: statsData.value?.daily?.map((d: any) => d.total_tokens) || [] }],
}))

const pieOption = computed(() => ({
  backgroundColor: "transparent",
  tooltip: { trigger: "item", backgroundColor: "#FFFFFF", borderColor: "#E5E7EB", textStyle: { color: "#111827", fontSize: 12 }, formatter: "{b}: {c} tokens ({d}%)" },
  legend: { bottom: "0", textStyle: { fontSize: 12, color: "#9CA3AF" } },
  series: [{ type: "pie", radius: ["45%", "72%"], center: ["50%", "45%"], avoidLabelOverlap: false, itemStyle: { borderRadius: 6, borderColor: "#FFFFFF", borderWidth: 3 }, label: { show: false }, emphasis: { label: { show: true, fontSize: 13, fontWeight: "bold", color: "#111827" } }, data: [{ value: statsData.value?.generate?.total_tokens || 0, name: "生成题目", itemStyle: { color: "#2563EB" } }, { value: statsData.value?.evaluate?.total_tokens || 0, name: "评判答案", itemStyle: { color: "#059669" } }] }],
}))

const columns = [
  { title: "ID", key: "id", width: 60, render(row: any) { return row.id } },
  { title: "类型", key: "api_type", width: 100, render(row: any) { return typeMap[row.api_type] || row.api_type } },
  { title: "模型", key: "model_name", ellipsis: { tooltip: true } },
  { title: "消耗 Token", key: "total_tokens", width: 100, render(row: any) { return row.total_tokens?.toLocaleString() || "—" } },
  { title: "调用时间", key: "created_at", width: 160, render(row: any) { return new Date(row.created_at).toLocaleString("zh-CN", { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit", second: "2-digit" }) } },
]

onMounted(async () => { loading.value = true; try { statsData.value = await api.get("/ai/token-stats/") } catch (e) { console.error(e) } finally { loading.value = false } })
</script>

<style scoped>
.stat-card { background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 12px; padding: 20px; transition: border-color 0.15s cubic-bezier(0.4, 0, 0.2, 1); }
.stat-card:hover { border-color: #D1D5DB; }
</style>
