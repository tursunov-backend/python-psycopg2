import psycopg2
from bot.config import settings


class DB:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASS,
            dbname=settings.DB_NAME,
        )
        self.cur = self.conn.cursor()

    def add_user(self, name, phone_number):
        query = """
        INSERT INTO users (name, phone_number)
        VALUES (%s, %s)
        RETURNING id
        """
        self.cur.execute(query, (name, phone_number))
        user_id = self.cur.fetchone()[0]
        self.conn.commit()
        return user_id

    def add_location(self, user_id, latitude, longitude):
        query = """
        INSERT INTO locations (user_id, latitude, longitude)
        VALUES (%s, %s, %s)
        """
        self.cur.execute(query, (user_id, latitude, longitude))
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()