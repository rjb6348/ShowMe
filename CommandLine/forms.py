# forms.py

from wtforms import StringField
from flask_wtf import FlaskForm


class BasicForm(FlaskForm):

    searchZip = StringField('ZipCode')
    searchArtist = StringField('Artist')

class ArtistResultForm(FlaskForm):
    searchZip = StringField('ZipCode')
