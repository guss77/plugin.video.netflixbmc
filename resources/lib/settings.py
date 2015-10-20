__author__ = 'corona'
import os
import xbmc
import xbmcaddon

addon = xbmcaddon.Addon()

addonID = addon.getAddonInfo('id')
osWin = xbmc.getCondVisibility('system.platform.windows')
osLinux = xbmc.getCondVisibility('system.platform.linux')
osOSX = xbmc.getCondVisibility('system.platform.osx')
osAndroid = xbmc.getCondVisibility('system.platform.android')
addonDir = xbmc.translatePath(addon.getAddonInfo('path'))
defaultFanart = os.path.join(addonDir ,'fanart.png')
addonUserDataFolder = xbmc.translatePath("special://profile/addon_data/"+addonID)
icon = xbmc.translatePath('special://home/addons/'+addonID+'/icon.png')
utilityPath = xbmc.translatePath('special://home/addons/'+addonID+'/resources/NetfliXBMC_Utility.exe')
sendKeysPath = xbmc.translatePath('special://home/addons/'+addonID+'/resources/NetfliXBMC_SendKeys.exe')
fakeVidPath = xbmc.translatePath('special://home/addons/'+addonID+'/resources/fakeVid.mp4')
downloadScript = xbmc.translatePath('special://home/addons/'+addonID+'/download.py')
browserScript = xbmc.translatePath('special://home/addons/'+addonID+'/browser.sh')
searchHistoryFolder = os.path.join(addonUserDataFolder, "history")
cacheFolder = os.path.join(addonUserDataFolder, "cache")
cacheFolderCoversTMDB = os.path.join(cacheFolder, "covers")
cacheFolderFanartTMDB = os.path.join(cacheFolder, "fanart")
libraryFolder = xbmc.translatePath(addon.getSetting("libraryPath"))
libraryFolderMovies = os.path.join(libraryFolder, "Movies")
libraryFolderTV = os.path.join(libraryFolder, "TV")
cookieFile = xbmc.translatePath("special://profile/addon_data/"+addonID+"/cookies")
sessionFile = xbmc.translatePath("special://profile/addon_data/"+addonID+"/session")
chromeUserDataFolder = os.path.join(addonUserDataFolder, "chrome-user-data")
dontUseKiosk = addon.getSetting("dontUseKiosk") == "true"
browseTvShows = addon.getSetting("browseTvShows") == "true"
isKidsProfile = addon.getSetting('isKidsProfile') == 'true'
showProfiles = addon.getSetting("showProfiles") == "true"
forceView = addon.getSetting("forceView") == "true"
useUtility = addon.getSetting("useUtility") == "true"
useChromeProfile = addon.getSetting("useChromeProfile") == "true"
remoteControl = addon.getSetting("remoteControl") == "true"
updateDB = addon.getSetting("updateDB") == "true"
useTMDb = addon.getSetting("useTMDb") == "true"
username = addon.getSetting("username")
password = addon.getSetting("password")
viewIdVideos = addon.getSetting("viewIdVideos")
viewIdEpisodes = addon.getSetting("viewIdEpisodesNew")
viewIdActivity = addon.getSetting("viewIdActivity")
winBrowser = int(addon.getSetting("winBrowserNew"))
language = addon.getSetting("language")
auth = addon.getSetting("auth")
authMyList = addon.getSetting("authMyList")
linuxUseShellScript = addon.getSetting("linuxUseShellScript") == "true"
debug_enabled = addon.getSetting("debug") == "true"
bug_reporting_enabled = addon.getSetting("send_bug_reports") == "true"

country = addon.getSetting("country")
if len(country)==0 and len(language.split("-"))>1:
    country = language.split("-")[1]

raven_dsn="https://1f1622b3b38d4e62a3d885d53a2ccf61:8a420bff60c84ee5b116b7c75ebf2aeb@sentry.alelec.net/2"