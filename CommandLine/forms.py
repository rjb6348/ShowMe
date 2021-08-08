# forms.py

from wtforms import StringField, SubmitField, SelectField
from flask_wtf import FlaskForm


class BasicForm(FlaskForm):
    searchZip = StringField('ZipCode')
    searchArtist = StringField('Artist')

class ArtistResultForm(FlaskForm):
    searchZip = StringField('ZipCode')

class HomePageForm(FlaskForm):
    basic_search = SubmitField('Basic Search')
    spotify_login = SubmitField('Login with Spotify')
    spotify_signout =  SubmitField('Spotify Logout')
'''
    return f'<a href="/basic_search">[Basic Search]<a/></h2> | ' \
        f'<a href="/spotify_login">[Login with Spotify]</a> | ' \
        f'<a href="/spotify_sign_out">[Sign out of Spotify]</a> | ' \
'''