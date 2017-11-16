/// <reference path="layout.js" />
$.sammy("#main", function () {
    this._checkFormSubmission = function (form) {
        return false;
    };


    this.use('Handlebars', 'html');
    this.get('#/settings', function (context) {
        var self = context;
        if (window.task) {
            clearInterval(window.task);
            window.task = null;
        }
        var sets = $.get('/api/settings');
        var ings = $.get('/api/ingredients');
        $.when(sets, ings).then(function (packedSettings, packedIngs) {
           
            $("#sHref").addClass("navactive");
            $("#oHref").removeClass("navactive");
            self.render('settings.html').replace("#main").then(function() {
                
                function SettingsFormModel(settings, ingsString) {
                    ings = JSON.parse(ingsString)
                    this.start = ko.observable(settings.Open);
                    this.end = ko.observable(settings.Close);
                    this.cap = ko.observable(settings.Capacity);
                    this.PizzaHouseId = settings.Id;
                    var dict = {};
                    settings.InStock.forEach(function (el) {
                        dict[el.IngredientDto.Id] = el.Quantity;
                    });

                    var list = $.map(ings, function(el) {
                        return {
                            name: el.Name,
                            price: el.Price,
                            id: el.Id,
                            quantity: ko.observable(dict[el.Id] ? dict[el.Id] : 0)
                        };
                    });

                    this.ing = list;

                    var self = this;
                    this.submit = function (data, event) {
                        $.ajax({
                            url: "/api/settings",
                            data: JSON.stringify( {
                                StartHour: self.start(),
                                EndHour: self.end(),
                                Capacity: self.cap(),
                                PizzaHouseId: self.PizzaHouseId,
                                IngState: $.map(self.ing, function(el) {
                                    return {
                                        Id: el.id,
                                        Quantity: el.quantity()
                                    }
                                })
                            }),
                            contentType: "application/json",
                            type: "POST"

                        })
                        .then(function() {
                            $.notify({
                                message: 'Налаштування оновлено',
                                type: 'success'
                            });
                        });
                    }
                }
                
                var model = new SettingsFormModel(packedSettings[0], packedIngs[0]);
                ko.applyBindings(model, document.getElementById('setview'));
               
            });

        });




    });

   

    this.get('#/', function (context) {
        if (window.task) {
            clearInterval(window.task);
            window.task = null;
        }

        var self = context;
        $("#oHref").addClass("navactive");
        $("#sHref").removeClass("navactive");
        var getOrds = $.get('/api/Order/GetCurrent');
        var getSet = $.get('/api/settings');
        $.when(getOrds, getSet).done(function (concatData, concatSettings) {
            var data = concatData[0];
            var settings = concatSettings[0];
                var list = [];
                var now = new Date();
                var stHour = now.getHours();
                var stMin = now.getMinutes();
                if (stHour < settings.Open) {
                    stHour = settings.Open;
                }

                var endHour = (settings.Close - stHour + 24) % 24 + stHour;
                for (var i = stHour; i < endHour; i++) {
                    for (var j = 0; j < 60; j = j + 10) {
                        var jText = '' + j;
                        if (j < 10) {
                            jText = '0' + jText;
                        }
                        list.push('' + i % 24 + ':' + jText);
                    }
                }
                
                self.partial('orders.html', { hours: list, cache: false }).then(function () {
                    
                    $('#calendar').height(((endHour - stHour) * 60) * 3);
                    
                    var layOutDay = function (cal_events) {
                        $('#calendar').addEvents(cal_events);
                    };
                  
                    $('#calendar').layOutDay({
                        'calendar_start': stHour * 60,
                        'calendar_end': endHour * 60,
                        'time_selector': 'body .time'
                    });
                   
                    var list = eventsMap(data);
                    layOutDay(list);


                    function OrderViewModel(data) {
                        this.dict = {};
                        var self = this;
                        this.selected = ko.observable(null);
                        self.orders = ko.observableArray([]);
                        data.forEach(function (el) {
                            self.dict[el.Id] = el;
                            el.State = ko.observable(el.State);
                            self.orders.push(el);
                        });

                        this.showSelected = ko.observable(false);
                        
                        this.toggleShowSelected = function () {
                            self.showSelected(!self.showSelected());
                        }

                        this.changeSelected = function(id) {
                            self.selected(self.dict[id]);
                        }

                        this.select = function(el) {
                            $this = $('.event[data-order-item-id="' + el.Id + '"]');
                            $(".event.active").removeClass('active');
                            $(".event.activeRelated").removeClass('activeRelated');
                            $this.addClass('active');
                            $('.event[data-order-id="' + el.OrderId + '"]').addClass('activeRelated');
                            model.changeSelected(el.Id);
                        }

                        this.accept = function (el) {
                            $.post('/api/order/accept/' + el.OrderId);
                            $('.event[data-order-item-id="' + el.Id + '"]').addClass('accepted');
                            el.State(1);

                        }

                        this.acceptSelected = function () {
                            var el = self.selected();
                            $.post('/api/order/accept/' + el.OrderId);
                            $('.event[data-order-item-id="' + el.Id + '"]').addClass('accepted');
                            el.State(1);
                        }

                        this.reject = function (el) {
                            $.post('/api/order/reject/' + el.OrderId);
                            $('.event[data-order-id="' + el.OrderId + '"]').remove();
                            self.orders.remove(function (ev) {
                                return el.OrderId == ev.OrderId;
                            });

                            refillCalendar(self.orders());
                        }
                        this.rejectSelected = function () {
                            var el = self.selected();
                            $.post('/api/order/reject/' + el.OrderId);
                            $('.event[data-order-id="' + el.OrderId + '"]').remove();
                            self.orders.remove(function (ev) {
                                return el.OrderId == ev.OrderId;
                            });

                            self.selected(null);
                            refillCalendar(self.orders());
                        }
                    }

                    var model = new OrderViewModel(data);
                    ko.applyBindings(model, document.getElementById('view'));
                    window.task = setInterval(function () {
                        $.get('/api/Order/GetNew', function (data) {
                            if (window.task) {
                                fillCalendarWithNewData(data, model);
                            }
                        });
                    }, 2000);
                    $("#calendar").on("click", ".event", function () {
                        $this = $(this);
                        $(".event.active").removeClass('active');
                        $(".event.activeRelated").removeClass('activeRelated');
                        $this.addClass('active');
                        $('.event[data-order-id="' + $this.attr("data-order-id") + '"]').addClass('activeRelated');
                        model.changeSelected($this.attr("data-order-item-id"));
                    });

                   
                 
            });
        
            
        });

    });


    


}).run("#/");

function eventsMap(data) {
    var now = new Date();
    return $.map(data, function (d) {
        return {
            event: {
                dateStart: new Date(now.getYear(), /* month */ now.getMonth(),  /* day */ now.getDate(), /* hour */ d.StHour, /* minute */ d.StMinute, 0, 0),
                dateEnd: new Date(now.getYear(), /* month */ now.getMonth(),  /* day */ now.getDate(), /* hour */ d.EndHour, /* minute */ d.EndMinute, 0, 0),
                title: d.Name,
                state: d.State,
                description: "Price: " + d.Price + " Start: " + d.StartStr + " End: " + d.EndStr,
                ordId: d.OrderId,
                id: d.Id
            }
        }
    });
}

function fillCalendarWithNewData(data, model) {
    var notYet = data.filter(function (el) {
        if (model.dict[el.Id]) {
            return false;
        } else {
            return true;
        }
    });
    var list = eventsMap(notYet);
    if (notYet.length > 0) {
        $('#calendar').addEvents(list);
        notYet.forEach(function (el) {
            model.dict[el.Id] = el;
            el.State = ko.observable(el.State);
            model.orders.push(el);
        });
    }
}

function refillCalendar(data) {
    $calendar = $("#calendar");
    $calendar.reset();
    $calendar.find(".event").remove();
    var list = eventsMap(data);
    if (list.length > 0) {
        $calendar.addEvents(list);
    }
}
function isBound(id) {
    if (document.getElementById(id) != null)
        return !!ko.dataFor(document.getElementById(id));
    else
        return false;
}