#### OUTDATED, SUPERSEDED BY SCRAPER.PY ####
import requests
from ge.constants import HEADERS
import pandas as pd
from typing import Optional

def get_data(item: int) -> Optional[pd.DataFrame]:
    url = f'https://api.weirdgloop.org/exchange/history/osrs/all?id={item}&compress=false'
       
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f'Item {item} Failed!')
        return None

    data = response.json()

    # Failure {"success": false}
    if 'success' in data:
        return None
    
    df = pd.DataFrame(data[str(item)])
    df['id'] = df['id'].astype(int)
    return df

def get_item_metadata() -> pd.DataFrame:
    url = 'https://chisel.weirdgloop.org/gazproj/gazbot/os_dump.json'

    response = requests.get(url)

    data = response.json()

    return pd.DataFrame(data).T.iloc[:-2].sort_values('id').reset_index(drop=1)