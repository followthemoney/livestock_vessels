
from typing import List, Dict
import requests
from dotenv import load_dotenv; load_dotenv()
import os
from pathlib import Path
import logging
import platform

GFW_API_KEY = os.environ.get('GFW_API_KEY')

if platform.system() == 'Linux':
    PATH_DATA= Path(os.environ.get('PATH_LIVESTOCK_UBUNTU'))
elif platform.system() == 'Darwin':
    PATH_DATA = Path(os.environ.get('PATH_LIVESTOCK'))

logging.basicConfig(level=logging.INFO, 
                    filename=PATH_DATA.joinpath('logs', 'livestock.logs'), 
                    filemode='w', 
                    format=('%(asctime)s - %(levelname)s - %(message)s'))

def get_vessels(query: List
                )-> List:

    ENDPOINT = 'https://gateway.api.globalfishingwatch.org/v3/vessels/search?'

    headers = {'Authorization': f"Bearer {GFW_API_KEY}",
               'Content-Type': 'application/json'}

    results = []

    for q in query:
        url = f'where=ssvid="{q}"&datasets[0]=public-global-vessel-identity:latest&includes[0]=OWNERSHIP&includes[1]=AUTHORIZATIONS&limit=5'
        r = requests.get(ENDPOINT + url, headers=headers)

        if r.status_code == 200:
            result = r.json()
            result.update({'query': q})
            results.append(result)
            with open(PATH_DATA.joinpath('data', 'events.json'), 'a') as file:
                file.write(f'{result}\n')

        elif r.status_code != 200:                
                logging.error(f'Something went wrong with query: {q} --> status code: {r.status_code} - reason: {r.reason}\nplease check')

    return results


def get_events(vessel_id: str,
               event_type: str,
               )-> Dict:

    ENDPOINT = 'https://gateway.api.globalfishingwatch.org/v3/events?'

    headers = {'Authorization': f"Bearer {GFW_API_KEY}",
               'Content-Type': 'application/json'}

    
    if event_type == 'encounter':
        dataset = 'public-global-encounters-events:latest'
    elif event_type == 'fishing': 
        dataset = 'public-global-fishing-events:latest'
    elif event_type == 'loitering':
        dataset = 'public-global-loitering-events:latest'
    elif event_type == 'port_visits':
        dataset = 'public-global-port-visits-c2-events:latest'
    elif event_type == 'ais':
        dataset = 'public-global-gaps-events:latest&gap-intentional-disabling=True'
    else:
        raise ValueError(f'Event type must be "encounter", "fishing", "loitering", "port_visits" or "ais" not {event_type}')

    url = f'vessels[0]={vessel_id}&datasets[0]={dataset}&start-date=2012-01-01&end-date=2024-01-01&limit=99999&offset=0'

    
    r = requests.get(ENDPOINT + url, headers=headers)
    

    if r.status_code == 200:
        result = r.json()
        result.update({'query': vessel_id})
        with open(PATH_DATA.joinpath('data', f'{event_type}.json'), 'a') as file:
            file.write(f'{result}\n')
    
        return result

    elif r.status_code != 200:                
            logging.error(f'Something went wrong with query: {vessel_id} --> status code: {r.status_code} - reason: {r.reason}\nplease check')

    return None
    