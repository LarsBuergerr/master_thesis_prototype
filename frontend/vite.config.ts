import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// The frontend talks to the FastAPI backend. By default it calls
// http://localhost:8000 directly (CORS is enabled there for :5173). You can
// override the base URL via VITE_API_BASE, or use the dev proxy below by
// pointing VITE_API_BASE at "/api".
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});
