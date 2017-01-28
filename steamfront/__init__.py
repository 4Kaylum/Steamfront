from __future__ import print_function
from .client import Client

__title__ = 'Steamfront'
__author__ = 'Callum Bartlett'
__license__ = 'MIT'
__copyright__ = 'Copyright 2017 Callum Bartlett'
__version__ = '0.0.5'

if __name__ == '__main__':
	from sys import argv

	if len(argv) < 2:
		print('Please give the name of a game you want to find the information of.')
	gameName = ' '.join(argv[1:])
	c = Client()
	g = c.getApp(name=gameName)
	i = '{0.name} :: {0.appid} :: {0.type}'
	print(i.format(g))
