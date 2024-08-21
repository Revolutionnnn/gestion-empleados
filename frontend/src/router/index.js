import { route } from 'quasar/wrappers';
import { createRouter, createMemoryHistory, createWebHistory } from 'vue-router';
import routes from './routes';
import request from '../utils/axios.js';
import { useUserStore } from 'src/stores/user';

export default route(function (/* { store, ssrContext } */) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : createWebHistory;

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,
    history: createHistory(process.env.VUE_ROUTER_BASE)
  });

  // Convertir la guardia de navegación a una función asíncrona
  Router.beforeEach(async (to, from, next) => {
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
    if (requiresAuth) {
      try {
        const profile = useUserStore()
        const response = await request.get('auth/profile/');
        profile.setProfile(response.data)

        if (response.status === 200) {
          next(); // La sesión es válida, permitir el acceso
        } else {
          next({ name: 'login' }); // La sesión no es válida, redirigir a login
        }
      } catch (error) {
        next({ name: 'login' }); // Error al verificar la sesión, redirigir a login
      }
    } else {
      next(); // La ruta no requiere autenticación, permitir el acceso
    }
  });

  return Router;
});
