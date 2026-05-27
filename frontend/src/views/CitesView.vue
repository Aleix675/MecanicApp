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
      <v-app-bar-title>Les meves cites</v-app-bar-title>
      <v-btn color="primary" prepend-icon="mdi-plus" @click="dialeg = true">Nova cita</v-btn>
    </v-app-bar>

    <v-main class="bg-grey-lighten-4">
      <v-container class="py-6">

        <v-row v-if="cites.length === 0">
          <v-col class="text-center py-12">
            <v-icon size="64" color="grey-lighten-1">mdi-calendar-blank</v-icon>
            <p class="text-h6 text-medium-emphasis mt-4">No tens cap cita reservada</p>
            <v-btn color="primary" class="mt-4" @click="dialeg = true">Reservar primera cita</v-btn>
          </v-col>
        </v-row>

        <v-card v-else rounded="lg" elevation="2">
          <v-data-table
            :headers="headers"
            :items="cites"
            :items-per-page="10"
          >
            <template #item.estat="{ item }">
              <v-chip :color="colorEstat(item.estat)" size="small" variant="tonal">
                {{ item.estat }}
              </v-chip>
            </template>
            <template #item.data_hora_inici="{ item }">
              {{ formatData(item.data_hora_inici) }}
            </template>
            <template #item.data_hora_fi="{ item }">
              {{ formatData(item.data_hora_fi) }}
            </template>
            <template #item.accions="{ item }">
              <v-btn
                v-if="item.estat !== 'CANCELADA' && item.estat !== 'COMPLETADA'"
                size="small"
                color="error"
                variant="tonal"
                @click="cancellarCita(item.id)"
              >
                Cancel·lar
              </v-btn>
            </template>
          </v-data-table>
        </v-card>

      </v-container>
    </v-main>

    <!-- Diàleg nova cita -->
    <v-dialog v-model="dialeg" max-width="520">
      <v-card rounded="lg">
        <v-card-title class="pa-4">Nova cita</v-card-title>
        <v-divider />
        <v-card-text class="pa-4">
          <v-alert v-if="error" type="error" variant="tonal" density="compact" class="mb-4">{{ error }}</v-alert>

          <v-select
            v-model="form.vehicle_id"
            label="Vehicle"
            :items="vehicles"
            :item-title="v => `${v.marca} ${v.model} - ${v.matricula}`"
            item-value="id"
            variant="outlined"
            density="compact"
            class="mb-3"
          />

          <v-select
            v-model="form.servei_id"
            label="Servei"
            :items="serveis"
            item-title="nom"
            item-value="id"
            variant="outlined"
            density="compact"
            class="mb-3"
          />

          <v-text-field
            v-model="form.data_hora_inici"
            label="Data i hora"
            type="datetime-local"
            variant="outlined"
            density="compact"
            class="mb-3"
          />

          <v-textarea
            v-model="form.observacions_client"
            label="Observacions (opcional)"
            variant="outlined"
            density="compact"
            rows="2"
            class="mb-3"
          />

          <!-- Disponibilitat -->
          <v-btn
            variant="tonal"
            color="info"
            block
            class="mb-3"
            :loading="loadingDisp"
            @click="comprovarDisponibilitat"
          >
            Comprovar disponibilitat
          </v-btn>

          <v-alert v-if="disponibilitat" :type="disponibilitat.disponible ? 'success' : 'error'" variant="tonal" density="compact">
            <span v-if="disponibilitat.disponible">
              ✅ Disponible — Hora fi: {{ formatData(disponibilitat.hora_fi) }} · {{ disponibilitat.mechanics_disponibles }} mecànics lliures
            </span>
            <span v-else>❌ No hi ha mecànics disponibles en aquest horari</span>
          </v-alert>
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-btn variant="text" @click="dialeg = false">Cancel·lar</v-btn>
          <v-spacer />
          <v-btn color="primary" :loading="loading" :disabled="!disponibilitat?.disponible" @click="crearCita">
            Confirmar cita
          </v-btn>
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
const cites = ref([])
const vehicles = ref([])
const serveis = ref([])
const dialeg = ref(false)
const loading = ref(false)
const loadingDisp = ref(false)
const error = ref('')
const disponibilitat = ref(null)

const form = ref({
  vehicle_id: null,
  servei_id: null,
  data_hora_inici: '',
  observacions_client: ''
})

const headers = [
  { title: 'ID', key: 'id', width: '60px' },
  { title: 'Vehicle', key: 'vehicle_id' },
  { title: 'Servei', key: 'servei_id' },
  { title: 'Inici', key: 'data_hora_inici' },
  { title: 'Fi', key: 'data_hora_fi' },
  { title: 'Estat', key: 'estat' },
  { title: 'Accions', key: 'accions', sortable: false }
]

function colorEstat(estat) {
  const colors = { PENDENT: 'warning', CONFIRMADA: 'info', EN_PROCES: 'primary', COMPLETADA: 'success', CANCELADA: 'error' }
  return colors[estat] || 'grey'
}

function formatData(data) {
  return new Date(data).toLocaleString('ca-ES', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

async function comprovarDisponibilitat() {
  if (!form.value.servei_id || !form.value.data_hora_inici) {
    error.value = 'Selecciona servei i data primer'
    return
  }
  error.value = ''
  loadingDisp.value = true
  try {
    const vehicle = vehicles.value.find(v => v.id === form.value.vehicle_id)
    const res = await api.post('/cites/disponibilitat', {
      servei_id: form.value.servei_id,
      data_hora_inici: new Date(form.value.data_hora_inici).toISOString(),
      tipus_vehicle: vehicle?.tipus || 'TURISME'
    })
    disponibilitat.value = res.data
  } catch (e) {
    error.value = 'Error en comprovar disponibilitat'
  } finally {
    loadingDisp.value = false
  }
}

async function crearCita() {
  error.value = ''
  loading.value = true
  try {
    await api.post('/cites', {
      ...form.value,
      data_hora_inici: new Date(form.value.data_hora_inici).toISOString()
    })
    dialeg.value = false
    disponibilitat.value = null
    await carregarCites()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error en crear la cita'
  } finally {
    loading.value = false
  }
}

async function cancellarCita(id) {
  try {
    await api.put(`/cites/${id}/cancellar`)
    await carregarCites()
  } catch (e) {
    console.error(e)
  }
}

async function carregarCites() {
  const res = await api.get('/cites/meves')
  cites.value = res.data
}

function logout() {
  auth.logout()
  router.push('/login')
}

onMounted(async () => {
  const [resCites, resVehicles, resServeis] = await Promise.all([
    api.get('/cites/meves'),
    api.get('/vehicles/meus'),
    api.get('/serveis')
  ])
  cites.value = resCites.data
  vehicles.value = resVehicles.data
  serveis.value = resServeis.data
})
</script>