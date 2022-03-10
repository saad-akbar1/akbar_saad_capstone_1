from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField


class AddSaleForm(FlaskForm):
    product = StringField('Product ID:')
    employee = StringField('Employee ID:')
    quantity = IntegerField("Quantity:")
    date = DateField("Date:")
    submit = SubmitField('Add Sale')
