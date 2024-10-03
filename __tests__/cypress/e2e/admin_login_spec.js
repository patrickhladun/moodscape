describe("Django Login Test with .env Variables", () => {
  const username = Cypress.env("username");
  const password = Cypress.env("password");

  beforeEach(() => {
    cy.session("login", () => {
      cy.visit("/account/login/");
      cy.get('input[name="login"]')
        .should("exist")
        .click()
        .type(Cypress.env("username"));
      cy.get('input[name="password"]')
        .should("exist")
        .click()
        .type(Cypress.env("password"));
      cy.get('form[action="/account/login/"]').submit();
      cy.get("h1").should("contain", "Where Art Meets Soul");
      cy.get("#desktopMenu").should("contain", "Sign Out");
    });
  });

  it("should be allowed to account page", () => {
    cy.visit("/account/");
    cy.get("h1").should("contain", "Account");
  });

  it("should logout", () => {
    cy.visit("/account/logout/");
    cy.get("h1").should("contain", "Sign Out");
    cy.get('form[action="/account/logout/"]').submit();
    cy.get("h1").should("contain", "Where Art Meets Soul");
    cy.get("#desktopMenu").should("contain", "Sign In");
  });
});
