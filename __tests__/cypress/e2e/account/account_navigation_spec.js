/**
 * Test suite for verifying user login and navigation through various account pages,
 * including direct page links and navigation via menu links.
 */
describe("Test Account user login and pages navigation.", () => {
  const username = Cypress.env("account_username");
  const password = Cypress.env("account_password");

  /**
   * Function to verify navigation to a specific URL via direct page links.
   * Ensures the link contains the correct page name, clicks on it, and verifies the resulting URL.
   */
  function checkPageLinks(expectedUrl, pageName) {
    cy.get(
      `a.account-nav-item[href="${expectedUrl}"][aria-label="Link to ${pageName}"]`
    )
      .should("contain", pageName)
      .click();
    cy.url().should("eq", Cypress.config().baseUrl + expectedUrl);
  }

  /**
   * Function to toggle the visibility of the navigation menu.
   * Ensures the menu is initially hidden, triggers its visibility, and checks if it is visible post-click.
   */
  function toggleMenu() {
    cy.get("#desktopMenu").should("have.class", "hidden");
    cy.get("#desktopMenuButton").click();
    cy.get("#desktopMenu").should("not.have.class", "hidden");
  }

  /**
   * Function to verify navigation through menu links.
   * Uses the toggleMenu function to ensure the menu is accessible, then navigates and checks URLs via menu links.
   */
  function checkNavLinks(expectedUrl, pageName) {
    cy.visit("/");
    toggleMenu();
    cy.get(
      `#desktopMenu a[href="${expectedUrl}"][aria-label="Link to ${pageName}"]`
    )
      .should("contain", pageName)
      .click();
    cy.url().should("eq", Cypress.config().baseUrl + expectedUrl);
  }

  /**
   * Before each test, clears browser storage and cookies, logs in with a session, and confirms successful login.
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
   * Test to verify navigation using direct page links.
   */
  it("should be able to navigate using pages links", () => {
    cy.visit("/account/orders/");
    checkPageLinks("/account/reviews/", "Reviews");
    checkPageLinks("/account/profile/", "Profile");
    checkPageLinks("/account/", "Account");
    checkPageLinks("/account/orders/", "Orders");
  });

  /**
   * Test to verify navigation using menu links after toggling the menu.
   */
  it("should be able to navigate using menu links", () => {
    checkNavLinks("/account/orders/", "Orders");
    checkNavLinks("/account/reviews/", "Reviews");
    checkNavLinks("/account/profile/", "Profile");
    checkNavLinks("/account/", "Account");
  });
});
