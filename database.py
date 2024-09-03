import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.curr = self.conn.cursor()  # Make sure you're using self.curr here
        self.curr.execute(
            "CREATE TABLE IF NOT EXISTS expense_record (item_name TEXT, item_price REAL, purchase_date TEXT)"
        )
        self.conn.commit()

    def insertRecord(self, item_name, item_price, purchase_date):
        self.curr.execute("INSERT INTO expense_record (item_name, item_price, purchase_date) VALUES (?, ?, ?)",
                          (item_name, item_price, purchase_date))
        self.conn.commit()

    def fetchRecord(self, query):
        self.curr.execute(query)
        return self.curr.fetchall()

    def updateRecord(self, item_name, item_price, purchase_date, rowid):
        self.curr.execute("UPDATE expense_record SET item_name = ?, item_price = ?, purchase_date = ? WHERE rowid = ?",
                          (item_name, item_price, purchase_date, rowid))
        self.conn.commit()

    def removeRecord(self, rowid):
        self.curr.execute("DELETE FROM expense_record WHERE rowid = ?", (rowid,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
