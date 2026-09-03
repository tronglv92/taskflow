/**
 * TaskFlow Frontend Application
 * Platform Engineering Bootcamp Reference Application
 *
 * Students will build and expand this Vue.js application throughout the bootcamp.
 */

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/main.css'

// Create Vue application
const app = createApp(App)

// Pinia holds global state (task list, auth session)
const pinia = createPinia()

// Install plugins
app.use(pinia)
app.use(router)

// Mount application
app.mount('#app')

console.log('🚀 TaskFlow Frontend Started')
console.log('📚 Platform Engineering Bootcamp - TeKanAid Academy')
