describe("Accessibility Tests", () => {
  it("All header <a> tags must have an aria-label attribute", () => {
    cy.visit("http://127.0.0.1:8000/");

    cy.get("body > header a").each(($el) => {
      expect($el).to.have.attr("aria-label");
    });
  });

  it("All footer <a> tags must have an aria-label attribute", () => {
    cy.visit("http://127.0.0.1:8000/");

    cy.get("body > footer a").each(($el) => {
      expect($el).to.have.attr("aria-label");
    });
  });
});
