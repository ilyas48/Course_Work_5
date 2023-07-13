from headhunter import HeadHunter
from config import config
from dbmanager import DBManager

employers_id = [1740, 2180, 3529, 8550, 39305, 41862, 64174, 67611, 78638, 87021]


def main():
    print("Добро пожаловать!")
    print("Идет сборка данных, пожалуйста, подождите...")
    print("Может занять некоторое время!\n")
    for id_employer in employers_id:
        hh = HeadHunter(id_employer)
        params = config()
        db = DBManager('postgres', params)
        hh.get_vacancy(3)
        db.insert_data(hh.format_employer())
        db.get_insert_vacancies(hh.format_vacancies())

    while True:
        command = input(f""""База данных с вакансиями 10 работодателей с сайта hh.ru создана.\n" \
               "Возможные действия:\n" \
               "1. Список всех компаний и количества вакансий у каждой компании.\n" \
               "2. Список всех вакансий всех компаний.\n" \
               "3. Список средней зарплаты по вакансиям компаний.\n" \
               "4. Список всех вакансий, у которых зарплата выше средней по всем вакансиям.\n" \
               "5. Список всех вакансий, содержащих ключевое слово, например: "Python"\n""")
        # Обработка команды 1:Сортировка вакансий
        if command == '1':
            for line in db.get_companies_and_vacancies_count():
                print(f"Компания : {line[0]} \nКоличество вакансий : {line[1]},")
            # Обработка команды 2 :все вакансии
        elif command == '2':
            for row in db.get_all_vacancies():
                print(row)
        # Обработка команды 3: Вывод на экран средней зарплаты
        elif command == '3':
            print(db.get_avg_salary())
        # Обработка команды 4: Вывод вакансий с большей зарплатой, чем средняя
        elif command == '4':
            for row in db.get_vacancies_with_higher_salary():
                print(f"Средняя зарплата: {row}")
        elif command == '5':
            word = input('Введите слово\n')
            if db.get_vacancies_with_keyword(word):
                for row in db.get_vacancies_with_keyword(word):
                    print(f"Вакансия : {row}")
            else:
                print('Нет вакансий с таким словом')
        elif command.lower() == 'exit':
            db.close_conn()
            break
        else:
            print('Неверная команда')
    db.close_conn()


if __name__ == '__main__':
    main()
