__author__ = 'corona'

import os
import xbmc
import xbmcplugin
import xbmcaddon
import xbmcvfs

from cookielib import CookieJar, MozillaCookieJar, DefaultCookiePolicy

from . import settings, util

addon = xbmcaddon.Addon()
addonID = addon.getAddonInfo('id')

import human_curl
import human_curl as requests
verify_ssl = True

MAX_REDIRECTS=5

USER_AGENT="Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
# USER_AGENT='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20130331 Firefox/21.0'

# _policy=DefaultCookiePolicy()#allowed_domains="netflix.com")
# cookies = MozillaCookieJar(settings.cookieFile)#,
#                            #policy=_policy)
# cookies=CookieJar()

# if xbmcvfs.exists(settings.cookieFile):
#     cookies.load(ignore_discard=True, ignore_expires=True)

def post(url, data, allow_redirects=True, expected_status=None, headers=None):
    if not expected_status:
        expected_status = [200]
    util.debug("URL: " + url)
    cookiefile = settings.cookieFile if settings.cookieFile else None
    response = human_curl.post(url,
                               data=data,
                               verify=verify_ssl,
                               cookies=cookiefile,
                               allow_redirects=allow_redirects,
                               max_redirects=MAX_REDIRECTS,
                               user_agent=USER_AGENT,
                               headers=headers)

    if response.status_code not in expected_status:
        util.debug("Error %s: %s" % (response.status_code, url))
        util.dialog("Error %s: %s" % (response.status_code, url))
    else:
        # cookies.extract_cookies(response, response.request)
        return response

def get(url, allow_redirects=True, expected_status=None, headers=None):
    if not expected_status:
        expected_status = [200]
    util.debug("URL: " + url)
    cookiefile = settings.cookieFile if settings.cookieFile else None
    response = human_curl.get(url,
                              verify=verify_ssl,
                              cookies=cookiefile,
                              allow_redirects=allow_redirects,
                              max_redirects=MAX_REDIRECTS,
                              user_agent=USER_AGENT,
                              headers=headers)

    if response.status_code not in expected_status:
        util.debug("Error %s: %s" % (response.status_code, url))
        util.dialog("Error %s: %s" % (response.status_code, url))
    else:
        # cookies.extract_cookies(response, response.request)
        return response

def saveState():
    """
    Not needed with pycurl set to automatically save cookies.
    :return:
    """
    pass
    # global cookies
    # if isinstance(cookies, MozillaCookieJar):
    #     cookies.save(settings.cookieFile)
    # else:
    #     util.debug("Not sure what to do with cookies")