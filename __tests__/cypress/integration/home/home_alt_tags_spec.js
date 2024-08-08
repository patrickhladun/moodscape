describe('Check all images have alt tags', () => {
  it('should ensure all img elements have non-empty alt attributes', () => {
    cy.visit('/');

    cy.get('img').each(($img) => {
      cy.wrap($img).should('have.attr', 'alt').and('not.be.empty');
    });
  });
});
