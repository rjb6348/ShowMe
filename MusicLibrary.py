#!/usr/bin/env python
# coding: utf-8
import base64
import requests
import datetime
import sys
import spotipy
import spotipy.oauth2 as oauth2
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

from pprint import pprint

class SpotifyInteractions(object):
    client_id = None
    client_secret = None

    def __init__(self, client_id, client_secret, redirect_uri, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None
        self.redirect_uri = redirect_uri
        self.sp = None 
        self.offset = 0
        self.scope = None

    def login(self):
        try:
            self.scope='user-library-read user-top-read'
            #username = input("Type the Spotify user ID to use: ")
            username = 'rrbvt'
            token = util.prompt_for_user_token(username, show_dialog=True, scope=self.scope, client_id=self.client_id, client_secret=self.client_secret, redirect_uri=self.redirect_uri)
            sp = spotipy.Spotify(auth = token,oauth_manager=SpotifyOAuth(scope=self.scope,client_id=self.client_id, client_secret=self.client_secret, redirect_uri=self.redirect_uri))
            self.token = token
            self.sp = sp
            #pprint(sp.me())
            return "Success"
        except:
            return "Failure"

    def pullUserTopArtists(self,offset=0,limit=20,time_range="long_term"):
        try:
            self.offset = self.offset + offset
            return [self.sp.current_user_top_artists(limit=limit, offset=self.offset, time_range=time_range),"success"]
        except:
            return [None, "failure"]


    #TODO follow up on this function
    
    def dispUser(self):
        print(self.sp.me())
    
    #def getTopTracks(self):

    '''
    client_id = self.client_id
    client_secret = self.client_secret
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
    '''