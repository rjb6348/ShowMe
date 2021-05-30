#!/usr/bin/env python
# coding: utf-8
import base64
import requests
import datetime
import sys
import spotipy
from spotipy import oauth2
def login():
    client_id = '1b55c01382b740c0b4c6fd22f7065fd6'
    client_secret = '0d1c6411f69342359bdaca85134120eb'
    redirect_uri = 'http://18.218.158.90:8080/'
    scopes = 'user-library-read'
    sp_oauth = oauth2.SpotifyOAuth(client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri,scope=scopes,show_dialog=True)
    token_info = sp_oauth.get_cached_token() 
    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        print(auth_url)
        response = input('Paste the above link into your browser, then paste the redirect url here: ')

        code = sp_oauth.parse_response_code(response)
        print(code)
        token_info = sp_oauth.get_access_token(code)

        token = token_info['access_token']

    sp = spotipy.Spotify(auth=token)

    results = sp.current_user_saved_tracks()
    for idx, item in enumerate(results['items']):
        track = item['track']
        print(idx, track['artists'][0]['name'], " – ", track['name'])