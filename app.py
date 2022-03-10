import os
from forms import AddSaleForm
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pymysql
app = Flask(__name__)

# Key for Forms
app.config['SECRET_KEY'] = 'mysecretkey'

############################################

# SQL DATABASE AND MODELS

##########################################
pymysql.install_as_MySQLdb()
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/tractors'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)


class Sales(db.Model):

    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.Text)
    employee = db.Column(db.Text)
    quantity = db.Column(db.Integer)
    date = db.Column(db.Date)

    def __init__(self, product, employee, quantity, date):
        self.product = product
        self.employee = employee
        self.quantity = quantity
        self.date = date


db.create_all()

############################################

# VIEWS WITH FORMS

##########################################


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/add', methods=['GET', 'POST'])
def add_sale():
    form = AddSaleForm()

    if form.validate_on_submit():
        product = form.product.data
        employee = form.employee.data
        quantity = form.quantity.data
        date = form.date.data

        # Add new Sale to database
        new_sale = Sales(product, employee, quantity, date)
        db.session.add(new_sale)
        db.session.commit()

        return redirect(url_for('list_sales'))

    return render_template('add_sale.html', form=form)


@app.route('/list')
def list_sales():
    # Grab a list of sales from database.
    sales = Sales.query.all()
    return render_template('list.html', sales=sales)


if __name__ == '__main__':
    app.run(debug=True)
