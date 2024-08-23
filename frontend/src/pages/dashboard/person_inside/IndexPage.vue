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
        </q-table>
    </div>
</template>
<script setup>
import { onMounted, ref, reactive } from 'vue'
import request from 'src/utils/axios.js';
import moment from 'moment'

const numberPersons = ref('')
const pagination = reactive({
    page: 1,
    rowsPerPage: 10,
    rowsNumber: 0
})

const rows = ref([])
const columns = ref([
    { name: 'check_in', align: 'center', label: 'Ingreso.', field: row => moment(row.check_in), format: val => val.format('LTS'), sortable: true },
    { name: 'person_name', align: 'left', label: 'Nombre', field: 'person_name', sortable: true, format: val => val || 'Sin datos' },
    { name: 'person_document', align: 'left', label: 'Documento', field: 'person_document', sortable: true, format: val => val || 'Sin datos' },
])

const startInfo = async () => {
    try {
        const response = await request.get('checking/inside/')
        rows.value = response.data
        if (rows.value.length == 0) {
            numberPersons.value = '0 personas en el edificio'
            return
        }
        numberPersons.value = `${response.data[0]?.people_inside_count} personas`
    } catch (error) {
    }
}

onMounted(async () => {
    startInfo()
})
</script>