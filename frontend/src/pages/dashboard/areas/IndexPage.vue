<template>
    <div class="q-pa-md q-gutter-sm">
        <div>
            <q-btn dense color="primary" label="Agregar area" @click="add" style="margin-right: 8px;" />
            <q-btn dense color="primary" label="Actualizar" @click="startInfo" />
        </div>

        <q-table title="Áreas" :rows="rows" :columns="columns" row-key="name" :pagination="pagination">
            <template v-slot:body-cell="props">
                <q-td :props="props">
                    <!-- Verifica si la columna es 'is_active' -->
                    <div v-if="props.col.name === 'is_active'">
                        <q-toggle v-model="props.row.is_active" @input="toggleIsActive(props.row)"
                            @click="toggleIsActive(props.row)" />
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
            <template v-slot:top-right>
                <q-input borderless dense debounce="300" v-model="filter" placeholder="Buscar"
                    @update:model-value="startInfo()">
                    <template v-slot:append>
                        <q-icon name="search" />
                    </template>
                </q-input>
            </template>
            <template v-slot:bottom>
                <q-pagination v-model="pagination.page" max="20" color="primary" boundary-numbers input
                    @update:model-value="startInfo" />
            </template>
        </q-table>
    </div>
    <q-dialog v-model="addStablishment">
        <q-card class="q-dialog-plugin" style="width: 700px; max-width: 80vw;">
            <q-card-section class="row items-center q-pb-none">
                <div class="text-h6">Agregar sede</div>
                <q-space />
                <q-btn icon="close" flat round dense v-close-popup />
            </q-card-section>

            <q-separator />

            <q-card-section>
                <q-form @submit.prevent="handleSubmit" ref="myForm">
                    <div class="q-gutter-md">
                        <q-card-section class="row q-col-gutter-md">
                            <q-input outlined v-model="user.name" label="Nombre de la sede" class="col-6 col-md-6"
                                :rules="[required, lengthRange(0, 20)]" lazy-rules />
                            <q-input outlined v-model="user.description" label="Descripcion de la sede"
                                class="col-6 col-md-6" :rules="[required, lengthRange(0, 30)]" />
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
import { onMounted, ref, reactive } from 'vue'
import request from 'src/utils/axios.js';
import { required, lengthRange } from 'src/utils/validations.js';
import { useQuasar } from 'quasar'
import { Notify } from 'quasar';

const $q = useQuasar()
const myForm = ref(null)
const filter = ref('')
const user = ref({
    uuid: null,
    name: null,
    description: null,
    is_active: null
})
const pagination = reactive({
    page: 1,
    rowsPerPage: 10,
    rowsNumber: 0
})
const editing = ref(false)

const rows = ref([])
const addStablishment = ref(false)
const columns = ref([
    { name: 'created', align: 'left', label: 'Creado el', field: 'created', sortable: true, format: val => val ? val.split('T')[0] : 'Sin datos' },
    { name: 'name', align: 'left', label: 'Nombre', field: 'name', sortable: true, format: val => val || 'Sin datos' },
    { name: 'description', align: 'left', label: 'Descripcion', field: 'description', sortable: true, format: val => val || 'Sin datos' },
])

const clean = () => {
    for (const key in user.value) {
        if (Object.hasOwnProperty.call(user.value, key)) {
            user.value[key] = null;
        }
    }
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
    addStablishment.value = true;
    if (row.name) {
        editing.value = true
        user.value.uuid = row.uuid
        user.value.name = row.name
        user.value.description = row.description
        return
    }
    clean()
    editing.value = false
}

const onDialogHide = () => {
    addStablishment.value = false
}

const save = async () => {
    const formData = new FormData();
    formData.append('name', user.value.name);
    formData.append('description', user.value.description);

    try {
        await request.post('register/areas/', formData);
        Notify.create({
            type: 'positive',
            message: 'Sede registrada',
            position: 'top',
        });
        startInfo()
        onDialogHide()
    } catch (error) {
        Notify.create({
            type: 'negative',
            message: 'Error al crear la sede',
            position: 'top',
        });     
    }
};

const update = async () => {
    const formData = new FormData();
    formData.append('name', user.value.name);
    formData.append('description', user.value.description);

    try {
        await request.patch(`register/areas/${user.value.uuid}/`, formData);
        Notify.create({
            type: 'positive',
            message: 'Sede actualizada',
            position: 'top',
        });
        startInfo()
        onDialogHide()
    } catch (error) {
        Notify.create({
            type: 'negative',
            message: 'Error al crear la sede',
            position: 'top',
        });    
    }
}

const startInfo = async () => {
    try {
        const response = await request.get('register/areas/', {
            params: {
                search: filter.value,
                page: pagination.page,
                page_size: pagination.rowsPerPage
            }
        })
        rows.value = response.data.results
        pagination.rowsNumber = response.data.count
    } catch (error) {
        if (pagination.page < 1) return pagination.page = 1
        pagination.page = pagination.page - 1
    }
}

const editUser = (row) => {
    add(row)
}

const deleteUser = (row) => {
    $q.dialog({
        title: 'Eliminar sede',
        message: 'Estas seguro de eliminar esta sede?',
        cancel: true,
        persistent: true
    }).onOk(async () => {
        await request.delete(`register/areas/${row.uuid}/`)
        await startInfo()
    })
}

onMounted(async () => {
    startInfo()
})
</script>