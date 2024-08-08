describe("Buttons and Links", () => {

  beforeEach(() => {
    cy.visit("/contact/");
  });

  it("should open the Twitter profile", () => {
    cy.get('a[aria-label="Link to Facebook Profile"]')
      .should("have.attr", "href", "https://www.facebook.com/")
      .and("have.attr", "target", "_blank");
  });

  it("should open the Twitter profile", () => {
    cy.get('a[aria-label="Link to Instagram Profile"]')
      .should("have.attr", "href", "https://www.instagram.com/")
      .and("have.attr", "target", "_blank");
  });

  it("should open the Twitter profile", () => {
    cy.get('a[aria-label="Link to Twitter Profile"]')
      .should("have.attr", "href", "https://www.twitter.com/")
      .and("have.attr", "target", "_blank");
  });

  it("should open the LinkedIn profile", () => {
    cy.get('a[aria-label="Link to LinkedIn Profile"]')
      .should("have.attr", "href", "https://www.linkedin.com/")
      .and("have.attr", "target", "_blank");
  });
});
