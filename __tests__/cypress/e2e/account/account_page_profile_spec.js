describe("Test Account profile page functionality.", () => {
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

  it("should navigate to order page", () => {
    cy.visit("/account/profile/");
    cy.url().should("eq", Cypress.config().baseUrl + "/account/profile/");
  });

  it("should update first name", () => {
    cy.visit("/account/profile/");

    cy.get('input[name="first_name"]')
      .invoke("val")
      .then((first_name) => {
        cy.get('input[name="first_name"]').clear().type("New First Name");
        cy.get('form[data-cy="profile_form"]').submit();
        cy.get('input[name="first_name"]')
          .invoke("val")
          .should("eq", "New First Name");

        cy.get('input[name="first_name"]').clear().type(first_name);
        cy.get('form[data-cy="profile_form"]').submit();
        cy.get('input[name="first_name"]')
          .invoke("val")
          .should("eq", first_name);
      });
  });

  it("should update last name", () => {
    cy.visit("/account/profile/");

    cy.get('input[name="last_name"]')
      .invoke("val")
      .then((last_name) => {
        cy.get('input[name="last_name"]').clear().type("New Last Name");
        cy.get('form[data-cy="profile_form"]').submit();
        cy.get('input[name="last_name"]')
          .invoke("val")
          .should("eq", "New Last Name");

        cy.get('input[name="last_name"]').clear().type(last_name);
        cy.get('form[data-cy="profile_form"]').submit();
        cy.get('input[name="last_name"]').invoke("val").should("eq", last_name);
      });
  });

  it("should update phone number", () => {
    cy.visit("/account/profile/");

    cy.get('input[name="phone_number"]')
      .invoke("val")
      .then((phone_number) => {
        cy.get('input[name="phone_number"]').clear().type("1234567890");
        cy.get('form[data-cy="profile_form"]').submit();
        cy.get('input[name="phone_number"]')
          .invoke("val")
          .should("eq", "1234567890");

        cy.get('input[name="phone_number"]').clear().type(phone_number);
        cy.get('form[data-cy="profile_form"]').submit();
        cy.get('input[name="phone_number"]')
          .invoke("val")
          .should("eq", phone_number);
      });
  });

  it("should update address_line_1", () => {
    cy.visit("/account/profile/");

    cy.get('input[name="address_line_1"]')
      .invoke("val")
      .then((address_line_1) => {
        cy.get('input[name="address_line_1"]').clear().type("123 Main St");
        cy.get('form[data-cy="profile_form"]').submit();
        cy.get('input[name="address_line_1"]')
          .invoke("val")
          .should("eq", "123 Main St");

        cy.get('input[name="address_line_1"]').clear().type(address_line_1);
        cy.get('form[data-cy="profile_form"]').submit();
        cy.get('input[name="address_line_1"]')
          .invoke("val")
          .should("eq", address_line_1);
      });
  });

  it("should update address_line_2", () => {
    cy.visit("/account/profile/");
    cy.get('input[name="address_line_2"]').clear().type("Apt 1");
    cy.get('form[data-cy="profile_form"]').submit();
    cy.get('input[name="address_line_2"]').invoke("val").should("eq", "Apt 1");
    cy.get('input[name="address_line_2"]').clear();
    cy.get('form[data-cy="profile_form"]').submit();
    cy.get('input[name="address_line_2"]').invoke("val").should("eq", "");
  });

  it("should update town_city", () => {
    cy.visit("/account/profile/");

    cy.get('input[name="town_city"]')
      .invoke("val")
      .then((town_city) => {
        cy.get('input[name="town_city"]').clear().type("New York");
        cy.get('form[data-cy="profile_form"]').submit();
        cy.get('input[name="town_city"]')
          .invoke("val")
          .should("eq", "New York");

        cy.get('input[name="town_city"]').clear().type(town_city);
        cy.get('form[data-cy="profile_form"]').submit();
        cy.get('input[name="town_city"]').invoke("val").should("eq", town_city);
      });
  });

  it("should update postcode", () => {
    cy.visit("/account/profile/");

    cy.get('input[name="postcode"]')
      .invoke("val")
      .then((postcode) => {
        cy.get('input[name="postcode"]').clear().type("12345");
        cy.get('form[data-cy="profile_form"]').submit();
        cy.get('input[name="postcode"]').invoke("val").should("eq", "12345");

        cy.get('input[name="postcode"]').clear().type(postcode);
        cy.get('form[data-cy="profile_form"]').submit();
        cy.get('input[name="postcode"]').invoke("val").should("eq", postcode);
      });
  });

  it("should update country", () => {
    cy.visit("/account/profile/");
    cy.get('select[name="country"]')
      .invoke("val")
      .then((country) => {
        cy.get('select[name="country"]').select("US");
        cy.get('form[data-cy="profile_form"]').submit();
        cy.get('select[name="country"]')
          .find(":selected")
          .contains("United States of America");
        cy.get('select[name="country"]').select("IE");
        cy.get('form[data-cy="profile_form"]').submit();
        cy.get('select[name="country"]').find(":selected").contains("Ireland");
      });
  });
});
