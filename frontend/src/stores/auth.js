import { defineStore } from 'pinia'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    userId: localStorage.getItem('userId') || null,
    rol: localStorage.getItem('rol') || null,
    nom: localStorage.getItem('nom') || null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.rol === 'ADMIN',
    isMecanic: (state) => state.rol === 'MECANIC',
    isClient: (state) => state.rol === 'CLIENT'
  },

  actions: {
    async login(email, password) {
      const response = await api.post('/auth/login', { email, password })
      
      this.token = response.data.access_token

      // Al login action, després de guardar el token:
      this.userId = response.data.id  // cal afegir id al TokenResponse del backend

      this.rol = response.data.rol
      this.nom = response.data.nom
      localStorage.setItem('token', this.token)

      localStorage.setItem('userId', this.userId)

      localStorage.setItem('rol', this.rol)
      localStorage.setItem('nom', this.nom)
      return response.data
    },

    async register(nom, email, password, telefon) {
      return await api.post('/auth/register', { nom, email, password, telefon })
    },

    logout() {
      this.token = null
      this.rol = null
      this.nom = null
      this.userId = null
      localStorage.removeItem('token')
      localStorage.removeItem('rol')
      localStorage.removeItem('nom')
      localStorage.removeItem('userId')
    }
  }
})