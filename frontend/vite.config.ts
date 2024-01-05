import path from "path"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  // choose output dir for 'npm run build'
  build: {
    outDir: "../app/static",
    emptyOutDir: true,
  },
})
