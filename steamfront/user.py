from .game import *
from requests import get as _get
import xml.etree.ElementTree as _ET


class User(object):
    """
    Information given for a Steam user

    Parameters
    ----------
    id64 : str
        This will be the ID64 of the user in question
        To get a user from an steamID instead of id64, pass `isId64` as False
    isId64 : str
        Determines whether or not to parse the id input as id64 or steamID. Defaults to ``True``.
    """

    def __init__(self, id64:str, isId64:bool=True):


        # Get the user data
        if isId64 == False:
            formString = 'id/{}'.format(id64)
        else:
            formString = 'profiles/{}'.format(id64)

        # Get the site
        getSite = 'http://steamcommunity.com/{}/games?tab=all&xml=1'.format(formString)
        site = _get(getSite)

        # Parse and store the information
        self.root = root = _ET.fromstring(site.content)
        '''The raw output from the Steam API.'''
        self.id64 = root[0].text
        '''The user's ID64.'''
        self.id = root[1].text
        '''The user's SteamID.'''
        games = [i for i in root[2]]
        self.games = [UserGame(i) for i in games]
        '''A list of :class:`UserGame` for the user.'''

    def __str__(self):
        return self.id


class UserGame(object):
    """
    Describes the relation between a user and a game
    Generally should not be called
    """

    def __init__(self, data):
        
        datafinder = lambda x: data.findall(x)[0].text
        self.game = None
        '''The :class:`Game` object. Is ``None`` unless `get_game` is called.'''
        self.raw = data
        '''The raw user data for the game.'''
        self.name = datafinder('name')
        '''The name of the game.'''
        self.game_id = datafinder('appID')
        '''The game's app id.'''
        self.store_link = datafinder('storeLink')
        '''The store link to the game.'''

        self.stats = None
        '''The global stats for the game. May be ``None``.'''
        try:
            self.stats = datafinder('globalStatsLink')
        except IndexError:
            self.stats = None

        self.player_stats = None
        '''The user's stats for the game. May be ``None``.'''
        try:
            self.player_stats = datafinder('statsLink')
        except IndexError:
            self.player_stats = None

        self.play_time = None
        '''The user's stats for the game. May be ``None``.'''
        try:
            self.play_time = datafinder('hoursOnRecord')
        except IndexError:
            self.play_time = None

    def __str__(self):
        return self.game_id

    def get_game(self):
        """Gets the game object for the game relation being described

        Returns
        ----------
        :class:`Game`
            Gets the game object of the user game link.
        """

        if self.game == None:
            self.game = Game(self.game_id)
        return self.game
