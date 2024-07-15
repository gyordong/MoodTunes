import pandas as pd

class DataPreprocessing:
    #df = pd.read_csv('dataset.csv', index_col=False)
    pd.set_option('display.max_columns', 100)
    pd.set_option('display.width', None)

    excluded_classification = [
        'duration_ms', 'explicit', 'danceability', 'energy', 'key', 'loudness', 'mode',
        'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'tempo', 'time_signature',
        'track_id', 'album_name', 'Unnamed: 0']

    def __init__(self):
        self.loc = None
        self.df = pd.read_csv('dataset.csv', index_col=False)

    def print_dataframe(self):
        df = self.df.drop(DataPreprocessing.excluded_classification, axis='columns')
        return print(df)

    def print_list_of_genres(self):
        genre_list = self.df['track_genre'].unique().tolist()
        return genre_list

    def print_list_of_songs(self):
        song_list = self.df['track_name'].loc[0:10].tolist() #ex. prints out first 10 songs in the track_name
        return song_list

    def print_statistics(self):
        statistics = self.df.describe()
        return print(statistics)

    # Used for get_valence_value()
    def mean_valence(self, genre):
        df = self.df[self.df['track_genre'] == genre]
        mean = df[['valence']].copy().mean()
        return float(mean.iloc[0])

    # gets only the songs of a certain genre from the data frame
    def get_songs_of_genre(self, genre):
        new_df = self.df[self.df['track_genre'] == genre]
        return new_df

#Test Cases
#example = DataPreprocessing()
#example.print_dataframe()
#example.print_list_of_genres()
#print(example.print_list_of_songs())
#example.print_statistics()
#print(example.mean_valence('acoustic'))

