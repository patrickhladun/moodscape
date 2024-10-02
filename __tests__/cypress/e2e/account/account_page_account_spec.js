/**
 * This test suite validates the user's ability to update essential account
 * details on the Account page, following a successful login.
 */
describe("Test Account page.", () => {
  const username = Cypress.env("account_username");
  const password = Cypress.env("account_password");

  /**
   * Performs login before each test case and verifies that the login was
   * successful by checking specific UI elements. Clears all relevant local
   * storage and cookies to ensure a clean state for each test.
   */
  beforeEach(() => {
    cy.clearLocalStorage("bluelibs-token");
    cy.clearLocalStorage();
    cy.clearCookies();
    cy.session("login", () => {
      cy.visit("/account/login/");
      cy.get('input[name="login"]').type(username);
      cy.get('input[name="password"]').type(password);
      cy.get('form[action="/account/login/"]').submit();
      cy.get("h1").should("contain", "Great art in one place");
      cy.get("#desktopMenu").should("contain", "Sign Out");
    });
  });

  /**
   * Verifies that navigation to the account overview page works correctly by
   * checking the URL.
   */
  it("should navigate to order page", () => {
    cy.visit("/account/");
    cy.url().should("eq", Cypress.config().baseUrl + "/account/");
  });

  /**
   * Tests the functionality of updating the user's email. Ensures that changes
   * are submitted and verified,and then resets the email to its original value.
   */
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

  /**
   * Tests updating the username field in a similar manner to the email test,
   * verifying that changes persist and can be reverted back to the original username.
   */
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
