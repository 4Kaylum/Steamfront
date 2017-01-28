from requests import get as _get
from .errors import UserNotFound as _UserNotFound
from .errors import APIKeyRequired as _APIKeyRequired
from .userapp import UserApp as _UserApp


class User(object):
    '''
    The user object, representing a Steam user

    :param str id64: The user's ID64.
    :param apiKey: Your API key.
    :type apiKey: Optional[str]
    :ivar raw: The raw `dict` that was retrieved from the API.
    :ivar id64: A `str` containing the user's ID64 value.
    :ivar name: A `str` of the user's display name on Steam.
    :ivar profile_url: `str` linking to the user's profile.
    :ivar avatar: The `str` of the URL that links to the user's avatar.
    :ivar status: A `str` showing what status the user is displaying as.
    :ivar private: A `bool` indicating whether or not this user's profile is private.
    :ivar last_online: An `int` of a Unix timestamp of when the user was last online.
    :ivar raw_games: The raw `dict` of what was retrieved from the API.
    :ivar game_count: An `int` showing how many games are on the user's profile.
    :ivar games: A `list` of `str` containing the app IDs of the user's games.
    :raises steamfront.errors.APIKeyRequired: An API key is needed to get user information from Steam.
    :raises steamfront.errors.UserNotFound: Raised if the user's ID64 is not able to be found on Steam.
    '''

    getUser = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids={id64}'
    userGames = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={id64}'

    def __init__(self, id64: str, apiKey: str=None):
        
        # You need an API key to get any user data
        if apiKey == None:
            raise _APIKeyRequired('An API key is required to get user information from the Steam API.')

        # Get the website data
        siteurl = User.getUser.format(id64=id64, key=apiKey)
        site = _get(siteurl)
        rawdata = site.json()

        # Start to parse
        try:
            userdata = rawdata['response']['players'][0]
        except IndexError:
            raise _UserNotFound('The specified user could not be found.')

        # Parse and store
        self.raw = userdata
        self.id64 = userdata['steamid']
        self.name = userdata['personaname']
        self.profile_url = userdata['profileurl']
        self.avatar = userdata['avatarfull']
        self.status = {
            0: 'Offline',
            1: 'Online',
            2: 'Busy',
            3: 'Away',
            4: 'Snooze',
            5: 'Looking to trade',
            6: 'Looking to play'
        }[userdata['personastate']]
        self.private = {
            1: True, 
            3: False
        }[userdata['communityvisibilitystate']]
        self.last_online = userdata['lastlogoff']

        # Get the website data for games
        siteurl = User.userGames.format(id64=id64, key=apiKey)
        site = _get(siteurl)
        rawdata = site.json()
        gamedata = rawdata['response']['games']

        self.raw_apps = gamedata
        self.app_count = rawdata['response']['game_count']
        self.apps = [_UserApp(i, self) for i in gamedata] # playtime_forever
