const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { 
        path: '',
        component: () => import('pages/IndexPage.vue') 
      },
      
      { 
        path: 'configuracoes/portais',  // Antes era settings/portals
        component: () => import('pages/PortalsPage.vue') 
      },
      { 
        path: 'configuracoes/usuarios', 
        component: () => import('pages/UsersPage.vue') 
      }

    ]
  },

  {
    path: '/login',
    component: () => import('layouts/LoginLayout.vue'),
    children: [
      { path: '', component: () => import('pages/LoginPage.vue') }
    ]
  },

  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes