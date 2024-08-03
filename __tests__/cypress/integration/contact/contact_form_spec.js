describe("Forms and Input Fields", () => {
  it.skip("should submit the contact form", () => {
    cy.visit("http://127.0.0.1:8000/contact/");

    cy.get("#contact-form").within(() => {
      cy.get('input[name="name"]').type("Patrick");
      cy.get('input[name="email"]').type("patrickhladun@gmail.com");
      cy.get('textarea[name="message"]').type("Hello, this is a test message sent via Cypress.");
      cy.get('button[type="submit"]').click();
    });

    cy.url().should("include", "contact/success/");
    cy.get("h1").should("contain", "Thank you for your message!");
  });

  it("should throw an error on missing name field", () => {
    cy.visit("http://127.0.0.1:8000/contact/");

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
    cy.visit("http://127.0.0.1:8000/contact/");

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
    cy.visit("http://127.0.0.1:8000/contact/");

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
});
