from re import search
import requests
from dataclasses import dataclass
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim

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

def get_search(zip):
    geolocator = Nominatim(user_agent='weatherbot')
    coords = geolocator.geocode(zip, country_codes='us')
    url = f'https://forecast.weather.gov/MapClick.php?lat={coords.latitude}&lon={coords.longitude}'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    get_current(soup)
    get_extended(soup)

def get_current(soup):
    cur_summary = []
    for data in soup.find(id = 'current_conditions-summary'):
        if data.string != '\n':
            if data.string != None:
                cur_summary.append(data.string)
    
    cur_detail = []
    for data in soup.findAll('td'):
        cur_detail.append(data.string)

    cur_detail[11] = cur_detail[11].replace("\n", '')
    cur_detail[11] = cur_detail[11].strip()
    
    search_current_data =  current_data(
    cur_summary[0], cur_summary[1], cur_summary[2], cur_detail[1], 
    cur_detail[3], cur_detail[5], cur_detail[7], cur_detail[9], cur_detail[11]
    )
    
def get_extended(soup):
    for data in soup.findAll(class_ = 'short-desc'):
        print(data.string)

def main(zip):
    weather_data = get_search(zip)


main('42069')