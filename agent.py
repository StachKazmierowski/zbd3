import psycopg2
from psycopg2 import Error
from psycopg2 import extensions
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
        connection.set_isolation_level(extensions.ISOLATION_LEVEL_SERIALIZABLE)
        cursor = connection.cursor()
        # Print PostgreSQL details
        # Executing a SQL query
        cursor.execute("SELECT * FROM paczka_pomocnicza limit 1;")
        # Fetch result
        record = cursor.fetchone()
        paczka_pomocnicza_id = record[0]
        kraj = record[1]
        opis = record[2]
        slodycz = record[3]
        liczba = record[4]
        remove_from_tmp_paczka(paczka_pomocnicza_id, cursor)
        connection.commit()
        connection.set_isolation_level(extensions.ISOLATION_LEVEL_DEFAULT)
        print('Paczka numer ' ,paczka_pomocnicza_id)
        print(record)

        SQL = "INSERT into paczka(kraj, opis_obdarowanego) values (%s, %s) RETURNING id;"
        data = (kraj, opis)
        cursor.execute(SQL, data)
        paczka_id = cursor.fetchone()[0]

        print('pozostało ', check_amount(slodycz, cursor))
        if(check_amount(slodycz, cursor) < liczba):
            print('zmieniamy słodycz')
            print(slodycz)
            slodycz = ask_for_similar(slodycz, cursor)
            print(slodycz)

        if(check_amount(slodycz, cursor) < liczba):
            print('cofamy tranzakcje')
            connection.rollback()
        else:
            print('komitujemy tranzakcje')
            insert_into_paczka(slodycz, liczba, paczka_id, cursor)
            update_slodycz_w_magazynie(slodycz, liczba, cursor)
            connection.commit()


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

def check_amount(name, cursor):
    SQL = "SELECT ilosc_pozostalych FROM slodycz_w_magazynie WHERE nazwa=%s;"
    data = (name, )
    cursor.execute(SQL, data)
    record = cursor.fetchone()
    return record[0]

def run():
    # while(True):
    for i in range(400):
        singe_run()
        time.sleep(0.1)

run()



