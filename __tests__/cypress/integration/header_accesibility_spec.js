describe("Header Accessibility Tests", () => {
  it("All header <a> tags must have an aria-label attribute", () => {
    cy.visit("/");

    cy.get("body > header a").each(($el) => {
      expect($el).to.have.attr("aria-label");
    });
  });
});
