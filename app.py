from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasker.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue with your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=tasks )

@app.route('/remove/<int:id>')

def remove(id):
    task_to_remove = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_remove)
        db.session.commit()
        return redirect('/')
    except:
        return 'Problem removing task'

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Problem editing task'

    else:
        return render_template('edit.html', task=task)

@app.route('/templates/doc')
def doc():
    return render_template('doc.html')

if __name__ == "__main__":
    app.run(debug=True)

# >>> from app import app, db
# >>> app.app_context().push()
# >>> db.create_all()
# it should be created under instance directory after those commands.