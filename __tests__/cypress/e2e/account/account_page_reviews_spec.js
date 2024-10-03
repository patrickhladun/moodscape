/**
 * Test suite for managing account reviews page navigations and content
 * verification under different review filters. Ensures that user login is
 * handled before each test and that each navigation and content verification
 * is correctly executed.
 */
describe("Test Account Reviews page.", () => {
  const username = Cypress.env("account_username");
  const password = Cypress.env("account_password");

  /**
   * Handles user login before each test. Clears any session, local storage,
   * nd cookies to ensure a clean state. Successfully logs in and verifies the
   * login by checking for specific elements.
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
   * Verifies navigation to the reviews page and ensures the URL is correct.
   */
  it("should navigate to reviews page", () => {
    cy.visit("/account/reviews/");
    cy.url().should("eq", Cypress.config().baseUrl + "/account/reviews/");
  });

  /**
   * Checks that products filtered as 'Not Reviewed' are displayed correctly,
   * with three items expected.
   */
  it("should display Not Reviewed products", () => {
    cy.visit("/account/reviews/");
    cy.get('[data-cy="reviews_filter"]').should("be.visible");
    cy.get('[data-cy="reviews_filter"]')
      .find(":selected")
      .contains("Not Reviewed");
    cy.get('[data-cy="reviews_list"]').children().should("have.length", 3);
  });

  /**
   * Ensures that when the 'Approved' filter is applied, if there are no items,
   * a specific message is displayed.
   */
  it("should display Approved products", () => {
    cy.visit("/account/reviews/");
    cy.get('[data-cy="reviews_filter"]')
      .should("be.visible")
      .select("Approved");
    cy.get('[data-cy="reviews_list"]')
      .children()
      .its("length")
      .then((length) => {
        if (length === 0) {
          cy.get('[data-cy="reviews_list"] p').should(
            "contain",
            "No approved reviews found."
          );
        }
      });
  });

  /**
   * Verifies that exactly one product is shown under the 'Pending' filter.
   */
  it("should display one Pending product", () => {
    cy.visit("/account/reviews/");
    cy.get('[data-cy="reviews_filter"]').should("be.visible").select("Pending");
    cy.get('[data-cy="reviews_list"]').children().should("have.length", 1);
  });

  /**
   * Confirms that no products are displayed under the 'Rejected' filter, and
   * checks for a specific message.
   */
  it("should not display Rejected products", () => {
    cy.visit("/account/reviews/");
    cy.get('[data-cy="reviews_filter"]')
      .should("be.visible")
      .select("Rejected");
    cy.get('[data-cy="reviews_list"]')
      .children()
      .its("length")
      .then((length) => {
        if (length === 0) {
          cy.get('[data-cy="reviews_list"] p').should(
            "contain",
            "No rejected reviews found."
          );
        }
      });
  });
});
