// frontend/src/router/index.js

import { route } from 'quasar/wrappers'
import { createRouter, createMemoryHistory, createWebHistory, createWebHashHistory } from 'vue-router'
import routes from './routes'
import { useAuthStore } from 'stores/auth' // <--- Importe a Store

export default route(function (/* { store, ssrContext } */) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : (process.env.VUE_ROUTER_MODE === 'history' ? createWebHistory : createWebHashHistory)

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,
    history: createHistory(process.env.VUE_ROUTER_BASE)
  })

  // --- AQUI COMEÇA A PROTEÇÃO ---
  Router.beforeEach((to, from, next) => {
    const authStore = useAuthStore()
    
    // 1. A rota exige autenticação?
    if (to.matched.some(record => record.meta.requiresAuth)) {
      
      // 2. O usuário NÃO está logado?
      if (!authStore.isAuthenticated) {
        // Manda para o login e salva para onde ele queria ir (opcional)
        next({ path: '/login', query: { next: to.fullPath } })
      } else {
        // Está logado, deixa passar
        next() 
      }
      
    } else {
      // Rota pública (ex: login), deixa passar
      next() 
    }
  })
  // ------------------------------

  return Router
})