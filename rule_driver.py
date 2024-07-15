from SpotifyAPI import SpotifyAPI


#def main():

    #Create the Spotify API Object
    #RecommenderAgent is created which has a DataPreprocessing and KnowledgeBase object created
frontend = SpotifyAPI()

    #Set up the authorization for Spotify
frontend.create_token()
frontend.create_spotify_client()

continue_recommendations = input("Hi! Do you want some song recommendations/ want to continue? y/n ")

# Use the recommender agent to prompt the user for their mood and desired genre
frontend.agent.get_user_input_mood()
frontend.agent.get_user_input_genre()
frontend.agent.get_valence_value()

while continue_recommendations == "y":

        #Calculate the valence value using the input genre; Determines the initial range of songs in the data set
    print("Test get valence value")
    print(frontend.agent.valence)
    print("\n")

        #Generate a list of potential songs from the data set to search through using get_potential_songs() then
        # search through potential songs to create a playlist
    print("Test get song recommendation")
    frontend.agent.get_potential_songs()
    frontend.agent.search_song()
    print("\n")
   # print(frontend.spotify_object.recommendations(seed_artists=['spotify:artist:246dkjvS1zLTtiykXe5h60'], seed_tracks=['spotify:track:0RiRZpuVRbi7oqRdSMwhQY'], seed_genres=['rock']))
        #Print out the suggested playlist songs
    print("Test printing out suggested songs")
    frontend.agent.get_song_recommendations()
    #print(frontend.agent.song_list)
    print("\n")
        #Use the generated playlist and create a playlist on the Spotify app
    print("Test generating Spotify playlist")
    frontend.create_playlist()
    frontend.populate_playlist()
    print("Success!\n")
        #Prompt user feedback (RULE BASE)
    frontend.agent.get_user_feedback()

    continue_recommendations = input("Hi! Do you want some song recommendations/ want to continue? y/n ")

