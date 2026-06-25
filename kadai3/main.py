import sqlite3

class ProductDAO:
    def add(self, conn, name, price):
        sql = "INSERT INTO product(name, price) VALUES(?, ?)"
        conn.execute(sql, (name, price))
        conn.commit()

    def show(self, conn):
        sql = "SELECT * FROM product"
        cursor = conn.execute(sql)
        rows = cursor.fetchall()
        return rows

# 建表
conn = sqlite3.connect('kadai3/sample.db')
conn.execute('''\
    CREATE TABLE IF NOT EXISTS product(
        id    INTEGER PRIMARY KEY AUTOINCREMENT,
        name  STRING,
        price INT
    )\
''')
conn.commit()
conn.close()

# 主循环
with sqlite3.connect('kadai3/sample.db') as conn:
    dao = ProductDAO()

    while True:
        print("Menu(1.登録 2.一覧 3.終了)")
        n = input()

        if n == '1':
            name = input("Name:")
            price = int(input("Price:"))
            dao.add(conn, name, price)
            print("登録しました")

        if n == '2':
            rows = dao.show(conn)
            for row in rows:
                print(f"ID:{row[0]}  Name:{row[1]}  Price:{row[2]}")

        if n == '3':
            print("終了")
            break
