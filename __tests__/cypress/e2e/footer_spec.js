import { largeDevices, breakpoints } from "../support/devices";

describe("Website Footer Tests", () => {
  beforeEach(() => {
    cy.visit("/");
  });

  it("all secondary links should navigate correctly to each page", () => {
    const hrefs = [];
    cy.get("[data-cy=secondary-links] li a")
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

  it("should open the Facebook profile", () => {
    cy.get('a[aria-label="Link to Facebook Profile"]')
      .should(
        "have.attr",
        "href",
        "https://www.facebook.com/people/Moodscape/61566307404663/"
      )
      .and("have.attr", "target", "_blank");
  });

  it("should open the Instagram profile", () => {
    cy.get('a[aria-label="Link to Instagram Profile"]')
      .should("have.attr", "href", "https://www.instagram.com/")
      .and("have.attr", "target", "_blank");
  });

  it("should open the Twitter profile", () => {
    cy.get('a[aria-label="Link to Twitter Profile"]')
      .should("have.attr", "href", "https://www.twitter.com/")
      .and("have.attr", "target", "_blank");
  });

  it("should open the LinkedIn profile", () => {
    cy.get('a[aria-label="Link to LinkedIn Profile"]')
      .should("have.attr", "href", "https://www.linkedin.com/")
      .and("have.attr", "target", "_blank");
  });
});
