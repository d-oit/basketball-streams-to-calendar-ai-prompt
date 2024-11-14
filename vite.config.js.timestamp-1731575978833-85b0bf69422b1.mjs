// vite.config.js
import { fileURLToPath, URL } from "url";
import { defineConfig, loadEnv } from "file:///workspaces/basketball-streams-to-calendar-ai-prompt/node_modules/vite/dist/node/index.js";
import react from "file:///workspaces/basketball-streams-to-calendar-ai-prompt/node_modules/@vitejs/plugin-react/dist/index.mjs";
import { resolve } from "path";
var __vite_injected_original_dirname = "/workspaces/basketball-streams-to-calendar-ai-prompt";
var __vite_injected_original_import_meta_url = "file:///workspaces/basketball-streams-to-calendar-ai-prompt/vite.config.js";
var vite_config_default = defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  return {
    server: {
      host: "::",
      port: "8080"
    },
    plugins: [react()],
    resolve: {
      alias: [
        {
          find: "@",
          replacement: fileURLToPath(new URL("./src", __vite_injected_original_import_meta_url))
        },
        {
          find: "lib",
          replacement: resolve(__vite_injected_original_dirname, "lib")
        }
      ]
    },
    define: {
      "process.env.REACT_APP_GEMINI_API_KEY": JSON.stringify(env.REACT_APP_GEMINI_API_KEY),
      "process.env.REACT_APP_GOOGLE_CLIENT_ID": JSON.stringify(env.REACT_APP_GOOGLE_CLIENT_ID),
      "process.env.REACT_APP_GOOGLE_API_KEY": JSON.stringify(env.REACT_APP_GOOGLE_API_KEY),
      "process.env.REACT_APP_GOOGLE_CALENDAR_ID": JSON.stringify(env.REACT_APP_GOOGLE_CALENDAR_ID)
    },
    build: {
      chunkSizeWarningLimit: 1e3
      // Adjust this value as needed
    }
  };
});
export {
  vite_config_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcuanMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCIvd29ya3NwYWNlcy9iYXNrZXRiYWxsLXN0cmVhbXMtdG8tY2FsZW5kYXItYWktcHJvbXB0XCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ZpbGVuYW1lID0gXCIvd29ya3NwYWNlcy9iYXNrZXRiYWxsLXN0cmVhbXMtdG8tY2FsZW5kYXItYWktcHJvbXB0L3ZpdGUuY29uZmlnLmpzXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ltcG9ydF9tZXRhX3VybCA9IFwiZmlsZTovLy93b3Jrc3BhY2VzL2Jhc2tldGJhbGwtc3RyZWFtcy10by1jYWxlbmRhci1haS1wcm9tcHQvdml0ZS5jb25maWcuanNcIjtpbXBvcnQgeyBmaWxlVVJMVG9QYXRoLCBVUkwgfSBmcm9tIFwidXJsXCI7XG5pbXBvcnQgeyBkZWZpbmVDb25maWcsIGxvYWRFbnYgIH0gZnJvbSBcInZpdGVcIjtcbmltcG9ydCByZWFjdCBmcm9tIFwiQHZpdGVqcy9wbHVnaW4tcmVhY3RcIjtcbmltcG9ydCB7IHJlc29sdmUgfSBmcm9tIFwicGF0aFwiO1xuXG4vLyBodHRwczovL3ZpdGVqcy5kZXYvY29uZmlnL1xuZXhwb3J0IGRlZmF1bHQgZGVmaW5lQ29uZmlnKCh7IG1vZGUgfSkgPT4ge1xuICBjb25zdCBlbnYgPSBsb2FkRW52KG1vZGUsIHByb2Nlc3MuY3dkKCksICcnKTtcbiAgcmV0dXJuIHtcbiAgICBzZXJ2ZXI6IHtcbiAgICAgIGhvc3Q6IFwiOjpcIixcbiAgICAgIHBvcnQ6IFwiODA4MFwiLFxuICAgIH0sXG4gICAgcGx1Z2luczogW3JlYWN0KCldLFxuICAgIHJlc29sdmU6IHtcbiAgICAgIGFsaWFzOiBbXG4gICAgICAgIHtcbiAgICAgICAgICBmaW5kOiBcIkBcIixcbiAgICAgICAgICByZXBsYWNlbWVudDogZmlsZVVSTFRvUGF0aChuZXcgVVJMKFwiLi9zcmNcIiwgaW1wb3J0Lm1ldGEudXJsKSksXG4gICAgICAgIH0sXG4gICAgICAgIHtcbiAgICAgICAgICBmaW5kOiBcImxpYlwiLFxuICAgICAgICAgIHJlcGxhY2VtZW50OiByZXNvbHZlKF9fZGlybmFtZSwgXCJsaWJcIiksXG4gICAgICAgIH0sXG4gICAgICBdLFxuICAgIH0sXG4gICAgZGVmaW5lOiB7XG4gICAgICAncHJvY2Vzcy5lbnYuUkVBQ1RfQVBQX0dFTUlOSV9BUElfS0VZJzogSlNPTi5zdHJpbmdpZnkoZW52LlJFQUNUX0FQUF9HRU1JTklfQVBJX0tFWSksXG4gICAgICAncHJvY2Vzcy5lbnYuUkVBQ1RfQVBQX0dPT0dMRV9DTElFTlRfSUQnOiBKU09OLnN0cmluZ2lmeShlbnYuUkVBQ1RfQVBQX0dPT0dMRV9DTElFTlRfSUQpLFxuICAgICAgJ3Byb2Nlc3MuZW52LlJFQUNUX0FQUF9HT09HTEVfQVBJX0tFWSc6IEpTT04uc3RyaW5naWZ5KGVudi5SRUFDVF9BUFBfR09PR0xFX0FQSV9LRVkpLFxuICAgICAgJ3Byb2Nlc3MuZW52LlJFQUNUX0FQUF9HT09HTEVfQ0FMRU5EQVJfSUQnOiBKU09OLnN0cmluZ2lmeShlbnYuUkVBQ1RfQVBQX0dPT0dMRV9DQUxFTkRBUl9JRCksXG4gICAgfSxcbiAgICBidWlsZDoge1xuICAgICAgY2h1bmtTaXplV2FybmluZ0xpbWl0OiAxMDAwLCAvLyBBZGp1c3QgdGhpcyB2YWx1ZSBhcyBuZWVkZWRcbiAgICB9LFxuICB9O1xufSk7Il0sCiAgIm1hcHBpbmdzIjogIjtBQUE4VSxTQUFTLGVBQWUsV0FBVztBQUNqWCxTQUFTLGNBQWMsZUFBZ0I7QUFDdkMsT0FBTyxXQUFXO0FBQ2xCLFNBQVMsZUFBZTtBQUh4QixJQUFNLG1DQUFtQztBQUF1SyxJQUFNLDJDQUEyQztBQU1qUSxJQUFPLHNCQUFRLGFBQWEsQ0FBQyxFQUFFLEtBQUssTUFBTTtBQUN4QyxRQUFNLE1BQU0sUUFBUSxNQUFNLFFBQVEsSUFBSSxHQUFHLEVBQUU7QUFDM0MsU0FBTztBQUFBLElBQ0wsUUFBUTtBQUFBLE1BQ04sTUFBTTtBQUFBLE1BQ04sTUFBTTtBQUFBLElBQ1I7QUFBQSxJQUNBLFNBQVMsQ0FBQyxNQUFNLENBQUM7QUFBQSxJQUNqQixTQUFTO0FBQUEsTUFDUCxPQUFPO0FBQUEsUUFDTDtBQUFBLFVBQ0UsTUFBTTtBQUFBLFVBQ04sYUFBYSxjQUFjLElBQUksSUFBSSxTQUFTLHdDQUFlLENBQUM7QUFBQSxRQUM5RDtBQUFBLFFBQ0E7QUFBQSxVQUNFLE1BQU07QUFBQSxVQUNOLGFBQWEsUUFBUSxrQ0FBVyxLQUFLO0FBQUEsUUFDdkM7QUFBQSxNQUNGO0FBQUEsSUFDRjtBQUFBLElBQ0EsUUFBUTtBQUFBLE1BQ04sd0NBQXdDLEtBQUssVUFBVSxJQUFJLHdCQUF3QjtBQUFBLE1BQ25GLDBDQUEwQyxLQUFLLFVBQVUsSUFBSSwwQkFBMEI7QUFBQSxNQUN2Rix3Q0FBd0MsS0FBSyxVQUFVLElBQUksd0JBQXdCO0FBQUEsTUFDbkYsNENBQTRDLEtBQUssVUFBVSxJQUFJLDRCQUE0QjtBQUFBLElBQzdGO0FBQUEsSUFDQSxPQUFPO0FBQUEsTUFDTCx1QkFBdUI7QUFBQTtBQUFBLElBQ3pCO0FBQUEsRUFDRjtBQUNGLENBQUM7IiwKICAibmFtZXMiOiBbXQp9Cg==
