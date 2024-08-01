import 'cypress-axe'

Cypress.Commands.add('checkA11y', (context, options) => {
  cy.injectAxe()
  cy.checkA11y(context, options)
})
