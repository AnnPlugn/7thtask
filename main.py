import math
import pymysql.cursors
import pandas as pd
import warnings
import os

import env
import universal

warnings.filterwarnings("ignore")
os.system('cls||clear')
name = input('Имя бд: ')
name_table = input('Имя таблицы: ')
def check_db() -> None:
    conn = pymysql.connect(host='localhost',
                             user=env.USER,
                             password=env.PASSWORD,
                             cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS `%s`" % name)

    conn = pymysql.connect(host='localhost',
                             user=env.USER,
                             password=env.PASSWORD,
                             database=name,
                             cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    print("База данных подключена")

    try:
        cursor.execute("SELECT * FROM %s" % name_table)
    except pymysql.err.MySQLError:
        with open('create_structure.sql', 'r') as sql_file:
            sql_script = sql_file.read()
            cursor.execute(sql_script % name_table)
            conn.commit()
            print("Скрипт SQL успешно выполнен")
    return

def save_result(operation, result):
    conn = pymysql.connect(host='localhost',
                             user=env.USER,
                             password=env.PASSWORD,
                             database=name,
                             cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    stri =  "INSERT INTO " + name_table + f" (operat, result) VALUES (%s, %s)", (operation, str(result))
    print(stri)
    cursor.execute("INSERT INTO " + name_table + f" (operat, result) VALUES (%s, %s)", (operation, str(result)))
    conn.commit()
    return
def save_db_to_xlsx():
    conn = pymysql.connect(host='localhost',
                            user=env.USER,
                            password=env.PASSWORD,
                            database=name,
                            cursorclass=pymysql.cursors.DictCursor)
    new_df = pd.read_sql("SELECT * FROM " + name_table, conn)
    new_df.to_csv("out.txt")
    return

def print_db():
    conn = pymysql.connect(host='localhost',
                            user=env.USER,
                            password=env.PASSWORD,
                            database=name,
                            cursorclass=pymysql.cursors.DictCursor)
    new_df = pd.read_sql_query(f"SELECT *  FROM {name_table}" , conn)
    print(new_df)
    return

def print_exel():
    name = input('Путь до файла и название: ')
    new_df = pd.read_csv(name)
    print(new_df)
    return

radius = int(input('Радиус равен: '))
def circle_diameter():
    print('D = 2 * radius')
    diameter = math.pi * (radius ** 2)
    print('Диаметр круга равен: ', diameter)
    save_result('D = 2 * radius', diameter)
    return
def circle_area():
    print('S = pi * radius^2')
    area = math.pi * (radius ** 2)
    print('Площадь круга равна: ', area)
    save_result('S = pi * radius^2', area)
    return
def circle_circumference():
    print('C = 2 * pi * radius')
    circumference = 2 * math.pi * radius
    print('Длина окружности круга равна: ', circumference)
    save_result('C = 2 * pi * radius', circumference)
    return
def main():
    run = True
    commands = """==========================================================================
1. Создать таблицу и БД и ввести радиус круга, результат сохранить в MySQL.
2. Найти площадь круга, результат сохранить в MySQL.
3. Найти длину окружности, результат сохранить в MySQL.
4. Найти диаметр круга, результат сохранить в MySQL.  
5. Все результаты вывести на экран из MySQL.
6. Сохранить все данные из MySQL в Excel.
7. Вывести все данные на экран из Excel.
8. Завершить"""
    while run:
        run = universal.uni(commands,
                      check_db,
                      circle_area, circle_circumference, circle_diameter,
                      print_db, save_db_to_xlsx, print_exel)
    return

if __name__ == '__main__':
    main()

