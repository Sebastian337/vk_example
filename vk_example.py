import requests
from urllib.parse import urlparse
from decouple import config


TOKEN = config("VK_TOKEN")


def shorten_link(token, url):
    api_url = "https://api.vk.com/method/utils.getShortLink"
    params = {
        "access_token": token,
        "url": url,
        "v": "5.199",
    }
    response = requests.get(api_url, params=params)
    response.raise_for_status()

    response_json = response.json()

    if "error" in response_json:
        raise requests.exceptions.HTTPError(response_json["error"])

    return response_json["response"]["short_url"]


def count_clicks(token, short_url):
    key = urlparse(short_url).path.lstrip("/")
    api_url = "https://api.vk.com/method/utils.getLinkStats"
    params = {
        "access_token": token,
        "key": key,
        "interval": "forever",
        "v": "5.199",
    }
    response = requests.get(api_url, params=params)
    response.raise_for_status()

    stats_json = response.json()
    if "error" in stats_json:
        raise requests.exceptions.HTTPError(stats_json["error"])

    stats = stats_json["response"]["stats"]
    return sum(item["views"] for item in stats)


def is_shorten_link(url):

    return "vk.cc" in url


def main():
    user_url = input("Введите ссылку: ")

    try:
        if is_shorten_link(user_url):
            clicks = count_clicks(TOKEN, user_url)
            print("Всего переходов по ссылке:", clicks)
        else:
            short_link = shorten_link(TOKEN, user_url)
            print("Сокращенная ссылка:", short_link)
    except requests.exceptions.RequestException as e:
        print("Некорректная ссылка или ошибка HTTP:", e)
    except requests.exceptions.HTTPError as e:
        print("Ошибка VK API:", e)


if __name__ == "__main__":
    main()
