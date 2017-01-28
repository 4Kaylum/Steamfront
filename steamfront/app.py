from requests import get as _get
from .errors import AppNotFound as _AppNotFound


class App(object):
    '''
    The app object, providing information on apps on the Steam store.

    .. warning::
        It should be noted that not all of these attributes will be available for every app, but all will be present. 
        Make sure that the attributes you want to use do not contain exceptions or `None`.

    :param str appid: The ID of an app.
    :ivar raw: The raw return of values from Steam.
    :ivar about_the_game: A `str` containing the 'about the game' section from the Steam store page.
    :ivar appid: A `str` containing the ID of the app.
    :ivar categories: A `list` of categories.
    :ivar controller_support: A `str` stating what kind of controller support there is.
    :ivar genres: A `list` of genres that the app is in.
    :ivar developers: A `list` of developers for the app.
    :ivar header_image: A `str` link to the header image of the app.
    :ivar is_free: A `bool` on whether the app is free or not.
    :ivar linux_requirements: A `dict` containing information on the Linux requirements for the app.
    :ivar mac_requirements: A `dict` containing information on the Mac requirements for the app.
    :ivar metacritic: A `dict` containing the URL and score of the Metacritic review of the app, with keys `score` and `url`.
    :ivar name: A `str` of the app's name.
    :ivar pc_requirements: A `dict` containing information on the PC requirements for the app.
    :ivar platforms: A `dict` of Linux, PC, and Mac, with boolean values on whether they're available on there or not.
    :ivar price_overview: A `dict` of the price of the app, with information including the current price, discount percentage, and initial price.
    :ivar publishers: A `list` of publishers that the app has.
    :ivar recommendations: An `int` of the amount of recommendations the app has.
    :ivar release_date: A `str` of when the app was released.
    :ivar released: A `bool` of whether it's out yet or not.
    :ivar required_age: An `int` of the required age. Is 0 if none.
    :ivar reviews: A `str` of some of the acclaimed reviews linked on the store page.
    :ivar screenshots: A `list` of links to the screenshots of the app linked on the store page.
    :ivar short_description: 
    :ivar support_info: A `dict` on the support info of the app.
    :ivar supported_languages: A `str` of comma seperated languages.
    :ivar type: A `str` pf the type of app that it is.
    :ivar website: The linked website of the app as a `str`.
    :raises steamfront.errors.AppNotFound: Raised if the app provided can't be found.
    '''

    getGame = 'http://store.steampowered.com/api/appdetails?appids={}&format=json'

    def __init__(self, appid: str):

        # Get the site page
        appid = str(appid)
        sitestr = App.getGame.format(appid)
        site = _get(sitestr)
        rawdata = site.json()
        appdata = rawdata[appid]

        # Sees if you sucessfully got the data or not
        if not appdata['success']:
            raise _AppNotFound('The given app ID was not found.')

        # Internal command for getting new values
        def getvalue(value: str, *, second: str=None, error='NOPE', iterate: str=None, listed: bool=False):
            if iterate == None:
                try:
                    if second is not None:
                        return appdata['data'][value][second]
                    else:
                        return appdata['data'][value]
                except Exception as e:
                    return e if error == 'NOPE' else error
            else:
                try:
                    if listed == False:
                        return [i[iterate] for i in appdata['data'][value]]
                    else:
                        return [i[iterate] for i in appdata['data'][value][0]]
                except Exception as e:
                    return e if error == 'NOPE' else error

        # Game page found, now store the relevant data in attributes
        self.raw = appdata['data']

        self.about_the_game = getvalue('about_the_game', error=None)
        self.appid = getvalue('steam_appid')
        self.background = getvalue('background')
        self.categories = getvalue('categories', iterate='description')
        self.controller_support = getvalue('controller_support', error=None)
        self.detailed_description = getvalue('detailed_description', error=None)
        self.genres = getvalue('genres', iterate='description')
        self.developers = getvalue('developers')
        self.header_image = getvalue('header_image')
        self.is_free = getvalue('is_free')
        self.linux_requirements = getvalue('linux_requirements', error=None)
        self.mac_requirements = getvalue('linux_requirements', error=None)
        self.metacritic = getvalue('metacritic')
        self.name = getvalue('name')
        self.pc_requirements = getvalue('pc_requirements', error=None)
        self.platforms = getvalue('platforms')
        self.price_overview = getvalue('price_overview', error=None)
        self.publishers = getvalue('publishers')
        self.recommendations = getvalue('recommendations', iterate='total')
        self.release_date = getvalue('release_date', second='date', error=None)
        self.released = getvalue('release_date', second='coming_soon')
        self.required_age = getvalue('required_age')
        self.reviews = getvalue('reviews')
        self.screenshots = getvalue('screenshots', iterate='path_full', listed=True)
        self.short_description = getvalue('short_description', error=None)
        self.support_info = getvalue('support_info')
        self.supported_languages = getvalue('supported_languages')
        self.type = getvalue('type')
        self.website = getvalue('website', error=None)
        # self.packages = getvalue('packages')
        # self.movies = DOESNT FIT NICELY INTO GETVALUE
        # self.package_groups = I don't actually know what this is
        # self.legal_notice = Not relevant tbh
        # self.achievements = Can't get all so won't get any
        
