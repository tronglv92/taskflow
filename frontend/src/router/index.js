/**
 * Vue Router Configuration
 * Platform Engineering Bootcamp Reference Application
 *
 * Week 3: Students learn about frontend routing
 * Later weeks: Add authentication guards and protected routes
 */

import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      title: 'Home - TaskFlow'
    }
  },
  {
    path: '/tasks',
    name: 'Tasks',
    component: () => import('../views/Tasks.vue'),
    meta: {
      title: 'Tasks - TaskFlow',
      // Week 4+: requiresAuth: true
    }
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/About.vue'),
    meta: {
      title: 'About - TaskFlow'
    }
  },
  // Week 4+: Authentication routes
  // {
  //   path: '/login',
  //   name: 'Login',
  //   component: () => import('../views/Login.vue')
  // },
  // {
  //   path: '/register',
  //   name: 'Register',
  //   component: () => import('../views/Register.vue')
  // }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// Set page title from route meta
router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'TaskFlow'

  // Week 4+: Add authentication guard
  // if (to.meta.requiresAuth && !isAuthenticated()) {
  //   next('/login')
  // } else {
  //   next()
  // }

  next()
})

export default router
