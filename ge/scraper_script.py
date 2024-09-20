from scraper import scrape_prices_all_items

TIMESTEP_OPTIONS = ['5m', '1h', '6h', '24h']

for timestep in TIMESTEP_OPTIONS:
    scrape_prices_all_items(timestep, verbose=True)