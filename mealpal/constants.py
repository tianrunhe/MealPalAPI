HOST = "secure.mealpal.com"
BASE_URL = F"https://{HOST}"
LOGIN_URL = F"{BASE_URL}/login"
MENU_URL = F'{BASE_URL}/api/v1/cities/%s/product_offerings/lunch/menu'
RESERVATIONS_URL = F'{BASE_URL}/api/v2/reservations'
NEIGHBORHOODS_URL = F'{BASE_URL}/1/functions/getCitiesWithNeighborhoods'
HEADERS = {
    'Host': HOST,
    'Origin': BASE_URL,
    'Referer': LOGIN_URL,
    'Content-Type': 'application/json'
}
