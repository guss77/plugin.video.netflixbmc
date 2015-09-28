#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import socket
import cookielib
import sys
import re
import os
import json
import time
import shutil
import subprocess
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmcvfs
 
 
socket.setdefaulttimeout(30)
pluginhandle = int(sys.argv[1])
addon = xbmcaddon.Addon()
addonID = addon.getAddonInfo('id')
cj = cookielib.MozillaCookieJar()
urlMain = "http://www.netflix.com"
osWin = xbmc.getCondVisibility('system.platform.windows')
osLinux = xbmc.getCondVisibility('system.platform.linux')
osOsx = xbmc.getCondVisibility('system.platform.osx')
addonDir = xbmc.translatePath(addon.getAddonInfo('path'))
defaultFanart = os.path.join(addonDir ,'fanart.png')
addonUserDataFolder = xbmc.translatePath("special://profile/addon_data/"+addonID)
icon = xbmc.translatePath('special://home/addons/'+addonID+'/icon.png')
utilityPath = xbmc.translatePath('special://home/addons/'+addonID+'/resources/NetfliXBMC_Utility.exe')
sendKeysPath = xbmc.translatePath('special://home/addons/'+addonID+'/resources/NetfliXBMC_SendKeys.exe')
fakeVidPath = xbmc.translatePath('special://home/addons/'+addonID+'/resources/fakeVid.mp4')
downloadScript = xbmc.translatePath('special://home/addons/'+addonID+'/download.py')
searchHistoryFolder = os.path.join(addonUserDataFolder, "history")
cacheFolder = os.path.join(addonUserDataFolder, "cache")
cacheFolderCoversTMDB = os.path.join(cacheFolder, "covers")
cacheFolderFanartTMDB = os.path.join(cacheFolder, "fanart")
libraryFolder = xbmc.translatePath(addon.getSetting("libraryPath"))
libraryFolderMovies = os.path.join(libraryFolder, "Movies")
libraryFolderTV = os.path.join(libraryFolder, "TV")
cookieFile = xbmc.translatePath("special://profile/addon_data/"+addonID+"/cookies")
authIDFile = xbmc.translatePath("special://profile/addon_data/"+addonID+"/authID")
dontUseKiosk = addon.getSetting("dontUseKiosk") == "true"
browseTvShows = addon.getSetting("browseTvShows") == "true"
singleProfile = addon.getSetting("singleProfile") == "true"
showProfiles = addon.getSetting("showProfiles") == "true"
forceView = addon.getSetting("forceView") == "true"
useUtility = addon.getSetting("useUtility") == "true"
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
if len(language.split("-"))>1:
    country = language.split("-")[1]
 
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
userAgent = "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0"
opener.addheaders = [('User-agent', userAgent)]
 
if not os.path.isdir(addonUserDataFolder):
    os.mkdir(addonUserDataFolder)
if not os.path.isdir(cacheFolder):
    os.mkdir(cacheFolder)
if not os.path.isdir(cacheFolderCoversTMDB):
    os.mkdir(cacheFolderCoversTMDB)
if not os.path.isdir(cacheFolderFanartTMDB):
    os.mkdir(cacheFolderFanartTMDB)
if not os.path.isdir(libraryFolder):
    xbmcvfs.mkdir(libraryFolder)
if not os.path.isdir(libraryFolderMovies):
    xbmcvfs.mkdir(libraryFolderMovies)
if not os.path.isdir(libraryFolderTV):
    xbmcvfs.mkdir(libraryFolderTV)
if os.path.exists(cookieFile):
    cj.load(cookieFile)
 
# TODO: finish authID caching so the REST API can be called directly
# without going through a full page load
class AuthID:
    def __init__(self, filename):
        self.filename = filename
        self.ts = None
        self.value = None
   
    def isExpired(self):
        if self.ts == None:
            return true
   
    def load(self):
        with open(filename) as f:
            self.ts = int(f.readline().strip())
            self.value = f.readline().strip()
   
    def save(self):
        with open(filename, "w") as f:
            f.write(str(self.ts) + "\n")
            f.write(self.value + "\n")
 
authID = AuthID(authIDFile)
if os.path.exists(authIDFile):
    authID.load()
 
while (username == "" or password == ""):
    addon.openSettings()
    username = addon.getSetting("username")
    password = addon.getSetting("password")
 
if not addon.getSetting("html5MessageShown"):
    dialog = xbmcgui.Dialog()
    ok = dialog.ok('IMPORTANT!', 'NetfliXBMC >=1.3.0 only supports the new Netflix HTML5 User Interface! The only browsers working with HTML5 DRM playback for now are Chrome>=37 (Win/OSX/Linux) and IExplorer>=11 (Win8.1 only). Make sure you have the latest version installed and check your Netflix settings. Using Silverlight may still partially work, but its not supported anymore. The HTML5 Player is also much faster, supports 1080p and gives you a smoother playback (especially on Linux). See forum.xbmc.org for more info...')
    addon.setSetting("html5MessageShown", "true")
 
   
def index():
    #if login():
    addDir(translation(30011), "", 'main', "", "movie")
    addDir(translation(30012), "", 'main', "", "tv")
    addDir(translation(30143), "", 'wiHome', "", "both")
    xbmcplugin.endOfDirectory(pluginhandle)
 
 
def main(type):
    print "Main"
    xbmcplugin.setContent(pluginhandle, "movies")
    addDir(translation(30002), urlMain+"/browse/my-list", 'myList', "", type)
    addDir(translation(30010), "", 'listViewingActivity', "", type)
    addDir(translation(30003), urlMain+"/browse/new-arrivals", 'newArrivals', "", type)
    if type=="tv":
        addDir(translation(30005), urlMain+"/browse/genre/83", 'listFiltered', "", type)
        addDir(translation(30007), "", 'listTvGenres', "", type)
    else:
        addDir(translation(30007), urlMain + "/browse", 'listMovieGenres', "", type)
    addDir(translation(30008), "", 'search', "", type)
    xbmcplugin.endOfDirectory(pluginhandle)
 
 
def wiHome(type):
    if not singleProfile:
        setProfile()
    content = opener.open(urlMain+"/WiHome").read()
    match1 = re.compile('<div class="mrow(.+?)"><div class="hd clearfix"><h3> (.+?)</h3></div><div class="bd clearfix"><div class="slider triangleBtns " id="(.+?)"', re.DOTALL).findall(content)
    match2 = re.compile('class="hd clearfix"><h3><a href="(.+?)">(.+?)<', re.DOTALL).findall(content)
    for temp, title, sliderID in match1:
        if not "hide-completely" in temp:
            addDir(title.strip(), sliderID, 'listSliderVideos', "", type)
    for url, title in match2:
        if "WiAltGenre" in url or "WiSimilarsByViewType" in url or "WiRecentAdditionsGallery" in url:
            addDir(title.strip(), url, 'listVideos', "", type)
    xbmcplugin.endOfDirectory(pluginhandle)
 
PAGE_SIZE = 100
 
def myList(url, type):
    (apidata, data) = getNetflixPage("/browse/my-list")
    addVideos(data["videos"], "myList", type, 0, 9999999)
 
def addVideos(vdict, op, type, startIndex, pageSize):
    xbmcplugin.setContent(pluginhandle, "movies")
    n = 0
    for videoId in vdict.keys():
        if videoId == "size" or videoId == "$size":
            continue
        n = n + 1
        print "VideoID: " + videoId
        vdata = vdict[videoId]
        if type == "tv" and vdata["summary"]["type"] == "show":
            listVideoFromJson(videoId, vdata, type, "listSeasons")
        elif type == "movie" and vdata["summary"]["type"] == "movie":
            listVideoFromJson(videoId, vdata, type, "playVideo")
        elif type == "both":
            if vdata["summary"]["type"] == "show":
                listVideoFromJson(videoId, vdata, type, "listSeasons")
            else:
                listVideoFromJson(videoId, vdata, type, "playVideo")
           
    if n == pageSize:
        nextFrom = startIndex + pageSize
        newUrl = re.sub("&from=[0-9]+", "", url) + "&from=" + str(nextFrom)
        addDir(translation(30001), newUrl, op, "", type)
    if op == "newArrivals" or op == "listFiltered" or op == "myList":
        xbmc.executebuiltin('Container.SetViewMode(500)')
    else:
        xbmc.executebuiltin('Container.SetViewMode(504)')
    xbmcplugin.endOfDirectory(pluginhandle)
 
def newArrivals(url, type):
    xbmcplugin.setContent(pluginhandle, "movies")
    (apidata, data) = getNetflixPage("/browse/new-arrivals")
    startIndex = getStartIndex(url)
    rid = getNewReleasesId(data)
    rid = rid.replace("SLW32-", "WWW-")
    data2 = getNetflixAjaxData(apidata, makeListsRequest(apidata, rid, startIndex, PAGE_SIZE))
    print "New arrivals: " + str(data2)
    addVideos(data2["value"]["videos"], "newArrivals", type, startIndex, PAGE_SIZE)
 
def listFiltered(url, type):
    (apidata, data) = getNetflixPage(url)
    gid = getGenreId(url)
    startIndex = getStartIndex(url)
    data2 = getNetflixAjaxData(apidata, makeFilteredRequest(apidata, gid, startIndex, PAGE_SIZE))
    addVideos(data2["value"]["videos"], "listFiltered", type, startIndex, PAGE_SIZE)
 
def makeFilteredRequest(apidata, gid, startIndex, pageSize):
    authURL = apidata["contextData"]["userInfo"]["data"]["authURL"]
    sgid = str(gid)
    sfrom = str(startIndex)
    sto = str(startIndex + pageSize - 1)
    return '{"paths":[["genres",%s,["id","length","name","trackIds","requestId"]],["genres",%s,"su",{"from":%s,"to":%s},["summary","title","info"]],["genres",%s,"su",{"from":%s,"to":%s},"boxarts","_342x192","jpg"],["genres",%s,"su","requestId"]],"authURL":"%s"}' % (sgid, sgid, sfrom, sto, sgid, sfrom, sto, sgid, authURL)
 
def getNetflixAjaxData(apidata, postdata):
    url = getNetflixAjaxUrl(apidata)
    print "POST: " + postdata
    content = opener.open(url, postdata).read()
    return json.loads(content)
   
def getNetflixAjaxUrl(apidata):
    apiId = apidata["contextData"]["services"]["data"]["api"]["path"]
    return "http://www.netflix.com/" + "/".join(apiId) + "/pathEvaluator?withSize=true&materialize=true&model=harris&fallbackEsn=WWW"
   
def makeListsRequest(apidata, rid, startIndex, pageSize):
    authURL = apidata["contextData"]["userInfo"]["data"]["authURL"]
    return '{"paths":[["lists","%s",{"from":%s,"to":%s},["summary","title","releaseYear","userRating","runtime","synopsis"]],["lists","%s",{"from":1,"to":100},"boxarts","_342x192","jpg"]],"authURL":"%s"}' % (rid, str(startIndex), str(startIndex + pageSize - 1), rid, authURL)
 
def getNetflixPage(path):
    print "Get netflix page " + path
    if not singleProfile:
        setProfile()
    url = "http://www.netflix.com" + path
    print "Url: " + url
    content = opener.open(url).read()
    if not 'id="page-LOGIN"' in content:
        if singleProfile and '"showGate":{"data":true' in content:
            print "Got profiles page. Reloading..."
            #forceChooseProfile()
            content = opener.open(url).read()
            #print "Content: " + content
        content = content.replace("\\t","").replace("\\n", "").replace("\\", "")
        apiInfo = getJson(content, "netflix.reactContext")
        data = getJson(content, "netflix.falkorCache")
        return (apiInfo, data)
    else:
        deleteCookies()
        xbmc.executebuiltin('XBMC.Notification(NetfliXBMC:,'+str(translation(30127))+',15000,'+icon+')')
 
def getGenreId(url):
    print "GetGenreId url: " + url
    gre = re.compile("/browse/genre/([0-9]+)", re.DOTALL).findall(url)
    if gre:
        return gre[0]
    return None
 
def getStartIndex(url):
    pagerRe = re.compile('&from=(.+?)&', re.DOTALL).findall(url)
    startIndex = 0
    if pagerRe:
        startIndex = int(pagerRe[1])
    return startIndex
 
def getJson(content, varName):
    ix = content.find(varName + " = ")
    ix2 = content.find("</script>", ix)
    js = content[ix + len(varName) + 3:ix2]
    js = js[:js.rfind(";")]
    if js.find('"focalPoint":"{"') >= 0:
        #the broken kind. Hey, netflix, use a proper json encoder
        js = re.sub('"focalPoint":"\{[^{]+\}",', "", js)
        print "Had to fix json"
    #print "json: " + js
    try:
        return json.loads(js)
    except Exception as ex:
        print "Could not parse:\n--------\n" + js + "\n---------\n"
        raise ex
 
 
def getNewReleasesId(data):
    print str(data.keys())
    for key in data["lists"].keys():
        if data["lists"][key]["displayName"]["value"] == "New Releases":
            return key
    return None
 
def listSliderVideos(sliderID, type):
    pDialog = xbmcgui.DialogProgress()
    pDialog.create('NetfliXBMC', translation(30142)+"...")
    if not singleProfile:
        setProfile()
    xbmcplugin.setContent(pluginhandle, "movies")
    content = opener.open(urlMain+"/WiHome").read()
    if not 'id="page-LOGIN"' in content:
        if singleProfile and 'id="page-ProfilesGate"' in content:
            forceChooseProfile()
        else:
            content = content.replace("\\t","").replace("\\n", "").replace("\\", "")
            contentMain = content
            content = content[content.find('id="'+sliderID+'"'):]
            content = content[:content.find('class="ft"')]
            match = re.compile('<span id="dbs(.+?)_', re.DOTALL).findall(content)
            i = 1
            for videoID in match:
                listVideo(videoID, "", "", False, False, type)
                i+=1
            spl = contentMain.split('"remainderHTML":')
            for i in range(1, len(spl), 1):
                entry = spl[i]
                entry = entry[:entry.find('"rowId":')]
                if '"domId":"'+sliderID+'"' in entry:
                    match = re.compile('<span id="dbs(.+?)_', re.DOTALL).findall(entry)
                    i = 1
                    for videoID in match:
                        pDialog.update(i*100/(len(match)+10), translation(30142)+"...")
                        listVideo(videoID, "", "", False, False, type)
                        i+=1
            if forceView:
                xbmc.executebuiltin('Container.SetViewMode('+viewIdVideos+')')
            xbmcplugin.endOfDirectory(pluginhandle)
    else:
        deleteCookies()
        xbmc.executebuiltin('XBMC.Notification(NetfliXBMC:,'+str(translation(30127))+',15000,'+icon+')')
 
 
def listSearchVideos(url, type):
    pDialog = xbmcgui.DialogProgress()
    pDialog.create('NetfliXBMC', translation(30142)+"...")
    if not singleProfile:
        setProfile()
    xbmcplugin.setContent(pluginhandle, "movies")
    content = opener.open(url).read()
    content = json.loads(content)
    i = 1
    if "galleryVideos" in content:
        for item in content["galleryVideos"]["items"]:
            pDialog.update(i*100/len(content["galleryVideos"]["items"]), translation(30142)+"...")
            listVideo(str(item["id"]), "", "", False, False, type)
            i+=1
        if forceView:
            xbmc.executebuiltin('Container.SetViewMode('+viewIdVideos+')')
        xbmcplugin.endOfDirectory(pluginhandle)
    else:
        xbmc.executebuiltin('XBMC.Notification(NetfliXBMC:,'+str(translation(30146))+',5000,'+icon+')')
 
def listVideoFromJson(videoID, vdata, type, action):
    print "VDATA: " + str(vdata)
    if isinstance(vdata["title"], dict):
        title = vdata["title"]["value"]
    else:
        title = vdata["title"]
    synopsis = ""
    if "info" in vdata and "narrativeSynopsis" in vdata["info"]:
        synopsis = vdata["info"]["narrativeSynopsis"].encode("utf-8")
    if "synopsis" in vdata:
        synopsis = vdata["synopsis"].encode("utf-8")
    icon = ""
    if "boxarts" in vdata:
        for k in vdata["boxarts"].keys():
            if len(k) > 0 and k[0] == "_":
                if "jpg" in vdata["boxarts"][k]:
                    icon = vdata["boxarts"][k]["jpg"]["url"]
                elif "webp" in vdata["boxarts"][k]:
                    icon = vdata["boxarts"][k]["webp"]["url"]
    year = ""
    if "releaseYear" in vdata:
        year = str(vdata["releaseYear"])
    duration = ""
    if "runtime" in vdata:
        duration = str(vdata["runtime"]["value"])
        if duration == None:
            duration = ""
    rating = ""
    if "userRating" in vdata:
        rating = str(vdata["userRating"]["predicted"])
    if action == "listSeasons":
        #addDir(title.encode("utf-8"), urlMain+"/title/" + videoID, "listSeasons", icon, type)
        #addVideoDirR(name, url, mode, iconimage, videoType="", desc="", duration="", year="", mpaa="", director="", genre="", rating=""):
        addVideoDir(title.encode("utf-8"), (urlMain+"/title/" + videoID).encode("utf-8"), "listSeasons", icon, type,
            synopsis, duration, year, "", "", "", rating)
    else:
        videoType = "movie"
        if type == "tv":
            videoType = "tvshow"
        addVideoDirR(title.encode("utf-8"), videoID.encode("utf-8"), "playVideoMain", icon, videoType,
            synopsis, duration, year, "", "", "", rating)
    return True
 
def listVideo(videoID, title, thumbUrl, tvshowIsEpisode, hideMovies, type):
    videoDetails = getVideoInfo(videoID)
    match = re.compile('<span class="title.*?>(.+?)<', re.DOTALL).findall(videoDetails)
    if not title:
        title = match[0].strip()
    year = ""
    match = re.compile('<span class="year.*?>(.+?)<', re.DOTALL).findall(videoDetails)
    if match:
        year = match[0]
    if not thumbUrl:
        match = re.compile('src="(.+?)"', re.DOTALL).findall(videoDetails)
        thumbUrl = match[0].replace("/webp/","/images/").replace(".webp",".jpg")
    match = re.compile('<span class="mpaaRating.*?>(.+?)<', re.DOTALL).findall(videoDetails)
    mpaa = ""
    if match:
        mpaa = match[0]
    match = re.compile('<span class="duration.*?>(.+?)<', re.DOTALL).findall(videoDetails)
    duration = ""
    if match:
        duration = match[0].lower()
    if duration.split(' ')[-1] in ["minutes", "minutos", "minuter", "minutter", "minuuttia", "minuten"]:
        videoType = "movie"
        videoTypeTemp = videoType
        duration = duration.split(" ")[0]
    else:
        videoTypeTemp = "tv"
        if tvshowIsEpisode:
            videoType = "episode"
            year = ""
        else:
            videoType = "tvshow"
        duration = ""
    if useTMDb:
        yearTemp = year
        titleTemp = title
        if " - " in titleTemp:
            titleTemp = titleTemp[titleTemp.find(" - ")+3:]
        if ": " in titleTemp:
            titleTemp = titleTemp[:titleTemp.find(": ")]
        if "-" in yearTemp:
            yearTemp = yearTemp.split("-")[0]
        filename = (''.join(c for c in unicode(videoID, 'utf-8') if c not in '/\\:?"*|<>')).strip()+".jpg"
        filenameNone = (''.join(c for c in unicode(videoID, 'utf-8') if c not in '/\\:?"*|<>')).strip()+".none"
        coverFile = os.path.join(cacheFolderCoversTMDB, filename)
        coverFileNone = os.path.join(cacheFolderCoversTMDB, filenameNone)
        if not os.path.exists(coverFile) and not os.path.exists(coverFileNone):
            xbmc.executebuiltin('XBMC.RunScript('+downloadScript+', '+urllib.quote_plus(videoTypeTemp)+', '+urllib.quote_plus(videoID)+', '+urllib.quote_plus(titleTemp)+', '+urllib.quote_plus(yearTemp)+')')
    match = re.compile('src=".+?">.*?<.*?>(.+?)<', re.DOTALL).findall(videoDetails)
    desc = ""
    if match:
        desc = match[0].replace("&amp;", "&")
    match = re.compile('Director:</dt><dd>(.+?)<', re.DOTALL).findall(videoDetails)
    director = ""
    if match:
        director = match[0].strip()
    match = re.compile('<span class="genre.*?>(.+?)<', re.DOTALL).findall(videoDetails)
    genre = ""
    if match:
        genre = match[0]
    match = re.compile('<span class="rating.*?>(.+?)<', re.DOTALL).findall(videoDetails)
    rating = ""
    if rating:
        rating = match[0]
    title = title.replace("&amp;", "&")
    nextMode = "playVideoMain"
    if browseTvShows and videoType == "tvshow":
        nextMode = "listSeasons"
    added = False
    if "/MyList" in url and videoTypeTemp==type:
        addVideoDirR(title, videoID, nextMode, thumbUrl, videoType, desc, duration, year, mpaa, director, genre, rating)
        added = True
    elif videoType == "movie" and hideMovies:
        pass
    elif videoTypeTemp==type or type=="both":
        addVideoDir(title, videoID, nextMode, thumbUrl, videoType, desc, duration, year, mpaa, director, genre, rating)
        added = True
    return added
 
def makeListsGenresRequest(apidata, count):
    authURL = apidata["contextData"]["userInfo"]["data"]["authURL"]
    return '{"paths":[["genreList",{"from":0,"to":%s},["id","menuName"]],["genreList","summary"]],"authURL":"%s"}' % (str(count), authURL)
   
def listMovieGenres(url, type):
    (apidata, data) = getNetflixPage("/browse")
    data2 = getNetflixAjaxData(apidata, makeListsGenresRequest(apidata, 40))
    xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_LABEL)
    for key in data2["value"]["genres"].keys():
        if key == "$size" or key == "size" or key == "83":
            continue
        gid = data2["value"]["genres"][key]["id"]
        gname = data2["value"]["genres"][key]["menuName"]
        addDir(gname, "/browse/genre/" + str(gid), "listFiltered", "", type)
    xbmcplugin.endOfDirectory(pluginhandle)
 
def listTvGenres(url, type):
    (apidata, data) = getNetflixPage("/browse/genre/83")
    xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_LABEL)
    for key in data["genres"].keys():
        if key == "$size" or key == "size" or key == "83":
            continue
        print "Key: " + key
        print "Value: " + str(data["genres"][key])
        gid = data["genres"][key]["summary"]["id"]
        gname = data["genres"][key]["summary"]["menuName"]
        addDir(gname, "/browse/genre/" + str(gid), "listFiltered", "", type)
    xbmcplugin.endOfDirectory(pluginhandle)
 
def getSeriesId(url):
    print "GetSeriesId url: " + url
    gre = re.compile("/title/([0-9]+)", re.DOTALL).findall(url)
    if gre:
        return gre[0]
    return None
 
def makeSeasonListRequest(apidata, seriesId):
    authURL = apidata["contextData"]["userInfo"]["data"]["authURL"]
    return '{"paths":[["videos", %s, "seasonList", {"from": 0, "to": 40}, "summary"], ["videos", %s, "seasonList", "summary"]],"authURL":"%s"}' % (seriesId, seriesId, authURL)
   
def listSeasons(url, name, thumb):
    print "List Seasons"
    seriesId = getSeriesId(url)
    (apidata, data) = getNetflixPage("/browse/title/" + seriesId)
    data2 = getNetflixAjaxData(apidata, makeSeasonListRequest(apidata, seriesId))
    #print "Seasons list: " + str(data2)
    sort = []
    addVideoDirR("Play Next Episode", seriesId.encode("utf-8"), "playVideoMain", thumb, "tvshow", "", "", "", "", "", "", "")
    standardNames = True
    for key in data2["value"]["seasons"].keys():
        if key == "$size" or key == "size":
            continue
        name = data2["value"]["seasons"][key]["summary"]["name"]
        sort.append([key, name])
        if not re.match("Season [0-9]+", name):
            standardNames = False
    if standardNames:
        sort = sorted(sort, key = lambda x: int(x[1].split(" ")[1]))
    else:
        sort = sorted(sort, key = lambda x: x[1])
    for ix in sort:
        key = ix[0]
        val = data2["value"]["seasons"][key]
        seasonId = val["summary"]["id"]
        addSeasonDir(val["summary"]["name"].encode("utf-8"), str(seasonId), 'listEpisodes', thumb, name, str(seriesId))
    xbmcplugin.endOfDirectory(pluginhandle)
 
def makeEpisodeListRequest(apidata, seasonId):
    authURL = apidata["contextData"]["userInfo"]["data"]["authURL"]
    return '{"paths":[["seasons", %s, "episodes", {"from": -1, "to": 40}, ["summary", "title", "synopsis", "runtime"]], ["seasons", %s, "episodes", {"from": -1, "to": 40}, "interestingMoment", "_260x146", "jpg"], ["seasons", %s, "episodes", "summary"]],"authURL":"%s"}' % (seasonId, seasonId, seasonId, authURL)
 
 
def listEpisodes(seriesId, seasonId):
    xbmcplugin.setContent(pluginhandle, "episodes")
    (apidata, data) = getNetflixPage("/browse/title/" + seriesId)
    data2 = getNetflixAjaxData(apidata, makeEpisodeListRequest(apidata, seasonId))
   
    sort = []
    for key in data2["value"]["videos"].keys():
        if key == "$size" or key == "size":
            continue
        sort.append([key, data2["value"]["videos"][key]["summary"]["episode"]])
    sort = sorted(sort, key = lambda x: x[1])
    for ix in sort:
        key = ix[0]
       
        val = data2["value"]["videos"][key]
        title = val["title"].encode("utf-8")
        episode = val["summary"]["episode"]
        season = val["summary"]["season"]
        synopsis = val["synopsis"]
        runtime = val["runtime"]
        eid = val["summary"]["id"]
        thumb = val["interestingMoment"]["_260x146"]["jpg"]["url"]
        print "Thumb: " + thumb
        addEpisodeDir("Episode " + str(episode) + " - " + title, str(eid), "playVideoMain", thumb, synopsis, str(runtime), str(season), str(episode), seriesId, "")
    xbmc.executebuiltin('Container.SetViewMode(504)')
    xbmcplugin.endOfDirectory(pluginhandle)
 
 
def listViewingActivity(type):
    pDialog = xbmcgui.DialogProgress()
    pDialog.create('NetfliXBMC', translation(30142)+"...")
    if not singleProfile:
        setProfile()
    xbmcplugin.setContent(pluginhandle, "movies")
    content = opener.open(urlMain+"/WiViewingActivity").read()
    count = 0
    videoIDs = []
    spl = content.split('<li data-series=')
    for i in range(1, len(spl), 1):
        entry = spl[i]
        pDialog.update((count+1)*100/len(spl), translation(30142)+"...")
        matchId1 = re.compile('"(.*?)"', re.DOTALL).findall(entry)
        matchId2 = re.compile('data-movieid="(.*?)"', re.DOTALL).findall(entry)
        if matchId1[0]:
            videoID = matchId1[0]
        elif matchId2[0]:
            videoID = matchId2[0]
        match = re.compile('class="col date nowrap">(.+?)<', re.DOTALL).findall(entry)
        date = match[0]
        matchTitle1 = re.compile('class="seriestitle">(.+?)</a>', re.DOTALL).findall(entry)
        matchTitle2 = re.compile('class="col title">.+?>(.+?)<', re.DOTALL).findall(entry)
        if matchId1[0]:
            title = matchTitle1[0].replace("&amp;", "&").replace("&quot;", '"').replace("</span>", "")
        elif matchId2[0]:
            title = matchTitle2[0]
        title = date+" - "+title
        if videoID not in videoIDs:
            videoIDs.append(videoID)
            added = listVideo(videoID, title, "", False, False, type)
            if added:
                count += 1
            if count == 40:
                break
    if forceView:
        xbmc.executebuiltin('Container.SetViewMode('+viewIdActivity+')')
    xbmcplugin.endOfDirectory(pluginhandle)
 
 
def getVideoInfo(videoID):
    cacheFile = os.path.join(cacheFolder, videoID+".cache")
    if os.path.exists(cacheFile):
        fh = xbmcvfs.File(cacheFile, 'r')
        content = fh.read()
        fh.close()
    else:
        content = opener.open(urlMain+"/JSON/BOB?movieid="+videoID).read()
        fh = xbmcvfs.File(cacheFile, 'w')
        fh.write(content)
        fh.close()
    return content.replace("\\t","").replace("\\n", "").replace("\\", "")
 
 
def getSeriesInfo(seriesID):
    cacheFile = os.path.join(cacheFolder, seriesID+"_episodes.cache")
    if os.path.exists(cacheFile) and (time.time()-os.path.getmtime(cacheFile) < 60*5):
        fh = xbmcvfs.File(cacheFile, 'r')
        content = fh.read()
        fh.close()
    else:
        url = "http://api-global.netflix.com/desktop/odp/episodes?languages="+language+"&forceEpisodes=true&routing=redirect&video="+seriesID+"&country="+country
        content = opener.open(url).read()
        fh = xbmcvfs.File(cacheFile, 'w')
        fh.write(content)
        fh.close()
    return content
 
 
def addMyListToLibrary():
    if not singleProfile:
        setProfile()
    content = opener.open(urlMain+"/MyList?leid=595&link=seeall").read()
    if not 'id="page-LOGIN"' in content:
        if singleProfile and 'id="page-ProfilesGate"' in content:
            forceChooseProfile()
        else:
            if '<div id="queue"' in content:
                content = content[content.find('<div id="queue"'):]
            content = content.replace("\\t","").replace("\\n", "").replace("\\", "")
            match1 = re.compile('<span id="dbs(.+?)_.+?alt=".+?"', re.DOTALL).findall(content)
            match2 = re.compile('<span class="title.*?"><a id="b(.+?)_', re.DOTALL).findall(content)
            match3 = re.compile('<a href="http://dvd.netflix.com/WiPlayer\?movieid=(.+?)&', re.DOTALL).findall(content)
            match4 = re.compile('<a class="playHover" href=".+?WiPlayer\?movieid=(.+?)&', re.DOTALL).findall(content)
            match5 = re.compile('"boxart":".+?","titleId":(.+?),', re.DOTALL).findall(content)
            if match1:
                match = match1
            elif match2:
                match = match2
            elif match3:
                match = match3
            elif match4:
                match = match4
            elif match5:
                match = match5
            for videoID in match:
                videoDetails = getVideoInfo(videoID)
                match = re.compile('<span class="title ".*?>(.+?)<\/span>', re.DOTALL).findall(videoDetails)
                title = match[0].strip()
                title = title.replace("&amp;", "&")
                match = re.compile('<span class="year".*?>(.+?)<\/span>', re.DOTALL).findall(videoDetails)
                year = ""
                if match:
                    year = match[0]
                match = re.compile('<span class="duration.*?".*?>(.+?)<\/span>', re.DOTALL).findall(videoDetails)
                duration = ""
                if match:
                    duration = match[0].lower()
                if "minutes" in duration:
                    try:
                        if year:
                            title = title+" ("+year+")"
                        addMovieToLibrary(videoID, title, False)
                    except:
                        pass
                else:
                    try:
                        addSeriesToLibrary(videoID, title, "", False)
                    except:
                        pass
            if updateDB:
                xbmc.executebuiltin('UpdateLibrary(video)')
 
 
def playVideo(id):
    playVideoMain(id)
    xbmc.sleep(5000)
    listitem = xbmcgui.ListItem(path=fakeVidPath)
    xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
    xbmc.PlayList(xbmc.PLAYLIST_VIDEO).clear()
     
 
def playVideoMain(id):
    xbmc.Player().stop()
    if singleProfile:
        url = urlMain+"/WiPlayer?movieid="+id
    else:
        token = ""
        if addon.getSetting("profile"):
            token = addon.getSetting("profile")
        url = "https://www.netflix.com/SwitchProfile?tkn="+token+"&nextpage="+urllib.quote_plus(urlMain+"/WiPlayer?movieid="+id)
    kiosk = "yes"
    if dontUseKiosk:
        kiosk = "no"
    if osOsx:
        xbmc.executebuiltin("RunPlugin(plugin://plugin.program.chrome.launcher/?url="+urllib.quote_plus(url)+"&mode=showSite&kiosk="+kiosk+")")
        try:
            xbmc.sleep(5000)
            subprocess.Popen('cliclick c:500,500', shell=True)
            subprocess.Popen('cliclick kp:arrow-up', shell=True)
            xbmc.sleep(5000)
            subprocess.Popen('cliclick c:500,500', shell=True)
            subprocess.Popen('cliclick kp:arrow-up', shell=True)
            xbmc.sleep(5000)
            subprocess.Popen('cliclick c:500,500', shell=True)
            subprocess.Popen('cliclick kp:arrow-up', shell=True)
        except:
            pass
    elif osLinux:
        xbmc.executebuiltin("RunPlugin(plugin://plugin.program.chrome.launcher/?url="+urllib.quote_plus(url)+"&mode=showSite&kiosk="+kiosk+")")
        try:
            xbmc.sleep(5000)
            subprocess.Popen('xdotool mousemove 9999 9999', shell=True)
            xbmc.sleep(5000)
            subprocess.Popen('xdotool mousemove 9999 9999', shell=True)
            xbmc.sleep(5000)
            subprocess.Popen('xdotool mousemove 9999 9999', shell=True)
        except:
            pass
    elif osWin:
        if winBrowser == 1:
            path = 'C:\\Program Files\\Internet Explorer\\iexplore.exe'
            path64 = 'C:\\Program Files (x86)\\Internet Explorer\\iexplore.exe'
            if os.path.exists(path):
                subprocess.Popen('"'+path+'" -k "'+url+'"', shell=False)
            elif os.path.exists(path64):
                subprocess.Popen('"'+path64+'" -k "'+url+'"', shell=False)
        else:
            xbmc.executebuiltin("RunPlugin(plugin://plugin.program.chrome.launcher/?url="+urllib.quote_plus(url)+"&mode=showSite&kiosk="+kiosk+")")
        if useUtility:
            subprocess.Popen('"'+utilityPath+'"', shell=False)
    if remoteControl:
        myWindow = window('window.xml', addon.getAddonInfo('path'), 'default',)
        myWindow.doModal()
       
 
def configureUtility():
    if osWin:
        subprocess.Popen('"'+utilityPath+'"'+' config=yes', shell=False)
 
 
def deleteCookies():
    if os.path.exists(cookieFile):
        os.remove(cookieFile)
        xbmc.executebuiltin('XBMC.Notification(NetfliXBMC:,Cookies have been deleted!,5000,'+icon+')')
 
 
def deleteCache():
    if os.path.exists(cacheFolder):
        try:
            shutil.rmtree(cacheFolder)
            xbmc.executebuiltin('XBMC.Notification(NetfliXBMC:,Cache has been deleted!,5000,'+icon+')')
        except:
            pass
 
 
def resetAddon():
    dialog = xbmcgui.Dialog()
    if dialog.yesno("NetfliXBMC:", "Really reset the addon?"):
      if os.path.exists(addonUserDataFolder):
          try:
              shutil.rmtree(addonUserDataFolder)
              xbmc.executebuiltin('XBMC.Notification(NetfliXBMC:,Addon has been reset!,5000,'+icon+')')
          except:
              pass
 
 
def search(type):
    keyboard = xbmc.Keyboard('', translation(30008))
    keyboard.doModal()
    if keyboard.isConfirmed() and keyboard.getText():
        search_string = keyboard.getText().replace(" ", "+")
        listSearchVideos("http://api-global.netflix.com/desktop/search/instantsearch?esn=www&term="+search_string+"&locale="+language+"&country="+country+"&authURL="+auth+"&_retry=0&routing=redirect", type)
 
 
def addToQueue(id):
    opener.open(urlMain+"/AddToQueue?movieid="+id+"&authURL="+auth)
    xbmc.executebuiltin('XBMC.Notification(NetfliXBMC:,'+str(translation(30144))+',3000,'+icon+')')
 
 
def removeFromQueue(id):
    opener.open(urlMain+"/QueueDelete?movieid="+id+"&authURL="+auth)
    xbmc.executebuiltin('XBMC.Notification(NetfliXBMC:,'+str(translation(30145))+',3000,'+icon+')')
    xbmc.executebuiltin("Container.Refresh")
 
 
def login():
    content = opener.open(urlMain+"/Login").read()
    match = re.compile('"LOCALE":"(.+?)"', re.DOTALL).findall(content)
    if match and not addon.getSetting("language"):
        addon.setSetting("language", match[0])
    if not "Sorry, Netflix is not available in your country yet." in content and not "Sorry, Netflix hasn't come to this part of the world yet" in content:
        match = re.compile('id="signout".+?authURL=(.+?)"', re.DOTALL).findall(content)
        if match:
            addon.setSetting("auth", match[0])
        if 'id="page-LOGIN"' in content:
            match = re.compile('name="authURL" value="(.+?)"', re.DOTALL).findall(content)
            authUrl = match[0]
            addon.setSetting("auth", authUrl)
            content = opener.open("https://signup.netflix.com/Login", "authURL="+urllib.quote_plus(authUrl)+"&email="+urllib.quote_plus(username)+"&password="+urllib.quote_plus(password)+"&RememberMe=on").read()
            match = re.compile('"LOCALE":"(.+?)"', re.DOTALL).findall(content)
            if match and not addon.getSetting("language"):
                addon.setSetting("language", match[0])
            cj.save(cookieFile)
        if not addon.getSetting("profile") and not singleProfile:
            chooseProfile()
        elif not singleProfile and showProfiles:
            chooseProfile()
        print "Login OK"
        return True
    else:
        xbmc.executebuiltin('XBMC.Notification(NetfliXBMC:,'+str(translation(30126))+',10000,'+icon+')')
        print "Login Failed"
        return False
 
 
def setProfile():
    token = addon.getSetting("profile")
    opener.open("https://www.netflix.com/ProfilesGate?nextpage=http%3A%2F%2Fwww.netflix.com%2FDefault")
    opener.open("https://api-global.netflix.com/desktop/account/profiles/switch?switchProfileGuid="+token)
    cj.save(cookieFile)
 
 
def chooseProfile():
    content = opener.open("https://www.netflix.com/ProfilesGate?nextpage=http%3A%2F%2Fwww.netflix.com%2FDefault").read()
    print "Profile Content: " + content
    match = re.compile('"guid":"(.+?)","profileName":"(.+?)"', re.DOTALL).findall(content)
    profiles = []
    tokens = []
    for t, p in match:
        profiles.append(p)
        tokens.append(t)
    print "Profiles: " + str(profiles)
    for nr in range(len(profiles)):
        if profiles[nr] != "Kids":
            break
    #dialog = xbmcgui.Dialog()
    #nr = dialog.select(translation(30113), profiles)
    print "Selected profile: " + tokens[nr]
    print "In choose profile"
    if nr >= 0:
        token = tokens[nr]
        # Profile selection isn't remembered, so it has to be executed before every requests (setProfile)
        # If you know a solution for this, please let me know
        # opener.open("https://api-global.netflix.com/desktop/account/profiles/switch?switchProfileGuid="+token)
        addon.setSetting("profile", token)
        cj.save(cookieFile)
 
 
def forceChooseProfile():
    #addon.setSetting("singleProfile", "false")
    #xbmc.executebuiltin('XBMC.Notification(NetfliXBMC:,'+str(translation(30111))+',5000,'+icon+')')
    chooseProfile()
 
 
def addMovieToLibrary(movieID, title, singleUpdate=True):
    movieFolderName = (''.join(c for c in unicode(title, 'utf-8') if c not in '/\\:?"*|<>')).strip(' .')
    dir = os.path.join(libraryFolderMovies, movieFolderName)
    if not os.path.isdir(dir):
        xbmcvfs.mkdir(dir)
        fh = xbmcvfs.File(os.path.join(dir, "movie.strm"), 'w')
        fh.write("plugin://plugin.video.netflixbmc/?mode=playVideo&url="+movieID)
        fh.close()
    if updateDB and singleUpdate:
        xbmc.executebuiltin('UpdateLibrary(video)')
 
 
def addSeriesToLibrary(seriesID, seriesTitle, season, singleUpdate=True):
    seriesFolderName = (''.join(c for c in unicode(seriesTitle, 'utf-8') if c not in '/\\:?"*|<>')).strip(' .')
    seriesDir = os.path.join(libraryFolderTV, seriesFolderName)
    if not os.path.isdir(seriesDir):
        xbmcvfs.mkdir(seriesDir)
    content = getSeriesInfo(seriesID)
    content = json.loads(content)
    for test in content["episodes"]:
        for item in test:
            episodeSeason = str(item["season"])
            seasonCheck = True
            if season:
                seasonCheck = episodeSeason == season
            if seasonCheck:
                seasonDir = os.path.join(seriesDir, "Season "+episodeSeason)
                if not os.path.isdir(seasonDir):
                    xbmcvfs.mkdir(seasonDir)
                episodeID = str(item["episodeId"])
                episodeNr = str(item["episode"])
                episodeTitle = item["title"].encode('utf-8')
                if len(episodeNr) == 1:
                    episodeNr = "0"+episodeNr
                seasonNr = episodeSeason
                if len(seasonNr) == 1:
                    seasonNr = "0"+seasonNr
                filename = "S"+seasonNr+"E"+episodeNr+" - "+episodeTitle+".strm"
                filename = (''.join(c for c in unicode(filename, 'utf-8') if c not in '/\\:?"*|<>')).strip(' .')
                fh = xbmcvfs.File(os.path.join(seasonDir, filename), 'w')
                fh.write("plugin://plugin.video.netflixbmc/?mode=playVideo&url="+episodeID)
                fh.close()
    if updateDB and singleUpdate:
        xbmc.executebuiltin('UpdateLibrary(video)')
 
 
def playTrailer(title):
    try:
        content = opener.open("http://gdata.youtube.com/feeds/api/videos?vq="+title.strip().replace(" ", "+")+"+trailer&racy=include&orderby=relevance").read()
        match = re.compile('<id>http://gdata.youtube.com/feeds/api/videos/(.+?)</id>', re.DOTALL).findall(content.split('<entry>')[1])
        xbmc.Player().play("plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=" + match[0])
    except:
        pass
 
 
def translation(id):
    return addon.getLocalizedString(id).encode('utf-8')
 
 
def parameters_string_to_dict(parameters):
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict
 
 
def addDir(name, url, mode, iconimage, type=""):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&type="+str(type)+"&thumb="+urllib.quote_plus(iconimage)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultTVShows.png", thumbnailImage=iconimage)
    liz.setInfo(type="video", infoLabels={"title": name})
    entries = []
    if "/MyList" in url:
        entries.append((translation(30122), 'RunPlugin(plugin://plugin.video.netflixbmc/?mode=addMyListToLibrary)',))
    if not singleProfile:
        entries.append((translation(30110), 'RunPlugin(plugin://plugin.video.netflixbmc/?mode=chooseProfile)',))
    liz.setProperty("fanart_image", defaultFanart)
    liz.addContextMenuItems(entries)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok
 
 
def addVideoDir(name, url, mode, iconimage, videoType="", desc="", duration="", year="", mpaa="", director="", genre="", rating=""):
    filename = (''.join(c for c in unicode(url, 'utf-8') if c not in '/\\:?"*|<>')).strip()+".jpg"
    print "Filename: " + filename
    coverFile = os.path.join(cacheFolderCoversTMDB, filename)
    fanartFile = os.path.join(cacheFolderFanartTMDB, filename)
    if os.path.exists(coverFile):
        iconimage = coverFile
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&thumb="+urllib.quote_plus(iconimage)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setInfo(type="video", infoLabels={"title": name, "plot": desc, "duration": duration, "year": year, "mpaa": mpaa, "director": director, "genre": genre, "rating": rating})
    #if os.path.exists(fanartFile):
    #    liz.setProperty("fanart_image", fanartFile)
    #elif os.path.exists(coverFile):
    #    liz.setProperty("fanart_image", coverFile)
    entries = []
    if videoType == "tvshow":
        if browseTvShows:
            entries.append((translation(30121), 'Container.Update(plugin://plugin.video.netflixbmc/?mode=playVideoMain&url='+urllib.quote_plus(url)+'&thumb='+urllib.quote_plus(iconimage)+')',))
        else:
            entries.append((translation(30118), 'Container.Update(plugin://plugin.video.netflixbmc/?mode=listSeasons&url='+urllib.quote_plus(url)+'&thumb='+urllib.quote_plus(iconimage)+')',))
    if videoType != "episode":
        entries.append((translation(30134), 'RunPlugin(plugin://plugin.video.netflixbmc/?mode=playTrailer&url='+urllib.quote_plus(name)+')',))
        entries.append((translation(30114), 'RunPlugin(plugin://plugin.video.netflixbmc/?mode=addToQueue&url='+urllib.quote_plus(url)+')',))
        entries.append((translation(30140), 'Container.Update(plugin://plugin.video.netflixbmc/?mode=listVideos&url='+urllib.quote_plus(urlMain+"/WiMovie/"+url)+'&type=movie)',))
        entries.append((translation(30141), 'Container.Update(plugin://plugin.video.netflixbmc/?mode=listVideos&url='+urllib.quote_plus(urlMain+"/WiMovie/"+url)+'&type=tv)',))
    if videoType == "tvshow":
        entries.append((translation(30122), 'RunPlugin(plugin://plugin.video.netflixbmc/?mode=addSeriesToLibrary&url=&name='+urllib.quote_plus(name.strip())+'&seriesID='+urllib.quote_plus(url)+')',))
    elif videoType == "movie":
        entries.append((translation(30122), 'RunPlugin(plugin://plugin.video.netflixbmc/?mode=addMovieToLibrary&url='+urllib.quote_plus(url)+'&name='+urllib.quote_plus(name.strip()+' ('+year+')')+')',))
    liz.addContextMenuItems(entries)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok
 
 
def addVideoDirR(name, url, mode, iconimage, videoType="", desc="", duration="", year="", mpaa="", director="", genre="", rating=""):
    filename = (''.join(c for c in unicode(url, 'utf-8') if c not in '/\\:?"*|<>')).strip()+".jpg"
    coverFile = os.path.join(cacheFolderCoversTMDB, filename)
    fanartFile = os.path.join(cacheFolderFanartTMDB, filename)
    if os.path.exists(coverFile):
        iconimage = coverFile
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&thumb="+urllib.quote_plus(iconimage)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultTVShows.png", thumbnailImage=iconimage)
    liz.setInfo(type="video", infoLabels={"title": name, "plot": desc, "duration": duration, "year": year, "mpaa": mpaa, "director": director, "genre": genre, "rating": rating})
    if os.path.exists(fanartFile):
        liz.setProperty("fanart_image", fanartFile)
    elif os.path.exists(coverFile):
        liz.setProperty("fanart_image", coverFile)
    entries = []
    if videoType == "tvshow":
        if browseTvShows:
            entries.append((translation(30121), 'Container.Update(plugin://plugin.video.netflixbmc/?mode=playVideoMain&url='+urllib.quote_plus(url)+'&thumb='+urllib.quote_plus(iconimage)+')',))
        else:
            entries.append((translation(30118), 'Container.Update(plugin://plugin.video.netflixbmc/?mode=listSeasons&url='+urllib.quote_plus(url)+'&thumb='+urllib.quote_plus(iconimage)+')',))
    entries.append((translation(30134), 'RunPlugin(plugin://plugin.video.netflixbmc/?mode=playTrailer&url='+urllib.quote_plus(name)+')',))
    entries.append((translation(30115), 'RunPlugin(plugin://plugin.video.netflixbmc/?mode=removeFromQueue&url='+urllib.quote_plus(url)+')',))
    entries.append((translation(30140), 'Container.Update(plugin://plugin.video.netflixbmc/?mode=listVideos&url='+urllib.quote_plus(urlMain+"/WiMovie/"+url)+'&type=movie)',))
    entries.append((translation(30141), 'Container.Update(plugin://plugin.video.netflixbmc/?mode=listVideos&url='+urllib.quote_plus(urlMain+"/WiMovie/"+url)+'&type=tv)',))
    if videoType == "tvshow":
        entries.append((translation(30122), 'RunPlugin(plugin://plugin.video.netflixbmc/?mode=addSeriesToLibrary&url=&name='+str(name.strip())+'&seriesID='+str(url)+')',))
    elif videoType == "movie":
        entries.append((translation(30122), 'RunPlugin(plugin://plugin.video.netflixbmc/?mode=addMovieToLibrary&url='+urllib.quote_plus(url)+'&name='+str(name.strip()+' ('+year+')')+')',))
    liz.addContextMenuItems(entries)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok
 
 
def addSeasonDir(name, url, mode, iconimage, seriesName, seriesID):
    filename = (''.join(c for c in unicode(seriesID, 'utf-8') if c not in '/\\:?"*|<>')).strip()+".jpg"
    fanartFile = os.path.join(cacheFolderFanartTMDB, filename)
    coverFile = os.path.join(cacheFolderCoversTMDB, filename)
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&seriesID="+urllib.quote_plus(seriesID)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultTVShows.png", thumbnailImage=iconimage)
    liz.setInfo(type="video", infoLabels={"title": name})
    if os.path.exists(fanartFile):
        liz.setProperty("fanart_image", fanartFile)
    elif os.path.exists(coverFile):
        liz.setProperty("fanart_image", coverFile)
    entries = []
    entries.append((translation(30122), 'RunPlugin(plugin://plugin.video.netflixbmc/?mode=addSeriesToLibrary&url='+urllib.quote_plus(url)+'&name='+str(seriesName.strip())+'&seriesID='+str(seriesID)+')',))
    liz.addContextMenuItems(entries)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok
 
 
def addEpisodeDir(name, url, mode, iconimage, desc="", duration="", season="", episodeNr="", seriesID="", playcount=""):
    filename = (''.join(c for c in unicode(seriesID, 'utf-8') if c not in '/\\:?"*|<>')).strip()+".jpg"
    fanartFile = os.path.join(cacheFolderFanartTMDB, filename)
    coverFile = os.path.join(cacheFolderCoversTMDB, filename)
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultTVShows.png", thumbnailImage=iconimage)
    liz.setInfo(type="video", infoLabels={"title": name, "plot": desc, "duration": duration, "season": season, "episode": episodeNr, "playcount": playcount})
    if os.path.exists(fanartFile):
        liz.setProperty("fanart_image", fanartFile)
    elif os.path.exists(coverFile):
        liz.setProperty("fanart_image", coverFile)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok
 
 
class window(xbmcgui.WindowXMLDialog):
    def onAction(self, action):
        ACTION_SELECT_ITEM = 7
        ACTION_PARENT_DIR = 9
        ACTION_PREVIOUS_MENU = 10
        ACTION_STOP = 13
        ACTION_SHOW_INFO = 11
        ACTION_SHOW_GUI = 18
        ACTION_MOVE_LEFT = 1
        ACTION_MOVE_RIGHT = 2
        ACTION_MOVE_UP = 3
        ACTION_MOVE_DOWN = 4
        KEY_BUTTON_BACK = 275
        if osWin:
            proc = subprocess.Popen('WMIC PROCESS get Caption', shell=True, stdout=subprocess.PIPE)
            procAll = ""
            for line in proc.stdout:
                procAll+=line
            if "chrome.exe" in procAll:
                if action in [ACTION_SHOW_INFO, ACTION_SHOW_GUI, ACTION_STOP, ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, KEY_BUTTON_BACK]:
                    subprocess.Popen('"'+sendKeysPath+'"'+' sendKey=Close', shell=False)
                    self.close()
                elif action==ACTION_SELECT_ITEM:
                    subprocess.Popen('"'+sendKeysPath+'"'+' sendKey=PlayPause', shell=False)
                elif action==ACTION_MOVE_LEFT:
                    subprocess.Popen('"'+sendKeysPath+'"'+' sendKey=SeekLeft', shell=False)
                elif action==ACTION_MOVE_RIGHT:
                    subprocess.Popen('"'+sendKeysPath+'"'+' sendKey=SeekRight', shell=False)
                elif action==ACTION_MOVE_UP:
                    subprocess.Popen('"'+sendKeysPath+'"'+' sendKey=VolumeUp', shell=False)
                elif action==ACTION_MOVE_DOWN:
                    subprocess.Popen('"'+sendKeysPath+'"'+' sendKey=VolumeDown', shell=False)
            else:
                self.close()
        elif osLinux:
            proc = subprocess.Popen('/bin/ps ax', shell=True, stdout=subprocess.PIPE)
            procAll = ""
            for line in proc.stdout:
                procAll+=line
            if "chrome" in procAll or "chromium" in procAll:
                if action in [ACTION_SHOW_INFO, ACTION_SHOW_GUI, ACTION_STOP, ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, KEY_BUTTON_BACK]:
                    subprocess.Popen('xdotool key alt+F4', shell=True)
                    self.close()
                elif action==ACTION_SELECT_ITEM:
                    subprocess.Popen('xdotool key Return', shell=True)
                elif action==ACTION_MOVE_LEFT:
                    subprocess.Popen('xdotool key Left', shell=True)
                elif action==ACTION_MOVE_RIGHT:
                    subprocess.Popen('xdotool key Right', shell=True)
                elif action==ACTION_MOVE_UP:
                    subprocess.Popen('xdotool key Up', shell=True)
                elif action==ACTION_MOVE_DOWN:
                    subprocess.Popen('xdotool key Down', shell=True)
            else:
                self.close()
        elif osOSX:
            proc = subprocess.Popen('/bin/ps ax', shell=True, stdout=subprocess.PIPE)
            procAll = ""
            for line in proc.stdout:
                procAll+=line
            if "chrome" in procAll:
                if action in [ACTION_SHOW_INFO, ACTION_SHOW_GUI, ACTION_STOP, ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, KEY_BUTTON_BACK]:
                    subprocess.Popen('cliclick kd:alt', shell=True)
                    subprocess.Popen('cliclick kp:f4', shell=True)
                    self.close()
                elif action==ACTION_SELECT_ITEM:
                    subprocess.Popen('cliclick kp:return', shell=True)
                elif action==ACTION_MOVE_LEFT:
                    subprocess.Popen('cliclick kp:arrow-left', shell=True)
                elif action==ACTION_MOVE_RIGHT:
                    subprocess.Popen('cliclick kp:arrow-right', shell=True)
                elif action==ACTION_MOVE_UP:
                    subprocess.Popen('cliclick kp:arrow-up', shell=True)
                elif action==ACTION_MOVE_DOWN:
                    subprocess.Popen('cliclick kp:arrow-down', shell=True)
            else:
                self.close()
 
 
params = parameters_string_to_dict(sys.argv[2])
mode = urllib.unquote_plus(params.get('mode', ''))
url = urllib.unquote_plus(params.get('url', ''))
thumb = urllib.unquote_plus(params.get('thumb', ''))
name = urllib.unquote_plus(params.get('name', ''))
season = urllib.unquote_plus(params.get('season', ''))
seriesID = urllib.unquote_plus(params.get('seriesID', ''))
type = urllib.unquote_plus(params.get('type', ''))
 
if mode == 'main':
    main(type)
elif mode == 'wiHome':
    wiHome(type)
elif mode == "myList":
    myList(url, type)
elif mode == "newArrivals":
    newArrivals(url, type)
elif mode == "listTvGenres":
    listTvGenres(url, type)
elif mode == "listMovieGenres":
    listMovieGenres(url, type)
elif mode == "listFiltered":
    listFiltered(url, type)
elif mode == 'listVideos':
    listVideos(url, type)
elif mode == 'listSliderVideos':
    listSliderVideos(url, type)
elif mode == 'listSearchVideos':
    listSearchVideos(url, type)
elif mode == 'addToQueue':
    addToQueue(url)
elif mode == 'removeFromQueue':
    removeFromQueue(url)
elif mode == 'playVideo':
    playVideo(url)
elif mode == 'playVideoMain':
    playVideoMain(url)
elif mode == 'search':
    search(type)
elif mode == 'login':
    login()
elif mode == 'chooseProfile':
    chooseProfile()
elif mode == 'listGenres':
    listGenres(url, type)
elif mode == 'listTvGenres':
    listTvGenres(type)
elif mode == 'listViewingActivity':
    listViewingActivity(type)
elif mode == 'listSeasons':
    listSeasons(url, name, thumb)
elif mode == 'listEpisodes':
    listEpisodes(seriesID, url)
elif mode == 'configureUtility':
    configureUtility()
elif mode == 'deleteCookies':
    deleteCookies()
elif mode == 'deleteCache':
    deleteCache()
elif mode == 'resetAddon':
    resetAddon()
elif mode == 'playTrailer':
    playTrailer(url)
elif mode == 'addMyListToLibrary':
    addMyListToLibrary()
elif mode == 'addMovieToLibrary':
    addMovieToLibrary(url, name)
elif mode == 'addSeriesToLibrary':
    addSeriesToLibrary(seriesID, name, url)
else:
    index()