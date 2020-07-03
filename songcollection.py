"""
Name: Nguyen Quoc Minh Quan
Date: 22/5/2020
Brief Project Description:  My CP1404 final assignment working with
    classes and Kivy, i have the chance to re-create my assignment 1 with classes and create GUI with Kivy
GitHub URL: https://github.com/JCUS-CP1404/assignment-02-songs-app-minhquan0902
"""
from song import Song


# TODO: Create your SongCollection class in this file


class SongCollection:
    """Song collection class"""

    def __init__(self):
        song_list = []
        self.song_list = song_list
        self.file = None

        self.search_list = []

    def load_songs(self, filename):
        """Load songs from file and put it inside song_list"""
        # open file
        self.file = open(filename, 'r')
        # Read data inside the file
        file_read = self.file.readlines()
        count = 0
        for song in file_read:
            count += 1
            new_lines = song.split(',')
            title = new_lines[0]
            artist = new_lines[1]
            year = new_lines[2]
            is_learned = 'l' in new_lines[3]
            self.song_list.append(Song(title, artist, year, is_learned))

        self.file.close()

    def add_song(self, song):
        """ Add songs to song list"""
        self.song_list.append(song)

    def count_unlearned(self):
        """Count the number of unlearned songs"""
        return len([song for song in self.song_list if not song.is_learned])

    def count_learned(self):
        """Count the number of learned songs"""
        return len([song for song in self.song_list if song.is_learned])

    def save_changes(self, file):
        """Save changes back to file"""
        self.file = open(file, "w")
        data = ""
        for song in self.song_list:
            if song.is_learned:
                learned_sign = "l"
            else:
                learned_sign = "u"
            data += "{},{},{},{}\n".format(song.title, song.artist, song.year, learned_sign)
        data = data[:-1]
        self.file.write(data)
        self.file.close()

    def search_song(self, keyword, year='', artist='', learn=None):
        """Search data by given keyword"""

        def filter_songs(song):
            filter_title = keyword.lower() in song.title.lower()
            filter_year = int(song.year) == int(year) if year else True
            filter_artist = song.artist.lower() == artist.lower() if artist else True
            filter_learn = True
            if learn == True or learn == False:
                filter_learn = song.is_learned if learn else not song.is_learned
            return filter_title, filter_year, filter_artist, filter_learn

        self.search_list = list(filter(filter_songs, self.song_list))

    def sort_song(self, keyword=None, descending=False):
        """Sort data function by take in input keywords from users, users can also input descending or ascending
        orders as preference """
        songs = self.search_list if self.search_list else self.song_list
        sort_data = []
        if keyword.lower() == 'year':
            # Lambda function takes in x as an argument and return x.value
            sort_data = sorted(songs, key=lambda song: int(song.year), reverse=descending)
        if keyword.lower() == 'title':
            sort_data = sorted(songs, key=lambda song: song.title, reverse=descending)
        if keyword.lower() == 'artist':
            sort_data = sorted(songs, key=lambda song: song.artist, reverse=descending)
        if keyword.lower() == 'unlearn':
            sort_data = sorted(songs, key=lambda song: song.is_learned, reverse=descending)
        return sort_data

    @staticmethod
    def format_data(raw_data):
        """Format data to print, this function is static because it doesnt take any self arguments but to be used in
        another function """
        output_data = ''
        if raw_data:
            longest_title = max([len(song.title) for song in raw_data])
            for index, song in enumerate(raw_data, start=1):
                mark = '*' if song.is_learned else ''
                output_data += '{0}. {1:<2} {2:<{3}} - {4:<4} ({5})\n'.format(index, mark, song.title, longest_title,
                                                                              song.artist, song.year)
        return output_data

    def __str__(self):
        return self.format_data(self.song_list)
