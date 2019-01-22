import datetime as dt
from statistics import median
from typing import Optional

from api import get_friends
from api_models import User


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    cur_date = dt.datetime.now()
    fr_list = get_friends(user_id, 'bdate')
    age_list = []
    for fr in fr_list:
    	user = User(**fr)
    	if user.bdate:
    		try:
    			bd = dt.datetime.strptime(user.bdate, '%d.%m.%Y')
    		except:
    			continue
    		age = cur_date.year - bd.year
    		if cur_date.month < bd.month:
    			age -= 1
    		elif (cur_date.month == bd.month) and (cur_date.day <= bd.day):
    			age -= 1
    		age_list.append(age)

    if age_list:
    	return float(median(age_list))