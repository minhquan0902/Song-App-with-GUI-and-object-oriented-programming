"""
Name: Nguyen Quoc Minh Quan
Date: 22/5/2020
Brief Project Description:  My CP1404 final assignment working with
    classes and Kivy, i have the chance to re-create my assignment 1 with classes and create GUI with Kivy
GitHub URL: https://github.com/JCUS-CP1404/assignment-02-songs-app-minhquan0902
"""
from song import Song
from songcollection import SongCollection


def run_tests():
    """Test SongCollection class."""

    # Test empty SongCollection (defaults)
    print("Test empty SongCollection:")
    song_collection = SongCollection()
    print(song_collection)
    assert not song_collection.song_list  # an empty list is considered False

    # Test loading songs
    print("Test loading songs:")
    song_collection.load_songs('songs.csv')
    print(song_collection)
    assert song_collection.song_list  # assuming CSV file is non-empty, non-empty list is considered True

    # Test adding a new Song with values
    print("Test adding new song:")
    song_collection.add_song(Song("My Happiness", "Powderfinger", 1996, True))
    print(song_collection)

    # Test sorting songs
    print("Test sorting - year:")
    sorted_list = song_collection.sort_song("year", descending=True)
    print(song_collection.format_data(sorted_list))
    # Test sorting artists
    print("Test sorting - artist:")
    sorted_list_2 = song_collection.sort_song("artist", descending=True)
    print(song_collection.format_data(sorted_list_2))
    # test sorting titles
    print("Test sorting - title:")
    sorted_list_3 = song_collection.sort_song("title", descending=False)
    print(song_collection.format_data(sorted_list_3))

    #  Test saving songs (check CSV file manually to see results)
    print("Test saving songs:")
    song_collection.save_changes("songs.csv")
    print("Open songs.csv to check whether new song appears or not")

    # Add more tests, as appropriate, for each method
    # Test count learned songs
    print("Test count learned songs:")
    print(song_collection.count_learned())
    # Test count unlearned songs
    print("Test count unlearned songs:")
    print(song_collection.count_unlearned())


run_tests()
