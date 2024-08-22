<template>
    <div class="q-pa-md q-gutter-sm">
        <div>
            <q-btn dense color="primary" label="Actualizar" @click="startInfo" />
        </div>

        <q-table title="Personas dentro del edificio sin salida" :rows="rows" :columns="columns" row-key="name">
            <template v-slot:body-cell="props">
                <q-td :props="props">
                    <div>
                        {{ props.value }}
                    </div>
                </q-td>
            </template>
            <template v-slot:top-right>
                <q-input dense readonly debounce="300" v-model="numberPersons" placeholder="Cantidad de personas"></q-input>
            </template>
            <template v-slot:bottom>
                <q-pagination v-model="pagination.page" max="20" color="primary" boundary-numbers input
                    @update:model-value="startInfo" />
            </template>
        </q-table>
    </div>
</template>
<script setup>
import { onMounted, ref, reactive } from 'vue'
import request from 'src/utils/axios.js';
import { required, lengthRange } from 'src/utils/validations.js';
import { useQuasar } from 'quasar'
import { Notify } from 'quasar';
import moment from 'moment'

const $q = useQuasar()
const myForm = ref(null)
const filter = ref('')
const numberPersons = ref('')
const pagination = reactive({
    page: 1,
    rowsPerPage: 10,
    rowsNumber: 0
})
const editing = ref(false)

const rows = ref([])
const addStablishment = ref(false)
const columns = ref([
    { name: 'check_in', align: 'center', label: 'Ingreso.', field: row => moment(row.check_in), format: val => val.format('LTS'), sortable: true },
    { name: 'person_name', align: 'left', label: 'Nombre', field: 'person_name', sortable: true, format: val => val || 'Sin datos' },
    { name: 'person_document', align: 'left', label: 'Documento', field: 'person_document', sortable: true, format: val => val || 'Sin datos' },
])

const clean = () => {
    for (const key in user.value) {
        if (Object.hasOwnProperty.call(user.value, key)) {
            user.value[key] = null;
        }
    }
}

const onDialogHide = () => {
    addStablishment.value = false
}

const startInfo = async () => {
    try {
        const response = await request.get('checking/inside/')
        rows.value = response.data
        numberPersons.value = `${response.data[0]?.people_inside_count} personas`
    } catch (error) {
    }
}

onMounted(async () => {
    startInfo()
})
</script>