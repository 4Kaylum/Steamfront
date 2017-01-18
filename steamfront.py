from requests import get
import xml.etree.ElementTree as ET


'''
Todo :: 
* Add Steam game comparisons
* Add case sensitivity flag

--------------------

* http://steamcommunity.com/id/USERID/games?tab=all&xml=1i
* http://steamcommunity.com/profiles/USERID64/games?tab=all&xml=1
-- Both of those return XML of all games

* http://store.steampowered.com/api/appdetails?appids={}&format=json
-- Gives info of a Steam game via its ID

* http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=XXXXXXXXXXXXXXXXX&steamid=76561197960434622&format=json
-- Returns owned games of a player from an ID64 and API key

* http://api.steampowered.com/ISteamApps/GetAppList/v0001/
-- Returns all games on Steam

* https://developer.valvesoftware.com/wiki/Steam_Web_API
'''


class NeedsAPIKey(Exception):
    """
    This function cannot be used without an API key
    """

    pass


class GameDoesNotExist(Exception):
    """
    The given game's ID does not exist on Steam
    """

    pass


class UserDoesNotExist(Exception):
    """
    The given user's ID or ID64 does not exist
    """

    pass


class User:

    def __init__(self, id64:str, isId64:bool=True):
        """
        Information given for a Steam user

        Parameters
        ----------
        id64 : ``str``
            This will be the ID64 of the user in question
            To get a user from an steamID instead of id64, pass `isId64` as False
        isId64 : ``str``
            Determines whether or not to parse the id input as id64 or steamID. Defaults to ``True``.

        Raises
        ----------
        :class:`UserDoesNotExist`
            Should the parser fail to get an existing user, this will be thrown
        """

        # Get the user data
        if isId64 == False:
            formString = 'id/{}'.format(id64)
        else:
            formString = 'profiles/{}'.format(id64)

        # Get the site
        getSite = 'http://steamcommunity.com/{}/games?tab=all&xml=1'.format(formString)
        site = get(getSite)

        # Parse and store the information
        self.root = root = ET.fromstring(site.content)
        self.id64 = root[0].text
        self.id = root[1].text
        games = [i for i in root[2]]
        self.games = [UserGame(i) for i in games]

    def __str__(self):
        return self.id


class UserGame:

    def __init__(self, data):
        """
        Describes the relation between a user and a game
        Generally should not be called
        """
        
        datafinder = lambda x: data.findall(x)[0].text
        self.game = None
        self.raw = data
        self.name = datafinder('name')
        self.game_id = datafinder('appID')
        self.store_link = datafinder('storeLink')

        try:
            self.stats = datafinder('globalStatsLink')
        except IndexError:
            self.stats = None

        try:
            self.player_stats = datafinder('statsLink')
        except IndexError:
            self.player_stats = None

        try:
            self.play_time = datafinder('hoursOnRecord')
        except IndexError:
            self.play_time = None

    def __str__(self):
        return self.game_id

    def get_game(self):
        """
        Gets the game object for the game relation being described

        Returns
        ----------
        :class:`Game`
        """

        self.game = Game(self.game_id)
        return self.game


class Game:
    
    def __init__(self, gameID:str):
        """
        A container for the information of a game on Steam

        Parameters
        ----------
        gameID : ``str``
            The ID of the game that's going to be looked at.

        Raises
        ----------
        :class:`GameDoesNotExist`
            If the given ID does not show a game, the class will throw steamfront.GameDoesNotExist
        """

        get_game = 'http://store.steampowered.com/api/appdetails?appids={}&format=json'
        site_page = get(get_game.format(gameID))

        # Get the information from the site page
        site_json = site_page.json()
        self.game_id = list(site_json.keys())[0]

        # See if the page actually exists
        if site_json[self.game_id]['success'] == False:
            raise GameDoesNotExist

        # It does - get and store the information
        self.raw = site_json[self.game_id]['data']
        self.name = self.raw['name']
        self.type = self.raw['type']
        self.required_age = self.raw['required_age']
        self.detailed_description = self.raw['detailed_description']
        self.about_the_game = self.raw['about_the_game']
        self.developers = self.raw['developers']
        self.publishers = self.raw['publishers']
        self.categories = [i['description'] for i in self.raw['categories']]
        self.genres = [i['description'] for i in self.raw['genres']]
        self.screenshots = [i['path_full'] for i in self.raw['screenshots']]

        try:
            self.release_date = self.raw['release_date']['date']
        except KeyError:
            self.release_date = None

        try:
            self.price = self.raw['price_overview']
        except KeyError:
            self.price = None

        try:
            self.dlc = [Game(i) for i in self.raw['dlc']]
        except KeyError:
            self.dlc = None

        try:
            self.description = self.raw['description']
        except KeyError:
            self.description = None

        try:
            self.metacritic = self.raw['metacritic']
        except KeyError:
            self.metacritic = None

    def __str__(self):
        return self.game_id


class Steamfront:
    
    def __init__(self, *, api_key:str=None):
        """ 
        Provides a front for the Steam store and all relevant applications and data

        Parameters
        ----------
        api_key : (Optional [str])
            The key used for API functions
            This is not required for all methods, but a good few of them.
            Defaults to ``None``.
        """

        self.api_key = api_key
        self.steam_games = None
        #self.needs_key = lambda: raise NeedAPIKey

        # Populate game list
        self.get_steam_games()

    def get_steam_games(self) -> list:
        """
        Gives a list of all games on Steam

        Returns
        ----------
        ``list``
            The list will correspond to a list of every (around 32k) games on the Steam store. You shouldn't *really* be 
            using this, but I won't judge. 
            It's stored inside of :attr:`steam_games`
        """

        # Get the list from the API
        dict_games = get('http://api.steampowered.com/ISteamApps/GetAppList/v0001/')

        # Get the list from the dictionary
        json_games = dict_games.json()
        game_list = json_games['applist']['apps']['app']

        # Store everything nicely
        self.steam_games = game_list
        return game_list

    def get_game_from_id(self, appid:str) -> Game:
        """
        Gets the information of a game from an appid.
        Just calls :class:`Game` with the id passed into it.

        Parameters
        ----------
        appid : ``str``
            The ID of the game you're trying to get.

        Returns
        ----------
        :class:`Game`

        Raises
        ----------
        :class:`GameDoesNotExist`
            If the given game cannot be found through the API.
        """

        return Game(appid)

    def get_game_from_name(self, name:str, *, refresh:bool=False, case_sensitive:bool=True) -> Game:
        """
        Gets the data from a game via its name
        Not guarenteed to be accurate
        Will return a list of given results

        Parameters
        ----------
        name : str
            The name of the game you're trying to get
        refresh : (Optional [bool])
            Determines whether or not to repopulate the internal game list. Defaults to ``False``.
        case_sensitive : (Optional [bool])
            Determines whether your search is case sensitive or not. Defaults to ``True``.

        Returns
        ----------
        :class:`Game`
            This will be a game from a name, but it may not give the exact game you asked if there are
            games with duplicate names.
        ``False``
            If no matching games can be found, then the return value will be ``False``
        """

        if refresh:
            self.get_steam_games()

        if case_sensitive:
            namecheck = lambda x, y: x == y 
        else:
            namecheck = lambda x, y: x.lower() == y.lower()

        for i in self.steam_games:
            if namecheck(i['name'], name):
                g = Game(i['appid'])
                return g

        return False

    def get_games_from_search(self, name:str, *, refresh:bool=False, case_sensitive:bool=True) -> list:
        """
        Gets a list of all the names matching a game via its name
        Not guarenteed to be accurate
        Will return a list of given results

        Parameters
        ----------
        name : str
            The name of the game you're trying to get
        refresh : (Optional [bool])
            Determines whether or not to repopulate the internal game list. Defaults to ``False``.
        case_sensitive : (Optional [bool])
            Determines whether your search is case sensitive or not. Defaults to ``True``.

        Returns
        ----------
        ``list``
            This will be a list of ``tuple``s, containing a string of the name of the game as the first item, and the game's ID as 
            the second item.
        """

        if refresh:
            self.get_steam_games()

        if case_sensitive:
            namecheck = lambda x, y: x == y 
        else:
            namecheck = lambda x, y: x.lower() == y.lower()

        game_tuple = []

        for i in self.steam_games:
            if namecheck(i['name'], name):
                n = i['name']
                d = i['appid']
                game_tuple.append((n, d))

        return game_tuple
