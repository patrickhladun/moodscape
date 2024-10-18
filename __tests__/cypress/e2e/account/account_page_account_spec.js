describe("Test Account page functionality.", () => {
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

  it("should navigate to order page", () => {
    cy.visit("/account/");
    cy.url().should("eq", Cypress.config().baseUrl + "/account/");
  });

  it("should update first name", () => {
    cy.visit("/account/");

    cy.get('input[name="email"]')
      .invoke("val")
      .then((email) => {
        cy.get('input[name="email"]').clear().type("newemail@example.com");
        cy.get('form[data-cy="account_form"]').submit();
        cy.get('input[name="email"]')
          .invoke("val")
          .should("eq", "newemail@example.com");

        cy.get('input[name="email"]').clear().type(email);
        cy.get('form[data-cy="account_form"]').submit();
        cy.get('input[name="email"]').invoke("val").should("eq", email);
      });
  });

  it("should update first name", () => {
    cy.visit("/account/");

    cy.get('input[name="username"]')
      .invoke("val")
      .then((username) => {
        cy.get('input[name="username"]').clear().type("New Username");
        cy.get('form[data-cy="account_form"]').submit();
        cy.get('input[name="username"]')
          .invoke("val")
          .should("eq", "New Username");

        cy.get('input[name="username"]').clear().type(username);
        cy.get('form[data-cy="account_form"]').submit();
        cy.get('input[name="username"]').invoke("val").should("eq", username);
      });
  });
});
