import requests
from urllib.parse import urlparse
from decouple import config


TOKEN = config('VK_TOKEN')


def shorten_link(token, url):
    api_url = 'https://api.vk.com/method/utils.getShortLink'
    params = {
        'access_token': token,
        'url': url,
        'v': '5.199'
    }
    response = requests.get(api_url, params=params)
    data = response.json()

    if 'error' in data:
        return None

    return data['response']['short_url']


def count_clicks(token, short_url):
    key = urlparse(short_url).path.lstrip('/')
    api_url = 'https://api.vk.com/method/utils.getLinkStats'
    params = {
        'access_token': token,
        'key': key,
        'interval': 'forever',
        'v': '5.199'
    }
    response = requests.get(api_url, params=params)
    data = response.json()

    if 'error' in data:
        return None

    stats = data['response']['stats']
    return sum(item['views'] for item in stats)


def is_shorten_link(token, url):
    key = urlparse(url).path.lstrip('/')
    api_url = 'https://api.vk.com/method/utils.getLinkStats'
    params = {
        'access_token': token,
        'key': key,
        'interval': 'day',
        'v': '5.199'
    }
    response = requests.get(api_url, params=params)
    data = response.json()
    return 'response' in data


def main():
    user_url = input('Введите ссылку: ')

    if is_shorten_link(TOKEN, user_url):
        clicks = count_clicks(TOKEN, user_url)
        if clicks is not None:
            print('Всего переходов по ссылке:', clicks)
        else:
            print('Ошибка: не удалось получить статистику.')
    else:
        short = shorten_link(TOKEN, user_url)
        if short:
            print('Сокращенная ссылка:', short)
        else:
            print('Ошибка: неправильная ссылка.')


if __name__ == '__main__':
    main()
