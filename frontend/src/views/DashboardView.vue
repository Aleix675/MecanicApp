<template>
  <v-app>
    <v-navigation-drawer v-model="drawer" app>
      <v-list-item
        title="MecànicApp"
        subtitle="🔧 Taller"
        nav
        class="py-4"
      />
      <v-divider />
      <v-list density="compact" nav>
        <v-list-item prepend-icon="mdi-view-dashboard" title="Inici" to="/dashboard" />
        <v-list-item prepend-icon="mdi-car" title="Els meus vehicles" to="/vehicles" />
        <v-list-item prepend-icon="mdi-calendar" title="Les meves cites" to="/cites" />
      </v-list>
      <template #append>
        <v-list density="compact" nav>
          <v-list-item
            prepend-icon="mdi-logout"
            title="Tancar sessió"
            @click="logout"
          />
        </v-list>
      </template>
    </v-navigation-drawer>

    <v-app-bar app elevation="1">
      <v-app-bar-nav-icon @click="drawer = !drawer" />
      <v-app-bar-title>Benvingut, {{ auth.nom }}</v-app-bar-title>
    </v-app-bar>

    <v-main class="bg-grey-lighten-4">
      <v-container class="py-6">

        <!-- KPIs -->
        <v-row class="mb-4">
          <v-col cols="12" sm="4">
            <v-card rounded="lg" elevation="2">
              <v-card-text class="text-center">
                <div class="text-h3 font-weight-bold text-primary">{{ citesPendents }}</div>
                <div class="text-body-2 text-medium-emphasis mt-1">Cites pendents</div>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="12" sm="4">
            <v-card rounded="lg" elevation="2">
              <v-card-text class="text-center">
                <div class="text-h3 font-weight-bold text-success">{{ vehicles.length }}</div>
                <div class="text-body-2 text-medium-emphasis mt-1">Vehicles registrats</div>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="12" sm="4">
            <v-card rounded="lg" elevation="2">
              <v-card-text class="text-center">
                <div class="text-h3 font-weight-bold text-orange">{{ citesCompletades }}</div>
                <div class="text-body-2 text-medium-emphasis mt-1">Serveis completats</div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <v-row>
          <!-- Cites recents -->
          <v-col cols="12" md="7">
            <v-card rounded="lg" elevation="2">
              <v-card-title class="pa-4 pb-2">
                <v-icon class="mr-2">mdi-calendar-clock</v-icon>
                Les meves cites
                <v-spacer />
                <v-btn size="small" color="primary" to="/cites">Nova cita</v-btn>
              </v-card-title>
              <v-divider />
              <v-list lines="two">
                <template v-if="cites.length === 0">
                  <v-list-item>
                    <v-list-item-title class="text-medium-emphasis">
                      No tens cap cita. Reserva la primera!
                    </v-list-item-title>
                  </v-list-item>
                </template>
                <v-list-item
                  v-for="cita in citesRecents"
                  :key="cita.id"
                  :subtitle="`Vehicle #${cita.vehicle_id} · ${formatData(cita.data_hora_inici)}`"
                >
                  <template #title>
                    Cita #{{ cita.id }}
                  </template>
                  <template #append>
                    <v-chip
                      :color="colorEstat(cita.estat)"
                      size="small"
                      variant="tonal"
                    >
                      {{ cita.estat }}
                    </v-chip>
                  </template>
                </v-list-item>
              </v-list>
            </v-card>
          </v-col>

          <!-- Vehicles -->
          <v-col cols="12" md="5">
            <v-card rounded="lg" elevation="2">
              <v-card-title class="pa-4 pb-2">
                <v-icon class="mr-2">mdi-car</v-icon>
                Els meus vehicles
                <v-spacer />
                <v-btn size="small" color="primary" to="/vehicles">Gestionar</v-btn>
              </v-card-title>
              <v-divider />
              <v-list lines="two">
                <template v-if="vehicles.length === 0">
                  <v-list-item>
                    <v-list-item-title class="text-medium-emphasis">
                      No tens cap vehicle registrat.
                    </v-list-item-title>
                  </v-list-item>
                </template>
                <v-list-item
                  v-for="vehicle in vehicles"
                  :key="vehicle.id"
                  :title="`${vehicle.marca} ${vehicle.model}`"
                  :subtitle="`${vehicle.matricula} · ${vehicle.any_fabricacio || 'S/D'}`"
                  prepend-icon="mdi-car-side"
                />
              </v-list>
            </v-card>
          </v-col>
        </v-row>

      </v-container>
    </v-main>
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
const vehicles = ref([])

const citesRecents = computed(() => cites.value.slice(0, 5))
const citesPendents = computed(() =>
  cites.value.filter(c => c.estat === 'PENDENT' || c.estat === 'CONFIRMADA').length
)
const citesCompletades = computed(() =>
  cites.value.filter(c => c.estat === 'COMPLETADA').length
)

function colorEstat(estat) {
  const colors = {
    PENDENT: 'warning',
    CONFIRMADA: 'info',
    EN_PROCES: 'primary',
    COMPLETADA: 'success',
    CANCELADA: 'error'
  }
  return colors[estat] || 'grey'
}

function formatData(data) {
  return new Date(data).toLocaleString('ca-ES', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  })
}

async function logout() {
  auth.logout()
  router.push('/login')
}

onMounted(async () => {
  try {
    const [resCites, resVehicles] = await Promise.all([
      api.get('/cites/meves'),
      api.get('/vehicles/meus')
    ])
    cites.value = resCites.data
    vehicles.value = resVehicles.data
  } catch (e) {
    console.error(e)
  }
})
</script>