import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server : {
    port : 8080,
    proxy : {
      '/upload' : {
        target : 'http://127.0.0.1:5500/',
        changeOrigin : true,
        secure : false
      },
      '/login' : {
        target : 'http://127.0.0.1:5500/',
        changeOrigin : true,
        secure : false
      },
      '/signup' : {
        target : 'http://127.0.0.1:5500/',
        changeOrigin : true,
        secure : false
      }, 
      '/blogs' : {
        target : 'http://127.0.0.1:5500/',
        changeOrigin : true,
        secure : false
      }
    }
  },
  preview : {
    port : 8080
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
})
