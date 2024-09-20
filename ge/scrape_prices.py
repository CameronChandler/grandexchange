import requests

# URL for the OSRS price API
# https://prices.runescape.wiki/api/v1/osrs/5m?timestamp=1615733400
url = "https://prices.runescape.wiki/api/v1/osrs/5m?timestamp=1615733400"

# Sending a GET request to the URL
response = requests.get(url)

# Checking if the request was successful
if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Failed to retrieve data: {response.status_code}")
