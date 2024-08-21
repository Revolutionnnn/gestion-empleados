const routes = [
  {
    path: '/login',
    component: () => import('layouts/AuthLayout.vue'),
    children: [
      { path: '', name: 'login', component: () => import('pages/LoginPage.vue') }
    ]
  },
  {
    path: '/dashboard',
    component: () => import('layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', name: 'home', component: () => import('pages/IndexPage.vue') },
      { path: 'user', name: 'users', component: () => import('pages/dashboard/users/IndexPage.vue') },
      { path: 'areas', name: 'areas', component: () => import('pages/dashboard/areas/IndexPage.vue') },
      { path: 'persons', name: 'persons', component: () => import('pages/dashboard/persons/IndexPage.vue') },
    ]
  },
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
