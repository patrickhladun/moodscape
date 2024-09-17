describe("Privacy Page", () => {
  before(() => {
    cy.visit("/privacy-policy/");
  });

  it("should have the correct headers", () => {
    cy.get("h1").contains("Privacy Policy").should("exist");
    cy.get("h2").contains("Introduction").should("exist");
    cy.get("h2").contains("Information We Collect").should("exist");
    cy.get("h2").contains("How We Use Your Information").should("exist");
    cy.get("h2").contains("Sharing Your Information").should("exist");
    cy.get("h2").contains("Data Security").should("exist");
    cy.get("h2").contains("Retention of Data").should("exist");
    cy.get("h2").contains("Your Rights").should("exist");
    cy.get("h2").contains("Changes to This Privacy Policy").should("exist");
    cy.get("h2").contains("Contact Us").should("exist");
  });
});
