describe("Header Accessibility Tests", () => {
  it("All footer <a> tags must have an aria-label attribute", () => {
    cy.visit("/");

    cy.get("body > footer a").each(($el) => {
      expect($el).to.have.attr("aria-label");
    });
  });
});
