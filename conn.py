#module for manage connection to the sqlite3 database
import sqlite3
import os


#change to the actual directory

os.chdir(os.path.dirname(os.path.realpath(__file__)))

class DB():
    """This class make calls to a sqlite3 database for save matches and errors"""
    def __init__(self):
        self.con = sqlite3.connect("database.db")
        #asignet cursor is necesary for sqlite call SELECT
        self.cur = self.con.cursor()
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

            self.con.execute("""create table Statistics (
                id_session integer primary key autoincrement,
                match integer ,
                not_found integer,
                error integer,
                critical_error integer   
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

    def added_std(self, upgrade, match = 0, not_found = 0,error = 0, critical_error = 0 ):
        """method for save sttistics info and make reports"""

        
        try:
            if upgrade == False:
                self.con.execute("insert into Statistics (match, not_found, error, critical_error) values (?,?,?,?)", \
                    (match, not_found,error,critical_error))
                self.con.commit()
            elif upgrade == True:

                self.con.execute("update Statistics SET match = ?, not_found = ?, error = ?, critical_error = ? ORDER BY  id_session DESC LIMIT 1", \
                    (match, not_found,error,critical_error))
                self.con.commit()
            return True
        except Exception as err:
            return (False, err)




