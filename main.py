# -*- coding: utf-8 -*-

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "resources/lib")))

from resources.lib import kodilogging
from resources.lib import service

import logging
import xbmcaddon

# Keep this file to a minimum, as Kodi
# doesn't keep a compiled copy of this
ADDON = xbmcaddon.Addon()
kodilogging.config()

service.run()


