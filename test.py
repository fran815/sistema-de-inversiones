import mysql.connector
from datetime import datetime

fa = datetime.now()

db = mysql.connector.connect(
    host = 'bj7l3xtoftrlpschwtah-mysql.services.clever-cloud.com',
    user = 'u28owjanx91fbbgg',
    database = 'bj7l3xtoftrlpschwtah',
    password = 'Hib9YhOmKLh3xa3MMPMZ',
    port = 3306
)

sql = """CREATE TABLE dividendos (
id INTEGER AUTO_INCREMENT PRIMARY KEY,
fecha DATE NOT NULL,
fibra VARCHAR(50) NOT NULL,
titulos INTEGER,
dividendo DECIMAL(10,4),
impuesto DECIMAL(10,2),
ganancia DECIMAL(10,2)
);
"""

# cur = db.cursor()
# cur.execute("SELECT * FROM inversiones")
# data = cur.fetchall()

# print (data)
# cur.execute(sql)
# db.commit()

# cur.execute("SHOW COLUMNS FROM dividendos")
# data = cur.fetchall()

# for x in data:
#     print (x)