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

@dataclass
class extended_data:
    per: str = None
    des: str = None
    temp: str = None


def get_search(zip):
    """Get weather.gov page based off of zipcode

    Args:
        zip (int): given zipcode

    Returns:
        bs4.BeautifulSoup: parsed html
        string: geocode address (city, county, state, zipcode, country)
    """
    geolocator = Nominatim(user_agent='weatherbot')
    location = geolocator.geocode(zip, country_codes='us')
    url = f'https://forecast.weather.gov/MapClick.php?lat={location.latitude}&lon={location.longitude}'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    return (soup, location.address)

def get_current(soup):
    """Get current weather.gov data from the page soup

    Args:
        soup (bs4.BeautifulSoup): parsed html

    Returns:
        object: current_data object of scraped info
    """
    cur_summary = []

    print(type(soup))
    for data in soup.find(id = 'current_conditions-summary'):
        if data.string != '\n':
            if data.string != None:
                cur_summary.append(data.string)
    
    cur_detail = []

    for data in soup.findAll('td'):
        cur_detail.append(data.string)

    if cur_detail[11] == None:
        cur_detail[11] = "No update timestamp!"
    cur_detail[11] = cur_detail[11].replace('\n', '')
    cur_detail[11] = cur_detail[11].strip()
    
    search_current_data =  current_data(
    cur_summary[0], cur_summary[1], cur_summary[2], cur_detail[1], 
    cur_detail[3], cur_detail[5], cur_detail[7], cur_detail[9], cur_detail[11]
    )

    return search_current_data

def get_ext_data(soup, class_name):
    temp_list = []

    for data in soup.findAll(class_ = class_name):
        line_strings = []
        for line in data:
            if str(line) != '<br/>':
                line_strings.append(line)
        temp_list.append(line_strings)
    return temp_list

def clean_ext_data(data_list):
    cleaned_list = []

    for i in range(len(data_list)):
        cleaned_list.append(' '.join(data_list[i]))
    return cleaned_list       
    
def get_extended(soup):
    """Get extended weather.gov data from page soup,
    uses get_ext_data() and clean_ext_data() in processing,
    probably should consolidate these functions

    Args:
        soup (bs4.BeautifulSoup): parsed html

    Returns:
        list: list of extended_data objects for each period listing
    """
    extended_temps = []

    for data in soup.findAll(class_ = 'temp'):
        extended_temps.append(data.string)
    
    period_names_raw = get_ext_data(soup, 'period-name')
    short_descriptions_raw = get_ext_data(soup, 'short-desc')

    period_names = clean_ext_data(period_names_raw)
    short_descriptions = clean_ext_data(short_descriptions_raw)

    extended_forecast = []

    for i in range(len(period_names)):
        extended_forecast.append(extended_data(period_names[i], 
        short_descriptions[i], extended_temps[i]))

    return extended_forecast 
    
def main(zip):
    s_data = get_search(zip)
    w_data = (get_current(s_data[0]), get_extended(s_data[0]))
    print(f'Current Weather of {s_data[1]}:')
    print(f'Condition: {w_data[0].cond} | Temp: {w_data[0].far}/{w_data[0].cel} | Humidity: {w_data[0].hum}')


main('20782')