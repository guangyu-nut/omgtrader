import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "../e2e/tests",
  use: {
    baseURL: "http://127.0.0.1:5173",
    headless: true,
  },
});
