#!/usr/bin/env python
# coding: utf-8
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth


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
        self.user_name = None

    def login(self, username=None):
        try:
            self.scope = 'user-library-read user-top-read'
            if username is None:
                username = input("Type the Spotify user ID to use: ")
            token = util.prompt_for_user_token(username, show_dialog=True, scope=self.scope,
                                               client_id=self.client_id, client_secret=self.client_secret, redirect_uri=self.redirect_uri)
            sp = spotipy.Spotify(auth=token, oauth_manager=SpotifyOAuth(
                scope=self.scope, client_id=self.client_id, client_secret=self.client_secret, redirect_uri=self.redirect_uri))
            self.token = token
            try:
                self.user_name = sp.me()['display_name']
            except Exception:
                self.user_name = username
            self.sp = sp
            return "Success"
        except Exception:
            return "Failure"

    def pull_user_top_artists(self, offset=0, limit=20, time_range="long_term"):
        try:
            self.offset = self.offset + offset
            return [self.sp.current_user_top_artists(limit=limit, offset=self.offset, time_range=time_range), "success"]
        except:
            return [None, "failure"]

    # TODO follow up on this function

    def disp_user(self):
        print(self.user_name)

    def logout(self):
        self.token = None
        self.sp = None
        self.user_name = None
