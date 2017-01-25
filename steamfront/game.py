from requests import get as _get


class Game(object):
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
    
    def __init__(self, gameID:str):

        get_game = 'http://store.steampowered.com/api/appdetails?appids={}&format=json'
        site_page = _get(get_game.format(gameID))

        # Get the information from the site page
        site_json = site_page.json()
        self.game_id = list(site_json.keys())[0]
        '''The ID of the game from the API.'''

        # See if the page actually exists
        if site_json[self.game_id]['success'] == False:
            raise GameDoesNotExist

        # It does - get and store the information
        self.raw = site_json[self.game_id]['data']
        '''The raw data that was aquired from the API.'''
        self.name = self.raw['name']
        '''The name of the game.'''
        self.type = self.raw['type']
        '''The type of app that was recieved.'''
        self.required_age = self.raw['required_age']
        '''The required age to buy the game. Is 0 if there is none.'''
        self.detailed_description = self.raw['detailed_description']
        '''The detailed description from the Steam page.'''
        self.about_the_game = self.raw['about_the_game']
        '''The 'about the game' page from the Steam page.'''
        self.developers = self.raw['developers']
        '''A list of developers that worked on the game.'''
        self.publishers = self.raw['publishers']
        '''A list of publishers for the game.'''
        self.categories = [i['description'] for i in self.raw['categories']]
        '''A list of categories the game appears in.'''
        self.genres = [i['description'] for i in self.raw['genres']]
        '''A list of genres the game appears in.'''
        self.screenshots = [i['path_full'] for i in self.raw['screenshots']]
        '''List of URLs to the Steam page's screenshots.'''

        self.release_date = None
        '''The release date for the game. May be ``None``.'''
        try:
            self.release_date = self.raw['release_date']['date']
        except KeyError:
            pass

        self.price = None
        '''The price for the game. May be ``None``.'''
        try:
            self.price = self.raw['price_overview']
        except KeyError:
            pass

        self.dlc = None
        '''A list of class:`Game` representing the DLCs. May be ``None``.'''
        # try:
        #     self.dlc = [Game(i) for i in self.raw['dlc']]
        # except KeyError:
        #     pass


        self.description = None
        '''The description of the Steam page. May be an ``None``.'''
        try:
            self.description = self.raw['description']
        except KeyError:
            pass


        self.metacritic = None
        '''The Metacritic score for the Steam page, if it was registered. May be ``None``.'''
        try:
            self.metacritic = self.raw['metacritic']
        except KeyError:
            pass

    def __str__(self):
        return self.game_id
