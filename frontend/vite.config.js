import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 5173,
    host: true,
    // Academy exposes the dev server through a per-learner subdomain. Allow
    // that trusted parent domain so Vite's host-header protection accepts the
    // TaskFlow App service tab without opening the server to arbitrary hosts.
    allowedHosts: ['.academy.tekanaid.com'],
    // Dev-only: forward /api calls to the backend so the browser sees one origin
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
