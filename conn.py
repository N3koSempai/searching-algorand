#module for manage connection to the postgresql database
import psycopg2
import os

host = os.environ.get("DATABASE_URL")




class Database():
    """Class for manage the database I/O"""

    def __init__(self, host):
        self.host = host


    def create_table(self):
        """create the database if not exist"""

        conexion = psycopg2.connect(self.host)
        cursor = conexion.cursor()
        try:
            cursor.execute('CREATE TABLE match (ID SERIAL PRIMARY KEY, PRIVATE_KEY VARCHAR(100), PUBLIC_KEY VARCHAR(100), ITER INTEGER);')
            cursor.execute('CREATE TABLE error (ID SERIAL PRIMARY KEY, PRIVATE_KEY VARCHAR(100), PUBLIC_KEY VARCHAR(100), ITER INTEGER, ERRORMESSAGE VARCHAR(50));')

        except psycopg2.ProgrammingError:
            print("the table exist")
            
    

