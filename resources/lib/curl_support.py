__author__ = 'corona'

import os
import xbmc
import xbmcplugin
import xbmcaddon
import xbmcvfs

from cookielib import CookieJar, FileCookieJar

from . import settings, util

addon = xbmcaddon.Addon()
addonID = addon.getAddonInfo('id')

import human_curl
import human_curl as requests
verify_ssl = True

cookies = FileCookieJar(settings.cookieFile)
if xbmcvfs.exists(settings.cookieFile):
    cookies.load(ignore_discard=True, ignore_expires=True)

def post(url, data, json=False):
    util.debug("URL: " + url)
    global cookies
    response = human_curl.post(url, data=data, verify=verify_ssl, cookies=cookies)

    if response.status_code != 200:
        util.debug("Error %s: %s" % (response.status_code, url))
        util.dialog("Error %s: %s" % (response.status_code, url))
    else:
        cookies = response.cookies
        return response.json if json else response.content

def get(url, json=False):
    util.debug("URL: " + url)
    global cookies
    response = human_curl.get(url, verify=verify_ssl, cookies=cookies)
    assert isinstance(response, human_curl.Response)
    if response.status_code != 200:
        util.debug("Error %s: %s" % (response.status_code, url))
        util.dialog("Error %s: %s" % (response.status_code, url))
    else:
        cookies = response.cookies
        return response.json if json else response.content


def saveState():
    global cookies
    if isinstance(cookies, FileCookieJar):
        cookies.save()
    else:
        util.debug("Not sure what to do with cookies")