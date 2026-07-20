import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
  ],
  // Base path khi deploy trên Frappe
  base: '/assets/dcnet_apps/htkk/',
  build: {
    // Output vào thư mục public của app
    outDir: path.resolve(__dirname, '../../public/htkk'),
    emptyDirBeforeWrite: true,
    rollupOptions: {
      input: {
        index: path.resolve(__dirname, 'index.html'),
        list: path.resolve(__dirname, 'list.html'),
      },
      output: {
        // File names với entry name
        entryFileNames: '[name].js',
        chunkFileNames: 'chunks/[name].js',
        assetFileNames: (assetInfo) => {
          if (assetInfo.name?.endsWith('.css')) {
            return '[name].css';
          }
          return 'assets/[name][extname]';
        },
      },
    },
  },
  server: {
    host: '0.0.0.0',
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
