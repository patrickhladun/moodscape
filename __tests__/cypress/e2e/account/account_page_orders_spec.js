describe("Test Account Orders page functionality.", () => {
  const username = Cypress.env("account_username");
  const password = Cypress.env("account_password");

  beforeEach(() => {
    cy.clearLocalStorage("bluelibs-token");
    cy.clearLocalStorage();
    cy.clearCookies();
    cy.session("login", () => {
      cy.visit("/account/login/");
      cy.get('input[name="login"]').type(username);
      cy.get('input[name="password"]').type(password);
      cy.get('form[action="/account/login/"]').submit();
      cy.get("h1").should("contain", "Where Art Meets Soul");
      cy.get("#desktopMenu").should("contain", "Sign Out");
    });
  });

  it("should navigate to orders page", () => {
    cy.visit("/account/orders/");
    cy.get("ul[role=list]").within(() => {
      cy.get("li[role='listitem']:first-child ").click();
    });
  });
});
