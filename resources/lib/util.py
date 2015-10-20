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

def clean_filename(n, chars=None):
    if isinstance(n, str):
        return (''.join(c for c in unicode(n, "utf-8") if c not in '/\\:?"*|<>')).strip(chars)
    elif isinstance(n, unicode):
        return (''.join(c for c in n if c not in '/\\:?"*|<>')).strip(chars)

def handle_exception():
    if settings.bug_reporting_enabled:
        import raven
        raven.Client(settings.raven_dsn).captureException()
