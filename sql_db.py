import mysql.connector as mysql
from config import HOST, PORT, USER, PASSWORD, DATABASE

async def db_connect() -> None:
    global db, cur
    db = mysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, database=DATABASE)
    cur = db.cursor()
    db.commit()

async def get_data():
    cur.execute("""SELECT firstname, DATE_FORMAT(end_date, '%d.%m.%Y') AS end_date FROM EDS WHERE end_date 
    BETWEEN CURDATE() AND CURDATE() + INTERVAL 31 DAY ORDER BY -end_date DESC""")
    rows = cur.fetchall()
    return rows
