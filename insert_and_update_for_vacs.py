import psycopg2
from get_vacs import get_vacs
from get_vacs import possible_ids
from psycopg2 import errors
import requests
import time

def clean_dict(dict):
    """Метод для промежуточной очистки ответов апи от значений Null для возможности работы
    с ними"""
    result = {}
    for k, v in dict.items():
        if v is None:
            v = "None"
        result[k] = v
    return result


def create_vacancy(vac_api_type):
    """Метод для создания объекта класса 'словарь' в формате,
    предназначенном для переноса в базу данных"""
    vac = clean_dict(vac_api_type)
    my_vac = {'vacancy_id': vac['id'], 'vacancy_name': vac['name'],
              'url': vac['alternate_url'], 'employer_name': vac['employer']['name'],
              'employer_id': vac['employer']['id'],
              'employment': vac['employment']['name'],
              'experience': vac['experience']['name'],
              'responsibility': vac['snippet']['responsibility']}
    try:
        my_vac['salary_from'] = vac['salary']['from']
    except TypeError:
        my_vac['salary_from'] = None
    try:
        my_vac['salary_to'] = vac['salary']['to']
    except TypeError:
        my_vac['salary_to'] = None
    try:
        my_vac['city'] = vac['address']['city']
    except TypeError:
        my_vac['city'] = None
    try:
        my_vac['address'] = vac['address']['raw']
    except TypeError:
        my_vac['address'] = None

    return my_vac


def insert_into_table():
    """Метод для получения вакансий от выбранных работодателей через апи и добавления
    их в таблицу vacancies, пропуская те, которые в ней уже есть"""
    conn = psycopg2.connect(
        port="8080",
        host="localhost",
        database="vacancies",
        user="postgres",
        password="RosGus80"
    )
    vacancies = []
    cur = conn.cursor()

    for emp_id in possible_ids.values():
        emp_vacs = get_vacs(emp_id)['items']
        for vacancy in emp_vacs:
            vacancies.append(create_vacancy(vacancy))

    for vacancy in vacancies:
        try:
            cur.execute('INSERT INTO '
                    'vacancies(vacancy_id, vacancy_name, url, salary_from, salary_to, city,'
                    'address, employer_name, employer_id, employment, experience, responsibility)'
                    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    [vacancy['vacancy_id'], vacancy['vacancy_name'], vacancy['url'],
                     vacancy['salary_from'], vacancy['salary_to'], vacancy['city'],
                     vacancy['address'], vacancy['employer_name'], vacancy['employer_id'],
                     vacancy['employment'], vacancy['experience'], vacancy['responsibility']])
        except psycopg2.errors.UniqueViolation:
            continue

    conn.commit()
    cur.close()
    conn.close()


def update_table():
    """Метод для обновления таблицы по фильтру актуальности вакансий: метод получит все
    данные из таблицы vacancies, проверит каждую вакансию через апи и удалит те, которые были
    закрыты со времени прошлого обновления. Рекомендую обращаться к методу каждый раз
    при начале работы с базой данных, однако, из-за ограничения на количество запросов за
    промежуток времени, между проверкой двух вакансий приходится делать паузу в полсекунды,
    так что работа метода становится мучительно продолжительной пропорционально увеличению базы."""
    conn = psycopg2.connect(
        port="8080",
        host="localhost",
        database="vacancies",
        user="postgres",
        password="RosGus80"
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM vacancies")
    data = cur.fetchall()
    for vacancy in data:
        api_answer = requests.get(f"https://api.hh.ru/vacancies/{vacancy[0]}").json()
        if not api_answer["type"]["id"] == "open":
            cur.execute(f"DELETE FROM vacancies WHERE vacancies.vacancy_id = {vacancy[0]}")
        time.sleep(0.5)
    conn.commit()
    cur.close()
    conn.close()



