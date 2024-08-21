<template>
    <div class="q-pa-md q-gutter-sm">
        <div>
            <q-btn dense color="primary" label="Agregar persona" @click="add" style="margin-right: 8px;" />
            <q-btn dense color="primary" label="Actualizar" @click="startInfo" />
        </div>
        <div class="row">
            <q-select filled outlined use-chips v-model="typeFilter" option-label="description" option-value="code" :options="TYPE_CHOICES"
                label="Tipo de personas" @update:model-value="startInfo" emit-value class="col-3" map-options/>
        </div>

        <q-table title="Registro de personas" :rows="rows" :columns="columns" row-key="name" :pagination="pagination">
            <template v-slot:body-cell="props">
                <q-td :props="props">
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
        </q-table>
    </div>
    <q-dialog v-model="addStablishment">
        <q-card class="q-dialog-plugin" style="width: 700px; max-width: 80vw;">
            <q-card-section class="row items-center q-pb-none">
                <div class="text-h6" v-if="!editing">Registrar personas</div>
                <div class="text-h6" v-if="editing">Editar registro de personas</div>
                <q-space />
                <q-btn icon="close" flat round dense v-close-popup />
            </q-card-section>

            <q-separator />

            <q-card-section>
                <q-form @submit.prevent="handleSubmit" ref="myForm">
                    <div class="q-gutter-md">
                        <q-card-section class="row q-col-gutter-md">
                            <q-input outlined v-model="user.name" label="Nombre" class="col-6 col-md-6"
                                :rules="[required, lengthRange(0, 20)]" lazy-rules />
                            <q-input outlined v-model="user.document" label="Documento"
                                class="col-6 col-md-6" :rules="[required, lengthRange(0, 30), isInteger]" />
                        </q-card-section>
                    </div>
                    <div class="q-gutter-md">
                        <q-card-section class="row q-col-gutter-md">
                            <q-input outlined v-model="user.phone" label="Telefono (Opcional)" class="col-6 col-md-6"
                                :rules="[isInteger]" lazy-rules />
                            <q-select outlined use-chips v-model="user.type" :options="TYPE_CHOICES"
                                label="Tipo de persona a registrar" class="col-6 col-md-6" option-label="description" option-value="code" map-options
                                emit-value :rules="[required]" />
                        </q-card-section>
                    </div>
                    <div class="q-gutter-md">
                        <q-card-section class="row q-col-gutter-md">
                            <q-select outlined use-chips v-model="user.area" :options="areasOptions" v-if="user.type === EMPLOYEE"
                                label="Sede" class="col-6 col-md-6" option-label="name" option-value="id" map-options
                                emit-value :rules="[required]" />
                            <q-input outlined v-model="user.rol" label="Cargo o Rol" class="col-6 col-md-6"
                                :rules="[required, lengthRange(0, 20)]" lazy-rules v-if="user.type === EMPLOYEE"/>
                            <q-input outlined v-model="user.business" label="Nombre de la empresa" class="col-6 col-md-6"
                                :rules="[required, lengthRange(0, 20)]" lazy-rules v-if="user.type === PROVIDER"/>
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
import { required, lengthRange, isInteger } from 'src/utils/validations.js';
import { useQuasar } from 'quasar'
import { Notify } from 'quasar';
import { TYPE_CHOICES, EMPLOYEE, PROVIDER } from 'src/constants/users'

const $q = useQuasar()
const myForm = ref(null)
const filter = ref('')
const areasOptions = ref(null)
const typeFilter = ref(null)
const user = ref({
    uuid: null,
    name: null,
    phone: null,
    document: null,
    rol: null,
    description: null,
    type: null,
    area: null,
    business: null,
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
    { name: 'document', align: 'left', label: 'Documento', field: 'document', sortable: true, format: val => val || 'Sin datos' },
    { name: 'phone', align: 'left', label: 'Telefono', field: 'phone', sortable: true, format: val => val || 'Sin datos' },
    { name: 'type', align: 'left', label: 'Tipo de persona', field: 'type', sortable: true, format: val => val?.description || 'Sin datos' },
    { name: 'business', align: 'left', label: 'Negocio', field: 'business', sortable: true, format: val => val|| 'Sin datos' },

    { name: 'is_active', label: 'Persona activa', field: 'is_active', align: 'center' },
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
    myForm.value.resetValidation()
}

const add = async (row) => {
    addStablishment.value = true;
    clean()
    const { data } = await request.get('register/areas/')
    areasOptions.value = data.results
    if (row.name) {
        editing.value = true
        user.value.uuid = row.uuid
        user.value.name = row.name
        user.value.document = row.document
        user.value.type = row.type?.code
        user.value.area = row.area
        user.value.phone = row.phone
        user.value.business = row.business
        user.value.rol = row.rol
        return
    }
    editing.value = false
}

const onDialogHide = () => {
    addStablishment.value = false
}

const save = async () => {
    const formData = new FormData();
    formData.append('name', user.value.name);
    formData.append('document', user.value.document);
    formData.append('type', user.value.type);
    formData.append('is_active', true);
    if (user.value.area) formData.append('area', user.value.area);
    if (user.value.phone) formData.append('phone', user.value.phone);
    if (user.value.business) formData.append('business', user.value.business);
    if (user.value.rol) formData.append('rol', user.value.rol);

    try {
        await request.post('register/persons/', formData);
        Notify.create({
            type: 'positive',
            message: 'Persona registrada',
            position: 'top',
        });
        startInfo()
        onDialogHide()
    } catch (error) {
        Notify.create({
            type: 'negative',
            message: 'Error al crear la persona',
            position: 'top',
        });     
    }
};

const update = async () => {
    const formData = new FormData();
    formData.append('name', user.value.name);
    formData.append('document', user.value.document);
    formData.append('type', user.value.type);
    formData.append('is_active', true);

    if (user.value.area) formData.append('area', user.value.area.id ? user.value.area.id : user.value.area);
    if (user.value.phone) formData.append('phone', user.value.phone);
    if (user.value.business) formData.append('business', user.value.business);
    if (user.value.rol) formData.append('rol', user.value.rol);

    try {
        await request.patch(`register/persons/${user.value.uuid}/`, formData);
        Notify.create({
            type: 'positive',
            message: 'Persona actualizada',
            position: 'top',
        });
        startInfo()
        onDialogHide()
    } catch (error) {
        Notify.create({
            type: 'negative',
            message: 'Error al crear la persona',
            position: 'top',
        });    
    }
}

const toggleIsActive = async (row) => {
    await request.patch(`register/persons/${row.uuid}/`, { is_active: row.is_active });
}


const startInfo = async () => {
    try {
        const response = await request.get('register/persons/', {
            params: {
                search: filter.value,
                page: pagination.page,
                page_size: pagination.rowsPerPage,
                type: typeFilter.value
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
        title: 'Eliminar persona',
        message: 'Estas seguro de eliminar esta persona?',
        cancel: true,
        persistent: true
    }).onOk(async () => {
        await request.delete(`register/persons/${row.uuid}/`)
        await startInfo()
    })
}

onMounted(async () => {
    startInfo()
})
</script>