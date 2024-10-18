import { breakpoints } from "../support/devices";

describe("Header Links Tests", () => {
  beforeEach(() => {
    cy.visit("/");
  });

  it("bag icon should link to bag page", () => {
    cy.get("[data-cy=bag-link]").click();
    cy.url().should("eq", Cypress.config().baseUrl + "/bag/");
  });

  it("logo should link to home page", () => {
    cy.visit("/about/");
    cy.get("[data-cy=logo]").click();
    cy.url().should("eq", Cypress.config().baseUrl + "/");
  });

  it("all mobile main links should navigate correctly to each page", () => {
    const hrefs = [];
    cy.get("[data-cy=main-manu-links-mobile] a")
      .each(($el, index, $list) => {
        hrefs.push($el.prop("href"));
      })
      .then(() => {
        hrefs.forEach((href) => {
          cy.visit(href);
          cy.url().should("eq", href);
        });
      });
  });

  it("all desktop main links should navigate correctly to each page", () => {
    const hrefs = [];
    cy.get("[data-cy=main-manu-links-desktop] a")
      .each(($el, index, $list) => {
        hrefs.push($el.prop("href"));
      })
      .then(() => {
        hrefs.forEach((href) => {
          cy.visit(href);
          cy.url().should("eq", href);
        });
      });
  });
});

describe("Header Responsive Tests", () => {
  beforeEach(() => {
    cy.visit("/");
  });

  it("sign in button should be visible on desktop", () => {
    cy.viewport(breakpoints.md.min, 600);
    cy.visit("/");
    cy.wait(200);
    cy.get("[data-cy=button-sign-in]").should("be.visible");
  });

  it("sign in button should not be visible on mobile", () => {
    cy.viewport(breakpoints.md.min, 600);
    cy.visit("/");
    cy.wait(200);
    cy.get("[data-cy=button-sign-in]").should("be.visible");
  });

  it("main menu links should be visible on desktop", () => {
    cy.viewport(breakpoints.md.min, 600);
    cy.visit("/");
    cy.wait(200);
    cy.get("[data-cy=main-manu-links-desktop]").should("be.visible");
  });

  it("main menu links should not be visible on mobile", () => {
    cy.viewport(breakpoints.sm.max, 600);
    cy.visit("/");
    cy.wait(200);
    cy.get("[data-cy=navigation-mobile]").should("not.exist");
  });

  it("menu toggle button should be visible on mobile", () => {
    cy.viewport(breakpoints.sm.max, 600);
    cy.visit("/");
    cy.wait(200);
    cy.get("[data-cy=menu-toggle]").should("be.visible");
  });

  it("menu toggle button should not be visible on desktop", () => {
    cy.viewport(breakpoints.md.min, 600);
    cy.visit("/");
    cy.wait(200);
    cy.get("[data-cy=menu-toggle]").should("not.be.visible");
  });
});
