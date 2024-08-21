<template>
    <div class="login-background">
        <div class="login-container">
            <q-icon name="person" size="150px" color="primary" />
            <div class="login-title">
                <div>Iniciar Sesión</div>
            </div>

            <q-form ref="form" @submit="login">
                <q-input v-model="user.username" label="Usuario" placeholder="Usuario" dense outlined
                    :rules="[required, lengthRange(0, 20)]" style="border-radius: 10px;" />
                <q-input v-model="user.password" label="Contraseña" placeholder="Contraseña" type="password" dense
                    outlined :rules="[required, lengthRange(0, 20)]" style=" border-radius: 10px;" />
                <q-btn type="submit" label="Iniciar sesión" color="primary" style="border-radius: 10px;" />
                <q-btn flat label="¿Olvidaste tu contraseña?" class="ml-4" @click="showForgotPassword = true" />
            </q-form>

            <q-dialog v-model="showForgotPassword">
                <q-card style="width: 700px; max-width: 80vw;">
                    <q-card-section>
                        <div class="text-h6">Recuperar Contraseña</div>
                    </q-card-section>
                    <q-form ref="formForgot">
                        <q-card-section>
                            <q-input v-model="forgotPasswordEmail" label="Correo electrónico"
                                placeholder="Correo electrónico" dense outlined
                                :rules="[required, email, lengthRange(0, 20)]" style="border-radius: 10px;" />
                        </q-card-section>

                        <q-card-actions align="right">
                            <q-btn flat label="Cancelar" v-close-popup />
                            <q-btn label="Enviar" color="primary" @click="sendForgotPassword" />
                        </q-card-actions>
                    </q-form>
                </q-card>
            </q-dialog>
        </div>
    </div>
</template>
<script setup>
import { ref } from 'vue';
import request from '../utils/axios.js';
import { useRouter } from 'vue-router'
import { Notify } from 'quasar';
import { required, email, lengthRange } from 'src/utils/validations.js';

const router = useRouter()
const form = ref()
const formForgot = ref()

defineOptions({
    name: 'LoginPage'
});

const user = ref({
    username: null,
    password: null,
});

const showForgotPassword = ref(false);
const forgotPasswordEmail = ref('');

async function login() {
    const validate = await form.value.validate()
    if (!validate) return

    const data = {
        username: user.value.username,
        password: user.value.password
    };

    try {
        const response = await request.post('auth/login/', data);

        if (response.status === 200) {
            router.push({ name: 'home' });
        }
    } catch (error) {
    }
}

async function sendForgotPassword() {
    const validate = await formForgot.value.validate()
    if (!validate) return
    if (!forgotPasswordEmail.value) {
        Notify.create({
            type: 'negative',
            message: 'Por favor introduce tu correo electrónico',
            position: 'top',
        });
        return;
    }

    const data = {
        email: forgotPasswordEmail.value
    };

    try {
        const response = await request.post('auth/send-email/', data);

        if (response.status === 200) {
            Notify.create({
                type: 'positive',
                message: 'Correo de recuperación enviado',
                position: 'top',
            });

            showForgotPassword.value = false;
        }
    } catch (error) {
    }
}
</script>
<style scoped>
.login-container {
    max-width: 400px;
    margin: auto;
    text-align: center;
    padding: 20px;
    border-radius: 15px;
    background-color: white;
    box-shadow: 0 8px 4px rgba(0, 0, 0, 0.1);
}

.login-background {
    background-color: rgba(237, 237, 237, 0.7);
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}

.body {
    margin: 0;
}
</style>
