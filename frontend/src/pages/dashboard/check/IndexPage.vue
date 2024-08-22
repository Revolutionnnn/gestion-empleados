<template>
    <div class="q-pa-md flex flex-center full-height">
      <q-card class="q-pa-lg" style="max-width: 500px; width: 100%;">
        <q-card-section>
          <div class="text-h6 text-center q-mb-md">
            Control de ingreso y salida 
          </div>
          <q-form @submit.prevent="handleSubmit" ref="myForm">
            <div class="q-gutter-md">
              <q-card-section class="row q-col-gutter-md">
                <q-input
                  outlined
                  v-model="user.document"
                  label="Número de documento"
                  class="col-12"
                  :rules="[required, lengthRange(0, 20), isInteger]"
                  lazy-rules
                />
                <q-select v-if="motive" outlined use-chips v-model="user.reason" :options="REASON_CHOICES"
                                label="Motivo de retiro" class="col-12 col-md-12" option-label="description" option-value="code" map-options
                                emit-value />
              </q-card-section>
            </div>
  
            <q-card-actions align="right" class="q-mt-md">
                <q-btn 
                    color="primary" 
                    :label="motive ? 'Quitar motivo' : 'Agregar motivo'" 
                    @click="toggleMotive" 
                />              
                <q-btn color="primary" label="Guardar" type="submit" />
            </q-card-actions>
          </q-form>
        </q-card-section>
      </q-card>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { required, lengthRange, isInteger } from 'src/utils/validations.js'
  import { Notify } from 'quasar';
  import { REASON_CHOICES } from 'src/constants/users'
  import request from 'src/utils/axios.js';

  const myForm = ref(null)
  const motive = ref(false)
  const user = ref({
    document: null,
    reason: null
  })
  
  const handleSubmit = async () => {
    const validation = await myForm.value.validate()
    if (!validation) return

    save()
  }
  const toggleMotive = () => {
    motive.value = !motive.value
    if (!motive.value) {
        user.value.reason = null
    }
  }

  const save = async () => {
    const formData = new FormData();
    if (user.value.reason) formData.append('reason', user.value.reason);
    try {
        const respuesta = await request.post(`checking/${user.value.document}/`, formData)
        user.value.document = null
        if (!respuesta.data.check_out) {
        Notify.create({
            type: 'positive',
            message: 'Su ingreso se ha registrado exitosamente',
            position: 'top',
        });
        return
    }
    Notify.create({
            type: 'positive',
            message: 'Su salida se ha registrado exitosamente',
            position: 'top',
        });
    } catch (error) {
        return
    }
  }
  </script>
  
  <style scoped>
  .full-height {
    height: 100vh;
  }
  
  .flex-center {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  </style>
  