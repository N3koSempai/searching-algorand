#module for manage connection to the sqlite3 database
import sqlite3
import os


#change to the actual directory

os.chdir(os.path.dirname(os.path.realpath(__file__)))

class DB():
    """This class make calls to a sqlite3 database for save matches and errors"""
    def __init__(self):
        self.con = sqlite3.connect("database.db")

    def start(self):
        """Method for initialize the database and the tables"""
        try:
            self.con.execute("""create table Match (
                id_match integer primary key autoincrement,
                status_code integer,
                acuracy text,
                private text,
                public text,
                amount integer,
                assets integer
            )""")
        
            self.con.execute("""create table Error (
                id_err integer primary key autoincrement,
                status_code integer,
                private text,
                public text,
                message text
            )""")

            return True
        except sqlite3.OperationalError:
            return True
                
        except Exception as err:
            return False
    
    def added_match(self, status_code, acuracy, private, public, amount = 0, assets = 0):
        """method for insert data into the tables"""
        try:
            self.con.execute("insert into Match (status_code, acuracy, private, public, amount, assets) values (?,?,?,?,?,?)", \
                (status_code, acuracy, private, public, amount, assets))
            self.con.commit()
            return True
        except Exception as err:
            return False
    
    def added_error(self, status_code, message , private = 'not have', public = 'not have' ):
        """method for save a logs of errors"""
        try:
            self.con.execute("insert into Error (status_code,  private, public, message) values (?,?,?,?)", \
                (status_code,  private, public, message))
            self.con.commit()
            return True
        except Exception as err:
            return False


