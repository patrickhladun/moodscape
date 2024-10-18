describe("Checkout Page UI and Accessibility Tests", () => {
  it("empty checkout poage should should redirect to shop", () => {
    cy.visit("/checkout/");
    cy.url().should("include", "/shop/");
  });

  it("checkout should show correct items count and Order Total", () => {
    cy.visit("/shop/");
    cy.get("[data-cy=product-irish-watercolor-seascape-abstract]").click();
    cy.get("[data-cy=product-large-red-flower]").click();
    cy.get('[data-cy="bag-link"]').click();
    cy.get("[data-cy=button-checkout]").click();
    cy.get("[data-cy=checkout-summary-items-list]").children().should("have.length", 2);
    cy.get("[data-cy=checkout-summary-order-total]").should("have.text","Order Total: €256.00");
  });
});

describe("Test Orders", () => {
    it("visitor should add items to bag and make an order", () => {
      cy.clearLocalStorage("bluelibs-token");
      cy.clearLocalStorage();
      cy.clearCookies();
      cy.visit("/shop/");
      cy.get("[data-cy=product-irish-watercolor-seascape-abstract]").click();
      cy.get("[data-cy=product-large-red-flower]").click();
      cy.get('[data-cy="bag-link"]').click();
      cy.get("[data-cy=button-checkout]").click();
      cy.get("[data-cy=checkout-summary-items-list]").children().should("have.length", 2);
      cy.get("[data-cy=checkout-summary-order-total]").should("have.text", "Order Total: €256.00");
      cy.get('input[name="first_name"]').type("Sean");
      cy.get('input[name="last_name"]').type("O'Connor");
      cy.get('input[name="email"]').type("sean.oconnor@example.ie");
      cy.get('input[name="phone_number"]').type("+353 87 123 4567");
      cy.get('select[name="country"]').select("IE");
      cy.get('input[name="postcode"]').type("T12 XY45");
      cy.get('input[name="town_city"]').type("Cork");
      cy.get('input[name="address_line_1"]').type("123 Main Street");
      cy.get('input[name="county"]').type("Co. Cork");
      cy.getWithinIframe('[name="cardnumber"]').type("4242424242424242");
      cy.getWithinIframe('[name="exp-date"]').type("1232");
      cy.getWithinIframe('[name="cvc"]').type("987");
      cy.getWithinIframe('[name="postal"]').type("12345");
      cy.get('[data-cy="complete-order"]').click();
    });
});
