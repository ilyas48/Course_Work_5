import psycopg2


class DBManager:
    """
    Класс для создания и наполнения базы данных, а также взаимодействия при помощи СУБД Postgres.
    """

    def __init__(self):
        """
        Конструктор класса
        """
        self.conn = psycopg2.connect(host='localhost',
                                     database='hhbase',
                                     user='postgres',
                                     password='25041988')

    def insert_data(self, temp_dict):
        """
        Метод для заполнения базы данных
        """
        with self.conn.cursor() as cur:
            cur.execute("INSERT INTO employers VALUES (%s,%s,%s)", (temp_dict['id_employer'],
                                                                    temp_dict['employer_name'],
                                                                    temp_dict['industries']))
            cur.execute("SELECT * FROM employers")
            rows = cur.fetchall()
            for row in rows:
                print(row)
        self.conn.commit()

    def get_insert_vacancies(self, vacancies_list):
        """
        Записывает информацию о компании в БД
        """
        with self.conn.cursor() as cur:
            for row in vacancies_list:
                cur.execute("INSERT INTO vacancies VALUES (%s,%s,%s,%s,%s,%s)", (row['title'],
                                                                                 row['salary_from'],
                                                                                 row['salary_to'],
                                                                                 row['requirement'],
                                                                                 row['link'],
                                                                                 row['employer_name']))
            cur.execute("SELECT * FROM vacancies")
            rows = cur.fetchall()
            for row in rows:
                print(row)
        self.conn.commit()

    def get_companies_and_vacancies_count(self):
        """
        Выводит количество вакансий у компаний
        """
        with self.conn.cursor() as cur:
            cur.execute("""SELECT employers.employer_name, COUNT(vacancies.title) FROM employers LEFT JOIN vacancies 
            ON employers.employer_name = vacancies.employer_name GROUP BY employers.employer_name""")
            result = cur.fetchall()
        return result

    def get_all_vacancies(self):
        """
        Функция выводит информацию о вакансии
        """
        with self.conn.cursor() as cur:
            cur.execute("""SELECT employer_name,title, salary_from, salary_to,url 
             FROM vacancies """)
            result = cur.fetchall()

        return result

    def get_avg_salary(self):
        """
        Метод для получения средней зарплаты по вакансиям
        """
        with self.conn.cursor() as cur:
            cur.execute("""SELECT CAST((AVG(salary_from)+AVG(salary_to))/2 AS int)  FROM vacancies """)
            result = cur.fetchone()
        return result[0]

    def get_vacancies_with_higher_salary(self):
        """
        Метод для получения списка всех вакансий, у которых зарплата выше средней по всем вакансиям
        """
        with self.conn.cursor() as cur:
            avg_salary = self.get_avg_salary()
            cur.execute(
                f"""SELECT title, salary_from, salary_to
                FROM vacancies WHERE CAST(salary_from AS numeric) > {avg_salary}
                 OR CAST(salary_from AS numeric) > {avg_salary}""")
            result = cur.fetchall()
        return result

    def get_vacancies_with_keyword(self, word):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”.
        """
        with self.conn.cursor() as cur:
            cur.execute(
                f"SELECT * FROM vacancies WHERE title LIKE '%{word.title()}%' "
                f"OR title LIKE'%{word.lower()}%' "
                f"OR title LIKE '%{word.upper()}%'")
            result = cur.fetchall()
        return result

    def close_conn(self):
        """
        Функция закрытия соединения с бд
        """
        self.conn.close()
