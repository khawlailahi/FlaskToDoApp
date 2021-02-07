from flask import Flask , render_template, url_for, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)

#relative path for db
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///test.db'

#intializing db 
db = SQLAlchemy(app)

#Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content =db.Column(db.String(200), nullable = False)
    completed =db.Column(db.Integer, default = 0)
    date_created =db.Column(db.DateTime, default = datetime.utcnow)

#everytime we create an element this function will return the task and the id
    def __repr__ (self):
        return '<Task %r>' % self.id



#index route so we dont get 404 when we open page
@app.route('/', methods=['POST','GET'])
#defining function for that route
def index():
    if request.method == 'POST':
        task_content = request.form ['content']
        new_task = Todo(content = task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "there was a problem with saving task"
    else:
        tasks= Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)
   
@app.route('/delete/<int:id>')
def delete (id):
    to_delete = Todo.query.get_or_404(id)
    print(id)
    try:
        db.session.delete(to_delete)
        db.session.commit()
        return redirect('/')

    except :
        return "there was problem in deleting the task"
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update (id):
    task = Todo.query.get_or_404(id)

    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
             return 'there was a problem updating the task'

    else:
       return render_template('update.html', task = task)



    
if __name__ == "__main__":
    app.run(debug=True)
