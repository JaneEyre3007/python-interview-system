<template>
  <div class="max-w-4xl mx-auto space-y-6 animate-in">
    <div class="rounded-xl overflow-hidden" style="background: #FFFFFF; border: 1px solid #E5E7EB;">
      <div class="h-1" style="background: linear-gradient(90deg, #2563EB, #7C3AED 60%, #059669);"></div>
      <div class="p-6 sm:p-8 text-center">
        <div class="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4" style="background: #EFF6FF; color: #2563EB;"><TrophyIcon class="w-8 h-8" /></div>
        <h1 class="text-xl sm:text-2xl font-bold mb-1" style="color: #111827;">考试成绩</h1>
        <p class="text-sm mb-6" style="color: #9CA3AF;">{{ result?.exam?.title }}</p>
        <div class="grid grid-cols-3 gap-3 max-w-md mx-auto mb-6">
          <div class="p-4 rounded-xl text-center" style="background: #F9FAFB; border: 1px solid #E5E7EB;">
            <p class="text-[11px] font-medium uppercase tracking-wider mb-1" style="color: #9CA3AF;">总分</p>
            <p class="text-2xl font-black number-transition" style="color: #2563EB; font-variant-numeric: tabular-nums;">{{ result?.total_score ?? '—' }}</p>
          </div>
          <div class="p-4 rounded-xl text-center" style="background: #F9FAFB; border: 1px solid #E5E7EB;">
            <p class="text-[11px] font-medium uppercase tracking-wider mb-1" style="color: #9CA3AF;">正确</p>
            <p class="text-2xl font-black number-transition" style="color: #059669; font-variant-numeric: tabular-nums;">{{ result?.correct_count ?? 0 }} <span class="text-sm font-normal" style="color: #9CA3AF;">/ {{ result?.answers?.length ?? 0 }}</span></p>
          </div>
          <div class="p-4 rounded-xl text-center" style="background: #F9FAFB; border: 1px solid #E5E7EB;">
            <p class="text-[11px] font-medium uppercase tracking-wider mb-1" style="color: #9CA3AF;">正确率</p>
            <p class="text-2xl font-black number-transition" :style="{ color: accuracyColor, fontVariantNumeric: 'tabular-nums' }">{{ accuracy }}%</p>
          </div>
        </div>
        <div class="flex flex-wrap justify-center gap-2">
          <n-button type="primary" size="small" @click="$router.push('/exams')" class="!rounded-lg !px-6 !font-medium"><template #icon><RotateCwIcon class="w-3.5 h-3.5" /></template>再来一次</n-button>
          <n-button quaternary size="small" @click="$router.push('/history')" class="!rounded-lg !px-6 !font-medium"><template #icon><HistoryIcon class="w-3.5 h-3.5" /></template>考试历史</n-button>
        </div>
      </div>
    </div>

    <div class="space-y-3">
      <h2 class="text-sm font-bold px-1" style="color: #111827;">逐题分析</h2>
      <div v-for="(ans, idx) in result?.answers" :key="ans.id" class="rounded-xl overflow-hidden animate-in" :style="{ animationDelay: `${Number(idx) * 0.05}s`, background: '#FFFFFF', border: '1px solid #E5E7EB' }">
        <div class="p-4 sm:p-5">
          <div class="flex items-start gap-3">
            <div class="w-6 h-6 rounded flex items-center justify-center shrink-0 mt-0.5" :style="ans.is_correct ? 'background: #ECFDF5; color: #059669;' : 'background: #FEF2F2; color: #DC2626;'">
              <CheckCircleIcon v-if="ans.is_correct" class="w-3.5 h-3.5" /><XCircleIcon v-else class="w-3.5 h-3.5" />
            </div>
            <div class="flex-1 min-w-0 space-y-3">
              <div class="flex flex-wrap items-center gap-2">
                <span class="text-[11px] font-medium" style="color: #9CA3AF;">第 {{ Number(idx) + 1 }} 题</span>
                <span class="text-[11px] font-medium" style="color: #2563EB;">{{ ans.question_type }}</span>
                <n-tag size="small" :type="ans.is_correct ? 'success' : 'error'" round>{{ ans.score }} 分</n-tag>
              </div>
              <p class="text-sm font-medium leading-relaxed" style="color: #111827;">{{ ans.question_content }}</p>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-2.5">
                <div class="p-3 rounded-lg" style="background: #F9FAFB; border: 1px solid #E5E7EB;">
                  <p class="text-[11px] font-semibold mb-1.5 uppercase tracking-wider" style="color: #9CA3AF;">你的答案</p>
                  <p class="text-xs leading-relaxed" :class="ans.user_answer ? '' : 'italic'" :style="{ color: ans.user_answer ? '#4B5563' : '#9CA3AF', whiteSpace: 'pre-wrap', wordBreak: 'break-word' }">{{ ans.user_answer || '未作答' }}</p>
                </div>
                <div class="p-3 rounded-lg" :style="{ background: ans.is_correct ? '#ECFDF5' : '#FEF2F2', border: `1px solid ${ans.is_correct ? '#059669' : '#DC2626'}` }">
                  <p class="text-[11px] font-semibold mb-1.5 uppercase tracking-wider" :style="{ color: ans.is_correct ? '#059669' : '#DC2626' }">AI 反馈</p>
                  <p class="text-xs leading-relaxed" style="color: #4B5563; white-space: pre-wrap; word-break: break-word;">{{ ans.ai_feedback || 'AI 正在生成反馈...' }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="!result" class="rounded-xl p-12 flex items-center justify-center" style="background: #FFFFFF; border: 1px solid #E5E7EB;">
      <div class="text-center"><div class="spinner mx-auto mb-3"></div><p class="text-sm" style="color: #9CA3AF;">加载成绩中...</p></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue"
import { useRoute } from "vue-router"
import { TrophyIcon, CheckCircleIcon, XCircleIcon, RotateCwIcon, HistoryIcon } from "lucide-vue-next"
import api from "@/api"

const route = useRoute()
const result = ref<any>(null)
const accuracy = computed(() => { if (!result.value?.answers?.length) return 0; return Math.round((result.value.correct_count / result.value.answers.length) * 100) })
const accuracyColor = computed(() => { if (accuracy.value >= 80) return '#059669'; if (accuracy.value >= 60) return '#D97706'; return '#DC2626' })
onMounted(async () => { try { result.value = await api.get("/exams/" + route.params.id + "/result/") } catch (e) { console.error(e) } })
</script>
