from flask import Flask, render_template, request, redirect, url_for, flash
from psycopg import connect
from psycopg.rows import dict_row
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://taskuser:taskpass@localhost:5432/taskmanager"
)


def get_db_connection():
    return connect(DATABASE_URL, row_factory=dict_row)


def initialize_database():
    with get_db_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(120) NOT NULL,
                description TEXT DEFAULT '',
                completed BOOLEAN NOT NULL DEFAULT FALSE,
                created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)


@app.route("/")
def index():
    with get_db_connection() as connection:
        tasks = connection.execute(
            "SELECT * FROM tasks ORDER BY completed ASC, id DESC"
        ).fetchall()
    return render_template("index.html", tasks=tasks)


@app.route("/tasks", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()

    if not title:
        flash("Please enter a task title.", "error")
        return redirect(url_for("index"))

    with get_db_connection() as connection:
        connection.execute(
            "INSERT INTO tasks (title, description) VALUES (%s, %s)",
            (title, description),
        )

    flash("Task added successfully.", "success")
    return redirect(url_for("index"))


@app.route("/tasks/<int:task_id>/toggle", methods=["POST"])
def toggle_task(task_id):
    with get_db_connection() as connection:
        connection.execute(
            "UPDATE tasks SET completed = NOT completed WHERE id = %s",
            (task_id,),
        )
    return redirect(url_for("index"))


@app.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete_task(task_id):
    with get_db_connection() as connection:
        connection.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    flash("Task deleted.", "success")
    return redirect(url_for("index"))


@app.route("/health")
def health():
    try:
        with get_db_connection() as connection:
            connection.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}, 200
    except Exception:
        return {"status": "unhealthy", "database": "disconnected"}, 503


@app.route("/about")
def about():
    return render_template("about.html")


initialize_database()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
