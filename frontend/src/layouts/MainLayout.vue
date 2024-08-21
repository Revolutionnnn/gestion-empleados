<template>
  <q-layout view="hhr lpr lfr">
    <q-header elevated>
      <q-toolbar>
        <q-btn flat dense round icon="menu" aria-label="Menu" @click="toggleLeftDrawer" />

        <q-toolbar-title>
          Bienvenido
        </q-toolbar-title>

        <div>Version 0.0.1</div>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered>
      <q-list>
        <q-item-label header>
          Menu
        </q-item-label>

        <EssentialLink v-for="link in linksList" :key="link.title" v-bind="link" />
        <q-item clickable v-ripple @click="logout">
          <q-item-section avatar>
            <q-icon name="exit_to_app" />
          </q-item-section>
          <q-item-section>
            <q-item-label>
              Cerrar Sesión
            </q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'
import EssentialLink from 'components/EssentialLink.vue'
import request from 'src/utils/axios.js';
import { useRouter } from 'vue-router'
import { useUserStore } from 'src/stores/user';

const router = useRouter()

defineOptions({
  name: 'MainLayout'
})

const linksList = [
  {
    title: 'Usuarios',
    caption: 'Usuarios del sistema',
    icon: 'person',
    link: '/dashboard/user'
  }
]

const leftDrawerOpen = ref(false)

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
}

async function logout() {
  const userStore = useUserStore();
  const response = await request.post('auth/logout/')
  if (response.status === 200) {
    cookieStore.delete('csrftoken');
    cookieStore.delete('sessionid');
    userStore.logout();

    router.push({ name: 'login' });
  }
}
</script>
