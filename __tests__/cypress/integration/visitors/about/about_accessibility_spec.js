import "cypress-axe";

describe("Home Accessibility Test", () => {
  beforeEach(() => {
    cy.visit("/about/");
  });

  it("has no a11y violations", () => {
    cy.injectAxe();
    cy.checkA11y();
  });
});
