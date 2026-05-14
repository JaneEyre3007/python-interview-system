<template>
  <div class="history-page">
    <el-card>
      <template #header>
        <h2>答题历史记录</h2>
      </template>

      <el-table :data="exams" stripe v-loading="loading">
        <el-table-column prop="title" label="试卷标题" />
        <el-table-column label="题目数量" width="100">
          <template #default="{ row }">
            {{ row.questions ? row.questions.length : 0 }} 道
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button
              v-if="row.status === 'pending'"
              type="primary"
              link
              @click="router.push(`/exam/${row.id}`)"
            >
              开始
            </el-button>
            <el-button
              v-if="row.status === 'in_progress'"
              type="warning"
              link
              @click="router.push(`/exam/${row.id}`)"
            >
              继续
            </el-button>
            <el-button
              v-if="row.status === 'completed'"
              type="success"
              link
              @click="router.push(`/result/${row.id}`)"
            >
              查看成绩
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getExamList } from '../api/exam'

const router = useRouter()
const exams = ref([])
const loading = ref(true)

const statusMap = {
  pending: { label: '待完成', type: 'info' },
  in_progress: { label: '进行中', type: 'warning' },
  completed: { label: '已完成', type: 'success' }
}

const getStatusLabel = (status) => statusMap[status]?.label || status
const getStatusType = (status) => statusMap[status]?.type || ''

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN')
}

onMounted(async () => {
  try {
    const res = await getExamList()
    exams.value = res.data.results || []
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.history-page {
  max-width: 1200px;
  margin: 0 auto;
}

h2 {
  margin: 0;
  color: #303133;
}
</style>
