describe("Bag Page UI and Accessibility Tests", () => {
  beforeEach(() => {
    cy.visit("/");
  });

  it("should navigate to bag page", () => {
    cy.get("[data-testid=bag-icon]").click();
    cy.url().should("include", "/bag/");
  });
});
