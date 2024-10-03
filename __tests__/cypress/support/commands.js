import "cypress-axe";

Cypress.Commands.add("checkA11y", (context, options) => {
  cy.injectAxe();
  cy.checkA11y(context, options);
});

Cypress.Commands.add("isWithinViewport", { prevSubject: true }, (subject) => {
  cy.window().then((win) => {
    const winInnerWidth = win.innerWidth;
    const winInnerHeight = win.innerHeight;
    const bounding = subject[0].getBoundingClientRect();

    expect(bounding.top).to.be.at.least(0, "Top boundary within viewport");
    expect(bounding.left).to.be.at.least(0, "Left boundary within viewport");
    expect(bounding.right).to.be.lessThan(
      winInnerWidth,
      "Right boundary within viewport"
    );
    expect(bounding.bottom).to.be.lessThan(
      winInnerHeight,
      "Bottom boundary within viewport"
    );

    return subject;
  });
});

Cypress.Commands.add(
  'iframeLoaded',
  {prevSubject: 'element'},
  ($iframe) => {
      const contentWindow = $iframe.prop('contentWindow');
      return new Promise(resolve => {
          if (
              contentWindow &&
              contentWindow.document.readyState === 'complete'
          ) {
              resolve(contentWindow)
          } else {
              $iframe.on('load', () => {
                  resolve(contentWindow)
              })
          }
      })
  });


Cypress.Commands.add(
  'getInDocument',
  {prevSubject: 'document'},
  (document, selector) => Cypress.$(selector, document)
);

Cypress.Commands.add(
  'getWithinIframe',
  (targetElement) => cy.get('iframe').iframeLoaded().its('document').getInDocument(targetElement)
);