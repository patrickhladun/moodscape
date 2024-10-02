import "cypress-axe";

describe("Contact Page UI and Accessibility Tests", () => {
  beforeEach(() => {
    cy.visit("/contact/");
  });

  it("has no a11y violations", () => {
    cy.injectAxe();
    cy.checkA11y();
  });

  it.skip("should submit the contact form", () => {
    cy.get("#contact-form").within(() => {
      cy.get('input[name="name"]').type("Patrick");
      cy.get('input[name="email"]').type("patrickhladun@gmail.com");
      cy.get('textarea[name="message"]').type(
        "Hello, this is a test message sent via Cypress."
      );
      cy.get('button[type="submit"]').click();
    });

    cy.url().should("include", "/contact/success/");
    cy.get("h1").should("contain", "Thank you for your message!");
  });

  it("should throw an error on missing name field", () => {
    cy.get("#contact-form").within(() => {
      cy.get('input[name="name"]').should("be.empty");
      cy.get('input[name="email"]').type("patrickhladun@gmail.com");
      cy.get('textarea[name="message"]').type("Hello, this is a test message.");
      cy.get('button[type="submit"]').click();
    });

    cy.get('input[name="name"]').then(($input) => {
      expect($input[0].validationMessage).to.eq("Please fill out this field.");
    });
  });

  it("should throw an error on missing email field", () => {
    cy.get("#contact-form").within(() => {
      cy.get('input[name="name"]').type("Patrick");
      cy.get('input[name="email"]').should("be.empty");
      cy.get('textarea[name="message"]').type("Hello, this is a test message.");
      cy.get('button[type="submit"]').click();
    });

    cy.get('input[name="email"]').then(($input) => {
      expect($input[0].validationMessage).to.eq("Please fill out this field.");
    });
  });

  it("should throw an error on missing message field", () => {
    cy.get("#contact-form").within(() => {
      cy.get('input[name="name"]').type("Patrick");
      cy.get('input[name="email"]').type("patrickhladun@gmail.com");
      cy.get('textarea[name="message"]').should("be.empty");
      cy.get('button[type="submit"]').click();
    });

    cy.get('textarea[name="message"]').then(($input) => {
      expect($input[0].validationMessage).to.eq("Please fill out this field.");
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
