from requests import get as _get


class Game(object):
    """
    A container for the information of a game on Steam

    :param str gameID: The ID of the game that's going to be looked at.
    :ivar raw: The raw JSON information from Steam.
    :ivar name: The name of the game as it appears on the Steam store.
    :ivar type: The type of app that it is, eg game, soundtrack, dlc, etc.
    :ivar required_age: The age that is required to buy the game. Is ``0`` if there is none.
    :ivar detailed_description:  The body text of the description from the store page.
    :ivar about_the_game:
    :ivar developers: A list of developers that are listed on the Steam page
    :ivar publishers: A list of publishers that are listed on the Steam page
    :ivar categories: A list of catergories that are listed on the Steam page
    :ivar genres: A list of genres that are listed on the Steam page
    :ivar screenshots: A list of links to URLs that are listed on the Steam page
    :ivar release_date: A string containing information on the game's release date. May be ``None``.
    :ivar dlc: A list of :class:`Game` containing the DLC for the game.
    :ivar price: A dictionary with values 'initial', 'discount_percent', 'final', and 'currency'. May be ``None``.
    :ivar description: May be ``None``.
    :ivar metacritic: A dictionary with values 'url' and 'score', if there's a Metacritic page linked to the Steam. May be ``None``.
    :ivar game_id: The ID of the game.
    :raises GameDoesNotExist: If the given ID does not show a game, the class will throw :class:`GameDoesNotExist`.
    """
    
    def __init__(self, gameID:str):

        get_game = 'http://store.steampowered.com/api/appdetails?appids={}&format=json'
        site_page = _get(get_game.format(gameID))

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

        self.release_date = None
        try:
            self.release_date = self.raw['release_date']['date']
        except KeyError:
            pass

        self.price = None
        try:
            self.price = self.raw['price_overview']
        except KeyError:
            pass

        self.dlc = []
        try:
            self.dlc = [Game(i) for i in self.raw['dlc']]
        except KeyError:
            pass


        self.description = None
        try:
            self.description = self.raw['description']
        except KeyError:
            pass


        self.metacritic = None
        try:
            self.metacritic = self.raw['metacritic']
        except KeyError:
            pass

    def __str__(self):
        return self.game_id
