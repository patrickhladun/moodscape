describe("Bag Page UI and Accessibility Tests", () => {
  beforeEach(() => {
    cy.visit("/");
  });

  it("should navigate to bag page", () => {
    cy.get("[data-cy=bag-link]").click();
    cy.url().should("include", "/bag/");
  });

  it("bag icon should show correct items count", () => {
    cy.visit("/shop/");
    cy.get("[data-cy=product-irish-watercolor-seascape-abstract]").click();
    cy.get("[data-cy=product-large-red-flower]").click();
    cy.get('[data-cy="bag-link-count"]').should("have.text", "2");
  });

  it("success message should popup when item is added", () => {
    cy.visit("/shop/");
    cy.get("[data-cy=product-irish-watercolor-seascape-abstract]").click();
    cy.get("#toast-success").should("exist");
  });

  it("two items should be displayed on bag page", () => {
    cy.visit("/shop/");
    cy.get("[data-cy=product-irish-watercolor-seascape-abstract]").click();
    cy.get("[data-cy=product-large-red-flower]").click();

    cy.visit("/bag/");
    cy.get("[data-cy=bag-items-list]").children().should("have.length", 3);
    cy.get('[data-cy="price-total"]').should("have.text", "Total: €256.00");
  });

  it("correct total should be displayed Total: €256.00", () => {
    cy.visit("/shop/");
    cy.get("[data-cy=product-irish-watercolor-seascape-abstract]").click();
    cy.get("[data-cy=product-large-red-flower]").click();

    cy.visit("/bag/");
    cy.get('[data-cy="price-total"]').should("have.text", "Total: €256.00");
  });
});
