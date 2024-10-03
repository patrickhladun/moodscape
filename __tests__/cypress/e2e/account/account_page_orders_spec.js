/**
 * This test suite assesses the functional aspects of the Orders page within
 * the user's account section.
 */
describe("Test Account Orders page.", () => {
  const username = Cypress.env("account_username");
  const password = Cypress.env("account_password");

  /**
   * Before each test, the environment is prepared by clearing stored data and
   * authenticating the user. This ensures a clean state and a consistent
   * starting point for each test.
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
      cy.get("h1").should("contain", "Where Art Meets Soul");
      cy.get("#desktopMenu").should("contain", "Sign Out");
    });
  });

  /**
   * Confirms the user can navigate to the Orders page and perform an action,
   * such as selecting an order. This test simulates user interaction to
   * verify that the page's dynamic elements are functioning correctly.
   */
  it("should navigate to order page", () => {
    cy.visit("/account/orders/");
    cy.get("ul[role=list]").within(() => {
      cy.get("li[role='listitem']:first-child ").click();
    });
  });
});
