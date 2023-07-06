-- Создание таблицы вакансий
CREATE TABLE vacancies
(
	vacancy_id int PRIMARY KEY,
	vacancy_name varchar,
	url varchar,
	salary_from int,
	salary_to int,
	city varchar,
	address varchar,
	employer_name varchar,
	employer_id int,
	employment varchar,
	experience varchar,
	responsibility text
)

-- Создание таблицы работодателей
CREATE TABLE employers
(
	employer_id int PRIMARY KEY,
	employer_name varchar,
	open_vacancies int
)