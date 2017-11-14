var payment = (function ($) {
    return {
        init: init,
        ViewModel: ViewModel
    };

    function ViewModel(pizzas) {
        var self = this;

        self.cardNumber = ko.observable();
        self.cardCvc = ko.observable();
        self.cardExpMonth = ko.observable();
        self.cardExpYear = ko.observable();

        self.bonusesHas = ko.observable(500);
        self.bonusesToPay = ko.observable(750);
        self.moneyToPay = ko.observable(200);

        self.submitBonusesPayment = function (e) {
            if (self.bonusesHas() >= self.bonusesToPay()) {
                // TODO
                successfullyPaid();
            }
            else {
                failedToPay('У вас недостатньо бонусів =(');
            }
        }

        self.submitMoneyPayment = function (e) {
            payWithStripe(e);
            //successfullyPaid();
        }

        function payWithStripe(e) {
            $form = $("money-payment-form");
            /* Visual feedback */
            $form.find('[type=submit]').html('Validating <i class="fa fa-spinner fa-pulse"></i>');

            var PublishableKey = 'pk_test_aJg3RiIHme0PcBL3abE0DqnL'; // Replace with your API publishable key
            Stripe.setPublishableKey(PublishableKey);

            /* Create token */
            var ccData = {
                number: self.cardNumber().replace(/\s/g, ''),
                cvc: self.cardCvc(),
                exp_month: self.cardExpMonth(),
                exp_year: self.cardExpYear()
            };

            Stripe.card.createToken(ccData, function stripeResponseHandler(status, response) {
                if (response.error) {
                    /* Visual feedback */
                    $form.find('[type=submit]').html('Try again');
                    /* Show Stripe errors on the form */
                    failedToPay(response.error.message);
                } else {
                    /* Visual feedback */
                    $form.find('[type=submit]').html('Processing <i class="fa fa-spinner fa-pulse"></i>');
                    /* Hide Stripe errors on the form */
                    $form.find('.payment-errors').closest('.row').hide();
                    $form.find('.payment-errors').text("");
                    // response contains id and card, which contains additional card details            
                    console.log(response.id);
                    console.log(response.card);
                    var token = response.id;
                    // AJAX - you would send 'token' to your server here.
                    $.post('/account/stripe_card_token', {
                        token: token
                    })
                        // Assign handlers immediately after making the request,
                        .done(function (data, textStatus, jqXHR) {
                            $form.find('[type=submit]').html('Payment successful <i class="fa fa-check"></i>').prop('disabled', true);
                        })
                        .fail(function (jqXHR, textStatus, errorThrown) {
                            $form.find('[type=submit]').html('There was a problem').removeClass('success').addClass('error');
                            /* Show Stripe errors on the form */
                            $form.find('.payment-errors').text('Try refreshing the page and trying again.');
                            $form.find('.payment-errors').closest('.row').show();
                        });
                }
            });
        }
    }

    function init() {
        applyJQueryInputMasks();
        ko.applyBindings(new ViewModel(), document.getElementById('paymentView'));
    }

    function applyJQueryInputMasks() {
        ko.bindingHandlers.masked = {
            init: function (element, valueAccessor, allBindingsAccessor) {
                var mask = allBindingsAccessor().mask || {};
                $(element).mask(mask, {
                    completed: function () {
                        var $next = $(".payment-field").eq($(".payment-field").index(element) + 1);
                        $next.focus();
                    }
                });
                $(element).click(function () {
                    var val = $(this).val();
                    if (!val || val.trim() == "") {
                        if ($(this).is("input[type=text]")) {
                            $(this).caret(0);
                        }
                    }
                });
                ko.utils.registerEventHandler(element, 'focusout', function () {
                    var observable = valueAccessor();
                    observable($(element).val());
                });
            },
            update: function (element, valueAccessor) {
                var value = ko.utils.unwrapObservable(valueAccessor());
                $(element).val(value);
            }
        };
    }

    function successfullyPaid() {
        $.notify({
            message: 'Оплата пройшла успішно',
            type: 'success'
        });
    }

    function failedToPay(message) {
        $.notify({
            // options
            message: message
        }, {
                // settings
                type: 'danger'
            });
    }
})(jQuery);




//var $form = $('#payment-form');
//$form.on('submit', payWithStripe);

///* If you're using Stripe for payments */
//function payWithStripe(e) {
//    e.preventDefault();

//    /* Visual feedback */
//    $form.find('[type=submit]').html('Validating <i class="fa fa-spinner fa-pulse"></i>');

//    var PublishableKey = 'pk_test_aJg3RiIHme0PcBL3abE0DqnL'; // Replace with your API publishable key
//    Stripe.setPublishableKey(PublishableKey);

//    /* Create token */
//    var expiry = $form.find('[name=cardExpiry]').payment('cardExpiryVal');
//    var ccData = {
//        number: $form.find('[name=cardNumber]').val().replace(/\s/g, ''),
//        cvc: $form.find('[name=cardCVC]').val(),
//        exp_month: expiry.month,
//        exp_year: expiry.year
//    };

//    Stripe.card.createToken(ccData, function stripeResponseHandler(status, response) {
//        if (response.error) {
//            /* Visual feedback */
//            $form.find('[type=submit]').html('Try again');
//            /* Show Stripe errors on the form */
//            $form.find('.payment-errors').text(response.error.message);
//            $form.find('.payment-errors').closest('.row').show();
//        } else {
//            /* Visual feedback */
//            $form.find('[type=submit]').html('Processing <i class="fa fa-spinner fa-pulse"></i>');
//            /* Hide Stripe errors on the form */
//            $form.find('.payment-errors').closest('.row').hide();
//            $form.find('.payment-errors').text("");
//            // response contains id and card, which contains additional card details            
//            console.log(response.id);
//            console.log(response.card);
//            var token = response.id;
//            // AJAX - you would send 'token' to your server here.
//            $.post('/account/stripe_card_token', {
//                token: token
//            })
//                // Assign handlers immediately after making the request,
//                .done(function (data, textStatus, jqXHR) {
//                    $form.find('[type=submit]').html('Payment successful <i class="fa fa-check"></i>').prop('disabled', true);
//                })
//                .fail(function (jqXHR, textStatus, errorThrown) {
//                    $form.find('[type=submit]').html('There was a problem').removeClass('success').addClass('error');
//                    /* Show Stripe errors on the form */
//                    $form.find('.payment-errors').text('Try refreshing the page and trying again.');
//                    $form.find('.payment-errors').closest('.row').show();
//                });
//        }
//    });
//}
///* Fancy restrictive input formatting via jQuery.payment library*/
//$('input[name=cardNumber]').payment('formatCardNumber');
//$('input[name=cardCVC]').payment('formatCardCVC');
//$('input[name=cardExpiry').payment('formatCardExpiry');

///* Form validation using Stripe client-side validation helpers */
//jQuery.validator.addMethod("cardNumber", function (value, element) {
//    return this.optional(element) || Stripe.card.validateCardNumber(value);
//}, "Please specify a valid credit card number.");

//jQuery.validator.addMethod("cardExpiry", function (value, element) {
//    /* Parsing month/year uses jQuery.payment library */
//    value = $.payment.cardExpiryVal(value);
//    return this.optional(element) || Stripe.card.validateExpiry(value.month, value.year);
//}, "Invalid expiration date.");

//jQuery.validator.addMethod("cardCVC", function (value, element) {
//    return this.optional(element) || Stripe.card.validateCVC(value);
//}, "Invalid CVC.");

//validator = $form.validate({
//    rules: {
//        cardNumber: {
//            required: true,
//            cardNumber: true
//        },
//        cardExpiry: {
//            required: true,
//            cardExpiry: true
//        },
//        cardCVC: {
//            required: true,
//            cardCVC: true
//        }
//    },
//    highlight: function (element) {
//        $(element).closest('.form-control').removeClass('success').addClass('error');
//    },
//    unhighlight: function (element) {
//        $(element).closest('.form-control').removeClass('error').addClass('success');
//    },
//    errorPlacement: function (error, element) {
//        $(element).closest('.form-group').append(error);
//    }
//});

//paymentFormReady = function () {
//    if ($form.find('[name=cardNumber]').hasClass("success") &&
//        $form.find('[name=cardExpiry]').hasClass("success") &&
//        $form.find('[name=cardCVC]').val().length > 1) {
//        return true;
//    } else {
//        return false;
//    }
//}

//$form.find('[type=submit]').prop('disabled', true);
//var readyInterval = setInterval(function () {
//    if (paymentFormReady()) {
//        $form.find('[type=submit]').prop('disabled', false);
//        clearInterval(readyInterval);
//    }
//}, 250);


///*
//https://goo.gl/PLbrBK
//*/