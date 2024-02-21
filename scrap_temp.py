import time
from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import numpy as np
import re
import requests
from datetime import datetime

# ---------------------------------------------------
# Check if numeric

def is_string_numeric(input_string):
    pattern = r'^[-]?[0-9]*\.?[0-9]+$'
    return bool(re.match(pattern, input_string))

# ---------------------------------------------------
# Web scrap the temperatures

def get_random_user_agent():
    ua = UserAgent()
    return ua.random

def scrape_temperature(url):

    while True:

        headers = {'User-Agent': get_random_user_agent()}
        response = requests.get(url, headers)

        if response.status_code == 200:

            soup = BeautifulSoup(response.text, 'html.parser')
            temperature_span = soup.find('span', {'class': 'CurrentConditions--tempValue--MHmYY'}, {'data-testid': 'TemperatureValue'})

            if temperature_span:

                temperature_value = temperature_span.get_text(strip=True)
                if is_string_numeric(f'{temperature_value}'[:-1]) == True:
                    return f'{temperature_value}'[:-1]
                
            else:
                return 'Temperature information not found on the page.'

        #else:
        #    return f"Failed to retrieve the page. Status code: {response.status_code}"
            
# ---------------------------------------------------
# Scrap the temperatures

longitudes = np.loadtxt("parishes_coordinates.dat")[:, 0]
latitudes = np.loadtxt("parishes_coordinates.dat")[:, 1]

temperatures_converted = []
url_batch = []

for i in range (len(latitudes)):
    url_to_scrape = 'https://weather.com/weather/today/l/' + str(longitudes[i]) + ',' + str(latitudes[i]) + '?par=google'  # Replace with the actual URL
    url_batch.append(url_to_scrape)

# ---------------------------------------------------
# Loop for the hours

now = 1
last_time = datetime.now()

while True:

    current_time = datetime.now()
    time_difference = current_time - last_time

    if time_difference.total_seconds() >= 3600 or (datetime.now().minute == 1 and now == 1):

        current_time = datetime.now()
        last_time = current_time

        temperatures_converted = np.zeros(len(latitudes))
        now = 0

        with ThreadPoolExecutor(max_workers=20) as executor:
            temperatures = list(executor.map(scrape_temperature, url_batch))

        for i in range (len(temperatures)):
            if is_string_numeric(temperatures[i]) == True:
                temp = (float(temperatures[i]) - 32)*5/9
                temperatures_converted[i] = round(temp, 3)
        
            else:
                temperatures_converted[i] = 0.0

        filename = "./temperatures/temperatures_" + str(current_time.year) + "_" + str(current_time.month) + "_" + str(current_time.day) + "_" + str(current_time.hour)
        np.savetxt(filename, temperatures_converted)

    time.sleep(10)