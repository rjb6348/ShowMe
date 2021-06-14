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

class SpotifyUserInteractions(object):
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
        self.userName = None

    def login(self, username = None):
        try:
            self.scope='user-library-read user-top-read'
            if username == None:
                username = input("Type the Spotify user ID to use: ")
            token = util.prompt_for_user_token(username, show_dialog=True, scope=self.scope, client_id=self.client_id, client_secret=self.client_secret, redirect_uri=self.redirect_uri)
            sp = spotipy.Spotify(auth = token,oauth_manager=SpotifyOAuth(scope=self.scope,client_id=self.client_id, client_secret=self.client_secret, redirect_uri=self.redirect_uri))
            self.token = token
            self.userName = sp.me()['display_name']
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
        print(self.userName)

    def logout(self):
        self.token = None
        self.sp = None 
        self.userName = None
        print("logout")
