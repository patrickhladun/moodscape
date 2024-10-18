var stripePublicKey = $("#id_stripe_public_key").text().slice(1, -1);
var clientSecret = $("#id_client_secret").text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();

var style = {
  base: {
    color: "#000",
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: "antialiased",
    fontSize: "16px",
    "::placeholder": {
      color: "#aab7c4",
    },
  },
  invalid: {
    color: "#dc3545",
    iconColor: "#dc3545",
  },
};

var card = elements.create("card", { style: style });
card.mount("#card-element");

card.addEventListener("change", function (event) {
  var errorDiv = document.getElementById("card-errors");
  if (event.error) {
    var html = `<span>${event.error.message}</span>`;
    $(errorDiv).html(html);
  } else {
    errorDiv.textContent = "";
  }
});

var form = document.getElementById("payment-form");

form.addEventListener("submit", function (ev) {
  ev.preventDefault();
  card.update({ disabled: true });
  $("#submit-button").attr("disabled", true);
  $("#payment-form").fadeToggle(100);
  $("#loading-overlay").fadeToggle(100);

  var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
  var postData = {
    csrfmiddlewaretoken: csrfToken,
    client_secret: clientSecret,
  };
  console.log(postData.client_secret);
  var url = "/checkout/cache_checkout_data/";

  $.post(url, postData)
    .done(function () {
      stripe
        .confirmCardPayment(clientSecret, {
          payment_method: {
            card: card,
            billing_details: {
              name:
                $.trim(form.first_name.value) +
                " " +
                $.trim(form.last_name.value),
              phone: $.trim(form.phone_number.value),
              email: $.trim(form.email.value),
              address: {
                line1: $.trim(form.address_line_1.value),
                line2: $.trim(form.address_line_2.value),
                city: $.trim(form.town_city.value),
                postal_code: $.trim(form.postcode.value),
                country: $.trim(form.country.value),
                state: $.trim(form.county.value),
              },
            },
          },
        })
        .then(function (result) {
          if (result.error) {
            var errorDiv = document.getElementById("card-errors");
            var html = `
                  <span>${result.error.message}</span>`;
            $(errorDiv).html(html);
            $("#payment-form").fadeToggle(100);
            $("#loading-overlay").fadeToggle(100);
            card.update({ disabled: false });
            $("#submit-button").attr("disabled", false);
          } else {
            if (result.paymentIntent.status === "succeeded") {
              form.submit();
            }
          }
        });
    })
    .fail(function () {
      location.reload();
    });
});
