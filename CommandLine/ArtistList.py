import Artist

class ArtistList(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.artistjson = None
        self.artists = []
        self.artists_dictionaries = []

    def add_artist(self, artist):
        if self.get_artist_names() is []:
            self.artists.append(artist)
            self.add_dict(artist)
        elif artist.get_artist_name() not in self.get_artist_names():
            self.artists.append(artist)
            self.add_dict(artist)

    def create_artist_list(self, artists):
        if len(self.artists) > 0:
            print("ArtistList already contains artist")
        else:
            for artist in artists:
                self.artists.append(artist)
                self.add_dict(artist)

    def add_dict(self, artist):
        self.artists_dictionaries.append(artist.get_dictionary())

    def get_artists_dictionaries(self):
        return self.artists_dictionaries

    def get_artists(self):
        return self.artists
    
    def get_artist_names(self):
        names = []
        for artist in self.artists:
            names.append(artist.get_artist_name())
        return names
