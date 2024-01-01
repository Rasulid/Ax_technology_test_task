from core.config import *
import psycopg2.extras
from api.auth.auth import get_password_hash

conn = None

try:
    with psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        port=DB_PORT,
        password=DB_PASSWORD
    ) as conn:
        with conn.cursor() as cur:
            check_query = """
            SELECT 1 FROM "user" WHERE username = %s OR email = %s;
            """
            cur.execute(check_query, ("admin", "admin@admin.com"))
            if cur.fetchone() is None:
                insert_script = """
                INSERT INTO "user" (username, email, hashed_password, is_active, 
                                    is_staff, is_superuser, is_moderator)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
                """
                insert_values = ("admin", "admin@admin.com", str(get_password_hash("root")), True, True, True, True)

                cur.execute(insert_script, insert_values)
                user_id = cur.fetchone()[0]
                print("Создан пользователь с ID:", user_id)
            else:
                print("Пользователь с таким username или email уже существует.")
except Exception as err:
    print("Ошибка при работе с PostgreSQL:", err)
finally:
    if conn is not None:
        conn.close()
        print("Соединение с PostgreSQL закрыто")
