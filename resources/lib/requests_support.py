__author__ = 'corona'

import os
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmcvfs

from . import settings, util

try:
    import cPickle as pickle
except ImportError:
    import pickle


addon = xbmcaddon.Addon()
addonID = addon.getAddonInfo('id')


import requests
verify_ssl = False
print "SSL verification is disabled"

#supress warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl

class SSLAdapter(HTTPAdapter):
    '''An HTTPS Transport Adapter that uses an arbitrary SSL version.'''
    def init_poolmanager(self, connections, maxsize, block=False):
        ssl_version = addon.getSetting("sslSetting")
        ssl_version = None if ssl_version == 'Auto' else ssl_version
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl_version)

def newSession():
    s = requests.Session()
    s.mount('https://', SSLAdapter())
    s.headers.update({
        'User-Agent': 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20130331 Firefox/21.0',
    })
    return s

def post(url, data, json=False):
    util.debug("URL: " + url)

    response = session.post(url, data=data, verify=verify_ssl)

    if response.status_code != 200:
        util.debug("Error %s: %s" % (response.status_code, url))
        util.dialog("Error %s: %s" % (response.status_code, url))
    else:
        return response.json if json else response.content



def get(url, json=False):
    util.debug("URL: " + url)

    response = session.get(url, verify=verify_ssl).text

    if response.status_code != 200:
        util.debug("Error %s: %s" % (response.status_code, url))
        util.dialog("Error %s: %s" % (response.status_code, url))
    else:
        return response.json if json else response.content


def saveState():
    global session
    tempfile = settings.sessionFile+".tmp"
    if xbmcvfs.exists(tempfile):
        xbmcvfs.delete(tempfile)
    ser = pickle.dumps(session)
    fh = xbmcvfs.File(tempfile, 'wb')
    fh.write(ser)
    fh.close()
    if xbmcvfs.exists(settings.sessionFile):
        xbmcvfs.delete(settings.sessionFile)
    xbmcvfs.rename(tempfile, settings.sessionFile)


## Create session object for reuse

if os.path.exists(settings.sessionFile):
    fh = xbmcvfs.File(settings.sessionFile, 'rb')
    content = fh.read()
    fh.close()
    session = pickle.loads(content)
else:
    session = newSession()

