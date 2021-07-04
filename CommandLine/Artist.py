class Artist(object):
    """
    A class to represent an Artist
    """

    def __init__(self, *args, **kwargs):
        ''' Initialize object without info'''
        super().__init__(*args, **kwargs)

        self.artist_dict = {}

        self.has_spotify_data = False
        self.artist_json      = None
        self.artist_name      = None
        self.artist_images    = None
        self.artist_genres    = None
        self.spotify_url      = None

        self.has_songkick_data    = False
        self.artist_touring_until = None
        self.artist_id            = None
        self.sonkick_artist_json  = None
        self.disply_name          = None

    def add_spotify_info(self, artist_json):
        self.spotify_artist_json = artist_json
        self.artist_name         = self.spotify_artist_json['name']
        self.artist_images       = self.spotify_artist_json['images']
        self.artist_genres       = self.spotify_artist_json['genres']
        self.spotify_url         = self.spotify_artist_json['external_urls']['spotify']
        self.has_spotify_data    = True

        self.artist_dict['artist_name']      = self.artist_name
        self.artist_dict['artist_image']    = self.get_artist_first_image_url()
        self.artist_dict['artist_genres']    = self.artist_genres
        self.artist_dict['spotify_url']      = self.spotify_url
        self.artist_dict['has_spotify_data'] = True



    def add_songkick_data(self, artist_json):
        self.sonkick_artist_json  = artist_json
        self.disply_name          = self.sonkick_artist_json['displayName']
        self.artist_id            = self.sonkick_artist_json['id']
        self.artist_touring_until = self.sonkick_artist_json['onTourUntil']
        self.songkick_url         = self.sonkick_artist_json['uri']
        self.has_songkick_data    = True

        self.artist_dict['disply_name']          = self.artist_name
        self.artist_dict['artist_id']            = self.artist_id
        self.artist_dict['artist_touring_until'] = self.artist_touring_until
        self.artist_dict['songkick_url']         = self.songkick_url
        self.artist_dict['has_songkick_data']    = True

    def has_spotify_data(self):
        return self.has_spotify_data

    def get_artist_name(self):
        ''' get artist Name'''
        return self.artist_name

    def get_artist_images(self):
        ''' get artist Name'''
        return self.artist_images

    def get_artist_genres(self):
        ''' get artist Name'''
        return self.artist_genres

    def get_artist_spotify_url(self):
        ''' get artist Name'''
        return self.spotify_url

    def get_artist_first_image_url(self):
        return self.get_artist_images()[0]['url']

    def has_songkick_data(self):
        return self.has_songkick_data

    def get_disply_name(self):
        ''' get artist Name'''
        return self.disply_name

    def get_artist_id(self):
        ''' get artist Name'''
        return self.artist_id

    def get_artist_touring(self):
        ''' get artist Name'''
        return self.artist_touring_until is not None

    def get_songkick_url(self):
        ''' get artist Name'''
        return self.songkick_url


    def get_dictionary(self):
        return self.artist_dict
