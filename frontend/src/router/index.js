import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: () => import('@/views/LoginView.vue') },
  { path: '/register', component: () => import('@/views/RegisterView.vue') },
  {
    path: '/dashboard',
    component: () => import('@/views/DashboardView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/vehicles',
    component: () => import('@/views/VehiclesView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/cites',
    component: () => import('@/views/CitesView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin',
    component: () => import('@/views/AdminView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/mecanic',
    component: () => import('@/views/MecanicView.vue'),
    meta: { requiresAuth: true, requiresMecanic: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return next('/login')
  }
  if (to.meta.requiresAdmin && !auth.isAdmin) {
    return next('/dashboard')
  }
  if (to.meta.requiresMecanic && !auth.isMecanic && !auth.isAdmin) {
    return next('/dashboard')
  }
  next()
})

export default router