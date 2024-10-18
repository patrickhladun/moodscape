describe("Test Account user login and pages navigation.", () => {
  const username = Cypress.env("account_username");
  const password = Cypress.env("account_password");

  function checkPageLinks(expectedUrl, pageName) {
    cy.get(
      `a.account-nav-item[href="${expectedUrl}"][aria-label="Link to ${pageName}"]`
    )
      .should("contain", pageName)
      .click();
    cy.url().should("eq", Cypress.config().baseUrl + expectedUrl);
  }

  function toggleMenu() {
    cy.get("#desktopMenu").should("have.class", "hidden");
    cy.get("#desktopMenuButton").click();
    cy.get("#desktopMenu").should("not.have.class", "hidden");
  }

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

  it("should be able to navigate using pages links", () => {
    cy.visit("/account/orders/");
    checkPageLinks("/account/reviews/", "Reviews");
    checkPageLinks("/account/profile/", "Profile");
    checkPageLinks("/account/", "Account");
    checkPageLinks("/account/orders/", "Orders");
  });

  it("should be able to navigate using menu links", () => {
    checkNavLinks("/account/orders/", "Orders");
    checkNavLinks("/account/reviews/", "Reviews");
    checkNavLinks("/account/profile/", "Profile");
    checkNavLinks("/account/", "Account");
  });
});
