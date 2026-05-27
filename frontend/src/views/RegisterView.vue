<template>
  <v-app>
    <v-main class="fondo-login">
      <v-container class="fill-height" fluid>
        <v-row align="center" justify="center">
          <v-col cols="12" sm="8" md="4">

            <v-card elevation="4" rounded="lg" class="pa-4">
              <v-card-title class="text-center text-h5 font-weight-bold pt-4">
                🔧 MecànicApp
              </v-card-title>
              <v-card-subtitle class="text-center mb-4">
                Crea el teu compte
              </v-card-subtitle>

              <v-card-text>
                <v-alert
                  v-if="error"
                  type="error"
                  variant="tonal"
                  class="mb-4"
                  density="compact"
                >
                  {{ error }}
                </v-alert>

                <v-alert
                  v-if="exit"
                  type="success"
                  variant="tonal"
                  class="mb-4"
                  density="compact"
                >
                  Compte creat! Ara pots iniciar sessió.
                </v-alert>

                <v-text-field
                  v-model="nom"
                  label="Nom complet"
                  prepend-inner-icon="mdi-account"
                  variant="outlined"
                  density="compact"
                  class="mb-3"
                />

                <v-text-field
                  v-model="email"
                  label="Email"
                  type="email"
                  prepend-inner-icon="mdi-email"
                  variant="outlined"
                  density="compact"
                  class="mb-3"
                />

                <v-text-field
                  v-model="telefon"
                  label="Telèfon (opcional)"
                  prepend-inner-icon="mdi-phone"
                  variant="outlined"
                  density="compact"
                  class="mb-3"
                />

                <v-text-field
                  v-model="password"
                  label="Contrasenya"
                  :type="showPassword ? 'text' : 'password'"
                  prepend-inner-icon="mdi-lock"
                  :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                  @click:append-inner="showPassword = !showPassword"
                  variant="outlined"
                  density="compact"
                  class="mb-4"
                />


                <v-btn
                  block
                  color="primary"
                  size="large"
                  :loading="loading"
                  @click="register"
                >
                  Crear compte
                </v-btn>

                <v-divider class="my-4" />

                <p class="text-center text-body-2">
                  Ja tens compte?
                  <router-link to="/login" class="text-primary">
                    Inicia sessió
                  </router-link>
                </p>
              </v-card-text>
            </v-card>

          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const nom = ref('')
const email = ref('')
const telefon = ref('')
const password = ref('')
const showPassword = ref(false)
const loading = ref(false)
const error = ref('')
const exit = ref(false)

async function register() {
  error.value = ''
  exit.value = false
  loading.value = true
  try {
    await auth.register(nom.value, email.value, password.value, telefon.value)
    exit.value = true
    setTimeout(() => router.push('/login'), 2000)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error en registrar-se'
  } finally {
    loading.value = false
  }
}
</script>
<style scoped>
.fondo-login {
  /* Crea un degradado moderno entre tonos oscuros y azulados */
  background: linear-gradient(135deg, #1717b5 0%, #0f172a 100%);
  background-size: cover;   
  min-height: 100vh;
}
</style>
