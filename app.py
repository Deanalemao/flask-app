import os
import psycopg2
from flask import Flask

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("POSTGRES_DB", "devopsdb")
DB_USER = os.getenv("POSTGRES_USER", "devopsuser")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "devopspassword")


@app.route("/")
def home():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

        cursor = conn.cursor()

        cursor.execute("SELECT version();")

        db_version = cursor.fetchone()

        cursor.close()
        conn.close()

        return f"Flask connected to PostgreSQL!<br><br>{db_version[0]}"

    except Exception as e:
        return f"Database connection failed: {str(e)}", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
