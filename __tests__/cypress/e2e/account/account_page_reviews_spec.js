describe("Test Account Reviews page functionality.", () => {
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

  it("should navigate to reviews page", () => {
    cy.visit("/account/reviews/");
    cy.url().should("eq", Cypress.config().baseUrl + "/account/reviews/");
  });

  it("should display Not Reviewed products", () => {
    cy.visit("/account/reviews/");
    cy.get('[data-cy="reviews_filter"]').should("be.visible");
    cy.get('[data-cy="reviews_filter"]')
      .find(":selected")
      .contains("Not Reviewed");
    cy.get('[data-cy="reviews_list"]').children().should("have.length", 1);
  });

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

  it("should display one Pending product", () => {
    cy.visit("/account/reviews/");
    cy.get('[data-cy="reviews_filter"]').should("be.visible").select("Pending");
    cy.get('[data-cy="reviews_list"]').children().should("have.length", 1);
  });

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
