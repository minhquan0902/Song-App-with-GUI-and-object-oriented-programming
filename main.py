"""
Name: Nguyen Quoc Minh Quan
Date: 22/5/2020
Brief Project Description:  My CP1404 final assignment working with
    classes and Kivy, i have the chance to re-create my assignment 1 with classes and create GUI with Kivy
GitHub URL: https://github.com/JCUS-CP1404/assignment-02-songs-app-minhquan0902
"""
# TODO: Create your main program in this file, using the SongsToLearnApp class

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.uix.button import Button
from string import capwords
from song import Song
from songcollection import SongCollection


class SongsToLearnApp(App):
    """ The main class for the GUI of the song app"""
    sort = StringProperty()
    category = ListProperty()
    order = ListProperty()
    current_order = StringProperty()

    def __init__(self, **kwargs):
        """ Initial class. Here i used **kwargs because I want to handle named arguments """
        super(SongsToLearnApp, self).__init__(**kwargs)

        self.song_collection = SongCollection()

        self.show_song = []

    def build(self):
        """Build app with the help of app.kv file"""
        # application window size
        Window.size = (1000, 800)
        self.title = "Songs to learn app"
        # load app.kv
        self.root = Builder.load_file('app.kv')
        self.category = ['Title', 'Year', 'Artist', 'Unlearn']
        self.sort = self.category[0]
        self.order = ['Ascending Order', 'Descending Order']
        self.current_order = self.order[0]

        return self.root

    def on_start(self):
        """This function start initially when the program start"""
        # Load songs from the csv file
        self.song_collection.load_songs('songs.csv')
        self.show_song = self.song_collection.song_list
        self.root.ids.song_list.bind(minimum_height=self.root.ids.song_list.setter('height'))
        # App's welcome message
        self.root.ids.message.text = "Click on songs to mark as learned"
        # Load songs to the app
        self.load_songs()
        # Show the initial number of songs learned and songs unlearned
        self.count_learn()

    def on_stop(self):
        """ Save changes to the csv file after closing the program"""
        self.song_collection.save_changes('songs.csv')

    def count_learn(self):
        """Count songs learned and songs unlearned and display them in the GUI"""
        self.root.ids.learn_count.text = '{} songs learned, {} still to learn'.format(
            self.song_collection.count_learned(), self.song_collection.count_unlearned())

    def handle_order(self, element):
        """Sort songs based on given order"""
        self.current_order = element
        self.load_songs()

    def sort_song(self, key):
        """Sort songs based on keywords"""
        self.sort = key
        self.load_songs()

    def handle_learn_song(self, instance):
        """Change songs status (Learned or unlearned) when users click on them"""
        current_song = instance.song
        current_song.is_learned = not current_song.is_learned

        self.load_songs()
        learn_mark = 'Learned' if current_song.is_learned else 'unlearned'
        self.root.ids.message.text = 'You have {} {}'.format(learn_mark, current_song)
        self.count_learn()

    def load_songs(self):
        """Load songs to the GUI """
        self.root.ids.song_list.clear_widgets()
        desc = self.current_order == 'Descending Order'
        self.show_song = self.song_collection.sort_song(self.sort, desc)

        for index, song in enumerate(self.show_song):
            learn_mark = 'Learned' if song.is_learned else ''
            btn = Button(text='{} - {} ({}) {}'.format(song.title, song.artist, song.year, learn_mark),
                         size_hint_y=None, height=30)

            btn.song = song
            btn.bind(on_press=self.handle_learn_song)
            if learn_mark:
                btn.background_color = (1, 0.5, 0.5, 1)
            self.root.ids.song_list.add_widget(btn)

    def handle_add_song(self, title, year, artist):
        """Check valid input and display messages telling that they have added song to songs lost successfully"""
        if title and year and artist:
            title_check = self.handle_input(title, is_title=True)

            artist_check = self.handle_input(artist, is_artist=True)

            year_check = self.handle_input(year, is_year=True)
            if year_check and artist_check and title_check:
                clean_title = ' '.join(title.split())
                pretty_title = capwords(clean_title)
                self.song_collection.add_song(Song(title_check, artist_check, year_check))
                self.load_songs()
                self.show_popup_message('{} have been add to song list'.format(pretty_title))
                self.handle_clear_button(is_add=True)
        else:
            # Error popup when users fail to input all the information
            self.show_popup_message("All fields are required")

    def handle_input(self, input_data, is_title=False, is_year=False, is_artist=False, is_learn=False, blank=False):
        """Check whether the users input the valid data"""
        # Check year valid input: must be a number that is greater than 0
        if blank and not input_data:
            return True
        else:
            if is_year:
                try:
                    year = int(input_data)
                    if year < 0:
                        raise ValueError()
                    return input_data.strip()
                except ValueError:
                    self.show_popup_message("Your year must be a number and greater than 0")
            # Check for valid artist input
            elif is_artist:
                # Check for appropriate artist name input
                if input_data.lower().strip() in ['`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-',
                                                  '+', '=', '{', '[', '}', '}', '|']:
                    self.show_popup_message("Please enter an appropriate artist name")
                else:
                    return input_data.strip()
            #  Check learn/unlearned status
            elif is_learn:
                if input_data.lower() not in ["y", 'n']:
                    self.show_popup_message('Learn field must be Y or N')
                else:
                    return True
            elif not input_data.strip() and is_title:
                self.show_popup_message("Your title must not be blank!")
            else:
                return input_data.strip()

    def show_popup_message(self, text):
        """Show pop-up messages for warning or displaying information in the GUI"""
        self.root.ids.popup_message.text = text
        self.root.ids.popup.open()

    def handle_close_popup(self):
        """Close the popup message"""
        self.root.ids.popup_message.text = ''
        self.root.ids.popup.dismiss()

    def handle_clear_button(self, is_add=False):
        """Clear the input when 'clear' button is pressed in the GUI """
        if is_add:
            self.root.ids.title.text = ''
            self.root.ids.year.text = ''
            self.root.ids.artist.text = ''
        else:
            self.root.ids.title.text = ''
            self.root.ids.year.text = ''
            self.root.ids.artist.text = ''


if __name__ == '__main__':
    # Run the GUI
    SongsToLearnApp().run()
