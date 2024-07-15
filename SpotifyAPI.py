import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

from RecommenderAgent import RecommenderAgent

class SpotifyAPI:
    agent = RecommenderAgent()
    username = ''
    spotify_object = None
    song_list = []
    playlist_id = 0


    def __init__(self):
        pass

    def create_token(self):
        token = SpotifyOAuth(scope='playlist-modify-public',
                             username=self.username,
                             client_id="",
                             client_secret="",
                             redirect_uri="http://127.0.0.1:8080/")
        print("The token has been created!\n")
        return token

    def create_spotify_client(self):
        self.spotify_object = spotipy.Spotify(auth_manager=self.create_token())
        print("The client has been created!\n")


    def create_playlist(self):
        playlist_name = input('Enter playlist name: ')
        playlist_description = input('Enter playlist description: ')

        playlist = self.spotify_object.user_playlist_create(user=self.username,name=playlist_name,
                                                 description=playlist_description,public=True)

        self.playlist_id = playlist['id']

    #def get_playlist_id(self):
        #playlist_list = self.spotify_object.user_playlists(user=self.username) #Searches all playlist on the Spotify account
        #self.playlist_id = playlist_list['items'][self.playlist_number]['id']
        #self.playlist_number += 1 #increment for next playlist generation
        #print("Playlist Number: " + str(self.playlist_number))
        #return self.playlist_id

    def populate_playlist(self):
        print(self.agent.song_list)
        print(self.agent.like_artist)
        print(self.agent.like_genre)
        print("Adding artists to the playlist ")
        for artist in self.agent.like_artist:
            result = self.spotify_object.search(q=artist,type='album') #REVIEW HOW THIS WORKS
            artist_id = result['albums']['items'][0]['artists'][0]['uri']
            print(artist_id)
            artist_tracks = self.spotify_object.artist_top_tracks(artist_id)
            self.song_list.append(artist_tracks['tracks'][0]['uri'])
        print("Adding genres to the playlist ")
        for genre in self.agent.like_genre:
            #**THIS PART STOPPED WORKING***
            print(self.spotify_object.recommendation_genre_seeds())
            result = self.spotify_object.recommendations(seed_genres=[genre]) #REVIEW HOW THIS WORKS
            print(result)
            artist_id = result['tracks'][0]['artists'][0]['id']
            print(artist_id)
            artist_tracks = self.spotify_object.artist_top_tracks(artist_id)
            self.song_list.append(artist_tracks['tracks'][0]['uri'])
            result = self.spotify_object.search(q=genre)  # REVIEW HOW THIS WORKS
            #print(json.dumps(result, sort_keys=4, indent=4)) #prints out result, basically a extensive nested dictionary
            self.song_list.append(result['tracks']['items'][0]['uri'])
        for song in self.agent.song_list:
            result = self.spotify_object.search(q=song) #REVIEW HOW THIS WORKS
            #print(json.dumps(result, sort_keys=4, indent=4)) #prints out result, basically a extensive nested dictionary
            self.song_list.append(result['tracks']['items'][0]['uri'])
        #print(json.dumps(result,sort_keys=4, indent=4))

        self.song_list = list(set(self.song_list)) #Removes duplicates before
        self.spotify_object.user_playlist_add_tracks(user=self.username,playlist_id=self.playlist_id,tracks=self.song_list)
        self.song_list.clear() #clear the song list so it does not duplicate songs from like_artist and like_genre


#test_object = SpotifyAPI()
#test_object.create_spotify_client()
#test_object.create_playlist()
#test_object.populate_playlist()

#test_object = SpotifyAPI()
##test_object.agent.get_user_feedback()
#test_object.create_spotify_client()
#test_object.create_playlist()
#test_object.populate_playlist()