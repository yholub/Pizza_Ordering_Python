var timeAndLoc = (function ($) {
    var icons = [
      'http://maps.google.com/mapfiles/markerA.png',
      'http://maps.google.com/mapfiles/markerB.png',
      'http://maps.google.com/mapfiles/markerC.png'
    ];

    var model = null;
    var lastData = null;

    return {
        init: init,
        initMap: initMap
    };

  
    function init(items) {
        var locInfo =  $.ajax({
            url: "/api/pizza",
            data: JSON.stringify(items),
            contentType: "application/json",
            type: "POST"

        });
        
        var timeInfo = $.post("/api/order/gettime", items);
        $.when(locInfo, timeInfo)
            .then(function (locs, time) {
                lastData =  locs[0];
                model = new TimeLocViewModel(locs[0], time[0], items);
                $("#gmap").on("change", "select", function () {
                    var val = parseInt($(this).val());
                    if (val > 0) {
                        model.selectedHouse(model.houses[val - 1]);
                    }
                    else {
                        model.selectedHouse(null);
                    }
                });
                $('#timepicker').timepicker({
                    altField: "#timepickerInput"
                });

                ko.applyBindings(model,
                    document.getElementById("timeAndLocView"));

               
            });

    }

    function TimeLocViewModel(locs, time, items) {
        this.houses = locs;
        this.items = items;
        this.houses.forEach(function (el, i) {
            el.index = i;
            el.time = ko.observable(null);
        });

        this.selectedHouse = ko.observable(null);
        this.showMap = ko.observable(false);
        this.map = null;
        
        this.loaded = ko.observable(window.google === undefined || window.google === null);

        var self = this;
        this.toggle = function () {
            if (!self.map) {
                self.map = createMapPlace(self.houses);
            }

            //self.showMap(!self.showMap());
            if (self.showMap()) {
                self.map.Load();
                if (self.selectedHouse()) {
                    self.map.ViewOnMap(self.selectedHouse().index + 1);
                } else {
                    self.map.ViewOnMap(0);
                }
            }
                

           
        }

        this.afterPickerRender = function (dom, el) {
            $(dom).find(".timepicker").timepicker({
                showPeriod: false,
                altField: '#timepickerInput' + el.Id,
                onSelect: timeChanged,
                onHourShow: createHourCallback(el.Id, time),
                onMinuteShow: createMinuteCallback(el.Id, time)
            });
        }

        this.next = function () {
            var data = {
                id: self.selectedHouse().Id,
                time: self.selectedHouse().time(),
                items: self.items
            };
        }
        
        function timeChanged(time) {
            self.selectedHouse().time(time);
        }
        
    }

    function createHourCallback(id, time) {
        return function (hour) {
            if (time[id].Hours[hour]) {
                return true;
            } else {
                return false;
            }
        }
    }

    function createMinuteCallback(id, time) {
        return function (hour, min) {
            if (time[id].Hours[hour]) {
                if (time[id].Time[hour][min]) {
                    return true;
                } else {
                    return false;
                }
            } else {
                return false;
            }
        }
    }

    function createMapPlace(locs) {
        return new Maplace({
            locations: $.map(locs, function (el, i) {
                return {
                    lat: el.Location.Lat,
                    lon: el.Location.Lon,
                    zoom: 15,
                    title: el.Location.StreetName + ' ' + el.Location.HouseNumber,
                    html: '<h5>' + el.Location.StreetName + ' ' + el.Location.HouseNumber + '</h5>',
                    icon: icons[i]

                };

            }),
            map_div: '#gmap',
            controls_on_map: true,
            controls_type: 'dropdown',
            force_generate_controls: true,
            controls_applycss: true,
            controls_title: 'Choose a location:',
        });
    }

    function initMap() {
        if(model)
            model.loaded(true);
    }


})(jQuery);