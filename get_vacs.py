import requests

possible_ids = {
    "ИДС Боржоми": 6,
    "Московский аэропорт Домодедово": 65,
    "Альфа-Банк": 80,
    "Samsung Research Russia": 429,
    "Норникель": 740,
    "HeadHunter": 1455,
    "Яндекс": 1740,
    "КонсультантПлюс": 2238,
    "Спортмастер": 2343
}


def get_vacs(employer_id):
    params = {
        'employer_id': employer_id
    }
    a = requests.get("https://api.hh.ru/vacancies", params).json()
    return a

#
# for id in possible_ids.values():
#     pprint(get_vacs(id))

