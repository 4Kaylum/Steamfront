from .game import *
from requests import get as _get
import xml.etree.ElementTree as _ET


class User(object):
    """
    Information for a given Steam user

    :param str id64: The ID64 of a given user.
    :param bool isId64: Determines whether to parse as name or ID64. Defaults to ``True``.
    :ivar id: The Steam ID/name of the user.
    :ivar id64: The ID64 of the user.
    :ivar root: The raw data from the Steam API.
    :ivar games: A list of :class:`UserGame` for all games in the user's library.
    :raises UserDoesNotExist:
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
        self.id64 = root[0].text
        self.id = root[1].text
        games = [i for i in root[2]]
        self.games = [UserGame(i) for i in games]

    def __str__(self):
        return self.id


class UserGame(object):
    """
    Describes the relation between a user and a game
    Generally should not be called

    :param data: The raw user game data.
    :ivar game: The :class:`steamfront.game.Game` object for the given game. Will be ``None`` until :meth:`get_game` is called.
    :ivar game_id: The ID of the game.
    :ivar name: The name of the game.
    :ivar play_time: The total hours of play time that the user has in the game.
    :ivar player_stats: The player's stats for the game. May be ``None``.
    :ivar stats: The gloabl stats for the game. May be ``None``.
    :ivar store_link: The link to the game's store page.
    """

    def __init__(self, data):
        
        datafinder = lambda x: data.findall(x)[0].text
        self.game = None
        self.raw = data
        self.name = datafinder('name')
        self.game_id = datafinder('appID')
        self.store_link = datafinder('storeLink')

        self.stats = None
        try:
            self.stats = datafinder('globalStatsLink')
        except IndexError:
            self.stats = None

        self.player_stats = None
        try:
            self.player_stats = datafinder('statsLink')
        except IndexError:
            self.player_stats = None

        self.play_time = None
        try:
            self.play_time = datafinder('hoursOnRecord')
        except IndexError:
            self.play_time = 0.0

    def __str__(self):
        return self.game_id

    def get_game(self):
        """
        Gets the game object for the game relation being described

        :return: The :class:`steamfront.game.Game` object for the given game.
        :rtype: :class:`steamfront.game.Game`
        """

        if self.game == None:
            self.game = Game(self.game_id)
        return self.game
