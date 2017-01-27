# Intro

Steamfront is a basic interface for working with Steam and Steampowered through Python. It should be pretty simple to use, and if there's anything badly documented here, everything is available on Github for you to look through.

**Installation**:
```bash
pip install steamfront
```

# Getting Started

There's quite basic usage. For most things you don't need an API key, but for others [you may need to get one](https://steamcommunity.com/dev/apikey).

First you need to make a `Client` object.

```python
>>> import steamfront
>>> client = steamfront.Client()
```

From there, you can get information on a game (through either name or ID), or list the games that a user has, through several methods each.

**Games**:
```python
>>> game = client.getApp(appid='530620')
>>> game.name
'Resident Evil 7 / Biohazard 7 Teaser: Beginning Hour'
>>> game.required_age
'18'
>>> game = client.getApp(name='Undertale')
>>> game.game_id
'391540'
```

**Users**:
```python
>>>
>>> "THIS IS NOT AT ALL TRUE. THIS IS IN DEVELOPMENT. PLEASE IGNORE THIS FOR NOW."
>>>
>>> u = client.get_user_from_name('Kaylum-')
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

[Click here](https://steamfront.readthedocs.io/en/latest/index.html)