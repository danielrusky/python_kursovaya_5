import os


from utils.utils import *
from config import config

companies = {
    1776381: "Apple",
    2324020: "Google",
    864086: "Amazon",
    2723603: "Microsoft",
    3407499: "Tencent",
    80660: "Макдоналдс",
    1008541: "VISA",
    2970204: "Meta",
    4759060: "Alibaba",
    5569859: "Louis Vuitton"
}
DB_NAME = 'vacancies'
params = config()
script_file = os.path.join('scripts', 'queries.sql')

if __name__ == '__main__':
    list_ = get_vacancies(companies)
    create_db(DB_NAME, params)
    print(colorama.Fore.BLUE + 'База данных создана...' + colorama.Fore.RESET)
    params.update({'dbname': DB_NAME})
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                create_tables(cur, script_file)
                print(colorama.Fore.BLUE + f"Успешно созданы таблицы {DB_NAME} в БД..." + colorama.Fore.RESET)

                fill_table_companies(cur, companies)
                print(colorama.Fore.BLUE + "Заполнена таблица companies..." + colorama.Fore.RESET)

                fill_table_vacancies(cur, list_)
                print(colorama.Fore.BLUE + "Заполнена таблица vacancies..." + colorama.Fore.RESET)

                add_foreign_key(cur)
                print(colorama.Fore.BLUE + "Связывание таблиц успешно..." + colorama.Fore.RESET)

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    user_interaction(params)
