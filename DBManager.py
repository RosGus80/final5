import psycopg2


class DBManager:

    @staticmethod
    def get_companies_and_vacancies_count(port, host, user, database, password):
        conn = psycopg2.connect(
            port=port,
            host=host,
            database=database,
            user=user,
            password=password
        )
        cur = conn.cursor()
        output = []
        cur.execute("SELECT * FROM employers")
        employers = cur.fetchall()
        for employer in employers:
            output.append((employer[1], employer[2]))
        cur.close()
        conn.close()
        return output

    @staticmethod
    def get_all_vacancies(port, host, user, database, password):
        conn = psycopg2.connect(
            port=port,
            host=host,
            database=database,
            user=user,
            password=password
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM vacancies")
        a = cur.fetchall()
        cur.close()
        conn.close()
        return a

    @staticmethod
    def get_avg_salary(port, host, user, database, password):
        vacancies = DBManager.get_all_vacancies(port, host, user, database, password)
        sum_ = 0
        vacnum = len(vacancies)
        for vacancy in vacancies:
            if vacancy[4] is not None and vacancy[3] is not None:
                sum_ += (vacancy[3] + vacancy[4])/2
            elif vacancy[3] is not None:
                sum_ += vacancy[3]
            elif vacancy[4] is not None:
                sum_ += vacancy[4]
            else:
                vacnum - 1
        return sum_/vacnum

    @staticmethod
    def get_vacancies_with_higher_salary(port, host, user, database, password):
        avg = DBManager.get_avg_salary(port, host, user, database, password)
        conn = psycopg2.connect(
            port=port,
            host=host,
            database=database,
            user=user,
            password=password
        )
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM "
                    f"(SELECT * FROM "
                    f"(SELECT * FROM vacancies "
                    f"WHERE vacancies.salary_from is not null) as notnullsalary "
                    f"WHERE notnullsalary.salary_to is not null) as fullnotnull "
                    f"WHERE(fullnotnull.salary_from+fullnotnull.salary_to)/2 > {avg}")
        fullnotnull = cur.fetchall()

        cur.execute(f'SELECT * FROM '
                    f'(SELECT * FROM '
                    f'(SELECT * FROM vacancies '
                    f'WHERE vacancies.salary_from is not null) as notnullsalary '
                    f'WHERE notnullsalary.salary_to is null) as fullnotnull '
                    f'WHERE (fullnotnull.salary_from) > {avg}')
        notnullfrom = cur.fetchall()

        notnullto = cur.execute(f'SELECT * FROM '
                                f'(SELECT * FROM '
                                f'(SELECT * FROM vacancies '
                                f'WHERE vacancies.salary_to is not null) as notnullsalary '
                                f'WHERE notnullsalary.salary_from is null) as fullnotnull '
                                f'WHERE (fullnotnull.salary_to) > {avg}')

        if fullnotnull is not None:
            try:
                fullnotnull.extend(notnullfrom)
            except TypeError:
                pass
            try:
                fullnotnull.extend(notnullto)
            except TypeError:
                pass
            return fullnotnull
        elif notnullfrom is not None:
            try:
                notnullfrom.extend(notnullto)
            except TypeError:
                return notnullfrom
        else:
            return notnullto

    @staticmethod
    def get_vacancies_with_keyword(port, host, user, database, password, keyword: str):
        conn = psycopg2.connect(
            port=port,
            host=host,
            database=database,
            user=user,
            password=password
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM vacancies "
                    "WHERE vacancy_name "
                    f"LIKE '%{str(keyword)}%'")
        output = cur.fetchall()
        cur.close()
        conn.close()
        return output



class UserDBManager(DBManager):
    @staticmethod
    def User_CnV_count(port, host, user, database, password):
        data = DBManager.get_companies_and_vacancies_count(port, host, user, database, password)
        for company in data:
            print(f"Компания: {company[0]}", end="  ")
            print(f"Вакансий: {company[1]}", end="\n\n")

    @staticmethod
    def User_all_vacs(port, host, user, database, password):
        data = DBManager.get_all_vacancies(port, host, user, database, password)
        for vacancy in data:
            print(f"Компания: {vacancy[7]} Вакансия: {vacancy[1]} Зарплата: от {vacancy[3]} до {vacancy[4]} ссылка: {vacancy[2]}")

    @staticmethod
    def User_avg(port, host, user, database, password):
        avg = DBManager.get_avg_salary(port, host, user, database, password)
        print(f"Средняя зарплата среди найденных вакансий: {avg} рублей")

    @staticmethod
    def User_higher(port, host, user, database, password):
        data = DBManager.get_vacancies_with_higher_salary(port, host, user, database, password)
        for vacancy in data:
            print(
                f"Компания: {vacancy[7]} Вакансия: {vacancy[1]} Зарплата: от {vacancy[3]} до {vacancy[4]} ссылка: {vacancy[2]}")

    @staticmethod
    def User_keyword(port, host, user, database, password, keyword: str):
        data = DBManager.get_vacancies_with_keyword(port, host, user, database, password, keyword)
        for vacancy in data:
            print(f"Компания: {vacancy[7]} Вакансия: {vacancy[1]} Зарплата: от {vacancy[3]} до {vacancy[4]} ссылка: {vacancy[2]}")
