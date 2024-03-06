from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import DataRequired

class LiblaryForm(FlaskForm):
    title = StringField('Tytuł', validators=[DataRequired()])
    creation_date = IntegerField('Data wydania')
    page_number = IntegerField('Liczba stron', validators=[DataRequired()])
    book_color = StringField('Kolor okładki', validators=[DataRequired()])
    shelf = BooleanField('Czy jest na półce')