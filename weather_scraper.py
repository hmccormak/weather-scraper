import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim

def get_search(zip):
    geolocator = Nominatim(user_agent='weatherbot')
    coords = geolocator.geocode(zip)
    url = f'https://forecast.weather.gov/MapClick.php?lat={coords.latitude}&lon={coords.longitude}'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    current = soup.find_all(id="current_conditions-summary")
    seven_day = soup.find_all('div', class_ = 'tombstone-container')
    results = (current, seven_day)
    return results

def process_search(weather_data_raw):
    print(weather_data_raw)

def main(zip):
    weather_data_raw = get_search(zip)
    process_search(weather_data_raw)


main('20782')