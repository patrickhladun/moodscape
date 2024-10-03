const { defineConfig } = require("cypress");
require("dotenv").config();

module.exports = defineConfig({
  e2e: {
    baseUrl: "http://127.0.0.1:8000",
    specPattern: "__tests__/cypress/e2e/**/*.{js,jsx,ts,tsx}",
    supportFile: "__tests__/cypress/support/commands.js",
    screenshotsFolder: "__tests__/cypress/screenshots",
    downloadsFolder: "__tests__/cypress/downloads",
    videosFolder: "__tests__/cypress/videos",
  },
  env: {
    cms_username: process.env.CY_CMS_EMAIL,
    cms_password: process.env.CY_CMS_PASS,
    account_username: process.env.CY_ACCOUNT_EMAIL,
    account_password: process.env.CY_ACCOUNT_PASS,
  },
  // video: true,
  // videoCompression: true,
});
