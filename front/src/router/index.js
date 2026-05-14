import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../store/user'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { guest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue'),
    meta: { guest: true }
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/questions',
    name: 'Questions',
    component: () => import('../views/Questions.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/exam',
    name: 'ExamSetup',
    component: () => import('../views/ExamSetup.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/exam/:id',
    name: 'Exam',
    component: () => import('../views/Exam.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/result/:id',
    name: 'Result',
    component: () => import('../views/Result.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/history',
    name: 'History',
    component: () => import('../views/History.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/token-stats',
    name: 'TokenStats',
    component: () => import('../views/TokenStats.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/ai-config',
    name: 'AIConfig',
    component: () => import('../views/AIConfig.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next('/login')
  } else if (to.meta.guest && userStore.isLoggedIn) {
    next('/')
  } else {
    next()
  }
})

export default router
