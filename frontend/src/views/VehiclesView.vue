<template>
  <v-app>
    <v-navigation-drawer v-model="drawer" app>
      <v-list-item title="MecànicApp" subtitle="🔧 Taller" nav class="py-4" />
      <v-divider />
      <v-list density="compact" nav>
        <v-list-item prepend-icon="mdi-view-dashboard" title="Inici" to="/dashboard" />
        <v-list-item prepend-icon="mdi-car" title="Els meus vehicles" to="/vehicles" />
        <v-list-item prepend-icon="mdi-calendar" title="Les meves cites" to="/cites" />
      </v-list>
      <template #append>
        <v-list density="compact" nav>
          <v-list-item prepend-icon="mdi-logout" title="Tancar sessió" @click="logout" />
        </v-list>
      </template>
    </v-navigation-drawer>

    <v-app-bar app elevation="1">
      <v-app-bar-nav-icon @click="drawer = !drawer" />
      <v-app-bar-title>Els meus vehicles</v-app-bar-title>
      <v-btn color="primary" prepend-icon="mdi-plus" @click="obrirDialeg()">
        Afegir vehicle
      </v-btn>
    </v-app-bar>

    <v-main class="bg-grey-lighten-4">
      <v-container class="py-6">

        <v-row v-if="vehicles.length === 0">
          <v-col cols="12" class="text-center py-12">
            <v-icon size="64" color="grey-lighten-1">mdi-car-off</v-icon>
            <p class="text-h6 text-medium-emphasis mt-4">No tens cap vehicle registrat</p>
            <v-btn color="primary" class="mt-4" @click="obrirDialeg()">Afegir primer vehicle</v-btn>
          </v-col>
        </v-row>

        <v-row>
          <v-col v-for="vehicle in vehicles" :key="vehicle.id" cols="12" sm="6" md="4">
            <v-card rounded="lg" elevation="2">
              <v-card-title class="pa-4 pb-2">
                <v-icon class="mr-2" color="primary">mdi-car-side</v-icon>
                {{ vehicle.marca }} {{ vehicle.model }}
              </v-card-title>
              <v-card-text>
                <v-list density="compact">
                  <v-list-item prepend-icon="mdi-card-account-details" :title="vehicle.matricula" subtitle="Matrícula" />
                  <v-list-item prepend-icon="mdi-calendar" :title="vehicle.any_fabricacio?.toString() || 'No especificat'" subtitle="Any" />
                  <v-list-item prepend-icon="mdi-car-info" :title="vehicle.tipus || 'No especificat'" subtitle="Tipus" />
                </v-list>
              </v-card-text>
              <v-card-actions class="pa-4 pt-0">
                <v-btn variant="tonal" color="primary" size="small" @click="obrirDialeg(vehicle)">
                  Editar
                </v-btn>
                <v-btn variant="tonal" color="error" size="small" @click="confirmarEliminar(vehicle)">
                  Eliminar
                </v-btn>
                <v-spacer />
                <v-btn variant="tonal" color="success" size="small" to="/cites">
                  Reservar cita
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>

      </v-container>
    </v-main>

    <!-- Diàleg crear/editar -->
    <v-dialog v-model="dialeg" max-width="500">
      <v-card rounded="lg">
        <v-card-title class="pa-4">
          {{ vehicleEditat ? 'Editar vehicle' : 'Afegir vehicle' }}
        </v-card-title>
        <v-divider />
        <v-card-text class="pa-4">
          <v-alert v-if="error" type="error" variant="tonal" density="compact" class="mb-4">
            {{ error }}
          </v-alert>
          <v-text-field v-model="form.marca" label="Marca" variant="outlined" density="compact" class="mb-3" />
          <v-text-field v-model="form.model" label="Model" variant="outlined" density="compact" class="mb-3" />
          <v-text-field v-model="form.matricula" label="Matrícula" variant="outlined" density="compact" class="mb-3" :disabled="!!vehicleEditat" />
          <v-text-field v-model="form.any_fabricacio" label="Any de fabricació" type="number" variant="outlined" density="compact" class="mb-3" />
          <v-select
            v-model="form.tipus"
            label="Tipus de vehicle"
            :items="['TURISME', 'SUV', 'FURGONETA', 'CAMIO']"
            variant="outlined"
            density="compact"
          />
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-btn variant="text" @click="dialeg = false">Cancel·lar</v-btn>
          <v-spacer />
          <v-btn color="primary" :loading="loading" @click="guardarVehicle">
            {{ vehicleEditat ? 'Guardar canvis' : 'Afegir vehicle' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Diàleg confirmar eliminar -->
    <v-dialog v-model="dialegEliminar" max-width="400">
      <v-card rounded="lg">
        <v-card-title class="pa-4">Eliminar vehicle</v-card-title>
        <v-card-text>
          Estàs segur que vols eliminar <strong>{{ vehicleAEliminar?.marca }} {{ vehicleAEliminar?.model }}</strong>?
          Aquesta acció no es pot desfer.
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-btn variant="text" @click="dialegEliminar = false">Cancel·lar</v-btn>
          <v-spacer />
          <v-btn color="error" :loading="loading" @click="eliminarVehicle">Eliminar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-app>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const router = useRouter()
const auth = useAuthStore()
const drawer = ref(true)
const vehicles = ref([])
const dialeg = ref(false)
const dialegEliminar = ref(false)
const vehicleEditat = ref(null)
const vehicleAEliminar = ref(null)
const loading = ref(false)
const error = ref('')

const form = ref({ marca: '', model: '', matricula: '', any_fabricacio: null, tipus: 'TURISME' })

function obrirDialeg(vehicle = null) {
  vehicleEditat.value = vehicle
  error.value = ''
  if (vehicle) {
    form.value = { ...vehicle }
  } else {
    form.value = { marca: '', model: '', matricula: '', any_fabricacio: null, tipus: 'TURISME' }
  }
  dialeg.value = true
}

function confirmarEliminar(vehicle) {
  vehicleAEliminar.value = vehicle
  dialegEliminar.value = true
}

async function carregarVehicles() {
  const res = await api.get('/vehicles/meus')
  vehicles.value = res.data
}

async function guardarVehicle() {
  error.value = ''
  loading.value = true
  try {
    if (vehicleEditat.value) {
      await api.put(`/vehicles/${vehicleEditat.value.id}`, {
        marca: form.value.marca,
        model: form.value.model,
        any_fabricacio: form.value.any_fabricacio ? parseInt(form.value.any_fabricacio) : null,
        matricula: form.value.matricula,
        tipus: form.value.tipus
      })
    } else {
      await api.post('/vehicles', {
        usuari_id: parseInt(auth.userId),
        marca: form.value.marca,
        model: form.value.model,
        any_fabricacio: form.value.any_fabricacio ? parseInt(form.value.any_fabricacio) : null,
        matricula: form.value.matricula,
        tipus: form.value.tipus
      })
    }
    dialeg.value = false
    await carregarVehicles()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error en guardar el vehicle'
  } finally {
    loading.value = false
  }
}

async function eliminarVehicle() {
  loading.value = true
  try {
    await api.delete(`/vehicles/${vehicleAEliminar.value.id}`)
    dialegEliminar.value = false
    await carregarVehicles()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error en eliminar'
  } finally {
    loading.value = false
  }
}

function logout() {
  auth.logout()
  router.push('/login')
}

onMounted(carregarVehicles)
</script>