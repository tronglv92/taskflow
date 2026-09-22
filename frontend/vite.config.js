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
    // Dev-only: forward /api calls to the backend so the browser sees one origin.
    // Defaults to localhost for a student running the backend directly on their
    // own machine; Docker Compose overrides this via VITE_API_PROXY_TARGET since
    // "localhost" inside the frontend container would otherwise mean itself,
    // not the separate backend container.
    proxy: {
      '/api': {
        target: process.env.VITE_API_PROXY_TARGET || 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
