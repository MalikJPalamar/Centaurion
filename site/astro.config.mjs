import { defineConfig } from "astro/config";
import tailwind from "@astrojs/tailwind";
import react from "@astrojs/react";

export default defineConfig({
  site: "https://centaurion.me",
  output: "static",
  integrations: [
    tailwind({ applyBaseStyles: false }),
    react(),
  ],
  build: {
    inlineStylesheets: "auto",
  },
  prefetch: {
    prefetchAll: false,
    defaultStrategy: "viewport",
  },
  compressHTML: true,
  scopedStyleStrategy: "where",
});
