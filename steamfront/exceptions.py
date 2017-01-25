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
