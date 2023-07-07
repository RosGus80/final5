import psycopg2
from get_vacs import get_vacs
from get_vacs import possible_ids
from psycopg2 import errors


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


def create_table(port, host, user, database, password):
    conn = psycopg2.connect(
        port=port,
        host=host,
        database=database,
        user=user,
        password=password
    )
    cur = conn.cursor()
    cur.execute("CREATE TABLE vacancies "
                "( "
                "vacancy_id int PRIMARY KEY, "
                "vacancy_name varchar, "
                "url varchar, "
                "salary_from int, "
                "salary_to int, "
                "city varchar, "
                "address varchar, "
                "employer_name varchar, "
                "employer_id int, "
                "employment varchar, "
                "experience varchar, "
                "responsibility text "
                ") ")
    conn.commit()
    cur.close()
    conn.close()


def insert_into_table(port, host, user, database, password):
    """Метод для получения вакансий от выбранных работодателей через апи и добавления
    их в таблицу vacancies, пропуская те, которые в ней уже есть"""
    conn = psycopg2.connect(
        port=port,
        host=host,
        database=database,
        user=user,
        password=password
    )
    vacancies = []
    cur = conn.cursor()

    for emp_id in possible_ids.values():
        emp_vacs = get_vacs(emp_id)['items']
        for vacancy in emp_vacs:
            vacancies.append(create_vacancy(vacancy))

    for vacancy in vacancies:
        try:
            cur.execute("TRUNCATE TABLE vacancies")
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


