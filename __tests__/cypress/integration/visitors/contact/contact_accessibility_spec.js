import "cypress-axe";

describe("Home Accessibility Test", () => {
  beforeEach(() => {
    cy.visit("/contact/");
  });

  it("has no a11y violations", () => {
    cy.injectAxe();
    cy.checkA11y();
  });
});
