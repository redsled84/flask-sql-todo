from flask import Flask, render_template, g, request
from time import localtime, strftime
import sqlite3
import uuid

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
def load_todos():
	with app.app_context():
		todo = {}
		cur = get_db().cursor()
		cur.execute("SELECT * FROM todos;")
		temp_todos = cur.fetchall()

		for x in xrange(len(temp_todos)):
			todo = {}

			todo["todo_id"] = temp_todos[x][0]
			todo["description"] = temp_todos[x][1]
			todo["date"] = temp_todos[x][2]

			todos.append(todo)

load_todos()

def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1

@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "POST":
		if "add-button" in request.form and len(request.form["todo-description"]) > 0:
			db = get_db()
			cur = db.cursor()
			todo_uuid = uuid.uuid4()
			todo_description = request.form["todo-description"]
			todo_date = strftime("%m/%d/%y", localtime())
			# print(todo_uuid.hex, todo_description, todo_date)
			with app.app_context():
				cur.execute("INSERT OR IGNORE INTO todos (todo_id, description, date) VALUES (?, ?, ?) ", \
					(todo_uuid.hex, todo_description, todo_date))
				db.commit()
				todos.append({"todo_id": todo_uuid.hex, "description": todo_description, "date": todo_date})
			# load_todos()
		if "delete-button" in request.form:
			db = get_db()
			cur = db.cursor()
			with app.app_context():
				cur.execute("DELETE FROM todos WHERE todo_id = ?;", (request.form["todo-id"],))
				db.commit()
				delete_index = find(todos, "todo_id", request.form["todo-id"])
				if delete_index >= 0:
					todos.remove(todos[delete_index])


	return render_template("index.html", todos=todos)