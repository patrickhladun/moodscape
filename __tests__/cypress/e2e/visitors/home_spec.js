import "cypress-axe";
import devices from "../../support/devices";

describe("Home Page UI and Accessibility Tests", () => {
  beforeEach(() => {
    cy.visit("/");
  });

  it("should have no detectable accessibility violations on load", () => {
    cy.injectAxe();
    cy.checkA11y();
  });

  it("should ensure all image elements have descriptive 'alt' attributes", () => {
    cy.get("img").each(($img) => {
      cy.wrap($img).should("have.attr", "alt").and("not.be.empty");
    });
  });

  it("should redirect to the shop page when the browse button is clicked", () => {
    cy.get("[data-cy=button-browse]").click();
    cy.url().should("include", "/shop");
  });

  const categories = ["watercolor", "photography", "plotter"];
  categories.forEach((category) => {
    it(`should redirect to the relevant ${category} category page when its link is clicked`, () => {
      cy.get(`[data-cy=button-${category}]`).click();
      cy.url().should("include", `/shop/?category=${category}`);
    });
  });

  it("should navigate correctly to each featured product's detail page", () => {
    const hrefs = [];
    cy.get('div[data-cy="featured-products"] a')
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

  devices.forEach((device) => {
    it(`should be visible on ${device.name} screensize`, () => {
      cy.viewport(device.width, device.height);
      cy.visit("/");
      cy.wait(200);
      cy.get("[data-cy=button-browse]").isWithinViewport();
    });
  });
});
