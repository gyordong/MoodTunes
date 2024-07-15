
from RecommenderAgent import RecommenderAgent

def main():
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