<template>
  <v-app>
    <v-navigation-drawer v-model="drawer" app>
      <v-list-item title="MecànicApp" subtitle="🔧 Taller" nav class="py-4" />
      <v-divider />
      <v-list density="compact" nav>
        <v-list-item prepend-icon="mdi-calendar-today" title="La meva agenda" to="/mecanic" />
      </v-list>
      <template #append>
        <v-list density="compact" nav>
          <v-list-item prepend-icon="mdi-logout" title="Tancar sessió" @click="logout" />
        </v-list>
      </template>
    </v-navigation-drawer>

    <v-app-bar app elevation="1">
      <v-app-bar-nav-icon @click="drawer = !drawer" />
      <v-app-bar-title>La meva agenda — {{ auth.nom }}</v-app-bar-title>
    </v-app-bar>

    <v-main class="bg-grey-lighten-4">
      <v-container class="py-6">

        <!-- KPIs -->
        <v-row class="mb-4">
          <v-col cols="6" sm="3">
            <v-card rounded="lg" elevation="2">
              <v-card-text class="text-center">
                <div class="text-h3 font-weight-bold text-primary">{{ citesAvui.length }}</div>
                <div class="text-body-2 text-medium-emphasis mt-1">Cites avui</div>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="6" sm="3">
            <v-card rounded="lg" elevation="2">
              <v-card-text class="text-center">
                <div class="text-h3 font-weight-bold text-success">{{ completadesAvui }}</div>
                <div class="text-body-2 text-medium-emphasis mt-1">Completades</div>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="6" sm="3">
            <v-card rounded="lg" elevation="2">
              <v-card-text class="text-center">
                <div class="text-h3 font-weight-bold text-warning">{{ pendentsAvui }}</div>
                <div class="text-body-2 text-medium-emphasis mt-1">Pendents</div>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="6" sm="3">
            <v-card rounded="lg" elevation="2">
              <v-card-text class="text-center">
                <div class="text-h3 font-weight-bold text-orange">{{ cites.length }}</div>
                <div class="text-body-2 text-medium-emphasis mt-1">Total assignades</div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Llista cites -->
        <v-card rounded="lg" elevation="2">
          <v-card-title class="pa-4">
            <v-icon class="mr-2">mdi-wrench</v-icon>
            Cites assignades
          </v-card-title>
          <v-divider />
          <v-list lines="three">
            <template v-if="cites.length === 0">
              <v-list-item>
                <v-list-item-title class="text-medium-emphasis">No tens cites assignades.</v-list-item-title>
              </v-list-item>
            </template>
            <v-list-item v-for="cita in cites" :key="cita.id" class="py-3">
              <template #prepend>
                <v-icon :color="colorEstat(cita.estat)" size="32">mdi-car-wrench</v-icon>
              </template>
              <template #title>
                Cita #{{ cita.id }} — Vehicle #{{ cita.vehicle_id }}
              </template>
              <template #subtitle>
                {{ formatData(cita.data_hora_inici) }} → {{ formatData(cita.data_hora_fi) }}
                <br>{{ cita.observacions_client || 'Sense observacions' }}
              </template>
              <template #append>
                <div class="d-flex flex-column align-end gap-2">
                  <v-chip :color="colorEstat(cita.estat)" size="small" variant="tonal">
                    {{ cita.estat }}
                  </v-chip>
                  <v-btn
                    v-if="cita.estat === 'PENDENT' || cita.estat === 'CONFIRMADA'"
                    size="small"
                    color="primary"
                    variant="tonal"
                    @click="obrirCompletarDialeg(cita)"
                  >
                    Completar
                  </v-btn>
                  <v-btn
                    size="small"
                    color="info"
                    variant="text"
                    @click="obrirNotaDialeg(cita)"
                  >
                    + Nota
                  </v-btn>
                </div>
              </template>
            </v-list-item>
          </v-list>
        </v-card>
      </v-container>
    </v-main>

    <!-- Diàleg completar -->
    <v-dialog v-model="dialegCompletar" max-width="400">
      <v-card rounded="lg">
        <v-card-title class="pa-4">Completar cita #{{ citaSeleccionada?.id }}</v-card-title>
        <v-divider />
        <v-card-text class="pa-4">
          <v-text-field
            v-model="preuFinal"
            label="Preu final (€)"
            type="number"
            variant="outlined"
            density="compact"
            prepend-inner-icon="mdi-currency-eur"
          />
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-btn variant="text" @click="dialegCompletar = false">Cancel·lar</v-btn>
          <v-spacer />
          <v-btn color="success" :loading="loading" @click="completarCita">Confirmar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Diàleg nota tècnica -->
    <v-dialog v-model="dialegNota" max-width="400">
      <v-card rounded="lg">
        <v-card-title class="pa-4">Nota tècnica — Cita #{{ citaSeleccionada?.id }}</v-card-title>
        <v-divider />
        <v-card-text class="pa-4">
          <v-textarea
            v-model="notaContingut"
            label="Nota tècnica"
            variant="outlined"
            density="compact"
            rows="4"
            placeholder="Ex: Frens desgastats, recomanat canvi en 6 mesos..."
          />
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-btn variant="text" @click="dialegNota = false">Cancel·lar</v-btn>
          <v-spacer />
          <v-btn color="primary" :loading="loading" @click="guardarNota">Guardar nota</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-app>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const router = useRouter()
const auth = useAuthStore()
const drawer = ref(true)
const cites = ref([])
const loading = ref(false)
const dialegCompletar = ref(false)
const dialegNota = ref(false)
const citaSeleccionada = ref(null)
const preuFinal = ref(0)
const notaContingut = ref('')

const avui = new Date().toDateString()
const citesAvui = computed(() =>
  cites.value.filter(c => new Date(c.data_hora_inici).toDateString() === avui)
)
const completadesAvui = computed(() =>
  citesAvui.value.filter(c => c.estat === 'COMPLETADA').length
)
const pendentsAvui = computed(() =>
  citesAvui.value.filter(c => c.estat === 'PENDENT' || c.estat === 'CONFIRMADA' ).length
)

function colorEstat(estat) {
  const colors = { PENDENT: 'warning', CONFIRMADA: 'info', EN_PROCES: 'primary', COMPLETADA: 'success', CANCELADA: 'error' }
  return colors[estat] || 'grey'
}

function formatData(data) {
  return new Date(data).toLocaleString('ca-ES', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

function obrirCompletarDialeg(cita) {
  citaSeleccionada.value = cita
  preuFinal.value = 0
  dialegCompletar.value = true
}

function obrirNotaDialeg(cita) {
  citaSeleccionada.value = cita
  notaContingut.value = ''
  dialegNota.value = true
}

async function completarCita() {
  loading.value = true
  try {
    await api.put(`/cites/${citaSeleccionada.value.id}/completar?preu_final=${preuFinal.value}`)
    dialegCompletar.value = false
    await carregarCites()
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function guardarNota() {
  loading.value = true
  try {
    await api.post(`/cites/${citaSeleccionada.value.id}/notes`, { contingut: notaContingut.value })
    dialegNota.value = false
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function carregarCites() {
  const res = await api.get('/cites/meves-assignades')
  cites.value = res.data
}

function logout() {
  auth.logout()
  router.push('/login')
}

onMounted(carregarCites)
</script>