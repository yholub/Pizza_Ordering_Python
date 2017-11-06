$.sammy("#main", function () {
    this._checkFormSubmission = function (form) {
        return false;
    };


    this.get('#/order', function (context) {
        updateHref();
        this
           .partial('/views/user/pizzaOrdering.html', { cache: false })
           .then(function () {
              
               pizzaOrdering.init();
           });
        
    });

    this.get('#/time', function () {
        this
             .partial('/views/user/timeAndLocation.html', { cache: false })
             .then(function () {
                 //Pass items
                 timeAndLoc.init(window.cacheOrders);
             });
    });

    this.get('#/payment', function () {
        updateHref();
        $("a.router-href.navactive").removeClass("navactive");
        $('a.router-href[href="#/uinfo"]').addClass("navactive");
        this
            .partial('/views/user/payment.html')
            .then(function () {
                payment.init();
            });
    });

    this.get('#/uinfo', function (context) {
        updateHref();
        $("a.router-href.navactive").removeClass("navactive");
        $('a.router-href[href="#/uinfo"]').addClass("navactive");
        this
             .partial('user/userInfoPage.html')
             .then(function () {
                 userInfo.init();
             });
    });

    this.get('#/', function (context) {
        updateHref();
        this.partial('/views/home.html').then(function () {
            //scroll for main page probably not needed know
            //$(document).ready(function () {
            //    $(document).on("scroll", onScroll);

            //    $('a[href^="#"]').on('click', function (e) {
            //        e.preventDefault();
            //        $(document).off("scroll");

            //        $('a').each(function () {
            //            $(this).removeClass('navactive');
            //        })
            //        $(this).addClass('navactive');

            //        var target = this.hash;
            //        $target = $(target);
            //        $('html, body').stop().animate({
            //            'scrollTop': $target.offset().top + 2
            //        }, 500, 'swing', function () {
            //            window.location.hash = target;
            //            $(document).on("scroll", onScroll);
            //        });
            //    });
            //});

            //function onScroll(event) {
            //    var scrollPosition = $(document).scrollTop();
            //    $('.nav li a').each(function () {
            //        var currentLink = $(this);
            //        var refElement = $(currentLink.attr("href"));
            //        if (refElement.position().top <= scrollPosition && refElement.position().top + refElement.height() > scrollPosition) {
            //            $('ul.nav li a').removeClass("navactive");
            //            currentLink.addClass("navactive");
            //        }
            //        else {
            //            currentLink.removeClass("navactive");
            //        }
            //    });


            //    $(function () {
            //        $('#portfolio').mixitup({
            //            targetSelector: '.item',
            //            transitionSpeed: 350
            //        });
            //    });

            //    $(function () {
            //        $("#datepicker").datepicker();
            //    });

            //};
        });
    });
    


    function updateHref() {
        $("a.router-href.navactive").removeClass("navactive");
        $('a.router-href[href="' + window.location.hash + '"]').addClass("navactive");
    }

}).run("#/");
