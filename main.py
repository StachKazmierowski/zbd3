import psycopg2
from psycopg2 import Error
from psycopg2 import extensions
import random
import time

SWEETS = ['Milka', 'Mieszanka studencka', 'Lindor', 'Prince polo', 'Delicje', 'Kinder niespodzianka', 'Jeżyki', 'Ferrero Rocher', 'Merci', 'Raphaello']


def get_paczka():
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
        print('Paczka numer ' ,paczka_pomocnicza_id)
        print(record)
        return paczka_pomocnicza_id, kraj, opis, slodycz, liczba
    except (Exception, Error) as error:
        print("Error ", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def remove_from_tmp_paczka(paczka_pomocnicza_id, cursor):
    SQL = "DELETE from paczka_pomocnicza WHERE id = %s;"
    data = (paczka_pomocnicza_id,)
    cursor.execute(SQL, data)

get_paczka()
