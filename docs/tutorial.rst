Basic Usage
======================================

Intro
--------------------

Steamfront is a basic interface for working with Steam and Steampowered through Python. It should be pretty simple to use, and if there's anything badly documented here, everything is available on Github for you to look through.

**Installation**:

.. code-block:: bash

	pip install steamfront


Getting Started
--------------------

There's quite basic usage. For most things you don't need an API key, but for others `you may need to get one`__.

__ https://steamcommunity.com/dev/apikey

First you need to make a `Client` object.

.. code-block:: python

	>>> import steamfront
	>>> client = steamfront.Client()

From there, you can get information on a game (through either name or ID), or list the games that a user has, through several methods each.

**Games**:

.. code-block:: python

	>>> client = steamfront.Client()
	>>> game = client.getApp(appid='530620')
	>>> game.name
	'Resident Evil 7 / Biohazard 7 Teaser: Beginning Hour'
	>>> game.required_age
	'18'
	>>> game = client.getApp(name='Undertale')
	>>> game.appid
	'391540'

**Users**:

.. code-block:: python

	>>> client = steamfront.Client(API_KEY)
	>>> user = client.getUser(id64='76561198054243905')
	>>> user.name
	'Kaylum-'
	>>> user.status
	'Online'
	>>> apps = user.apps
	>>> len(apps)
	137
	>>> rand = apps[44]
	>>> rand.play_time
	409

Most code is fully internally documented, so it will autofill and properly interface with Python's `help` function.
