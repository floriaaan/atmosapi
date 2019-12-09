import pymysql


atmosDB = pymysql.connect(
    host="localhost",
    user="atmosfr",
    passwd="atmosfr"
)

dbCursor = atmosDB.cursor(buffered=True)
dbCursor.execute("CREATE DATABASE atmosfr")

dbCursor.execute("SHOW DATABASES")

for x in dbCursor:
    print(x)