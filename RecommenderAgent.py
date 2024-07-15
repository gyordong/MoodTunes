
from DataPreprocessing import DataPreprocessing
from KnowledgeBase import KnowledgeBase
import math
#do df.df bc its nested haha
class RecommenderAgent:
    #Knowledge Base
    #do_not_recommend = dict() #Or use list
    #recommend = dict()      #Or use list
    kb = KnowledgeBase()
    dataset = DataPreprocessing()
    genre = ""
    song_list = []
    like_artist = set()
    like_genre = set()
    test_song_list = [
                        'Hope is the Thing With Feathers', 'Comedy', 'Ghost - Acoustic', 'To Begin Again',
                        "Can't Help Falling In Love", 'Hold On','Days I Will Remember', 'Say Something',
                        "I'm Yours", 'Lucky', 'Hunger', 'Give Me Your Forever'
                    ]
    valence = 0

    def __init__(self):
        valence = 1
        pass

    def get_user_input_mood(self):
        #Assume that its one word
        user_input1 = input("“How are you feeling? ")
        return user_input1

    def get_user_input_genre(self):
        while True:
            user_input2 = input("What genre do you like? ")
            if user_input2 not in self.dataset.print_list_of_genres():
                print("Invalid genre. Please try again.")
            else:
                self.genre = user_input2
                break
        return

    def get_valence_value(self):
        #Starting point is determined by average valence of selected genre
        self.valence = self.dataset.mean_valence(self.genre)
        return self.valence

    def get_potential_songs(self):
        # split dataframe into two dataframes based on valence no
        # needs to have feature to consider artists with 2 collaborators as songs for filters
        rangedf = self.dataset.df[(self.dataset.df['valence'] < (self.valence + 0.02)) & (self.dataset.df['valence'] >
                 (self.valence - 0.02))]
        arg_list = []
        #like_artist = []
        #like_genre = []
        # decipher knowledge base arguments
        for i in range(len(self.kb.clauses)):
            # verify for solo
            if self.kb.clauses[i].op != '&':
                arg = self.kb.clauses[i].op.split('(')[1].replace(')','')
                arg_list.append(arg)
            if self.kb.clauses[i].args:
                for prop in self.kb.clauses[i].args:
                    # clean up the argument
                    arg = prop.split('(')[1].replace(')','')
                    arg_list.append(arg)
                    # find out which category it belongs to
                    # validate if working please and delete the comment
        for arg in arg_list:
            if self.kb.dislike_artist(arg) and arg != "none" and arg != "None":
                rangedf = rangedf[rangedf['artists'] != arg]
            if self.kb.dislike_genre(arg) and arg != "none" and arg != "None":
                rangedf = rangedf[rangedf['track_genre'] != arg]
            # these tags will be added first to playlist b4 adding others
            if self.kb.like_artist(arg) and arg != "none" and arg != "None":
                self.like_artist.add(arg)
            if self.kb.like_genre(arg) and arg != "none" and arg != "None":
                self.like_genre.add(arg)
        print("Testing lists")
        print(arg_list)
        print(self.like_artist)
        print(self.like_genre)
        return rangedf

    def search_song(self):
        #implement search algorithm
        # Use the genre + any filters from the “do not recommend” and “recommend” lists to generate a list of n songs

        #Starting point is the valence
        # sort the list and find the value with the lowest abs value difference from self.valence
        rangedf = self.get_potential_songs().sort_values(by=['valence'])
        song_df = rangedf.iloc[(rangedf['valence'] - self.valence).abs().argsort()[:50]]
        self.song_list = song_df['track_name'].tolist()
        return self.song_list

    def get_song_recommendations(self):
        #song_list = search_song
        #self.song_list = self.dataset.print_list_of_songs()

        for song in self.song_list:
            print(song)
        return


    def get_user_feedback(self):
        user_input1 = input(
            "What artists did you like? (Separate artists with ';') (Enter 'none' if there is none) ").strip()
        user_input2 = input(
            "What artists didn't you like? (Separate artists with ';') (Enter 'none' if there is none) ").strip()
        user_input3 = input("What genres did you like? (Separate genres with ';') (Enter 'none' if there is none) ").strip()
        user_input4 = input("What genres didn't you like? (Separate genres with ';') (Enter 'none' if there is none) ").strip()
        user_input5 = input("On a scale of 1-10 did the songs match your mood? ")
        user_input6 = input("Do you want to see a previously excluded artist/genre again? (Enter 'yes' or 'no') ")

        list1 = user_input1.split(';')
        list2 = user_input2.split(';')
        list3 = user_input3.split(';')
        list4 = user_input4.split(';')

        for artist in list1:
            self.kb.tell("Artist({artist})".format(artist=artist))

        for artist in list2:
            self.kb.tell("!Artist({artist})".format(artist=artist))

        for genre in list3:
            self.kb.tell("Genre({genre})".format(genre=genre))

        for genre in list4:
            self.kb.tell("!Genre({genre})".format(genre=genre))

        if int(user_input5) < 3:
            self.valence -= 0.05
        elif int(user_input5) < 5:
            self.valence -= 0.02
        elif int(user_input5) == 5:
            self.valence += 0
        elif int(user_input5) > 5 and int(user_input5) < 8:
            self.valence += 0.02
        else:
            self.valence += 0.05

        if user_input6 == "yes":
            str = input("Artist or Genre? ").lower()
            if str == "artist":
                artist = input("Enter the artist: ")
                self.kb.retract("Artist({artist})".format(artist=artist))
                self.kb.retract("!Artist({artist})".format(artist=artist))
            elif str == "genre":
                genre = input()
                self.kb.retract("Genre({genre})".format(genre=genre))
                self.kb.retract("!Genre({genre})".format(genre=genre))

        #self.song_list.clear() #DONT FORGET THIS!!!!
        return print("Thank you for your feedback!\n")

#Version w/o Spotify Developer Account
example = RecommenderAgent()
continue_recommendations = input("Hi! Do you want some song recommendations/ want to continue? y/n ")
example.get_user_input_mood()
example.get_user_input_genre()
example.get_valence_value()
while continue_recommendations == 'y':
    example.get_song_recommendations()
    print(example.search_song())
    example.get_user_feedback()
    continue_recommendations = input("Hi! Do you want some song recommendations/ want to continue? y/n ")


