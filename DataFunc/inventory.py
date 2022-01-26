import sqlite3
import datetime as dt

time = dt.datetime.now()
date = time.strftime("%Y-%m-%d")
formatted_time = time.strftime("%d/%m/%Y %H:%M:%S")


class Inventory:

    def __init__(self):
        self.conn = sqlite3.connect("inventory.db")
        self.c = self.conn.cursor()
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS items (itemname TEXT PRIMARY KEY, amount INTEGER, price REAL) 
        """)
        self.conn.commit()

    def getitemamt(self, item):
        self.c.execute("""
        SELECT amount FROM items WHERE itemname = (?)
        """, (item, ))
        results = self.c.fetchall()
        cleanresults = [elem[0] for elem in results]
        return cleanresults

    def getitems(self):
        self.c.execute("""
        SELECT itemname FROM items 
        """)
        results = self.c.fetchall()
        cleanlist = [elem[0] for elem in results]
        sortedlst  = sorted(cleanlist)
        return sortedlst

    def checkifavailable(self, itemName):
        self.c.execute("""
        SELECT amount FROM items WHERE itemname = (?)
        """, (itemName,))
        results = self.c.fetchone()
        amount_left = results[0]
        return amount_left

    def getvalue(self, itemName):
        self.c.execute("""
        SELECT price FROM items WHERE itemname = (?)
        """, (itemName,))
        results = self.c.fetchone()
        price = results[0]
        return price

    def checkitemexists(self, itemName):
        self.c.execute("""
        SELECT price FROM items WHERE itemname = (?)
        """, (itemName,))
        results = self.c.fetchone()
        if results is None:
            return False
        else:
            return True

    def additem(self, itemName, amount, value):
        condition = self.checkitemexists(itemName=itemName)
        if condition is False:
            self.c.execute("""
            INSERT INTO items VALUES (?, ?, ?) 
            """, (itemName, amount, value))
            self.conn.commit()
            return True
        else:
            return False

    def deleteitem(self, itemName):
        condition = Inventory().checkitemexists(itemName=itemName)
        if condition is True:
            self.c.execute("""
            DELETE FROM items WHERE itemname = (?)
            """, (itemName,))
            self.conn.commit()
            return True
        else:
            return False

    def getcolumns(self):
        cursor = self.c.execute("""
        SELECT * FROM items 
        """)
        names = list(map(lambda x: x[0], cursor.description))
        return names

    def updatequantity(self, newamt, itemName):
        try:
            self.c.execute("""
            UPDATE items SET amount = (?) WHERE itemname = (?)
            """, (newamt, itemName))
            self.conn.commit()
        except Exception as e:
            print(e)

    def getmultipleitemprice(self, items):
        try:
            itemvaldict = {}
            for item in items:
                val = self.getvalue(item)
                itemvaldict[item] = val
            return itemvaldict
        except Exception as e:
            print(e)

    def getdetails(self, item):
        value = self.getvalue(item)
        amt = self.getitemamt(item)
        details = {
            'Value': value,
            'Amount': amt,
        }
        return details

    def savedetails(self, itemname, amt, value):
        try:
            self.c.execute("""
            UPDATE items SET amount = (?) WHERE itemname = (?)
            """, (amt, itemname))
            self.c.execute("""
            UPDATE items SET price = (?) WHERE itemname = (?)
            """, (value, itemname))
            self.conn.commit()

        except Exception as e:
            print(e)

    def delitem(self, itemname):
        try:
            self.c.execute("""
            DELETE FROM items WHERE itemname = (?)
            """, [itemname])
            self.conn.commit()
        except Exception as e:
            print(e)

    def amt_change_on_transaction(self, itemdict):
        try:
            for key, value in itemdict.items():
                storedamt = self.getitemamt(item=key)
                updatedamt = storedamt[0] - value
                self.updatequantity(newamt=updatedamt, itemName=key)
        except Exception as e:
            print(e)