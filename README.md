# MealPalAPI
[MealPal](mealpal.com) is a subscription lunch service that lets you order your lunch every morning and then pick it up from the restaurant at reservation time. Since it launched, it has become my favorite to-go lunch options. This project is aim to develop a custom API to interact with MealPal service.

There are 3 routes now:
1. `/cities` returns all of the cities/countries with MealPal service
2. `/reserve/<schedule_id>/` makes reservation for a meal tomorrow
3. `/find/<city_id>/<neighborhood_id>?office=%s` returns the meal offerings tomorrow for a given city and neighborhood, ordered by walking distance from the passed-in office address
