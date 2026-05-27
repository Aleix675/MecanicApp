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
                Inicia sessió per continuar
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
                  v-model="password"
                  label="Contrasenya"
                  :type="showPassword ? 'text' : 'password'"
                  prepend-inner-icon="mdi-lock"
                  :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                  @click:append-inner="showPassword = !showPassword"
                  variant="outlined"
                  density="compact"
                  class="mb-4"
                  @keyup.enter="login"
                />

                <v-btn
                  block
                  color="primary"
                  size="large"
                  :loading="loading"
                  @click="login"
                >
                  Iniciar sessió
                </v-btn>

                <v-divider class="my-4" />

                <p class="text-center text-body-2">
                  No tens compte?
                  <router-link to="/register" class="text-primary">
                    Registra't
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

const email = ref('')
const password = ref('')
const showPassword = ref(false)
const loading = ref(false)
const error = ref('')

async function login() {
  error.value = ''
  loading.value = true
  try {
    const data = await auth.login(email.value, password.value)
    // Redirigir segons rol
    if (data.rol === 'ADMIN') {
      router.push('/admin')
    } else if (data.rol === 'MECANIC') {
      router.push('/mecanic')
    } else {
      router.push('/dashboard')
    }
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error en iniciar sessió'
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