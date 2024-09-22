from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Database model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Boolean, default=False)


# Home page
@app.route('/')
def index():
    tasks = Todo.query.all()
    return render_template('index.html', tasks=tasks)


# Add a new task
@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    new_task = Todo(task=task)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/update/<int:task_id>')
def update(task_id):
    print(f"Updating task with ID: {task_id}")
    task = Todo.query.get(task_id)
    if task:
        task.complete = not task.complete
        db.session.commit()
        print(f"Task updated: {task}")
    else:
        print("Task not found")
    return redirect(url_for('index', update=True))




# Delete a task
@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = Todo.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
