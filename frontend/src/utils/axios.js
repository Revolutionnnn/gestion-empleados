import axios from 'axios';
import { Notify } from 'quasar';

// Configurar Axios
const request = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/', // Reemplaza esto con la URL de tu API
  withCredentials: true // Asegúrate de incluir las credenciales en las solicitudes
});

// Interceptor para añadir CSRF Token y Session Key en cada solicitud
request.interceptors.request.use(
  async config => {
    try {
      const csrfToken = await cookieStore.get('csrftoken'); // O sessionStorage
      const sessionID = await cookieStore.get('sessionid'); // O sessionStorage

      if (csrfToken) {
        config.headers['X-CSRFToken'] = csrfToken.value;
      }

      if (sessionID) {
        config.headers['sessionid'] = sessionID.value;
      }

    } catch (error) {
      Promise.reject(error)
    }

    return config;
  },
  error => Promise.reject(error)
);

// Manejar errores de Axios
request.interceptors.response.use(
  response => response,
  error => {
    const { response } = error;
    if (response) {
      const { status } = response;
      if (status === 400) {
        Notify.create({
          type: 'negative',
          message: response.data[0],
          position: 'top',
        });
      }
      if (status === 402 || status === 500) {
        Notify.create({
          type: 'negative',
          message: 'Ops ha ocurrido un error',
          position: 'top',
        });
      }
      else if (status === 401) {
        Notify.create({
          type: 'negative',
          message: 'Error no estas autorizado',
          position: 'top',
        });
      }
    } else {
      Notify.create({
        type: 'negative',
        message: 'No se pudo conectar con el servidor',
        position: 'top',
      });
    }
    return Promise.reject(error);
  }
);

export default request;
