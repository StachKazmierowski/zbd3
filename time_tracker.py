import psycopg2
from psycopg2 import Error
import random
import time

def check_paczka():
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


        SQL = "SELECT count(*) FROM paczka;"
        cursor.execute(SQL)
        return cursor.fetchone()[0]
    except (Exception, Error) as error:
        print("Error ", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

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

def run():
    f = open("results", 'a')
    start = time.time()
    while(singe_run()):
        time.sleep(0.5)
    end = time.time()
    print(end-start)
    f.write('time: ' + str(end-start) + '\n')
    f.write('udane paczki: ' + check_paczka() + '\n')
    f.close()

run()
