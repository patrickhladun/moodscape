const { defineConfig } = require("cypress");

module.exports = defineConfig({
  e2e: {
    baseUrl: "http://127.0.0.1:8000",
    specPattern: "__tests__/cypress/integration/**/*.{js,jsx,ts,tsx}",
    supportFile: "__tests__/cypress/support/commands.js",
    screenshotsFolder: "__tests__/cypress/screenshots",
    downloadsFolder: "__tests__/cypress/downloads",
  },
});
