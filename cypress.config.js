const { defineConfig } = require("cypress");

module.exports = defineConfig({
  e2e: {
    specPattern: "__tests__/cypress/integration/**/*.{js,jsx,ts,tsx}",
    supportFile: "__tests__/cypress/support/commands.js",
    screenshotsFolder: "__tests__/cypress/screenshots",
  },
});
