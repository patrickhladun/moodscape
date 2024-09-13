/**
 * This test suite validates the presence and correctness of the title sections
 * across various account-related pages after a user logs in.
 */
describe("Check title section for account pages.", () => {
  const username = Cypress.env("account_username");
  const password = Cypress.env("account_password");

  /**
   * Checks if the page title section contains the correct text based on the
   * provided page name.
   */
  function checkPageTitleSection(pageName) {
    cy.get("section.md\\:hidden.bg-neutral-100")
      .should("exist")
      .within(() => {
        cy.get("div.container.py-sm")
          .should("exist")
          .within(() => {
            cy.get("h1.m-0").should("contain", pageName);
          });
      });
  }

  /**
   * Clears all relevant local storage and cookies before each test, then logs
   * in the user, ensuring each test starts from an authenticated state with a
   * clean slate.
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

  // Test cases for each account-related page to verify their respective title sections.
  it("orders page should contain correct page title", () => {
    cy.visit("/account/orders/");
    checkPageTitleSection("Orders");
  });

  it("reviews page should contain correct page title", () => {
    cy.visit("/account/reviews/");
    checkPageTitleSection("Reviews");
  });

  it("profile page should contain correct page title", () => {
    cy.visit("/account/profile/");
    checkPageTitleSection("Profile");
  });

  it("account page should contain correct page title", () => {
    cy.visit("/account/");
    checkPageTitleSection("Account");
  });
});
