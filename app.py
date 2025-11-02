from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# ✅ DB Path
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ✅ Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    complete = db.Column(db.Boolean, default=False)

# ✅ Create DB
with app.app_context():
    db.create_all()

# ✅ Get all Tasks
@app.route('/')
def index():
    todo_list = Todo.query.all()
    return render_template('base.html', todo_list=todo_list)

# ✅ Add Task
@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    if title:
        new_todo = Todo(title=title)
        db.session.add(new_todo)
        try:
            db.session.commit()
        except Exception as e:
            print("database error", e)
            db.session.rollback()
    return redirect(url_for('index'))

# ✅ Update Task
@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = Todo.query.get(todo_id)
    todo.complete = not todo.complete
    try:
        db.session.commit()
    except Exception as e:
        print("database error", e)
        db.session.rollback()
    return redirect(url_for('index'))

# ✅ Delete Task
@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    db.session.delete(todo)
    try:
        db.session.commit()
    except Exception as e:
        print("database error", e)
        db.session.rollback()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
