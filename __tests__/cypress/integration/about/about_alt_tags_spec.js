describe("Check all images have alt tags", () => {

  beforeEach(() => {
    cy.visit("/about/");
  });

  it("should ensure all img elements have non-empty alt attributes", () => {
    cy.get("img").each(($img) => {
      cy.wrap($img).should("have.attr", "alt").and("not.be.empty");
    });
  });
});
