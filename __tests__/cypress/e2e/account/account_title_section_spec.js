describe("Check title section for account pages.", () => {
  const username = Cypress.env("account_username");
  const password = Cypress.env("account_password");

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
