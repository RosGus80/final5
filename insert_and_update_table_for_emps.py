import psycopg2
from get_vacs import get_employer
from get_vacs import possible_ids
from psycopg2 import errors



def create_employer(emp_api_type):
    my_emp = {"id": emp_api_type['id'], "name": emp_api_type["name"],
    "vacancies": emp_api_type['open_vacancies']}
    return my_emp


def create_table(port, host, user, database, password):
    conn = psycopg2.connect(
        port=port,
        host=host,
        database=database,
        user=user,
        password=password
    )
    cur = conn.cursor()
    cur.execute("CREATE TABLE employers "
                "( "
                    "employer_id int PRIMARY KEY, "
                    "employer_name varchar, "
                    "open_vacancies int "
                ") ")
    conn.commit()
    cur.close()
    conn.close()


def insert_into_table(port, host, user, database, password):
    conn = psycopg2.connect(
        port=port,
        host=host,
        database=database,
        user=user,
        password=password
    )
    employers = []
    cur = conn.cursor()

    for emp_id in possible_ids.values():
        employer = get_employer(emp_id)
        output_employer = create_employer(employer)
        employers.append(output_employer)

    for employer in employers:
        try:
            cur.execute("TRUNCATE TABLE employers")
            cur.execute("INSERT INTO employers(employer_id, employer_name,"
                        "open_vacancies) VALUES (%s, %s, %s)",
                        [employer["id"], employer["name"], employer["vacancies"]])
        except psycopg2.errors.UniqueViolation:
            continue

    conn.commit()
    cur.close()
    conn.close()

