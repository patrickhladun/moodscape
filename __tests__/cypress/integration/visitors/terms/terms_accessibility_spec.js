import "cypress-axe";

describe("Privacy Policy Accessibility Test", () => {
  beforeEach(() => {
    cy.visit("/terms-and-conditions/");
  });

  it("has no a11y violations", () => {
    cy.injectAxe();
    cy.checkA11y();
  });
});
