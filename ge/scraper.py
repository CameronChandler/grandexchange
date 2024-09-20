import requests
from constants import ALL_ITEMS, HEADERS
from typing import Optional
from sqlalchemy import create_engine, text
from time import sleep
from tqdm import tqdm
import pandas as pd


def scrape_prices(item_id :int, timestep: str, sleep_seconds: int = 1) -> Optional[dict]:
    sleep(sleep_seconds)
    url = f"https://prices.runescape.wiki/api/v1/osrs/timeseries?timestep={timestep}&id={item_id}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        return response.json()['data']
    
    print(f"Error: {response.status_code}", item_id, timestep)
    return None


def insert_prices(conn, data: dict, item_id: int, timestep: str) -> None:
    for entry in data:
        timestamp   = entry['timestamp']
        avg_high    = entry['avgHighPrice']
        avg_low     = entry['avgLowPrice']
        high_volume = entry['highPriceVolume']
        low_volume  = entry['lowPriceVolume']

        # Prepare the values for the SQL query, converting None to 'NULL'
        query_values = [
            item_id,
            f'"{timestep}"',
            timestamp,
            'NULL' if avg_high    is None else avg_high,
            'NULL' if avg_low     is None else avg_low,
            'NULL' if high_volume is None else high_volume,
            'NULL' if low_volume  is None else low_volume,
        ]

        query = f'''
            INSERT OR IGNORE INTO prices (item_id, timestep, timestamp, avgHighPrice, avgLowPrice, highPriceVolume, lowPriceVolume)
            VALUES ({', '.join(map(str, query_values))})
        '''
    
        conn.execute(text(query))
    conn.commit()

# # Create table for the first time - Don't have to run this again
# from sqlalchemy import create_engine, Column, String, Integer, Float, MetaData, Table

# engine = create_engine('sqlite:///../data/runescape_prices.db')
# metadata = MetaData()

# prices_table = Table('prices', metadata,
#     Column('item_id',         Integer, primary_key=True),
#     Column('timestep',        String,  primary_key=True),
#     Column('timestamp',       Integer, primary_key=True),
#     Column('avgHighPrice',    Float,   nullable=True),
#     Column('avgLowPrice',     Float,   nullable=True),
#     Column('highPriceVolume', Integer, nullable=True),
#     Column('lowPriceVolume',  Integer, nullable=True)
# )

# # Create the table
# metadata.create_all(engine)

def scrape_prices_all_items(timestep: str, verbose: bool = False) -> None:
    ''' For a given timestep, will scrape and store all items '''
    engine = create_engine('sqlite:///../data/runescape_prices.db')

    iterator = tqdm(ALL_ITEMS) if verbose else ALL_ITEMS
    for item_id in iterator:
        with engine.connect() as conn:
            data = scrape_prices(item_id, timestep)
            if data:
                insert_prices(conn, data, item_id, timestep)


def get_prices(item_id: Optional[int] = None, timestep: Optional[str] = None):
    engine = create_engine('sqlite:///../data/runescape_prices.db')

    query = 'SELECT * FROM prices'
    conditions = []

    if item_id is not None:
        conditions.append(f'item_id = {item_id}')
    
    if timestep is not None:
        conditions.append(f'timestep = "{timestep}"')

    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)
    
    with engine.connect() as conn:
        result = pd.read_sql(query, conn)
    
    tz = 'Australia/Sydney'
    result['datetime'] = pd.to_datetime(result.timestamp, unit='s').dt.tz_localize('UTC').dt.tz_convert(tz)
    
    return result.reset_index(drop=1)