from flask import Flask, render_template, g
import sqlite3

app = Flask(__name__)

DATABASE = "databases/todos.db"

def get_db():
	db = getattr(g, "_database", None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
	db.row_factory = sqlite3.Row
	return db

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, "_database", None)
	if db is not None:
		db.close()

todos = []
with app.app_context():
	todo = {}
	cur = get_db().cursor()
	cur.execute("SELECT (description) FROM todos;")
	todo["description"] = cur.fetchall()[0][0]
	cur.execute("SELECT (date) FROM todos;")
	todo["date"] = cur.fetchall()[0][0]
	cur.execute("SELECT (todo_id) FROM todos;")
	todo["todo_id"] = cur.fetchall()[0][0]

	todos.append(todo)

@app.route("/")
def index():
	return render_template("index.html", todos=todos)