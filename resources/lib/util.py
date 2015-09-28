__author__ = 'corona'
import xbmc
import xbmcgui

from . import settings

def debug(message):
    if settings.debug_enabled:
        print message

def notify(message, displaytime=10000):
    xbmc.executebuiltin('XBMC.Notification(%s,%d,%s)' % (message, displaytime, settings.icon))

def dialog(message, title='IMPORTANT!'):
    xbmcgui.Dialog().ok(title, message)

