<template>
  <div class="space-y-5 animate-in">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-3">
      <div>
        <h1 class="text-xl font-bold flex items-center gap-2.5" style="color: #111827;">
          <div class="w-8 h-8 rounded-lg flex items-center justify-center text-white shrink-0"
            style="background: linear-gradient(135deg, #7C3AED, #2563EB);">
            <FileQuestionIcon class="w-4 h-4" />
          </div>
          题库管理
        </h1>
        <p class="text-xs mt-1 ml-[42px]" style="color: #9CA3AF;">{{ isAdmin ? '管理员模式：可管理全部题目及上线' : '我的题库 + 已上线题库' }}</p>
      </div>
      <div class="flex flex-wrap items-center gap-2">
        <n-button size="small" @click="showImport = true" quaternary class="!rounded-lg !font-medium">
          <template #icon><UploadIcon class="w-3.5 h-3.5" /></template>
          导入
        </n-button>
        <n-button size="small" type="primary" @click="showAdd = true" class="!rounded-lg !font-medium">
          <template #icon><PlusIcon class="w-3.5 h-3.5" /></template>
          添加题目
        </n-button>
        <n-button size="small" type="primary" secondary @click="showAIModal = true" class="!rounded-lg !font-medium">
          <template #icon><SparklesIcon class="w-3.5 h-3.5" /></template>
          AI 生成
        </n-button>
      </div>
    </div>

    <div class="p-4 rounded-xl" style="background: #FFFFFF; border: 1px solid #E5E7EB;">
      <div class="flex flex-wrap items-end gap-3">
        <div class="w-full sm:w-40">
          <p class="text-[11px] font-semibold mb-1.5 uppercase tracking-wider" style="color: #9CA3AF;">题目类型</p>
          <n-select v-model:value="filters.type" :options="typeOptions" clearable placeholder="全部" size="small" />
        </div>
        <div class="w-full sm:w-40">
          <p class="text-[11px] font-semibold mb-1.5 uppercase tracking-wider" style="color: #9CA3AF;">难度</p>
          <n-select v-model:value="filters.difficulty" :options="difficultyOptions" clearable placeholder="全部" size="small" />
        </div>
        <div class="w-full sm:w-40">
          <p class="text-[11px] font-semibold mb-1.5 uppercase tracking-wider" style="color: #9CA3AF;">题库名</p>
          <n-select v-model:value="filters.bank_name" :options="bankNameOptions" clearable filterable placeholder="全部" size="small" />
        </div>
        <n-button @click="fetchQuestions" type="primary" size="small" class="sm:ml-auto !rounded-lg !font-medium !px-6">
          <template #icon><SearchIcon class="w-3.5 h-3.5" /></template>
          筛选
        </n-button>
        <n-button v-if="hasFilters" @click="clearFilters" quaternary size="small" class="!rounded-lg">
          <template #icon><XIcon class="w-3.5 h-3.5" /></template>
          清除
        </n-button>
      </div>
    </div>

    <div class="rounded-xl overflow-hidden" style="background: #FFFFFF; border: 1px solid #E5E7EB;">
      <n-data-table remote :columns="columns" :data="questions" :loading="loading" :pagination="pagination" @update:page="handlePageChange" size="small" :bordered="false" />
    </div>

    <n-modal v-model:show="showAdd" preset="card" title="添加题目" class="max-w-lg" :segmented="{ content: true }">
      <div class="space-y-4">
        <n-form-item label="题库名" :show-feedback="false">
          <n-input v-model:value="addForm.bank_name" placeholder="可选，用于分组管理" />
        </n-form-item>
        <n-form-item label="题目内容" :show-feedback="false">
          <n-input v-model:value="addForm.content" type="textarea" placeholder="输入题目内容..." :autosize="{ minRows: 3, maxRows: 8 }" />
        </n-form-item>
        <div class="grid grid-cols-2 gap-3">
          <n-form-item label="题目类型" :show-feedback="false"><n-select v-model:value="addForm.type" :options="typeOptions" /></n-form-item>
          <n-form-item label="难度" :show-feedback="false"><n-select v-model:value="addForm.difficulty" :options="difficultyOptions" /></n-form-item>
        </div>
        <n-form-item v-if="isAdmin" label="上线" :show-feedback="false">
          <n-switch v-model:value="addForm.is_published" />
        </n-form-item>
        <div v-if="addForm.type === 'choice'" class="space-y-2 p-3 rounded-xl" style="background: #F9FAFB; border: 1px solid #E5E7EB;">
          <p class="text-[11px] font-semibold mb-1 uppercase tracking-wider" style="color: #9CA3AF;">选项设置</p>
          <n-input v-for="key in ['A', 'B', 'C', 'D']" :key="key" v-model:value="addForm.options[key]" :placeholder="`选项 ${key}`" size="small">
            <template #prefix><span class="font-bold text-xs" style="color: #2563EB;">{{ key }}</span></template>
          </n-input>
        </div>
        <n-form-item label="正确答案" :show-feedback="false"><n-input v-model:value="addForm.answer" placeholder="输入正确答案" /></n-form-item>
        <n-form-item label="解析（可选）" :show-feedback="false"><n-input v-model:value="addForm.explanation" type="textarea" placeholder="答案解析（可选）" :autosize="{ minRows: 2, maxRows: 5 }" /></n-form-item>
        <div class="flex gap-2 pt-1">
          <n-button type="primary" block :loading="addLoading" @click="handleAddQuestion" class="!rounded-lg !font-semibold !h-10">保存题目</n-button>
          <n-button quaternary @click="showAdd = false">取消</n-button>
        </div>
      </div>
    </n-modal>

    <n-modal v-model:show="showImport" preset="card" title="导入题目" class="max-w-md" :segmented="{ content: true }">
      <div class="space-y-4">
        <n-form-item label="题库名" :show-feedback="false">
          <n-input v-model:value="importBankName" placeholder="为这批题目命名（如：Python基础）" />
        </n-form-item>
        <div class="rounded-xl p-3 flex items-start gap-2" style="background: #EFF6FF; border: 1px solid #E5E7EB;">
          <InfoIcon class="w-4 h-4 mt-0.5 shrink-0" style="color: #2563EB;" />
          <div>
            <p class="text-xs font-medium mb-0.5" style="color: #2563EB;">支持格式</p>
            <p class="text-[11px] leading-relaxed" style="color: #4B5563;">JSON、CSV、Excel (.xlsx/.xls) 格式</p>
          </div>
        </div>
        <div class="rounded-xl p-8 text-center upload-area cursor-pointer" :class="{ 'upload-area--has-file': importFile }" style="border: 2px dashed #E5E7EB;" @click="triggerFileInput" @dragover.prevent @drop.prevent="handleDrop">
          <input ref="fileInput" type="file" accept=".json,.csv,.xlsx,.xls" @change="handleFileChange" class="hidden" />
          <UploadIcon class="w-8 h-8 mx-auto mb-2" :style="{ color: importFile ? '#2563EB' : '#9CA3AF' }" />
          <p class="text-sm font-medium mb-1" :style="{ color: importFile ? '#2563EB' : '#4B5563' }">{{ importFile ? importFile.name : '点击选择文件' }}</p>
          <p class="text-[11px]" style="color: #9CA3AF;">{{ importFile ? `${formatFileSize(importFile.size)} · 点击更换` : '或将文件拖拽到此处' }}</p>
        </div>
        <div class="flex gap-2">
          <n-button type="primary" block :loading="importLoading" :disabled="!importFile" @click="handleImport" class="!rounded-lg !font-semibold !h-10">开始导入</n-button>
          <n-button v-if="importFile" quaternary @click="importFile = null">清除</n-button>
        </div>
      </div>
    </n-modal>

    <n-modal v-model:show="showAIModal" preset="card" title="AI 智能出题" class="max-w-md" :segmented="{ content: true }">
      <div class="space-y-4">
        <div class="rounded-xl p-3 flex items-center gap-2.5" style="background: #F5F3FF; border: 1px solid #E5E7EB;">
          <SparklesIcon class="w-4 h-4 shrink-0" style="color: #7C3AED;" />
          <p class="text-xs leading-relaxed" style="color: #7C3AED;">使用 AI 自动生成面试题目</p>
        </div>
        <n-form-item label="主题" :show-feedback="false"><n-input v-model:value="aiForm.topic" placeholder="例如：Python 装饰器、异步编程..." /></n-form-item>
        <div class="grid grid-cols-2 gap-3">
          <n-form-item label="生成数量" :show-feedback="false"><n-input-number v-model:value="aiForm.count" :min="1" :max="10" class="w-full" /></n-form-item>
          <n-form-item label="难度" :show-feedback="false"><n-select v-model:value="aiForm.difficulty" :options="difficultyOptions" /></n-form-item>
        </div>
        <n-form-item label="题目类型" :show-feedback="false"><n-select v-model:value="aiForm.type" :options="typeOptions" /></n-form-item>
        <div class="flex gap-2 pt-1">
          <n-button type="primary" block :loading="aiLoading" @click="handleAIGenerate" class="!rounded-lg !font-semibold !h-10">
            <template #icon><SparklesIcon class="w-4 h-4" /></template>生成并保存
          </n-button>
          <n-button quaternary @click="showAIModal = false">取消</n-button>
        </div>
      </div>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed, h } from "vue"
import { useAuthStore } from "@/stores/auth"
import { PlusIcon, UploadIcon, SparklesIcon, TrashIcon, FileQuestionIcon, SearchIcon, XIcon, InfoIcon, GlobeIcon } from "lucide-vue-next"
import { NTag, NButton, NSwitch, useMessage, useDialog } from "naive-ui"
import api from "@/api"

const message = useMessage()
const dialog = useDialog()
const authStore = useAuthStore()
const fileInput = ref<HTMLInputElement | null>(null)
const loading = ref(false)
const questions = ref<any[]>([])
const showAIModal = ref(false)
const showImport = ref(false)
const showAdd = ref(false)
const aiLoading = ref(false)
const addLoading = ref(false)
const importLoading = ref(false)
const importFile = ref<File | null>(null)
const importBankName = ref("")
const bankNameOptions = ref<{ label: string; value: string }[]>([])

const filters = reactive({ type: null as string | null, difficulty: null as string | null, bank_name: null as string | null })
const pagination = reactive({ page: 1, pageSize: 10, itemCount: 0, showSizePicker: true, pageSizes: [10, 20, 50] })
const aiForm = reactive({ topic: "Python", count: 5, difficulty: "medium", type: "choice", save: true })
const addForm = reactive({ content: "", type: "choice", difficulty: "medium", bank_name: "", is_published: false, options: { A: "", B: "", C: "", D: "" } as Record<string, string>, answer: "", explanation: "" })

const hasFilters = computed(() => filters.type || filters.difficulty || filters.bank_name)
const isAdmin = computed(() => authStore.user?.is_staff === true)
const typeMap: Record<string, string> = { choice: "选择题", fill: "填空题", code: "编程题", short: "简答题" }
const diffMap: Record<string, string> = { easy: "简单", medium: "中等", hard: "困难" }
const typeColorMap: Record<string, "info" | "success" | "warning" | "default"> = { choice: "info", fill: "success", code: "warning", short: "default" }
const typeOptions = [{ label: "选择题", value: "choice" }, { label: "填空题", value: "fill" }, { label: "编程题", value: "code" }, { label: "简答题", value: "short" }]
const difficultyOptions = [{ label: "简单", value: "easy" }, { label: "中等", value: "medium" }, { label: "困难", value: "hard" }]

const columns = computed(() => {
  const cols: any[] = [
    { title: "ID", key: "id", width: 60, render(row: any) { return h("span", { style: "color: #9CA3AF; font-family: 'JetBrains Mono', monospace; font-size: 12px;" }, `#${row.id}`) } },
    { title: "题目内容", key: "content", ellipsis: { tooltip: true }, render(row: any) { return h("span", { style: "color: #111827; font-size: 14px;" }, row.content) } },
    { title: "类型", key: "type", width: 90, render(row: any) { const t = typeColorMap[row.type] || "default"; return h(NTag, { size: "small", round: true, type: t, bordered: false }, { default: () => typeMap[row.type] || row.type }) } },
    { title: "难度", key: "difficulty", width: 80, render(row: any) { const t = row.difficulty === "easy" ? "success" : row.difficulty === "hard" ? "error" : "warning"; return h(NTag, { type: t, size: "small", round: true, bordered: false }, { default: () => diffMap[row.difficulty] || row.difficulty }) } },
    { title: "题库名", key: "bank_name", width: 100, ellipsis: { tooltip: true }, render(row: any) { return row.bank_name ? h(NTag, { size: "small", round: true, type: "default", bordered: false }, { default: () => row.bank_name }) : h("span", { style: "color: #D1D5DB; font-size: 11px;" }, "—") } },
    { title: "状态", key: "is_published", width: 70, render(row: any) { return row.is_published ? h(NTag, { type: "success", size: "small", round: true, bordered: false }, { default: () => "已上线" }) : h(NTag, { type: "default", size: "small", round: true, bordered: false }, { default: () => "私有" }) } },
  ]
  if (isAdmin.value) {
    cols.push({
      title: "管理", key: "manage", width: 100,
      render(row: any) {
        return row.is_published
          ? h(NButton, { quaternary: true, size: "tiny", type: "warning", onClick: () => handleUnpublish(row.id) }, { default: () => "下线" })
          : h(NButton, { quaternary: true, size: "tiny", type: "success", onClick: () => handlePublish(row.id) }, { default: () => "上线" })
      }
    })
  }
  cols.push({
    title: "操作", key: "actions", width: 80,
    render(row: any) { return h(NButton, { quaternary: true, circle: true, size: "tiny", type: "error", onClick: () => handleDelete(row.id) }, { icon: () => h(TrashIcon, { class: "w-3.5 h-3.5" }) }) }
  })
  return cols
})

async function fetchBankNames() { try { const names: any = await api.get("/questions/bank_names/"); bankNameOptions.value = names.map((n: string) => ({ label: n, value: n })) } catch (e) {} }
async function fetchQuestions() { loading.value = true; try { const params: any = { page: pagination.page, page_size: pagination.pageSize }; if (filters.type) params.type = filters.type; if (filters.difficulty) params.difficulty = filters.difficulty; if (filters.bank_name) params.bank_name = filters.bank_name; const data: any = await api.get("/questions/", { params }); questions.value = data.results; pagination.itemCount = data.count } catch (e) { console.error(e) } finally { loading.value = false } }
function clearFilters() { filters.type = null; filters.difficulty = null; filters.bank_name = null; fetchQuestions() }
function handlePageChange(page: number) { pagination.page = page; fetchQuestions() }
function handleDelete(id: number) { dialog.warning({ title: "确认删除", content: "删除后无法恢复，确定要删除这道题目吗？", positiveText: "删除", negativeText: "取消", onPositiveClick: async () => { try { await api.delete("/questions/" + id + "/"); message.success("已删除"); fetchQuestions() } catch (e) { console.error(e) } } }) }
async function handlePublish(id: number) { try { await api.post("/questions/" + id + "/publish/"); message.success("已上线"); fetchQuestions() } catch (e) { console.error(e) } }
async function handleUnpublish(id: number) { try { await api.post("/questions/" + id + "/unpublish/"); message.success("已下线"); fetchQuestions() } catch (e) { console.error(e) } }
async function handleAddQuestion() { if (!addForm.content.trim() || !addForm.answer.trim()) { message.warning("请填写题目内容和正确答案"); return } addLoading.value = true; try { const payload: any = { ...addForm }; if (!isAdmin.value) delete payload.is_published; await api.post("/questions/", payload); message.success("题目已添加"); showAdd.value = false; resetAddForm(); fetchQuestions(); fetchBankNames() } catch (e) { console.error(e) } finally { addLoading.value = false } }
function resetAddForm() { addForm.content = ""; addForm.answer = ""; addForm.explanation = ""; addForm.bank_name = ""; addForm.is_published = false; addForm.options = { A: "", B: "", C: "", D: "" }; addForm.type = "choice"; addForm.difficulty = "medium" }
function triggerFileInput() { fileInput.value?.click() }
function handleFileChange(e: Event) { importFile.value = (e.target as HTMLInputElement).files?.[0] || null }
function handleDrop(e: DragEvent) { importFile.value = e.dataTransfer?.files?.[0] || null }
function formatFileSize(bytes: number): string { if (bytes < 1024) return `${bytes} B`; if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`; return `${(bytes / (1024 * 1024)).toFixed(1)} MB` }
async function handleImport() { if (!importFile.value) return; importLoading.value = true; try { const fd = new FormData(); fd.append("file", importFile.value); fd.append("bank_name", importBankName.value); const d: any = await api.post("/questions/import_questions/", fd); message.success(d.message || "导入成功"); showImport.value = false; importFile.value = null; importBankName.value = ""; fetchQuestions(); fetchBankNames() } catch (e) { console.error(e) } finally { importLoading.value = false } }
async function handleAIGenerate() { aiLoading.value = true; try { const d: any = await api.post("/ai/generate/", { ...aiForm }); message.success(d.message || "题目生成成功"); showAIModal.value = false; fetchQuestions(); fetchBankNames() } catch (e) { console.error(e) } finally { aiLoading.value = false } }

onMounted(async () => { fetchQuestions(); fetchBankNames() })
</script>

<style scoped>
.upload-area { transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1); }
.upload-area:hover { border-color: #2563EB !important; background: #EFF6FF; }
.upload-area--has-file { border-color: #2563EB !important; background: #EFF6FF; }
</style>
