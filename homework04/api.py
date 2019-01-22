import requests
import time
import config


domain = config.VK_CONFIG['domain']
access_token = config.VK_CONFIG['access_token']
version = config.VK_CONFIG['version']
user_id = config.VK_CONFIG['user_id']


def get(url: str, params={}, timeout=5, max_retries=5, backoff_factor=0.3) -> requests.models.Response:
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    for i in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=timeout)
            return response
        except:
            if i == max_retries - 1:
                raise
            exp_backoff = backoff_factor * (2 ** i)
            time.sleep(exp_backoff)

def get_friends(user_id: int, fields="") -> dict:
    """ Вернуть данных о друзьях пользователя

    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    
    query_params = {
        'domain': domain,
        'access_token': access_token,
        'user_id': user_id,
        'fields': fields,
        'version': version
    }

    query = "{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v={version}".format(**query_params)
    response = requests.get(query, params=query_params)
    return response.json()['response']['items']

def messages_get_history(user_id: int, offset=0, count=20) -> list:
    """ Получить историю переписки с указанным пользователем

    :param user_id: идентификатор пользователя, с которым нужно получить историю переписки
    :param offset: смещение в истории переписки
    :param count: число сообщений, которое нужно получить
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"

    query_params = {
        'domain': domain,
        'access_token': access_token,
        'user_id': user_id,
        'offset': offset,
        'count': count,
        'version': version
    }

    messages = []
    i = 0
    while i < count:
        if (i != 0) and ((i / 200) % 3 == 0):
            time.sleep(1)
        if count - i <= 200:
            query_params['count'] = count - i
        query = "{domain}/messages.getHistory?offset={offset}&count={count}&user_id={user_id}&access_token={access_token}&v={version}".format(**query_params)
        response = requests.get(query, params=query_params)
        json_file = response.json()['response']['items']
        messages.extend(json_file)
        i += 200
        query_params['offset'] += i

    return messages
