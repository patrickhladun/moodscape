import "cypress-axe";

describe("About Page UI and Accessibility Tests", () => {
  beforeEach(() => {
    cy.visit("/about/");
  });

  it("has no a11y violations", () => {
    cy.injectAxe();
    cy.checkA11y();
  });

  it("should ensure all img elements have non-empty alt attributes", () => {
    cy.get("img").each(($img) => {
      cy.wrap($img).should("have.attr", "alt").and("not.be.empty");
    });
  });
});
