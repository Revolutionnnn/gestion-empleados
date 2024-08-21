<template>
    <div class="q-pa-md q-gutter-sm">
        <div>
            <q-btn dense color="primary" label="Agregar usuario" @click="add" style="margin-right: 8px;" />
            <q-btn dense color="primary" label="Actualizar" @click="startInfo" />
        </div>

        <q-table title="Usuarios" :rows="rows" :columns="columns" row-key="name">
            <template v-slot:body-cell="props">
                <q-td :props="props">
                    <div v-if="props.col.name === 'is_active'">
                        <q-toggle v-model="props.row.is_active" @input="toggleIsActive(props.row)"
                            @click="toggleIsActive(props.row)" :disable="profie.username === props.row.username" />
                    </div>
                    <div v-else>
                        {{ props.value }}
                    </div>
                </q-td>
                <q-menu touch-position context-menu>

                    <q-list dense style="min-width: 100px">
                        <q-item clickable v-close-popup>
                            <q-item-section @click="editUser(props.row)">Editar</q-item-section>
                        </q-item>
                        <q-item clickable v-close-popup>
                            <q-item-section @click="deleteUser(props.row)">Eliminar</q-item-section>
                        </q-item>
                    </q-list>
                </q-menu>
            </template>
        </q-table>
    </div>
    <q-dialog v-model="addUsers">
        <q-card class="q-dialog-plugin" style="width: 700px; max-width: 80vw;">
            <q-card-section class="row items-center q-pb-none">
                <div class="text-h6">Agregar usuario</div>
                <q-space />
                <q-btn icon="close" flat round dense v-close-popup />
            </q-card-section>

            <q-separator />

            <q-card-section>
                <q-form @submit.prevent="handleSubmit" ref="myForm">
                    <div class="q-gutter-md">
                        <q-card-section class="row q-col-gutter-md">
                            <q-input outlined v-model="user.username" label="Nombre de usuario" class="col-6 col-md-6"
                                :rules="[required, lengthRange(0, 20)]" lazy-rules />
                            <q-input outlined v-model="user.email" label="Correo Electrónico" class="col-6 col-md-6"
                                :rules="[required, email, lengthRange(0, 30)]" />
                        </q-card-section>

                        <q-card-section class="row q-col-gutter-md">
                            <q-input outlined v-model="user.firstName" label="Nombre" class="col-6 col-md-6"
                                :rules="[required, lengthRange(0, 20)]" />
                            <q-input outlined v-model="user.lastName" label="Apellido" class="col-6 col-md-6"
                                :rules="[required, lengthRange(0, 20)]" />
                        </q-card-section>

                        <q-card-section class="row q-col-gutter-md">
                            <q-select outlined use-chips v-model="user.groups" :options="groupsOptions"
                                label="Roles" class="col-6 col-md-6" option-label="name" option-value="id" map-options
                                emit-value :rules="[required]" />
                        </q-card-section>
                    </div>

                    <q-card-actions align="right" class="q-mt-md">
                        <q-btn v-if="!editing" color="primary" label="Guardar" type="submit" />
                        <q-btn v-if="editing" color="primary" label="Editar" type="submit" />
                        <q-btn flat label="Cancelar" v-close-popup />
                    </q-card-actions>
                </q-form>
            </q-card-section>
        </q-card>
    </q-dialog>
</template>
<script setup>
import { onMounted, ref } from 'vue'
import request from 'src/utils/axios.js';
import { required, email, lengthRange } from 'src/utils/validations.js';
import { useQuasar } from 'quasar'
import { Notify } from 'quasar';
import { useUserStore } from 'src/stores/user';

const profie = useUserStore()
const $q = useQuasar()
const myForm = ref(null)
const groupsOptions = ref(null)
const user = ref({
    uuid: null,
    username: null,
    email: null,
    firstName: null,
    lastName: null,
    groups: [],
    is_active: null
})
const editing = ref(false)

const rows = ref([])
const addUsers = ref(false)
const columns = ref([
    { name: 'username', align: 'left', label: 'Usuario', field: 'username', sortable: true, format: val => `${val}` || 'Sin datos' },
    { name: 'first_name', align: 'left', label: 'Nombre', field: 'first_name', sortable: true, format: val => `${val}` || 'Sin datos' },
    { name: 'last_name', align: 'left', label: 'Segundo nombre', field: 'last_name', sortable: true, format: val => `${val}` || 'Sin datos' },
    { name: 'email', align: 'left', label: 'Correo', field: 'email', sortable: true, format: val => `${val}` || 'Sin datos' },
    { name: 'is_active', label: 'Activo', field: 'is_active', align: 'center' },
])

const clean = () => {
    for (const key in user.value) {
        if (Object.hasOwnProperty.call(user.value, key)) {
            user.value[key] = null;
        }
    }
}

const toggleIsActive = async (row) => {
    await request.patch(`auth/users/${row.uuid}/`, { is_active: row.is_active });
}

const handleSubmit = async () => {
    const validation = await myForm.value.validate()
    if (!validation) return
    if (editing.value) {
        update()
    } else {
        save()
    }
}

const add = async (row) => {
    const { data } = await request.get('auth/groups/')
    groupsOptions.value = data.results
    addUsers.value = true;
    if (row.username) {
        editing.value = true
        user.value.uuid = row.uuid
        user.value.username = row.username
        user.value.email = row.email
        user.value.firstName = row.first_name
        user.value.lastName = row.last_name
        user.value.groups = row.groups[0]?.id
        return
    }
    clean()
    editing.value = false
}

const onDialogHide = () => {
    addUsers.value = false
}

const save = async () => {
    const formData = new FormData();
    formData.append('username', user.value.username);
    formData.append('email', user.value.email);
    formData.append('first_name', user.value.firstName);
    formData.append('last_name', user.value.lastName);
    formData.append('is_active', true);
    if (user.value.groups) formData.append('groups', user.value.groups)

    try {
        await request.post('auth/users/', formData);
        Notify.create({
            type: 'positive',
            message: 'Usuario registrado',
            position: 'top',
        });
        startInfo()
        onDialogHide()
    } catch (error) {
        Notify.create({
            type: 'negative',
            message: 'Error al agregar usuario',
            position: 'top',
        });
    }
};

const update = async () => {
    const formData = new FormData();
    formData.append('username', user.value.username);
    formData.append('email', user.value.email);
    formData.append('first_name', user.value.firstName);
    formData.append('last_name', user.value.lastName);
    if (user.value.groups) formData.append('groups', [user.value.groups])


    try {
        await request.patch(`auth/users/${user.value.uuid}/`, formData);
        Notify.create({
            type: 'positive',
            message: 'Usuario actualizado',
            position: 'top',
        });
        startInfo()
        onDialogHide()
    } catch (error) {
        Notify.create({
            type: 'negative',
            message: 'Error al agregar usuario',
            position: 'top',
        });
    }
}

const startInfo = async () => {
    const response = await request.get('auth/users/')
    rows.value = response.data.results
}

const editUser = (row) => {
    clean()
    add(row)
}

const deleteUser = (row) => {
    $q.dialog({
        title: 'Eliminar usuario',
        message: 'Estas seguro de eliminar el usuario?',
        cancel: true,
        persistent: true
    }).onOk(async () => {
        await request.delete(`auth/users/${row.uuid}/`)
        await startInfo()
    })
}

onMounted(async () => {
    startInfo()
})
</script>