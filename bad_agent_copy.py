import psycopg2
from psycopg2 import Error
from psycopg2 import extensions
import random
import time
from main import get_paczka
# from time_tracker import still_running

def single_run():
    try:
        # Connect to an existing database
        connection = psycopg2.connect(user="stach",
                                      password="pol0pol9",
                                      host="localhost",
                                      port="5432",
                                      database="stach")
        # Create a cursor to perform database operations
        paczka_pomocnicza_id, kraj, opis, slodycz, liczba = get_paczka()
        print('Paczka numer ' ,paczka_pomocnicza_id)
        print(paczka_pomocnicza_id, kraj, opis, slodycz, liczba)
        connection.set_isolation_level(extensions.ISOLATION_LEVEL_READ_UNCOMMITTED)
        cursor = connection.cursor()


        SQL = "INSERT into paczka(kraj, opis_obdarowanego) values (%s, %s) RETURNING id;"
        data = (kraj, opis)
        cursor.execute(SQL, data)
        paczka_id = cursor.fetchone()[0]

        print('pozostało ', check_amount(slodycz, cursor))
        robimy = False
        if(check_amount(slodycz, cursor) < liczba):
            similar = ask_for_similar_many(slodycz, cursor)

            for i in range(9):
                if (check_amount(similar[i], cursor) >= liczba):
                    print('zmieniamy słodycz')
                    slodycz = similar[i]
                    robimy = True
                    break
                if(i == 9):
                    connection.rollback()
                    print('cofamy transakcje')
        else:
            robimy = True

        if(robimy):
            print('komitujemy transkcje')
            insert_into_paczka(slodycz, liczba, paczka_id, cursor)
            update_slodycz_w_magazynie(slodycz, liczba, cursor)
            time.sleep(1)
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

def ask_for_similar_many(name, cursor):
    SQL = "SELECT ktory_slodycz_jest_podobny FROM podobny_slodycz WHERE do_czego_slodycz_jest_podobny=%s ORDER BY podobienstwo"
    data = (name, )
    cursor.execute(SQL, data)
    return cursor.fetchall()

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

def still_running():
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


        SQL = "SELECT sum(ilosc_pozostalych) FROM slodycz_w_magazynie;"
        cursor.execute(SQL)
        if(cursor.fetchone()[0] < 1):
            return False

        SQL = "SELECT count(*) FROM paczka_pomocnicza;"
        cursor.execute(SQL)
        if (cursor.fetchone()[0] < 1):
            return False
        return True
    except (Exception, Error) as error:
        print("Error ", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
#
def run():
    while(still_running()):
        # print(check_paczka())
        single_run()
        time.sleep(0.1)



run()
# single_run()
# print(get_paczka())
