describe("Accessibility Tests", () => {
  it("All <a> tags must have an aria-label attribute", () => {
    cy.visit("http://127.0.0.1:8000/");

    cy.get("a").each(($el) => {
      expect($el).to.have.attr("aria-label");
    });
  });
});
