import psycopg2
from psycopg2 import Error
import random
import time

def singe_run():
    try:
        # Connect to an existing database
        connection = psycopg2.connect(user="stach",
                                      password="pol0pol9",
                                      host="localhost",
                                      port="5432",
                                      database="stach")
        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Print PostgreSQL details
        print("PostgreSQL server information")
        print(connection.get_dsn_parameters(), "\n")
        # Executing a SQL query
        cursor.execute("SELECT * FROM paczka_pomocnicza limit 1;")
        # Fetch result
        record = cursor.fetchone()
        print(record)
        paczka_pomocnicza_id = record[0]
        kraj = record[1]
        opis = record[2]
        slodycz = record[3]
        liczba = record[4]
        remove_from_tmp_paczka(paczka_pomocnicza_id, cursor)
        connection.commit()

        cursor.execute("BEGIN;")
        time.sleep(0.1)
        SQL = "INSERT into paczka(kraj, opis_obdarowanego) values (%s, %s) RETURNING id;"
        data = (record[1], record[2])
        cursor.execute(SQL, data)
        paczka_id = cursor.fetchone()[0]

        if(not check_if_is_enough(slodycz, liczba, cursor)):
            slodycz = ask_for_similar(slodycz, cursor)
        if(not check_if_is_enough(slodycz, liczba, cursor)):
            cursor.execute("ROLLBACK;")
        else:
            insert_into_paczka(slodycz, liczba, paczka_id, cursor)
            update_slodycz_w_magazynie(slodycz, liczba, cursor)
            cursor.execute("COMMIT;")

    except (Exception, Error) as error:
        print("Error ", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def remove_from_tmp_paczka(paczka_pomocnicza_id, cursor):
    SQL = "DELETE from paczka_pomocnicza WHERE id = %s;"
    data = (paczka_pomocnicza_id, )
    cursor.execute(SQL, data)

def update_slodycz_w_magazynie(name, amount, cursor):
    SQL = "UPDATE slodycz_w_magazynie SET ilosc_pozostalych = ilosc_pozostalych - %s WHERE nazwa = %s;"
    data = (amount, name)
    cursor.execute(SQL, data)

def ask_for_similar(name, cursor):
    SQL = "SELECT ktory_slodycz_jest_podobny FROM podobny_slodycz WHERE do_czego_slodycz_jest_podobny=%s ORDER BY podobienstwo LIMIT 1"
    data = (name, )
    cursor.execute(SQL, data)
    return cursor.fetchone()[0]

def insert_into_paczka(name, amount, package_id, cursor):
    SQL = "INSERT INTO slodycz_w_paczce values(%s, %s, %s)"
    data = (package_id, name, amount)
    cursor.execute(SQL, data)

def check_if_is_enough(name, amount, cursor):
    SQL = "SELECT ilosc_pozostalych FROM slodycz_w_magazynie WHERE nazwa=%s;"
    data = (name, )
    cursor.execute(SQL, data)
    return (amount < cursor.fetchone()[0])

def run():
    for i in range(100):
        singe_run()
        # time.sleep(2)

run()

