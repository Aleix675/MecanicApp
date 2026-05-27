<template>
  <v-app>
    <v-navigation-drawer v-model="drawer" app>
      <v-list-item title="MecànicApp" subtitle="🔧 Administrador" nav class="py-4" />
      <v-divider />
      <v-list density="compact" nav>
        <v-list-item prepend-icon="mdi-view-dashboard" title="Dashboard" @click="pestanya = 'dashboard'" />
        <v-list-item prepend-icon="mdi-calendar-multiple" title="Totes les cites" @click="pestanya = 'cites'" />
        <v-list-item prepend-icon="mdi-account-group" title="Empleats" @click="pestanya = 'empleats'" />
        <v-list-item prepend-icon="mdi-wrench" title="Serveis" @click="pestanya = 'serveis'" />
      </v-list>
      <template #append>
        <v-list density="compact" nav>
          <v-list-item prepend-icon="mdi-logout" title="Tancar sessió" @click="logout" />
        </v-list>
      </template>
    </v-navigation-drawer>

    <v-app-bar app elevation="1">
      <v-app-bar-nav-icon @click="drawer = !drawer" />
      <v-app-bar-title>Panell d'Administrador</v-app-bar-title>
    </v-app-bar>

    <v-main class="bg-grey-lighten-4">
      <v-container class="py-6">

        <!-- Dashboard estadístiques -->
        <div v-if="pestanya === 'dashboard' && stats">
          <v-row class="mb-4">
            <v-col cols="6" sm="3">
              <v-card rounded="lg" elevation="2">
                <v-card-text class="text-center">
                  <div class="text-h3 font-weight-bold text-primary">{{ stats.cites.total }}</div>
                  <div class="text-body-2 text-medium-emphasis mt-1">Total cites</div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="6" sm="3">
              <v-card rounded="lg" elevation="2">
                <v-card-text class="text-center">
                  <div class="text-h3 font-weight-bold text-success">{{ stats.cites.completades }}</div>
                  <div class="text-body-2 text-medium-emphasis mt-1">Completades</div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="6" sm="3">
              <v-card rounded="lg" elevation="2">
                <v-card-text class="text-center">
                  <div class="text-h3 font-weight-bold text-warning">{{ stats.cites.pendents }}</div>
                  <div class="text-body-2 text-medium-emphasis mt-1">Pendents</div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="6" sm="3">
              <v-card rounded="lg" elevation="2">
                <v-card-text class="text-center">
                  <div class="text-h3 font-weight-bold text-orange">{{ stats.ingressos_totals.toFixed(2) }} €</div>
                  <div class="text-body-2 text-medium-emphasis mt-1">Ingressos totals</div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12" md="6">
              <v-card rounded="lg" elevation="2">
                <v-card-title class="pa-4">Serveis més sol·licitats</v-card-title>
                <v-divider />
                <v-list>
                  <v-list-item v-for="(s, i) in stats.serveis_populars" :key="i" :title="s.nom"
                    :subtitle="`${s.total} cites`" prepend-icon="mdi-wrench" />
                </v-list>
              </v-card>
            </v-col>
            <v-col cols="12" md="6">
              <v-card rounded="lg" elevation="2">
                <v-card-title class="pa-4">Usuaris del sistema</v-card-title>
                <v-divider />
                <v-list>
                  <v-list-item prepend-icon="mdi-account" :title="stats.usuaris.clients.toString()"
                    subtitle="Clients" />
                  <v-list-item prepend-icon="mdi-account-hard-hat" :title="stats.usuaris.mechanics.toString()"
                    subtitle="Mecànics" />
                </v-list>
              </v-card>
            </v-col>
          </v-row>
        </div>

        <!-- Totes les cites -->
        <div v-if="pestanya === 'cites'">
          <v-card rounded="lg" elevation="2">
            <v-card-title class="pa-4">Totes les cites</v-card-title>
            <v-divider />
            <v-data-table :headers="headersCites" :items="totesCites" :items-per-page="15">
              <template #item.estat="{ item }">
                <v-chip :color="colorEstat(item.estat)" size="small" variant="tonal">{{ item.estat }}</v-chip>
              </template>
              <template #item.data_hora_inici="{ item }">
                {{ formatData(item.data_hora_inici) }}
              </template>
            </v-data-table>
          </v-card>
        </div>

        <!-- Serveis -->
        <div v-if="pestanya === 'serveis'">
          <v-card rounded="lg" elevation="2">
            <v-card-title class="pa-4 d-flex align-center">
              Serveis del taller
              <v-spacer />
              <v-btn color="primary" prepend-icon="mdi-plus" @click="obrirDialegServei()">
                Nou servei
              </v-btn>
            </v-card-title>
            <v-divider />
            <v-list lines="two">
              <v-list-item v-for="s in serveis" :key="s.id" :title="s.nom"
                :subtitle="`Base: ${s.duracio_base_min} min · SUV: ${s.duracio_suv_min} min · ${s.preu_orientatiu} €`"
                prepend-icon="mdi-wrench">
                <template #append>
                  <div class="d-flex align-center gap-2">
                    <v-chip :color="s.actiu ? 'success' : 'error'" size="small" variant="tonal">
                      {{ s.actiu ? 'Actiu' : 'Inactiu' }}
                    </v-chip>
                    <v-btn size="small" variant="tonal" color="primary" @click="obrirDialegServei(s)">
                      Editar
                    </v-btn>
                    <v-btn size="small" variant="tonal" color="error" @click="confirmarEliminarServei(s)">
                      Eliminar
                    </v-btn>
                  </div>
                </template>
              </v-list-item>
            </v-list>
          </v-card>
        </div>

        <!-- Empleats -->
        <div v-if="pestanya === 'empleats'">
          <v-card rounded="lg" elevation="2">
            <v-card-title class="pa-4 d-flex align-center">
              Mecànics del taller
              <v-spacer />
              <v-btn color="primary" prepend-icon="mdi-plus" @click="dialegMecanic = true">
                Nou mecànic
              </v-btn>
            </v-card-title>
            <v-divider />
            <v-list lines="two">
              <v-list-item v-for="m in mechanics" :key="m.id" :title="m.nom" :subtitle="m.email"
                prepend-icon="mdi-account-hard-hat">
                <template #append>
                  <v-chip color="success" size="small" variant="tonal">MECÀNIC</v-chip>
                </template>
              </v-list-item>
            </v-list>
          </v-card>
        </div>

        <!-- Diàleg crear/editar servei -->
        <v-dialog v-model="dialegServei" max-width="500">
          <v-card rounded="lg">
            <v-card-title class="pa-4">
              {{ serveiEditat ? 'Editar servei' : 'Nou servei' }}
            </v-card-title>
            <v-divider />
            <v-card-text class="pa-4">
              <v-alert v-if="errorServei" type="error" variant="tonal" density="compact" class="mb-4">
                {{ errorServei }}
              </v-alert>
              <v-text-field v-model="formServei.nom" label="Nom del servei" variant="outlined" density="compact"
                class="mb-3" />
              <v-textarea v-model="formServei.descripcio" label="Descripció" variant="outlined" density="compact"
                rows="2" class="mb-3" />
              <v-row>
                <v-col cols="6">
                  <v-text-field v-model="formServei.duracio_base_min" label="Durada base (min)" type="number"
                    variant="outlined" density="compact" />
                </v-col>
                <v-col cols="6">
                  <v-text-field v-model="formServei.duracio_suv_min" label="Durada SUV (min)" type="number"
                    variant="outlined" density="compact" />
                </v-col>
              </v-row>
              <v-text-field v-model="formServei.preu_orientatiu" label="Preu orientatiu (€)" type="number"
                variant="outlined" density="compact" class="mb-3 mt-2" />
              <v-switch v-model="formServei.actiu" label="Servei actiu" color="success" />
            </v-card-text>
            <v-card-actions class="pa-4">
              <v-btn variant="text" @click="dialegServei = false">Cancel·lar</v-btn>
              <v-spacer />
              <v-btn color="primary" :loading="loadingServei" @click="guardarServei">
                {{ serveiEditat ? 'Guardar canvis' : 'Crear servei' }}
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <!-- Diàleg confirmar eliminar servei -->
        <v-dialog v-model="dialegEliminarServei" max-width="400">
          <v-card rounded="lg">
            <v-card-title class="pa-4">Eliminar servei</v-card-title>
            <v-card-text>
              Estàs segur que vols eliminar <strong>{{ serveiAEliminar?.nom }}</strong>? Aquesta acció no es pot desfer.
            </v-card-text>
            <v-card-actions class="pa-4">
              <v-btn variant="text" @click="dialegEliminarServei = false">Cancel·lar</v-btn>
              <v-spacer />
              <v-btn color="error" :loading="loadingServei" @click="eliminarServei">Eliminar</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <!-- Diàleg nou mecànic -->
        <v-dialog v-model="dialegMecanic" max-width="450">
          <v-card rounded="lg">
            <v-card-title class="pa-4">Nou mecànic</v-card-title>
            <v-divider />
            <v-card-text class="pa-4">
              <v-alert v-if="errorMecanic" type="error" variant="tonal" density="compact" class="mb-4">
                {{ errorMecanic }}
              </v-alert>
              <v-text-field v-model="formMecanic.nom" label="Nom complet" variant="outlined" density="compact"
                class="mb-3" />
              <v-text-field v-model="formMecanic.email" label="Email" type="email" variant="outlined" density="compact"
                class="mb-3" />
              <v-text-field v-model="formMecanic.telefon" label="Telèfon (opcional)" variant="outlined"
                density="compact" class="mb-3" />
              <v-text-field v-model="formMecanic.password" label="Contrasenya inicial" type="password"
                variant="outlined" density="compact" />
            </v-card-text>
            <v-card-actions class="pa-4">
              <v-btn variant="text" @click="dialegMecanic = false">Cancel·lar</v-btn>
              <v-spacer />
              <v-btn color="primary" :loading="loadingMecanic" @click="crearMecanic">Crear mecànic</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

      </v-container>
    </v-main>
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
const pestanya = ref('dashboard')
const stats = ref(null)
const totesCites = ref([])
const mechanics = ref([])
const serveis = ref([])

const headersCites = [
  { title: 'ID', key: 'id' },
  { title: 'Vehicle', key: 'vehicle_id' },
  { title: 'Mecànic', key: 'mecanic_id' },
  { title: 'Inici', key: 'data_hora_inici' },
  { title: 'Estat', key: 'estat' },
  { title: 'Preu', key: 'preu_final' }
]

// Afegeix aquestes variables
const dialegServei = ref(false)
const dialegEliminarServei = ref(false)
const serveiEditat = ref(null)
const serveiAEliminar = ref(null)
const formServei = ref({ nom: '', descripcio: '', duracio_base_min: 60, duracio_suv_min: 90, preu_orientatiu: 0, actiu: true })
const errorServei = ref('')
const loadingServei = ref(false)

const dialegMecanic = ref(false)
const formMecanic = ref({ nom: '', email: '', password: '', telefon: '' })
const errorMecanic = ref('')
const loadingMecanic = ref(false)

function obrirDialegServei(servei = null) {
  serveiEditat.value = servei
  errorServei.value = ''
  if (servei) {
    formServei.value = { ...servei }
  } else {
    formServei.value = { nom: '', descripcio: '', duracio_base_min: 60, duracio_suv_min: 90, preu_orientatiu: 0, actiu: true }
  }
  dialegServei.value = true
}

function confirmarEliminarServei(servei) {
  serveiAEliminar.value = servei
  dialegEliminarServei.value = true
}

async function guardarServei() {
  errorServei.value = ''
  loadingServei.value = true
  try {
    if (serveiEditat.value) {
      await api.put(`/serveis/${serveiEditat.value.id}`, formServei.value)
    } else {
      await api.post('/serveis', formServei.value)
    }
    dialegServei.value = false
    const res = await api.get('/serveis')
    serveis.value = res.data
  } catch (e) {
    errorServei.value = e.response?.data?.detail || 'Error en guardar el servei'
  } finally {
    loadingServei.value = false
  }
}

async function eliminarServei() {
  loadingServei.value = true
  try {
    await api.delete(`/serveis/${serveiAEliminar.value.id}`)
    dialegEliminarServei.value = false
    const res = await api.get('/serveis')
    serveis.value = res.data
  } catch (e) {
    errorServei.value = e.response?.data?.detail || 'Error en eliminar'
  } finally {
    loadingServei.value = false
  }
}

async function crearMecanic() {
  errorMecanic.value = ''
  loadingMecanic.value = true
  try {
    await api.post('/auth/register', {
      nom: formMecanic.value.nom,
      email: formMecanic.value.email,
      password: formMecanic.value.password,
      telefon: formMecanic.value.telefon
    })
    // Buscar l'usuari creat i canviar-li el rol a MECANIC
    const resUsuaris = await api.get('/usuaris')
    const nouUsuari = resUsuaris.data.find(u => u.email === formMecanic.value.email)
    if (nouUsuari) {
      await api.put(`/admin/usuaris/${nouUsuari.id}/rol?nou_rol=MECANIC`)
    }
    dialegMecanic.value = false
    const resMecanics = await api.get('/admin/mechanics')
    mechanics.value = resMecanics.data
    formMecanic.value = { nom: '', email: '', password: '', telefon: '' }
  } catch (e) {
    errorMecanic.value = e.response?.data?.detail || 'Error en crear el mecànic'
  } finally {
    loadingMecanic.value = false
  }
}

function colorEstat(estat) {
  const colors = { PENDENT: 'warning', CONFIRMADA: 'info', EN_PROCES: 'primary', COMPLETADA: 'success', CANCELADA: 'error' }
  return colors[estat] || 'grey'
}

function formatData(data) {
  return new Date(data).toLocaleString('ca-ES', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

function logout() {
  auth.logout()
  router.push('/login')
}

onMounted(async () => {
  const [resStats, resCites, resMecanics, resServeis] = await Promise.all([
    api.get('/admin/estadistiques'),
    api.get('/cites'),
    api.get('/admin/mechanics'),
    api.get('/serveis')
  ])
  stats.value = resStats.data
  totesCites.value = resCites.data
  mechanics.value = resMecanics.data
  serveis.value = resServeis.data
})
</script>