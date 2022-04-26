from re import search
import requests
from dataclasses import dataclass
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim

def get_search(zip):
    geolocator = Nominatim(user_agent='weatherbot')
    coords = geolocator.geocode(zip, country_codes='us')
    url = f'https://forecast.weather.gov/MapClick.php?lat={coords.latitude}&lon={coords.longitude}'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    get_current(soup)

def get_current(soup):
    cur_cond = soup.find(class_ = 'myforecast-current').string
    cur_far = soup.find(class_ = 'myforecast-current-lrg').string
    cur_cel = soup.find(class_ = 'myforecast-current-sm').string
    
    cur_detail = []
    for data in soup.findAll('td'):
        cur_detail.append(data.string)

    cur_detail[11] = cur_detail[11].replace("\n", '')
    cur_detail[11] = cur_detail[11].strip()
    
    search_current_data =  current_data(
    cur_cond, cur_far, cur_cel, cur_detail[1], cur_detail[3], 
    cur_detail[5], cur_detail[7], cur_detail[9], cur_detail[11]
    )
    print(search_current_data)

@dataclass   
class current_data:
    cond: str = None
    far: str = None
    cel: str = None
    hum: str = None
    ws: str = None
    bar: str = None
    dew: str = None
    vis: str = None
    last: str = None

def main(zip):
    weather_data_raw = get_search(zip)


main('42069')