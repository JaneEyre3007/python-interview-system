<template>
  <div class="h-full flex flex-col max-w-4xl mx-auto space-y-4 animate-in">
    <div class="flex items-center justify-between p-4 rounded-xl shrink-0" style="background: #FFFFFF; border: 1px solid #E5E7EB;">
      <div class="flex items-center gap-2.5 min-w-0">
        <n-button quaternary circle size="small" @click="$router.back()" class="shrink-0"><template #icon><ArrowLeftIcon class="w-4 h-4" /></template></n-button>
        <div class="min-w-0">
          <h1 class="text-sm font-bold truncate" style="color: #111827;">{{ exam?.title }}</h1>
          <p class="text-[11px]" style="color: #9CA3AF;">第 {{ currentIndex + 1 }} / {{ exam?.questions?.length }} 题</p>
        </div>
      </div>
      <div class="flex items-center gap-2 shrink-0">
        <div class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg" :style="timerBgStyle">
          <ClockIcon class="w-3 h-3" :style="{ color: timerColor }" />
          <span class="font-mono font-bold text-xs" :style="{ color: timerColor, fontVariantNumeric: 'tabular-nums' }">{{ formattedTime }}</span>
        </div>
        <n-button type="primary" secondary size="small" @click="handleFinish" class="!font-medium">交卷</n-button>
      </div>
    </div>

    <div class="shrink-0"><n-progress type="line" :percentage="progressPercentage" :show-indicator="false" :status="progressPercentage === 100 ? 'success' : 'info'" processing :height="4" :border-radius="2" /></div>

    <div v-if="currentQuestion" class="flex-1 rounded-xl p-5 sm:p-7 overflow-y-auto" style="background: #FFFFFF; border: 1px solid #E5E7EB;">
      <div class="mb-6">
        <div class="flex flex-wrap items-center gap-2 mb-3">
          <n-tag :type="difficultyTagType" size="small" round>{{ diffMap[currentQuestion.question.difficulty] ?? currentQuestion.question.difficulty }}</n-tag>
          <n-tag size="small" quaternary>{{ typeMap[currentQuestion.question.type] ?? currentQuestion.question.type }}</n-tag>
          <n-tag v-if="currentQuestion.question.category" size="small" quaternary>{{ currentQuestion.question.category }}</n-tag>
        </div>
        <h2 class="text-base sm:text-lg font-bold leading-relaxed" style="color: #111827;">{{ currentQuestion.question.content }}</h2>
      </div>

      <div v-if="currentQuestion.question.type === 'choice'" class="space-y-2.5">
        <div v-for="(label, key) in currentQuestion.question.options" :key="key" @click="userAnswer = String(key)" @keydown.enter="userAnswer = String(key)" @keydown.space.prevent="userAnswer = String(key)" class="option-card flex items-center p-3.5 rounded-xl cursor-pointer" :class="{ 'option-card--selected': userAnswer === String(key) }" tabindex="0" role="radio" :aria-checked="userAnswer === String(key)">
          <div class="option-card__label w-8 h-8 rounded-lg flex items-center justify-center font-bold text-sm mr-3 shrink-0">{{ key }}</div>
          <span class="text-sm flex-1" style="color: #111827;">{{ label }}</span>
          <div v-if="userAnswer === String(key)" class="w-5 h-5 rounded-full flex items-center justify-center shrink-0" style="background: #2563EB; color: #FFFFFF;"><CheckIcon class="w-3 h-3" /></div>
        </div>
      </div>

      <div v-else class="space-y-3">
        <n-input v-model:value="userAnswer" type="textarea" :placeholder="placeholderText" :autosize="{ minRows: currentQuestion.question.type === 'code' ? 11 : 5 }" class="font-mono text-sm" />
        <div class="flex items-start gap-2 p-3 rounded-lg" style="background: #EFF6FF; border: 1px solid #E5E7EB;">
          <InfoIcon class="w-3.5 h-3.5 mt-0.5 shrink-0" style="color: #2563EB;" />
          <p class="text-[11px] leading-relaxed" style="color: #4B5563;">{{ currentQuestion.question.type === 'code' ? '请在编辑器中输入完整的 Python 代码。提交后由 AI 对代码正确性和代码风格进行评判。' : '提交后由 AI 对你的答案进行评判并给出反馈。' }}</p>
        </div>
      </div>
    </div>

    <div v-else class="flex-1 rounded-xl p-7 flex items-center justify-center" style="background: #FFFFFF; border: 1px solid #E5E7EB;">
      <div class="text-center"><div class="spinner mx-auto mb-3"></div><p class="text-sm" style="color: #9CA3AF;">加载试卷中...</p></div>
    </div>

    <div class="flex items-center justify-between pb-4 shrink-0">
      <n-button quaternary size="small" :disabled="currentIndex === 0" @click="navigate(-1)"><template #icon><ChevronLeftIcon class="w-4 h-4" /></template>上一题</n-button>
      <div class="hidden sm:flex items-center gap-1.5">
        <button v-for="(_, idx) in exam?.questions" :key="idx" @click="goToQuestion(Number(idx))" class="w-2 h-2 rounded-full transition-all" :class="idx === currentIndex ? 'w-3 h-3' : ''" :style="idx === currentIndex ? 'background: #2563EB;' : 'background: #E5E7EB;'" :title="`第 ${Number(idx) + 1} 题`"></button>
      </div>
      <n-button type="primary" :loading="submitting" @click="handleSubmit" class="!rounded-lg !px-8 !font-semibold">{{ isLastQuestion ? '提交并交卷' : '提交答案' }}</n-button>
      <n-button quaternary size="small" :disabled="isLastQuestion" @click="navigate(1)" class="sm:hidden">跳过</n-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { ArrowLeftIcon, ClockIcon, CheckIcon, ChevronLeftIcon, InfoIcon } from "lucide-vue-next"
import { useDialog, useMessage } from "naive-ui"
import api from "@/api"

const route = useRoute()
const router = useRouter()
const dialog = useDialog()
const message = useMessage()
const exam = ref<any>(null)
const currentIndex = ref(0)
const userAnswer = ref("")
const submitting = ref(false)
const seconds = ref(0)
let timer: ReturnType<typeof setInterval> | null = null

const typeMap: Record<string, string> = { choice: "选择题", fill: "填空题", code: "编程题", short: "简答题" }
const diffMap: Record<string, string> = { easy: "简单", medium: "中等", hard: "困难" }
const currentQuestion = computed(() => exam.value?.questions?.[currentIndex.value])
const isLastQuestion = computed(() => currentIndex.value === (exam.value?.questions?.length ?? 1) - 1)
const progressPercentage = computed(() => { if (!exam.value?.questions?.length) return 0; return Math.round(((currentIndex.value + 1) / exam.value.questions.length) * 100) })
const difficultyTagType = computed(() => { const d = currentQuestion.value?.question?.difficulty; if (d === "easy") return "success"; if (d === "hard") return "error"; return "warning" })
const placeholderText = computed(() => { const t = currentQuestion.value?.question?.type; if (t === "code") return "# 在此输入你的 Python 代码...\n\n"; if (t === "fill") return "输入答案..."; return "在此输入你的回答..." })
const formattedTime = computed(() => { const h = Math.floor(seconds.value / 3600); const m = Math.floor((seconds.value % 3600) / 60); const s = seconds.value % 60; return [h, m, s].map(v => String(v).padStart(2, "0")).join(":") })
const timerWarning = computed(() => seconds.value > 3600)
const timerColor = computed(() => timerWarning.value ? "#D97706" : "#111827")
const timerBgStyle = computed(() => ({ background: timerWarning.value ? "#FFFBEB" : "#F3F4F6", border: timerWarning.value ? "1px solid #D97706" : "1px solid transparent", transition: "all 0.3s cubic-bezier(0, 0, 0.2, 1)" }))

async function fetchExam() { try { const d: any = await api.get("/exams/" + route.params.id + "/"); exam.value = d; if (d.status === "pending") { await api.post("/exams/" + route.params.id + "/start/") } loadCurrentAnswer() } catch (e) { console.error(e) } }
function loadCurrentAnswer() { const a = exam.value?.answers?.find((a: any) => a.question === currentQuestion.value?.question?.id); userAnswer.value = a?.user_answer || "" }
async function handleSubmit() { if (!userAnswer.value.trim()) { message.warning("请先作答"); return } submitting.value = true; try { await api.post("/exams/" + route.params.id + "/submit_answer/", { question_id: currentQuestion.value.question.id, answer: userAnswer.value }); if (isLastQuestion.value) { await doFinish() } else { currentIndex.value++; loadCurrentAnswer() } } catch (e) { console.error(e) } finally { submitting.value = false } }
function navigate(delta: number) { const newIdx = currentIndex.value + delta; if (newIdx < 0 || newIdx >= (exam.value?.questions?.length ?? 0)) return; currentIndex.value = newIdx; loadCurrentAnswer() }
function goToQuestion(idx: number) { currentIndex.value = idx; loadCurrentAnswer() }
async function doFinish() { await api.post("/exams/" + route.params.id + "/finish/"); router.push("/result/" + route.params.id) }
function handleFinish() { dialog.warning({ title: "确认交卷", content: "确定要提交试卷吗？提交后无法修改答案。", positiveText: "确定交卷", negativeText: "继续答题", onPositiveClick: doFinish }) }
onMounted(() => { fetchExam(); timer = setInterval(() => seconds.value++, 1000) })
onUnmounted(() => { if (timer) clearInterval(timer) })
</script>

<style scoped>
.option-card { border: 2px solid #E5E7EB; transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1); outline: none; background: #FFFFFF; }
.option-card:hover:not(.option-card--selected) { border-color: #D1D5DB; background: #F9FAFB; }
.option-card:focus-visible { outline: 2px solid #2563EB; outline-offset: 2px; }
.option-card--selected { border-color: #2563EB; background: #EFF6FF; }
.option-card--selected .option-card__label { background: #2563EB; color: #FFFFFF; }
.option-card__label { background: #F3F4F6; color: #4B5563; transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1); }
</style>
