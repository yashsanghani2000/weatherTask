
from bs4 import BeautifulSoup
import requests 
from datetime import datetime
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
 
 
def getweather(city):
    city = city+" weather"
    city = city.replace(" ", "+")
    res = requests.get(
        f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
    
    soup = BeautifulSoup(res.text, 'html.parser')
    location = soup.select('#wob_loc')
    date = datetime.now().strftime("%d/%m/%Y")
    time =  datetime.now().strftime("%H:%M:%S")
    info = soup.select('#wob_dc')[0].getText()
    weathers = soup.select('#wob_tm')[0].getText()
    new_city = city.replace("+", " ")
    location = new_city.split(" ")
    print(weathers)
    data = {
        "date" : date,
        "time" : time,
        "info" : info,
        "weathers" : weathers+"°C",
        "location" : location,
    }
    return data
 