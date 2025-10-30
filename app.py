from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---- Model ----
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    complete = db.Column(db.Boolean, default=False)

# ---- Create new database file ----
with app.app_context():
    db.create_all()
    print("✅ New database created at:", os.path.join(basedir, 'db.sqlite'))

@app.route('/')
def index():
    todo_list = Todo.query.all()
    return render_template('base.html', todo_list=todo_list)

# def add():
#     title = request.form.get("title")
#     new_todo = Todo(title=title, complete=False)
#     db.session.add(new_todo)
#     db.session.commit()
#     return redirect(url_for())

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    if title:
        new_todo = Todo(title=title)
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
