from .app import App as _App


class UserApp(_App):
    '''
    An object based on the relationship between a user and an app. A subclass of :class:`steamfront.app.App`. 
    This will not contain any of the attributes for :class:`steamfront.app.App` until :meth unlazify: has been called.
    Should not be called manually - will be automatically generated with a :class:`steamfront.user.User` instance.

    :param dict appdata: The app data that came from the API through the user.
    :param steamfront.user.User user: The user to whom the app belongs.
    :ivar player_id: A `str` containing the player's ID.
    :ivar play_time: An `int` containing how many hours the user has in the app.
    :ivar player: The :class:`steamfront.user.User` to whom the app belongs.
    :ivar lazy: A `bool` representing whether or not the object has all of its aspects from :class:`steamfront.app.App`.
    '''

    def __init__(self, appdata:dict, user, lazy=True):

        self.appid = str(appdata['appid'])
        self.play_time = appdata['playtime_forever']
        self.player_id = user.id64
        self.player = user

        if lazy == False:
            super().__init__(self.appid)
        self.lazy = lazy

    def unlazify(self):
        '''
        To get all of the app attributes of an app, this must be called.
        '''

        self.lazy = False 
        super().__init__(self.appid)
