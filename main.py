

import os
import requests
from dotenv import load_dotenv
import argparse

load_dotenv()

def shorten_link(token, url):
    response = requests.post(
        'https://api-ssl.bitly.com/v4/bitlinks',
        json={'long_url': url},
        headers={'Authorization': f"Bearer {token}"},
    )
    response.raise_for_status()
    return response.json().get('link')


def count_clicks(token, url):
    response = requests.get(
        f'https://api-ssl.bitly.com//v4/bitlinks/{url}/clicks/summary',
        params={'units': -1},
        headers={'Authorization': f"Bearer {token}"}
    )
    response.raise_for_status()
    return response.json().get('total_clicks')


def is_bitlink(url, token):
    response = requests.get(
        f'https://api-ssl.bitly.com//v4/bitlinks/{url}',
        headers={'Authorization': f"Bearer {token}"}
    )
    return response.ok


if __name__ == '__main__':
    api_key = os.getenv('BITLY_TOKEN')
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    new_url = parser.parse_args().url
    status = is_bitlink(new_url, api_key)

    if status:
        try:
            print(count_clicks(api_key, new_url))
        except requests.exceptions.HTTPError:
            print('Неверный адрес ссылки')
    else:
        try:
            print(shorten_link(api_key, new_url))
        except requests.exceptions.HTTPError:
            print('Неверный адрес ссылки')




