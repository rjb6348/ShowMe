# forms.py

from wtforms import form, StringField, SelectField
from flask_wtf import FlaskForm

class basicformsz(FlaskForm):

    searchZip = StringField('ZipCode')
    searchArtist = StringField('Artist')