from .steamfront import *
from .game import *
from .exceptions import *
from .user import *

try:
	from collections import namedtuple
except ImportError:
	VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')
	version_info = VersionInfo(major=0, minor=0, micro=2, releaselevel='final', serial=0)

__title__ = 'Steamfront'
__author__ = 'Callum Bartlett'
__license__ = 'MIT'
__copyright__ = 'Copyright 2017 Callum Bartlett'
__version__ = '0.0.2'
