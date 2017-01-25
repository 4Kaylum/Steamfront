# Intro

Steamfront is a basic interface for working with Steam and Steampowered through Python. It should be pretty simple to use, and if there's anything badly documented here, everything is available on Github for you to look through.

# Getting Started

There's quite basic usage. For most things you don't need an API key, but for others [you may need to get one](https://steamcommunity.com/dev/apikey).

First you need to make a `Steamfront` object.

```python
>>> import steamfront
>>> sf = steamfront.Steamfront()
```

From there, you can get information on a game (through either name or ID), or list the games that a user has, through several methods each.

Games:
```python
>>> g = sf.get_game_from_id('530620')
>>> g.name
'Resident Evil 7 / Biohazard 7 Teaser: Beginning Hour'
>>> g.required_age
'18'
>>> g = sf.get_game_from_name('Undertale')
>>> g.game_id
'391540'
```

Users:
```python
>>> u = sf.get_user_from_name('Kaylum-')
>>> u.id64
'76561198054243905'
>>> gz = u.games
>>> len(gz)
138
>>> g = gz[0]
>>> g.name
'Terraria'
>>> g.play_time
'221'
```

Most code is fully internally documented, so it will autofill and properly interface with Python's `help` function.

# API Reference

## Steamfront Class

### Attributes

* `api_key: str`
	* Is the key you put in on the initialization of the function. `None` if nothing was input.

### Methods

#### \_\_init\_\_

* Parameters
	* `*api_key: str = None` 
		* Your Steam API key. Defaults to `None`.
* Returns
	* Steamfront

#### get_game_from_id

* Parameters
	* `appid: str`
		* The app ID of the game you're getting.
* Returns
	* `Game`
* Raises
	* `GameDoesNotExist`
		* If the ID of the game is unable to be found through the API, `GameDoesNotExist` will be thrown.

#### get_game_from_name

This is going to be considerably less accurate than getting a game from its ID, but still works for quite a few things.

* Parameters
	* `name: str`
		* The name of the game you're getting.
	* `*refresh: bool = False`
		* Whether or not to refresh the internal storage of games.
	* `*case_sensitive: bool = True`
		* Whether or not the title you're searching is case sensitive.
* Returns
	* `Game`
		* If a game is found, its `Game` object will be returned.
	* `False`
		* If no game with the title can be found, `False` is returned.
* Raises
	* `GameDoesNotExist`
		* In rare cases, a game ID may be internally stored for a game that does not exist.

#### get_games_from_search

This should be used if you're trying to get multiple search results.

* Parameters
	* `name: str`
		* The name of the game you're getting.
	* `*refresh: bool = False`
		* Whether or not to refresh the internal storage of games.
	* `*case_sensitive: bool = True`
		* Whether or not the title you're searching is case sensitive.
* Returns
	* `list`
		* A list of `tuple` will be returned, with the tuple being in terms of `('NAME', 'appid')`.
		* Will return an empty list if no search results can be found.

#### get_user_from_name

* Parameters
	* `name: str`
		* The name of the user.
* Returns
	* `User`
* Raises
	* `UserDoesNotExist`
		* If the user's name does not exist on Steam, this will be thrown.

#### get_user_from_id

* Parameters
	* `id64: str`
		* The id64 of the user.
* Returns
	* `User`
* Raises
	* `UserDoesNotExist`
		* If the user's name does not exist on Steam, this will be thrown.

## Game Class

### Attributes

* `game_id: str`
	* The game's ID.
* `raw: json`
	* The raw JSON data of the game.
* `type: str`
	* The type of app that was retrieved.
* `required_age: int`
	* The required age to view the game data. Will be 0 if there is no required age.
* `detailed_description: str`
* `about_the_game: str`
* `developers`
* `publishers`
* `categories`
* `genres`
* `screenshots`
* `release_date`
* `price`
* `dlc`
* `description`
* `metacritic`
* `name`

### Methods

#### \_\_str\_\_

* Returns
	* `str`
		* The ID of the game.

## User Class

### Attributes

* `root`
* `id64`
* `id`
* `games`

### Methods

#### \_\_str\_\_

* Returns
	* `str`
		* The user's ID (name).

## UserGame Class

The relation between a user and a game.

### Attributes

* `game`
* `raw`
* `name`
* `game_id`
* `store_link`
* `stats`
* `player_stats`
* `play_time`

### Methods

#### \_\_str\_\_

* Returns
	* `str`
		* The ID of the game.

#### get_game

* Returns
	* `Game`
		* The `Game` object generated from the internally stored ID.
