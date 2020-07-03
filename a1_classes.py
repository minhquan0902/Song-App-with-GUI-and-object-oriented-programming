"""
Name: Nguyen Quoc Minh Quan
Date: 22/5/2020
Brief Project Description:  My CP1404 final assignment working with
    classes and Kivy, i have the chance to re-create my assignment 1 with classes and create GUI with Kivy
GitHub URL: https://github.com/JCUS-CP1404/assignment-02-songs-app-minhquan0902
"""
# TODO: Copy your first assignment to this file, commit, then update to use Song class

from song import Song
import csv
from songcollection import SongCollection

my_song = SongCollection()
my_song.load_songs('songs.csv')


def main():
    """Main function of the program"""
    print("Songs to Learn 1.0 - by Quan Nguyen")
    print("{} songs loaded".format(len(my_song.song_list)))
    print("\n")

    flag = False
    while not flag:
        print("Menu: ")
        print("L - List songs")
        print("A - Add new song")
        print("S - Search a song")
        print("C - Complete a song")
        print("Q - Quit")

        menu = input(">>>").upper()
        if menu == "L":
            list_song()
        elif menu == "A":
            add_song(my_song)
        elif menu == "S":
            search_songs(my_song)
        elif menu == "C":
            learn_song(my_song)
        elif menu == "Q":
            my_song.save_changes('songs.csv')
            print("{} songs saved to songs.csv".format(len(my_song.song_list)))
            print("--Exiting program--")
            print("Have a nice day!")
            flag = True
        else:
            print("Invalid, please choose again")


def list_song():
    """Display all the songs from the csv file after the user choose L in the menu"""

    print(my_song)
    print("{} songs learned, {} songs still to learn".format(my_song.count_learned(), my_song.count_unlearned()))
    sort_song(my_song)


def add_song(collection):
    """Add songs function"""
    title = handle_text('Title: ')
    year = handle_year()
    artist = handle_text("artist")
    is_learned = handle_text("Learned? (Y/N)", is_bool=True)

    collection.add_song(Song(title, artist, year, is_learned))
    print("{} - {} ({}) added to song list".format(title, artist, year))


def sort_song(collection):
    """Sort out the order of the songs"""
    flag = False
    while not flag:
        print('Sort By:')
        print('T - Title')
        print('Y - Year')
        print('A - Artist')
        print('U - Unlearn')
        print('Q - Quit')

        choice = input(">>> ").upper()

        if choice == "T":
            sort_key(collection, 'title')
        elif choice == "Y":
            sort_key(collection, "year")
        elif choice == "A":
            sort_key(collection, 'artist')
        elif choice == "U":
            sort_key(collection, "unlearn")
        elif choice == "Q":
            flag = True
        else:
            print("Invalid choice, please choose again!")


def search_songs(collection):
    """Search the song by keywords that the users input"""
    flag = False
    while not flag:
        print("Search songs")
        title_search = handle_text('Title (keywords):', blank=True)
        year_search = handle_text('Year:', blank=True)
        artist_search = handle_text("Artist", blank=True)
        status_search = handle_text("Learned or unlearned? (Y/N)?", is_bool=True, blank=True)

        print("Here are the results: ")
        collection.search_song(title_search, year_search, artist_search, status_search)
        print(SongCollection.format_data(collection.search_list))
        choice = handle_text("Continue? (Y/N): ", is_bool=True)
        if not choice:
            collection.search_list = []
            flag = True


def sort_key(collection, key):
    """Ask for the order as descending or ascending"""
    descending = handle_text('Sort songs in descending order? (Y/N): ', is_bool=True)
    print("Results:")
    sort_results = collection.sort_song(key, descending)
    print(SongCollection.format_data(sort_results))


def handle_text(input_name, is_bool=False, blank=False):
    """This function handles error from users input and asks for appropriate input"""
    flag = False
    while not flag:
        try:
            user_input = input(input_name)
            if not user_input.strip() and not blank:
                raise ValueError("Your input must not be blank!")
            if is_bool and user_input.upper() in ["Y", "N"]:
                return user_input.upper() == 'Y'
            if is_bool and user_input.upper() not in ["Y", "N", ""]:
                raise ValueError("Your input is invalid, try again!")
            return user_input
        except ValueError as error:
            print(error)


def handle_year():
    """Year error handle for wrong user input"""
    flag = False
    while not flag:
        try:
            year_input = int(input("Year: "))
            if year_input <= 0:
                raise Exception('Year cannot be less than or equal zero')
            return year_input
        except ValueError:
            print("Please enter an appropriate number")
        # Handle Exception errors and print out
        except Exception as error:
            print(error)


def learn_song(collection):
    """Learn songs function"""
    # check if all the songs have been learnt
    if check_learn_all(collection.song_list):
        print("No more songs to learn!")
        return
    print("Enter the number of a song to mark as learn")
    flag = False
    while not flag:
        try:
            song_number = int(input(">>> "))
            # Raise error to catch the number input that is not in the songs' number range
            if song_number not in range(1, len(collection.song_list) + 1):
                raise KeyError()
            # Check if songs was already learnt
            if collection.song_list[song_number - 1].is_learned:
                raise Exception("You have learned this song")
            else:
                collection.song_list[song_number - 1].is_learned = True
                print("{song.title} - {song.artist} ({song.year})".format(song=collection.song_list[song_number - 1]))
            flag = True
        except ValueError:
            print("Invalid Input, enter a valid number: ")
        except KeyError:
            print("Invalid input, enter a valid number")
        # Check exception errors and print out
        except Exception as error:
            print(error)
            flag = True


def check_learn_all(data):
    """Check whether users have learnt all songs"""
    learned_all = True
    for song in data:
        learned_all = learned_all and song.is_learned
    return learned_all


if __name__ == '__main__':
    main()
