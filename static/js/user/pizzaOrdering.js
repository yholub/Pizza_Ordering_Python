var pizzaOrdering = (function ($) {
    return {
        init: init,
        getPizzas: getPizzas,
        getIngredients: getIngredients,
        ViewModel: ViewModel
    };


    function getPizzas() {
        
        var promise = 
            $.get("/api/pizzas/fix")
            .then(function(data) {
                var pizzaData = JSON.parse(data);
                var pizzasArr = [];
                for (var i = 0; i < pizzaData.length; i++) {
                    var pizza = pizzaData[i];
                    var ingredients = [];
                    for (var j = 0; j < pizza["Ingredients"].length; j++) {
                        ingredients.push({ name: ko.observable(pizza.Ingredients[j].Name), count: ko.observable(1), id: pizza.Ingredients[j].IngredientId, price: pizza.Ingredients[j].Price, initCount: 1 });
                    }

                    pizzasArr.push({ id: pizza.Id, imgUrl: "../assets/images/" + pizza.Name + ".jpg", name: pizza.Name, price: pizza.Price, ingredients: ko.observableArray(ingredients) });
                }

                
                return pizzasArr;
            });

        return promise;
    }


    function getIngredients() {

        var promise =
            $.get("/api/ingredients")
            .then(function (data) {
                var ingredientsArr = [];
                var ingredientsData = JSON.parse(data);
                for (var i = 0; i < ingredientsData.length; i++) {
                    var ingredient = ingredientsData[i];
                    ingredientsArr.push({ id: ingredient.Id, imgUrl: "../assets/images/" + ingredient.Name + ".png", name: ko.observable(ingredient.Name), price: ko.observable(ingredient.Price), weight: ingredient.Weight, count: ko.observable(0), totalPrice: ko.observable(ingredient.Price), initCount: 0 });
                }

                return ingredientsArr;
            });

        return promise;
    }

    function ViewModel(pizzas, ingredientsArr) {
        var self = this;

        self.selectedPizzaCount = 0;
        self.pizzas = pizzas;
        self.allIngredients = ko.observableArray(ingredientsArr);
        self.selectedProducts = ko.observableArray([]);
        self.searchIngredient = ko.observable('');

        self.order = function () {
            window.cacheOrders = { orderItems: $.map(self.selectedProducts(), function (el) { return { id: el.id, name: el.name, count: el.countOfPizzas(), ingredients: $.map(el.ingredients(), function (ing) { return { id: ing.id, count: ing.count() } }) } }) };
            console.log(window.cacheOrders);
            location.href = "#/time";
        }

        /*self.showIngredients = ko.computed(function (ingredients) {
            var ingredientsInRightFormat = ingredients.reduce(function (y, x) {
                return ((y == "") ? y : y + ", ") + x.name() + ((x.count() > 1) ? "(" + x.count() + ")" : "");
            }, "");

            return ingredientsInRightFormat;
        });*/

        self.addToCard = function (data, event) {
            var pizzaId = Number(event.target.id);
            var pizza = self.pizzas[pizzaId];
            self.selectedProducts.push({ id: self.selectedPizzaCount, name: pizza.name, price: ko.observable(pizza.price), initPrice: pizza.price, ingredients: ko.observableArray(pizza.ingredients()), countOfPizzas: ko.observable(1) });
            self.selectedPizzaCount += 1;
        };

        self.allIngredientsForPizza = ko.observable({});

        self.totalPrice = ko.computed(function () {
            var total = self.selectedProducts().reduce(function (y, x) {
                return y + (x.price() * x.countOfPizzas());
            }, 0);

            return total;
        });

        self.deletePizzaItem = function (data, event) {
            if (data.countOfPizzas() <= 1)
                self.selectedProducts.remove(data);
            else {
                var newData = data;
                newData.countOfPizzas(newData.countOfPizzas() - 1)
                self.selectedProducts.replace(data, newData);
            }

            event.stopPropagation();

        }

        self.addPizzaItem = function (data, event) {
            if (data.countOfPizzas() <= 4) {
                var newData = data;
                newData.countOfPizzas(newData.countOfPizzas() + 1)
                self.selectedProducts.replace(data, newData);
            }

            event.stopPropagation();
            
        }


        self.totalCountForIngr = function (item) {
            self.allIngredients[item.id] =  Number(item.price()) * Number(item.count());
        }

        self.ingredientsSetCount = function (data, event) {
            var selectedPizza = data;
            var ingredientWithCount = self.allIngredients();
            ingredientWithCount.forEach(function (ingredient) {
                if (selectedPizza.ingredients().some(e => e.name() == ingredient.name())) {
                    ingredient.count(selectedPizza.ingredients().filter(x => x.name() == ingredient.name())[0].count());
                    ingredient.initCount = 1;
                }
                else {
                    ingredient.count(0);
                }
            });
            console.log("111111111");
            self.allIngredientsForPizza({ pizza: ko.observable(selectedPizza), ingredients: ko.observableArray(ingredientWithCount) });
        };
        
        self.calculatePizzaPriceWithAdditionalIngredients = ko.computed(function () {

            if (self.allIngredientsForPizza().pizza == null)
                return 0;

            var ingredientsPrice = 0;

            ingredientsPrice += self.allIngredientsForPizza().pizza().ingredients().reduce(function (y, x) {
                if(x.initCount >= 1) {
                    return (x.count() <= x.initCount) ? y : (x.count() - x.initCount) * x.price;
                }
                else
                    return y +  x.count() * x.price;
            }, 0);

            ingredientsPrice += self.allIngredientsForPizza().ingredients().reduce(function (y, x) {
                if (x.initCount >= 1) {
                    return (x.count() <= x.initCount) ? y : (x.count() - x.initCount) * x.price();
                }
                else
                    return y + x.count() * x.price();
            }, 0);


            return self.allIngredientsForPizza().pizza().initPrice + ingredientsPrice;
        });

        self.addAdditionalIngredients = function (data, event) {
            data = self.allIngredientsForPizza().pizza();
            self.allIngredientsForPizza().ingredients().forEach(function (ingredient) {
                if (data.ingredients().some(e => e.name() == ingredient.name())) {
                    data.ingredients().filter(x => x.name() == ingredient.name())[0].count(ingredient.count());
                }
                else if (ingredient.count() >= 1) {
                    data.ingredients.push({ name: ko.observable(ingredient.name()), count: ko.observable(ingredient.count()) });
                }
            });

            var ingredientsPrice = self.allIngredientsForPizza().ingredients().reduce(function (y, x) {
                if (x.initCount >= 1) {
                    return (x.count() <= x.initCount) ? y : (x.count() - x.initCount) * x.price();
                }
                else
                    return y + x.count() * x.price();
            }, 0);

            data.price(data.initPrice + ingredientsPrice);

            $('#ingredientModal').modal('hide');
        }


        self.serchedIngredients = ko.dependentObservable(function() {
            var search = self.searchIngredient().toLowerCase();
            var pizzaIngr = self.allIngredientsForPizza();
            console.log(!$.isEmptyObject(pizzaIngr));
            if(!$.isEmptyObject(pizzaIngr)){
                var ingredients = pizzaIngr.ingredients();
                console.log(ingredients);
                return ko.utils.arrayFilter(ingredients, function(ingredient) {
                    return ingredient.name().toLowerCase().indexOf(search) >= 0;
                });
            }

        }, self);
    }



    function init() {
        getPizzas().then(function (pizzas) {
            getIngredients().then(function (ingredients) {
                ko.applyBindings(new ViewModel(pizzas, ingredients), document.getElementById('pizzaOrderView'));
            });
        });
        
    }
    
  
})(jQuery);


