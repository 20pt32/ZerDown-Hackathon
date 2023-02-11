import psycopg2
connection = psycopg2.connect(
    user = "postgres",
    password = "sivapriya",
    host = "127.0.0.1",
    database="postgres")
cursor=connection.cursor()
cursor.execute("Select * from brokerage")
cursor.fetchall()