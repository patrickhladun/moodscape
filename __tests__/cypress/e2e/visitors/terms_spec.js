import "cypress-axe";

describe("Terms and Conditions Page UI and Accessibility Tests", () => {
  beforeEach(() => {
    cy.visit("/terms-and-conditions/");
  });

  it("has no a11y violations", () => {
    cy.injectAxe();
    cy.checkA11y();
  });

  it("should have the correct headers", () => {
    cy.get("h1").contains("Terms and Conditions").should("exist");
    cy.get("h2").contains("Introduction").should("exist");
    cy.get("h2").contains("Acceptance of Terms").should("exist");
    cy.get("h2").contains("Account Terms").should("exist");
    cy.get("h2").contains("Products and Services").should("exist");
    cy.get("h2").contains("Order and Payment").should("exist");
    cy.get("h2").contains("Returns and Refunds").should("exist");
    cy.get("h2").contains("Shipping").should("exist");
    cy.get("h2").contains("Intellectual Property").should("exist");
    cy.get("h2").contains("Limitation of Liability").should("exist");
    cy.get("h2").contains("Governing Law").should("exist");
    cy.get("h2").contains("Changes to These Terms").should("exist");
    cy.get("h2").contains("Contact Us").should("exist");
  });
});
