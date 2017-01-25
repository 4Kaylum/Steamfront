from requests import get as _get


class Game(object):
    """
    A container for the information of a game on Steam. Any of these attributes may be ``None``.

    :param str gameID: The ID of the game that's going to be looked at.
    :ivar about_the_game: The body text of the description from the store page.
    :ivar categories: A list of catergories that are listed on the Steam page.
    :ivar detailed_description: The body text of the description from the store page.
    :ivar description: May be ``None``.
    :ivar developers: A list of developers that are listed on the Steam page.
    :ivar dlc: A list of :class:`Game` containing the DLC for the game.
    :ivar game_id: The ID of the game.
    :ivar genres: A list of genres that are listed on the Steam page.
    :ivar metacritic: A dictionary with values 'url' and 'score', if there's a Metacritic page linked to the Steam.
    :ivar name: The name of the game as it appears on the Steam store.
    :ivar price: A dictionary with values 'initial', 'discount_percent', 'final', and 'currency'.
    :ivar publishers: A list of publishers that are listed on the Steam page.
    :ivar raw: The raw JSON information from Steam.
    :ivar release_date: A dictionary with values 'coming_soon' and 'date', containing information on the game's release date.
    :ivar required_age: The age that is required to buy the game. Is ``0`` if there is none.
    :ivar screenshots: A list of links to URLs that are listed on the Steam page
    :ivar type: The type of app that it is, eg game, soundtrack, dlc, etc.
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
        def jsongetter(x, y=None):
            try: return self.raw[x]
            except KeyError: return y

        self.name = jsongetter('name')
        self.type = jsongetter('type')
        self.required_age = jsongetter('required_age')
        self.detailed_description = jsongetter('detailed_description')
        self.about_the_game = jsongetter('about_the_game')
        self.developers = jsongetter('developers')
        self.publishers = jsongetter('publishers')
        self.categories = [i['description'] for i in jsongetter('categories', {'description':''})]
        self.genres = [i['description'] for i in jsongetter('genres', {'description':''})]
        self.screenshots = [i['path_full'] for i in jsongetter('screenshots', {'path_full':''})]
        self.release_date = jsongetter('release_date')
        self.description = jsongetter('description')
        self.metacritic = jsongetter('metacritic')
        self.price = jsongetter('price_overview')
        try: self.dlc = [Game(i) for i in self.raw['dlc']]
        except KeyError: self.dlc = ['']

    def __str__(self):
        return self.game_id
