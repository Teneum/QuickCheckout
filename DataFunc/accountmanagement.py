import sqlite3
import datetime as dt
import hashlib
from misc import encrypthash

time = dt.datetime.now()
date = time.strftime("%Y-%m-%d")
formatted_time = time.strftime("%d/%m/%Y %H:%M:%S")


class UserData:

    def __init__(self):
        self.conn = sqlite3.connect("accounts.db")
        self.conn.execute("PRAGMA foreign_keys = 1")

        self.c = self.conn.cursor()
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS users (employeeID TEXT PRIMARY KEY, name TEXT, accountType TEXT,
                                              userpassword TEXT, joinDate TEXT, accountCompleted BLOB) 
        """)
        self.conn.commit()
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS userdata (name, accountID, nationality TEXT, gender TEXT,
            contactNumber TEXT, contactAddress TEXT, age TEXT, 
            FOREIGN KEY (accountID) REFERENCES users(employeeID))
        """)
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS moderationdata (accountID, totalHours7D REAL, salary REAL, performance 
            BLOB, notes TEXT, 
            FOREIGN KEY (accountID) REFERENCES users(employeeID))
        """)
        self.conn.commit()

    def close(self):
        self.conn.close()

    def set_mod_details(self, employeeID, hours7D=0, salary=0, performance='Not Set', notes='Not Set'):
        self.c.execute("""
        SELECT * FROM moderationdata WHERE accountID = (?)
        """, (employeeID, ))
        results = self.c.fetchall()
        if len(results) == 0:
            self.c.execute("""
            INSERT INTO moderationdata VALUES(?, ?, ?, ?, ?)
            """, (employeeID, hours7D, salary, performance, notes))
            self.conn.commit()
        else:
            self.c.execute("""
            UPDATE moderationdata SET totalHours7D = (?), salary = (?), performance = (?), notes = (?) WHERE accountID
            = (?)
            """, [hours7D, salary, performance, notes, employeeID])
            self.conn.commit()

    def get_mod_details(self, employeeID):
        try:
            self.c.execute("""
            SELECT * FROM moderationdata WHERE accountID = (?)
            """, [employeeID])
            results = self.c.fetchall()
            if len(results) == 0:
                self.set_mod_details(employeeID=employeeID)
            self.c.execute("""
            SELECT * FROM moderationdata WHERE accountID = (?)
            """, [employeeID])
            results = self.c.fetchall()
            return results[0]
        except Exception as e:
            print(e)

    def getempdetails(self, employeeID):
        try:
            self.c.execute("""
            SELECT * FROM userdata WHERE accountID = (?)
            """, [employeeID])
            results = self.c.fetchall()
            columns = ['Name', 'ID', 'Nationality', 'Gender', 'Contact Number', 'Address', 'Age']
            if len(results) == 0:
                return None
            else:
                returndict = dict(zip(columns, results[0]))
                return returndict
        except Exception as e:
            print(e)

    def createUser(self, userID: str, username: str, accountType: str, password: str, acccompl):
        """
        :param acccompl: The parameter to make sure account is completed
        :param userID: Enter employee's identification number
        :param username: Enter employee's name
        :param accountType: If account type is Admin or Regular
        :param password: Enter employee's password
        :return:
        """
        encrypted_password = encrypthash(password)
        self.c.execute("""
        SELECT name FROM users WHERE employeeID = (?)
        """, [userID])
        results = self.c.fetchall()
        if len(results) == 0:
            self.c.execute("""
            INSERT INTO users VALUES(?, ?, ?, ?, ?, ?)
            """, (userID, username, accountType, encrypted_password, date, acccompl))
            self.conn.commit()
            self.set_mod_details(employeeID=userID)
            self.registration(userID=userID)
            return "User Created"
        else:
            return "User Exists"

    def login(self, userID: str, password: str):
        """
        :param userID: Employee's Identification Number
        :param password: Employee's Personal Password
        :return:
        """
        encryptedpass = encrypthash(password)
        self.c.execute("""
        SELECT userpassword FROM users WHERE employeeID = (?)
        """, [userID])
        self.conn.commit()
        results = self.c.fetchall()
        if len(results) == 0:
            return "None"
        else:
            if encryptedpass in str(results[0]):
                return "Found"
            else:
                return "None"

    def check_if_account_complete(self, userID: str):
        """
        :param userID: Enter UserID to identify user
        :return: Returns True or False
        """
        self.c.execute("""
        SELECT accountCompleted FROM users WHERE employeeID = (?)
        """, [userID])
        self.conn.commit()
        results = self.c.fetchall()
        if len(results) == 0:
            return "None"
        else:
            return results

    def registration(self, userID, name='Null', nationality='Null', gender='Null', contactNumber='Null', contactAddress='Null',
                     age='Null'):
        """
        :param nationality: Enter user's nationality
        :param gender: User's Gender
        :param contactNumber: User's phone number
        :param contactAddress: User's Email Address
        :param age: User's Age
        :param password: User's new password
        :return:
        """
        self.c.execute("""
        INSERT INTO userdata VALUES(?, ?, ?, ?, ?, ?, ?)
        """, (name, userID, nationality, gender, contactNumber, contactAddress, age))
        self.conn.commit()
        self.c.execute("""
        UPDATE users set name = (?) WHERE employeeID = (?)
        """, (name, userID))
        self.conn.commit()

    def update_acc_complete(self, ID):
        self.c.execute("""
        UPDATE users set accountCompleted = (?) WHERE employeeID = (?)
        """, (True, ID))
        self.conn.commit()

    def update_password(self, ID, password):
        encrypted_password = encrypthash(password)
        self.c.execute("""
        UPDATE users set userpassword = (?) WHERE employeeID = (?)
        """, (encrypted_password, ID))
        self.conn.commit()

    def checkadmin(self, userid):
        self.c.execute("""
        SELECT accountType FROM users WHERE employeeID = (?)
        """, [userid])
        results = self.c.fetchall()
        if results[0][0].lower() == 'admin':
            return True
        else:
            return False

    def admin_list(self):
        self.c.execute("""
        SELECT employeeID FROM users WHERE accountType = 'admin'
        """)
        results = self.c.fetchall()
        return results

    def emplist(self):
        """
        Returns a list of employee names.
        """
        self.c.execute("""
        SELECT name FROM users
        """)
        results = self.c.fetchall()
        return results

    def emplistwithid(self):
        self.c.execute("""
        SELECT name, employeeID FROM users
        """)
        results = self.c.fetchall()
        cleanlst = [
            str(elem[0]) + f" / {elem[1]}" for elem in results
        ]
        return cleanlst

    def delete_account(self, employeeID):
        self.c.execute("""
        DELETE FROM moderationdata WHERE accountID = (?)
        """, (employeeID, ))
        self.c.execute("""
        DELETE FROM userdata WHERE accountID = (?)
        """, (employeeID,))
        self.c.execute("""
        DELETE FROM users WHERE employeeID = (?)
        """, (employeeID,))
        self.conn.commit()

    def check_account_exist(self, employeeID):
        self.c.execute("""
        SELECT * FROM users WHERE employeeID = (?)
        """, (employeeID, ))
        results = self.c.fetchall()
        if len(results) == 0:
            return False
        else:
            return True