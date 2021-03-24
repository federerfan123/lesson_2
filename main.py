import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv()
import os
import argparse


def shorten_link(token, base_api_url, link):
    url = f'{base_api_url}/bitlinks'
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    params = {
        'long_url': link
    }
    response = requests.post(
        url=url,
        headers=headers,
        json=params
    )
    response.raise_for_status()
    bitlink = response.json()['link']
    return bitlink


def count_clicks(token, base_api_url, bitlink):
    parsed = urlparse(bitlink)
    bitlink = f'{parsed.netloc}{parsed.path}/'
    url = f'{base_api_url}/bitlinks/{bitlink}clicks/summary'
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    response = requests.get(
        url=url,
        headers=headers,
    )
    response.raise_for_status()
    total_clicks = response.json()['total_clicks']
    return total_clicks


def is_bitlink(token, base_api_url, bitlink):
    parsed = urlparse(bitlink)
    bitlink = f'{parsed.netloc}{parsed.path}'
    url = f'{base_api_url}/bitlinks/{bitlink}'
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    response = requests.get(
        url=url,
        headers=headers,
    )
    return response.ok


if __name__ == '__main__':
    token = os.getenv('API_TOKEN_BITLY')
    base_api_url = 'https://api-ssl.bitly.com/v4'
    parser = argparse.ArgumentParser()
    parser.add_argument('link')
    link = parser.parse_args().link
    if is_bitlink(token, base_api_url, link):
        try:
            print(count_clicks(token, base_api_url, link))
        except requests.exceptions.HTTPError:
            print('Неверная bitlink ссылка')
    else:
        try:
            print(shorten_link(token, base_api_url, link))
        except requests.exceptions.HTTPError:
            print('Неверная ссылка')
