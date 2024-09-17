import "cypress-axe";

describe("Privacy Policy Accessibility Test", () => {
  beforeEach(() => {
    cy.visit("/faq/");
  });

  it("has no a11y violations", () => {
    cy.injectAxe();
    cy.checkA11y();
  });
});
