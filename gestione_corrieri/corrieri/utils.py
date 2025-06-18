import requests

def geocode_address(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': address,
        'format': 'json'
    }
    headers = {
        'User-Agent': 'gestione-corrieri-app'
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200 and response.json():
        data = response.json()[0]
        return float(data['lat']), float(data['lon'])
    return None, None
