"""
Name: Nguyen Quoc Minh Quan
Date: 22/5/2020
Brief Project Description:  My CP1404 final assignment working with
    classes and Kivy, i have the chance to re-create my assignment 1 with classes and create GUI with Kivy
GitHub URL: https://github.com/JCUS-CP1404/assignment-02-songs-app-minhquan0902
"""


# TODO: Create your Song class in this file


class Song:
    """Song Class"""

    def __init__(self, title='', artist='', year=0, is_learned=False):
        """"__init__ function of song class"""
        self.title = title
        self.year = year
        self.artist = artist
        self.is_learned = is_learned

    def __str__(self):
        """"Return a string containing song information"""
        check_learn = "learned" if self.is_learned else 'unlearned'
        return "{} - {}  {} ({})".format(self.title, self.artist, self.year, check_learn)

    def mark_learned(self):
        """"Marking between learned and unlearned"""
        self.is_learned = True

    def mark_unlearned(self):
        """"Marking between learned and unlearned"""
        self.is_learned = False
