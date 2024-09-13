describe("FAQ Page", () => {
  before(() => {
    cy.visit("/faq/");
  });

  it("should have the correct headers", () => {
    cy.get("h1").contains("Frequently Asked Questions (FAQ)").should("exist");
    cy.get("h2").contains("General Questions").should("exist");
    cy.get("h2").contains("Orders and Shipping").should("exist");
    cy.get("h2").contains("Returns and Refunds").should("exist");
    cy.get("h2").contains("Product Information").should("exist");
    cy.get("h3").contains("1. What is Moonscape?").should("exist");
    cy.get("h3").contains("2. How can I contact customer support?").should("exist");
    cy.get("h3").contains("3. What payment methods do you accept?").should("exist");
    cy.get("h3").contains("4. How can I track my order?").should("exist");
    cy.get("h3").contains("5. What are the shipping options?").should("exist");
    cy.get("h3").contains("6. Do you ship internationally?").should("exist");
    cy.get("h3").contains("7. How long does it take to process an order?").should("exist");
    cy.get("h3").contains("8. Can I change or cancel my order?").should("exist");
    cy.get("h3").contains("9. What is your return policy?").should("exist");
    cy.get("h3").contains("10. How do I return an item?").should("exist");
    cy.get("h3").contains("11. How long does it take to receive a refund?").should("exist");
    cy.get("h3").contains("12. Can I exchange an item?").should("exist");
    cy.get("h3").contains("13. Are all the art pieces original?").should("exist");
    cy.get("h3").contains("14. Do you offer custom art pieces?").should("exist");
    cy.get("h3").contains("15. How do I care for my artwork?").should("exist");
  });
});
