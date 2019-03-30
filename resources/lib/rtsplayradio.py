# -*- coding: utf-8 -*-

# Copyright (C) 2019 Alexander Seiler
#
#
# This file is part of plugin.audio.rtsplayradio.
#
# plugin.audio.rtsplayradio is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# plugin.audio.rtsplayradio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with plugin.audio.rtsplayradio.
# If not, see <http://www.gnu.org/licenses/>.

import sys
import traceback

try:  # Python 3
    from urllib.parse import unquote_plus
    from urllib.parse import parse_qsl
except ImportError:  # Python 2
    from urlparse import parse_qsl
    from urllib import unquote_plus

from kodi_six import xbmc, xbmcaddon, xbmcplugin
import srgssr

ADDON_ID = 'plugin.audio.rtsplayradio'
REAL_SETTINGS = xbmcaddon.Addon(id=ADDON_ID)
ADDON_NAME = REAL_SETTINGS.getAddonInfo('name')
ADDON_VERSION = REAL_SETTINGS.getAddonInfo('version')
DEBUG = REAL_SETTINGS.getSettingBool('Enable_Debugging')
CONTENT_TYPE = 'episodes'


class RTSPlayRadio(srgssr.SRGSSR):
    def __init__(self):
        super(RTSPlayRadio, self).__init__(
            int(sys.argv[1]), bu='rts', addon_id=ADDON_ID)


def log(msg, level=xbmc.LOGDEBUG):
    """
    Logs a message using Kodi's logging interface.

    Keyword arguments:
    msg   -- the message to log
    level -- the logging level
    """
    if DEBUG:
        if level == xbmc.LOGERROR:
            msg += ' ,' + traceback.format_exc()
    xbmc.log(ADDON_ID + '-' + ADDON_VERSION + '-' + msg, level)


def get_params():
    return dict(parse_qsl(sys.argv[2][1:]))


def run():
    """
    Run the plugin.
    """
    params = get_params()
    try:
        url = unquote_plus(params["url"])
    except Exception:
        url = None
    try:
        name = unquote_plus(params["name"])
    except Exception:
        name = None
    try:
        mode = int(params["mode"])
    except Exception:
        mode = None
    try:
        page_hash = unquote_plus(params['page_hash'])
    except Exception:
        page_hash = None
    try:
        page = unquote_plus(params['page'])
    except Exception:
        page = None

    log('run, mode = %s, url = %s, name = %s, page_hash = %s, '
        'page = %s' % (mode, url, name, page_hash, page))

    if mode is None:
        identifiers = [
            'All_Shows',
            # 'Shows_Topics',
            'Favourite_Shows',
            'Newest_Favourite_Shows',
            'Radio_Channels',
            # 'Newest_Audios',
            'Most_Listened',
            'Live_Radio',
        ]
        RTSPlayRadio().build_main_menu(identifiers)
    elif mode == 10:
        RTSPlayRadio().build_shows_menu('radio')
    elif mode == 11:
        RTSPlayRadio().build_favourite_radio_shows_menu()
    elif mode == 12:
        RTSPlayRadio().build_newest_favourite_menu(page=page, audio=True)
    elif mode == 19:
        RTSPlayRadio().manage_favourite_shows(audio=True)
    elif mode == 20:
        RTSPlayRadio().build_show_menu(name, page_hash=page_hash, audio=True)
    elif mode == 21:
        RTSPlayRadio().build_episode_menu(name, audio=True)
    elif mode == 40:
        RTSPlayRadio().build_radio_channels_menu()
    elif mode == 41:
        RTSPlayRadio().build_radio_channel_overview(name)
    elif mode == 42:
        RTSPlayRadio().build_shows_menu('radio', channel_id=name)
    elif mode == 43:
        RTSPlayRadio().build_audio_menu('Newest', 43, name, page=page)
    elif mode == 44:
        RTSPlayRadio().build_audio_menu('Most clicked', 44, name, page=page)
    # elif mode == 45:
    #     RTSPlayRadio().build_audio_menu('Newest', 45, page=page)
    elif mode == 46:
        RTSPlayRadio().build_audio_menu('Most clicked', 46, page=page)
    elif mode == 47:
        RTSPlayRadio().build_live_radio_menu()
    elif mode == 48:
        RTSPlayRadio().build_radio_topics_menu()
    # elif mode == 49:
    #     RTSPlayRadio().build_radio_shows_by_topic(name)
    elif mode == 50:
        RTSPlayRadio().play_video(name, audio=True)
    elif mode == 51:
        RTSPlayRadio().play_livestream(name)

    xbmcplugin.setContent(int(sys.argv[1]), CONTENT_TYPE)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_UNSORTED)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE)
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
