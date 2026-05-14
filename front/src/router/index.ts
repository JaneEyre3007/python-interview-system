import { createRouter, createWebHistory } from "vue-router"
import type { RouteRecordRaw } from "vue-router"

const routes: RouteRecordRaw[] = [
  {
    path: "/login",
    name: "Login",
    component: () => import("../views/auth/Login.vue")
  },
  {
    path: "/register",
    name: "Register",
    component: () => import("../views/auth/Register.vue")
  },
  {
    path: "/",
    component: () => import("../views/layout/MainLayout.vue"),
    children: [
      {
        path: "",
        name: "Dashboard",
        component: () => import("../views/dashboard/Index.vue")
      },
      {
        path: "questions",
        name: "Questions",
        component: () => import("../views/questions/Index.vue")
      },
      {
        path: "exams",
        name: "Exams",
        component: () => import("../views/exams/Index.vue")
      },
      {
        path: "exam/:id",
        name: "ExamDetail",
        component: () => import("../views/exams/ExamDetail.vue")
      },
      {
        path: "result/:id",
        name: "ExamResult",
        component: () => import("../views/exams/ExamResult.vue")
      },
      {
        path: "history",
        name: "History",
        component: () => import("../views/history/Index.vue")
      },
      {
        path: "token-stats",
        name: "TokenStats",
        component: () => import("../views/stats/TokenStats.vue")
      },
      {
        path: "ai-config",
        name: "AIConfig",
        component: () => import("../views/settings/AIConfig.vue")
      },
      {
        path: "profile",
        name: "Profile",
        component: () => import("../views/settings/Profile.vue")
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  const token = localStorage.getItem("access_token")
  if (to.name !== "Login" && to.name !== "Register" && !token) {
    return { name: "Login" }
  }
})

export default router