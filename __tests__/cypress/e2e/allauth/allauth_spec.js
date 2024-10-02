import "cypress-axe";

describe("Check allauth login page", () => {
  beforeEach(() => {
    cy.visit("/account/login/");
  });

  it("should have a login form", () => {
    cy.get("form").should("have.length", 2);
  });

  it("should have a username input", () => {
    cy.get("input[name='login']").should("have.length", 1);
  });

  it("should have a password input", () => {
    cy.get("input[name='password']").should("have.length", 1);
  });

  it("should have a submit button", () => {
    cy.get("button[type='submit']").should("exist");
  });
});
