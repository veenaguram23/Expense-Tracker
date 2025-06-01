from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    date = db.Column(db.String(10), nullable=False)

@app.route('/')
def index():
    expenses = Expense.query.all()
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        category = request.form['category']
        description = request.form['description']
        date = request.form['date']

        new_expense = Expense(
            amount=amount,
            category=category,
            description=description,
            date=date
        )
        db.session.add(new_expense)
        db.session.commit()
        return redirect('/')
    return render_template('add_expense.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
