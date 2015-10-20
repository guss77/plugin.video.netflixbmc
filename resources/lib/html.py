__author__ = 'corona'
import xbmcaddon
import xbmcgui
from . import util

addon = xbmcaddon.Addon()

verify_ssl = False
# if addon.getSetting("sslEnable") == "true":
# if False:
if True:
    try:
        from .curl_support import *
        verify_ssl = True
        using_pycurl = True
    except:
        util.handle_exception()
        import traceback
        print traceback.format_exc()
        print "ERROR importing OpenSSL handler"

        xbmcgui.Dialog().ok('IMPORTANT!', 'human_curl module not working. Please post kodi log to the forum.')
        addon.setSetting("sslEnable", "false")

if not verify_ssl:
    from .requests_support import *



def postContent(url, data, allow_redirects=True, expected_status=None, headers=None):
    try:
        return post(url, data, allow_redirects, expected_status, headers).content
    except AttributeError:
        return None

def postJson(url, data, allow_redirects=True, expected_status=None, headers=None):
    try:
        return post(url, data, allow_redirects, expected_status, headers).json
    except AttributeError:
        return None


def getContent(url, allow_redirects=True, expected_status=None, headers=None):
    try:
        return get(url, allow_redirects, expected_status, headers).content
    except AttributeError:
        return None

def getJson(url, allow_redirects=True, expected_status=None, headers=None):
    try:
        return get(url, allow_redirects, expected_status, headers).json
    except AttributeError:
        return None
