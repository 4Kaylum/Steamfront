# Intro

Steamfront is a basic interface for working with Steam and Steampowered through Python. It should be pretty simple to use, and if there's anything badly documented here, everything is available on Github for you to look through.

# Getting Started

There's quite basic usage. For most things you don't need an API key, but for others [you may need to get one](https://steamcommunity.com/dev/apikey).

First you need to make a `Steamfront` object.

```python
>>> import steamfront
>>> sf = steamfront.steamfront.Client()
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

[Click here](https://github.com/4Kaylum/Steamfront/wiki/API-Reference)