# -*- coding: utf-8 -*-
from resources.sites.LIVETV2 import *
AddonID = 'plugin.video.OTV_MEDIA'
loggeractive = ("debug") 

from resources.lib import comon as common
from resources.lib.comaddon import addon, window
import xbmcvfs
AddonID = 'plugin.video.OTV_MEDIA'
loggeractive = ("debug") 

import requests

mysettings = xbmcaddon.Addon(id='plugin.video.OTV_MEDIA')
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))

logos = xbmc.translatePath(os.path.join(home,'resources', 'art','logos\\'))  # subfolder for logos
        
addons= addon()

SITE_IDENTIFIER = 'stb_emula'
AddonID = 'plugin.video.OTV_MEDIA'
Addon = xbmcaddon.Addon(AddonID)

AddonName = Addon.getAddonInfo("name")
icon = Addon.getAddonInfo('icon')

addonDir = Addon.getAddonInfo('path')
addon_data_dir = os.path.join(xbmc.translatePath("special://userdata/addon_data" ), AddonID)
pwdir = os.path.join(home,'resources', 'art', "password")
cdir = os.path.join(xbmc.translatePath("special://temp"),"files")

LOCAL_VERSION_FILE = os.path.join(os.path.join(addonDir), 'version.xml' )
REMOTE_VERSION_FILE = "https://kodilive.eu/repo/version.xml"

LOCAL_VERSION_FILE2 = os.path.join(os.path.join(addonDir), 'list.xml' )
REMOTE_VERSION_FILE2 = "https://kodilive.eu/update/list.xml"

libDir = os.path.join(addonDir, 'resources', 'lib')
f4mProxy = os.path.join(addonDir, 'f4mProxy')
chanDir = os.path.join(addonDir, 'resources', 'channels')
#XML_FILE  = os.path.join(libDir, 'advancedsettings.xml' )
#ACTIVESETTINGSFILE = os.path.join(xbmc.translatePath('special://profile'), 'advancedsettings.xml')
playlistsFile = os.path.join(addonDir, "playLists.txt")
Italian = os.path.join(addonDir, "italian.txt")
French = os.path.join(addonDir, "french.txt")
German = os.path.join(addonDir, "german.txt")
English = os.path.join(addonDir, "english.txt")
ydldir = os.path.join(xbmc.translatePath("special://home/addons/"),'script.module.youtube.dl')
streamtype = "HLS"

EXTL = [ '.m3u', '.m3u8', '.txt']
EXTV = [ '.mkv','.mp4','.avi','.ogv','.flv','.f4v','.wmv','.mpg','.mpeg','.3gp','.3g2','.webm','.ogg', '.part' ]
EXTA = [ '.mp3','.flac','.aac','.wav','.raw','.m4a','.wma','.f4a' ]

UAA = "Android / Chrome 40: Mozilla/5.0 (Linux; Android 5.1.1; Nexus 4 Build/LMY48T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.89 Mobile Safari/537.36"

iconlist = logos
audio =logos
icondir = logos
video = logos
find = logos

playlistsFile2 = os.path.join(addon_data_dir, "StbemuLists.txt")
playlistsFile4 = os.path.join(addon_data_dir, "StbemuLists.txt")
playlistsFile3 = os.path.join(addon_data_dir, "StbemuplayLists.bkp")
playlistsFile5 = os.path.join(addon_data_dir, "StbemuFolderLists.bkp")

TVICO = os.path.join(addonDir, "resources", "images", "tv.png")
favoritesFile = os.path.join(addon_data_dir, 'favorites.txt')
SDownloader = "false"
DFolder = os.path.join(addon_data_dir, 'download', '')

def zip_PM_data():
    import zipfile
    dialog = xbmcgui.Dialog()
    path = dialog.browse( int(3), addons.VSlang(10124), "myprograms", "", True )

    if not path == "":
        ZipFile = zipfile.ZipFile(os.path.join(path,"backup_pm.zip"), "w" )
        ZipFile.write(playlistsFile2, os.path.basename(playlistsFile2), compress_type=zipfile.ZIP_DEFLATED)
        ZipFile.write(playlistsFile4, os.path.basename(playlistsFile4), compress_type=zipfile.ZIP_DEFLATED)
        dirpath = os.path.join(addon_data_dir, 'password','')
        basedir = os.path.dirname(dirpath) + '/'
        for root, dirs, files in os.walk(dirpath):
            dirname = root.replace(basedir, '')
            for f in files:
                ZipFile.write(root + '/' + f,  'password/' + f)
        ZipFile.close()   
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%("KLTV: " + "  "+ path + "backup_pm.zip",addons.VSlang(10126), 6500, icon))

def unzip_PM_data():
    import ziptools
    ZipFile = xbmcgui.Dialog().browse(int(1), addons.VSlang(10122), 'myprograms','.zip')
    if not ZipFile:
        return
    else:
        unzipper = ziptools.ziptools()
        unzipper.extract(os.path.join(xbmc.translatePath(ZipFile)),addon_data_dir)
        xbmc.sleep(450)
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%("KLTV: ",addons.VSlang(10125), 6500, icon))
        xbmc.sleep(850)
        xbmc.executebuiltin("XBMC.Container.Refresh()")

def find_single_match(data,patron,index=0):
    
    try:
        matches = re.findall( patron , data , flags=re.DOTALL )
        return matches[index]
    except:
        return ""

percent = 0

def DownloaderClass(url,dest):
    
    dp = xbmcgui.DialogProgress()
    dp.create("Kodi Live TV ZIP DOWNLOADER","Downloading File",url)
    urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
 
def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
    
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        dp.update(percent)
    except: 
        percent = 100
        dp.update(percent)
        time.sleep(20)
        dp.close()
    if dp.iscanceled(): 
        dp.close()

def emptydir(top):
    
    if(top == '/' or top == "\\"): 
        return
    else:
        for root, dirs, files in os.walk(top, topdown=False):
            for name in files:
                if not bool('default.py' in name) and not bool('ziptools.py' in name):
                    os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name)) 
 
def clean_cache():

    for i in os.listdir(cdir):    
        rf = format(i)
        if not bool('.' in i):
            file = os.path.join( cdir , i )
            if os.path.isfile(file):
                os.remove(file)
                #xbmc.log('KLTV Delete cache file : ' + rf )
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%("Kodi Live TV : ","m3u cache has been deleted!", 4500, icon))

##############################
# Inizia creazione pagine
#search.png    
def Categories():
    AddDir("[COLOR ff74ff4a][B]{0}[/B][/COLOR]".format(addons.VSlang(10106)), "update" ,46 ,os.path.join(addonDir, "resources", "images", "update.png"), isFolder=True)
    AddDir("[COLOR cyan][B][ {0} ][/B][/COLOR]".format(addons.VSlang(10003)), "favorites" ,30 ,os.path.join(addonDir, "resources", "images", "bright_yellow_star.png"))
    AddDir("[COLOR blue][B]{0}[/B][/COLOR]".format(addons.VSlang(10047)), "Manager" ,139 , os.path.join(addonDir, "resources", "images", "playlist.png"))
    AddDir("[COLOR gold][B]{0}[/B][/COLOR]".format(addons.VSlang(10020)), "italian" ,35 , "https://kodilive.eu/flag/it.png")
    AddDir("[COLOR gold][B]{0}[/B][/COLOR]".format(addons.VSlang(10021)), "french" ,36 , "https://kodilive.eu/flag/fr.png")
    AddDir("[COLOR gold][B]{0}[/B][/COLOR]".format(addons.VSlang(10022)), "german" ,37 , "https://kodilive.eu/flag/de.png")
    AddDir("[COLOR gold][B]{0}[/B][/COLOR]".format(addons.VSlang(10023)), "english" ,38 ,  "https://kodilive.eu/flag/uk.png")
    list = common.ReadList(playlistsFile)
    for item in list:
        mode = 2
        image = item.get('image', '')
        icon = image.encode("utf-8")
        name = addons.VSlang(item["name"])
        cname = "[COLOR gold][B]{0}[/B][/COLOR]".format(name)
        
        if name == addons.VSlang(10070) :
            cname = "[COLOR violet][B]{0}[/B][/COLOR]".format(name)
        elif name == addons.VSlang(10050) :
            cname = "[COLOR pink][B]{0}[/B][/COLOR]".format(name)
        elif name == addons.VSlang(10051) :
            cname = "[COLOR FED9DB93][B]{0}[/B][/COLOR]".format(name)                    
        AddDir(cname ,item["url"], mode , icon)
    
    if xbmcaddon.Addon('plugin.video.OTV_MEDIA').getSetting('XXX_section')=="true":
        AddDir("[COLOR red][B]Video XXX[/B][/COLOR]" ,"?l=pornazzi", 2 , "https://kodilive.eu/icon/XXX.png")
    
def importList():
    
    method = GetSourceLocation(addons.VSlang(10120), [addons.VSlang(10122), addons.VSlang(10123)])
        
    if method == -1:
        return
    elif method == 0:
        listUrl = GetKeyboardText(addons.VSlang(10005)).strip()
    else:
        listUrl = xbmcgui.Dialog().browse(int(1), addons.VSlang(10006), 'myprograms','.txt')
        if not listUrl:
            return
    if len(listUrl) < 1:
        return
 
    if common.check_url(listUrl):
        lista = common.OpenURL(listUrl)
    else:
        lista = common.ReadFile(listUrl)
 
    if os.path.isfile( playlistsFile3 ) : os.remove( playlistsFile3 )
    shutil.copyfile( playlistsFile2, playlistsFile3 )
    xbmc.sleep ( 500 )
    os.remove( playlistsFile2 )
    xbmc.sleep ( 500 )
    common.write_file( playlistsFile2, lista )
    xbmc.executebuiltin("XBMC.Container.Update('plugin://{0}')".format(AddonID))
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%("Kodi Live TV : ",addons.VSlang(10124), 3600, icon))    
  
def AddNewList():
	
    method1 = GetSourceLocation(addons.VSlang(10001), [addons.VSlang(10040), addons.VSlang(10220), addons.VSlang(10042), addons.VSlang(10266)])
	
    if method1 == -1:
            return	
    elif method1 == 0:
        AddNewDir()
    elif method1 == 1:
        AddNewDir("xml")    
    elif method1 == 3:
        AddNewDir("pyt")
    else:
        listName = GetKeyboardText(addons.VSlang(10004)).strip()
        if len(listName) < 1:
            return

        method = GetSourceLocation(addons.VSlang(10002), [addons.VSlang(10016), addons.VSlang(10017)])	

        if method == -1:
            return
        elif method == 0:
            listUrl = GetKeyboardText(addons.VSlang(10005)).strip()
        else:
            listUrl = xbmcgui.Dialog().browse(int(1), addons.VSlang(10006), 'myprograms','.m3u8|.m3u')
            if not listUrl:
                return
            
        if len(listUrl) < 1:
            return
        
        exists = ""
        list = common.ReadList(playlistsFile2)
        for item in list:
            if item["url"] == listUrl:
                exists = "yes"
                xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%("Kodi Live TV : ",addons.VSlang(10264), 3600, icon))
                break       
        
        if exists == "":
            list.append({"name": listName, "url": listUrl})
            if common.SaveList(playlistsFile2, list):
                    xbmc.executebuiltin("XBMC.Container.Update('plugin://{0}')".format(AddonID))
                    
def AddNewDir(loc = "l"):
    if loc == "xml":
        method = GetSourceLocation(addons.VSlang(10221), [addons.VSlang(10222), addons.VSlang(10223)])
        
        if method == -1:
            return
        elif method == 0:
            listUrl = GetKeyboardText(addons.VSlang(10224)).strip()
        else:
            listUrl = xbmcgui.Dialog().browse(int(1), addons.VSlang(10225), 'myprograms','.xml')
    elif loc == "pyt":
        listName = GetKeyboardText(addons.VSlang(10265)).strip()
        listUrl = GetKeyboardText(addons.VSlang(10226)).strip()
    else:
        if loc == "l":
            method2 = GetSourceLocation(addons.VSlang(10040), [addons.VSlang(10260), addons.VSlang(10043), addons.VSlang(10261)] )
         
            if method2 == -1:
                return           
            elif method2 == 0:
                listName = GetKeyboardText(addons.VSlang(10263)).strip()
                listUrl = xbmcgui.Dialog().browse(int(0), addons.VSlang(10041), 'myprograms')       
            elif method2 == 1:
                listName = GetKeyboardText(addons.VSlang(10263)).strip()
                listUrl = xbmcgui.Dialog().browse(int(0), addons.VSlang(10041), 'files')
            else:
                listName = GetKeyboardText(addons.VSlang(10263)).strip()
                listUrl = GetKeyboardText(addons.VSlang(10262)).strip() 
               
	
    if not listUrl or len(listUrl) < 1:
            return

    list = common.ReadList(playlistsFile4)
    Url = ""
    pUrl = ""
    
    if listUrl.endswith(".xml") or loc == "xml":
        if common.check_url(listUrl):
            response = common.OpenURL(listUrl)
        else:
            response = common.ReadFile(listUrl)
            
        Url = find_single_match(response,"<url>([^<]+)</url>").strip()
        pUrl = find_single_match(response,"<web>([^<]+)</web>").strip()
        xUrl = find_single_match(response,"<xweb>([^<]+)</xweb>").strip()
        
        if not Url == "":
            loc = "repo"
            listUrl = Url
            listName = find_single_match(response,"<name>([^<]+)</name>").strip()
        elif not pUrl == "":
            loc = "page"
            listUrl = pUrl
            listName = find_single_match(response,"<name>([^<]+)</name>").strip()
        elif not xUrl == "":
            loc = "xml"
            listUrl = xUrl
            listName = find_single_match(response,"<name>([^<]+)</name>").strip()
        else:
            listName = GetKeyboardText(addons.VSlang(10263)).strip()
    else:
        if not listName:
            listName = listName.split("/")[-2]
    
    exists = ""
    
    if len(listUrl)>0 and len(listName)>0:
        for item in list:
            if item["url"] == listUrl:
                exists = "yes"
                xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%("Kodi Live TV : ",addons.VSlang(10264), 3600, icon))
                break
        
        if exists == "":
            if loc == "xml":
                list.append({"name": listName, "url": listUrl, "type":"xml"})
            elif loc == "page":
                list.append({"name": listName, "url": listUrl, "type":"page"})
            elif loc == "pyt":
                list.append({"name": listName, "url": listUrl, "type":"pyt"})
            else:
                list.append({"name": listName, "url": listUrl})
                
            if common.SaveList(playlistsFile4, list):
                    xbmc.executebuiltin("XBMC.Container.Update('plugin://{0}')".format(AddonID))
	
def RemoveFromLists(url):
    
    list = common.ReadList(playlistsFile2)
    for item in list:
        if item["url"] == url:
            list.remove(item)
            if common.SaveList(playlistsFile2, list):
                xbmc.executebuiltin("XBMC.Container.Refresh()")
            break
			
def RemoveDirFromLists(url,name):
    
    return_value = xbmcgui.Dialog().yesno(addons.VSlang(10045), addons.VSlang(10206) + " " + name + "?")
    if not return_value == 0:
                
        list = common.ReadList(playlistsFile4)
        for item in list:
            if item["url"] == url:
                list.remove(item)
                if common.SaveList(playlistsFile4, list):
                    xbmc.executebuiltin("XBMC.Container.Refresh()")
                break
				
def m3uCategory(url,Logo=True):
    
    try:
        urldec = base64.decodestring(url)
        if common.check_url(urldec):
            url = urldec
    except:
        pass
    
    if not common.check_url(url):
        list = common.m3u2list(os.path.join(chanDir, url)) 
    else :
        list = common.cachelist(url,cdir)
    
    playheaders = ""
    
    try:
        surl,playheaders=url.split('|')
    except:
        playheaders = ""
    
    for channel in list:
        name = channel["display_name"]

        if channel.get("tvg_logo", ""): 
            logo = channel.get("tvg_logo", "")
            iconname = "https://kodilive.eu/logo/" + logo
        else :
            iconname = TVICO
        
        if Logo == False:
            if channel.get("tvg_logo", "") and common.check_url(channel.get("tvg_logo", "")):
                iconname = channel.get("tvg_logo", "")
            else:
                iconname = TVICO
        
        channel["url"] = channel["url"].strip()
        if not playheaders == "":
            channel["url"] = channel["url"] + "|" + playheaders
        
        ext = "." + channel["url"].split(".")[-1]
        EXT = EXTV + EXTA
        if bool(ext in EXT):
            AddDir(name ,channel["url"],3, iconname, isFolder=False)
        else:
            FastDir(name,channel["url"],3,iconname,fanart="",description="",res=False,isFolder=False)
        
def FastDir(name,url,mode,icon="",fanart="",description="",res=False,isFolder=True,linkType=None):

        u=sys.argv[0]+"?url="+Unquote_plus(url)+"&mode="+ str(mode) + "&name="+Unquote_plus(name)+"&iconimage="+Unquote_plus(icon)+"&description="+Unquote_plus(description)
        liz = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
        ok = True
        
        if fanart == "":
            liz.setArt({'fanart': Addon.getAddonInfo('fanart')})
        else:
            liz.setArt({'fanart':fanart})
        
        items = [ ]
           
        if not isFolder and not mode==73:
            if not mode == 78:
                liz.setProperty('IsPlayable', 'true')
            liz.setProperty( "Video", "true")
            liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description })           
            items = [('{0}'.format(addons.VSlang(10009)), 'XBMC.RunPlugin({0}?url={1}&mode=31&name={2}&iconimage={3})'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(name), Unquote_plus(icon)))]

        if not res and not mode==73:
            
            try:
                urldec = base64.decodestring(url)
                if common.check_url(urldec):
                    url = urldec
            except:
                pass
            
            if url.find(".m3u8")>0 or url.startswith("opus"):
                items.append(('Play with HLS-Player','XBMC.RunPlugin({0}?url={1}&iconimage={2}&name={3}&mode=5)'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(iconimage), Unquote_plus(name))))
        
            if os.path.exists(ydldir):
                items.append(('Youtube-dl Control','XBMC.RunPlugin({0}?url={1}&name={2}&mode=80)'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(name))))
            items.append(('Refresh', 'Container.Refresh'))
        
        if linkType:
            u="XBMC.RunPlugin(%s&linkType=%s)" % (u, linkType)
            
        liz.addContextMenuItems(items, replaceItems=True)            
        #xbmc.log("Channel -->" + u)    
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)
        return ok
    
def PlayUrl(name,url,iconimage=None):
    
    url = url.replace("\n","").replace("\r","")
    #name = common.GetEncodeString(name)
    urldec = ""
    
    try:
        urldec = base64.decodestring(url)
        if common.check_url(urldec):
            url = urldec
    except:
        pass    
    
    if url.find("pornhd.com")>0:
        try:
            url = common.pornHD(url)
        except:
            pass
    
    urluhd = 0
    
    if url.find("urhd.tv")>0:
        try:
            url = common.urhd(url)
            urluhd = 1
        except:
            pass
    
    if url.startswith("opus"):
        url = Opus(url)    
    
    if url.find(":enc")>0:
        url = rsich(url)
    
    if not url.endswith(".ts") and not url.find(".ts|")>-1 and not url.endswith(".f4m") and url.find(".f4m?") < 0 and not url.endswith("Player=HLS"):
    
        print('--- Playing "{0}". {1}'.format(name, url))
        listitem = xbmcgui.ListItem(path=url, thumbnailImage=iconimage)
        listitem.setInfo(type="Video", infoLabels={ "Title": name })
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
                
    else :
        
        if xbmc.Player().isPlaying():
            xbmc.executebuiltin( "XBMC.Action(Stop)" )
            xbmc.sleep(4000)
            xbmc.executebuiltin('Dialog.Close(all, true)')

        if Addon.getSetting('use_shani') == "true":
            MyF4m = False
        else:
            MyF4m = True
            
        if url.endswith(".ts") or url.find(".ts|")>-1:        
            StreamType = 'TSDOWNLOADER'
        elif url.find("Player=HLS") > 0 or urluhd>0:
            StreamType = 'HLS'
        else:
            StreamType = 'HDS'
        
        if MyF4m :
            url = 'plugin://plugin.video.OTV_MEDIA/?url='+Unquote_plus(url)+'&streamtype=' + StreamType + '&name='+urllib.quote(name)+'&mode=5&iconImage=' + iconimage
            xbmc.executebuiltin('XBMC.RunPlugin('+url+')')
            xbmc.executebuiltin('Dialog.Close(all, true)')
        else:
            f4mDir = xbmcaddon.Addon('plugin.video.f4mTester').getAddonInfo('path')
            if not os.path.exists(f4mDir):
                xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(AddonName,"Plugin f4mTester required!", 3200, icon))
            else:
                url = 'plugin://plugin.video.f4mTester/?url='+Unquote_plus(url)+'&streamtype=' + StreamType + '&name='+urllib.quote(name)+'&iconImage=' + iconimage
                xbmc.executebuiltin('XBMC.RunPlugin('+url+')')
                xbmc.executebuiltin('Dialog.Close(all, true)')

def findm3u(url, string="",live=False):
    
    if url == "ipbox":
        getIpBoxList(string=string,live=live)
        
    elif "urhd.tv" in url:
        
        ch_list = common.urhd_list()
        for idx, ch in enumerate(ch_list, 1):
            
            if ch["alive"]:
                active = ""
            else:
                active = " - [B][COLOR red][INACTIVE][/COLOR][/B]"
        
            display_name = ch["display_name"]
            url = "http://urhd.tv/" + ch["display_name"].lower()
            
            if string == "":    
                AddDir("[COLOR orangered]" + display_name + "[/COLOR]" + active, url, 3 , TVICO, "", isFolder=False)
            else:
                sname = common.BBTagRemove(display_name).replace("_"," ").lower()
                if sname.find(string)>-1:
                    listName = "  " + "[CR][I][COLOR blue][LIGHT]* {0}[/COLOR]".format(addons.VSlang(10004)) + " -->  [COLOR yellow]{0}[/COLOR][/I][/LIGHT]".format("urhd.tv")
                    cname = "[COLOR orange][B]{0}[/B][/COLOR]".format(display_name) + active + listName
                    AddDir(cname , url, 3 , TVICO, "", isFolder=False)
    else:
        
        from bs4 import BeautifulSoup
        from urlparse import urlparse
        import html5lib
        
        try:
            urldec = base64.decodestring(url)
            if common.check_url(urldec):
                url = urldec
        except:
            pass
        
        data = common.cachepage(url,7200,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko'})
        soup = BeautifulSoup(data,'html5lib')
        flink = 0
        
        if string == "":
            AddDir("[COLOR yellow][B]{0}[/B][/COLOR]".format(addons.VSlang(10250)), url, 81, find, isFolder=True)
        nu = 0
        for link in soup.find_all('a', href=True):
            if '.m3u' in link['href']:
                nu = nu + 1
                flink = 1
                nurl = urlparse(link['href'])
                listnamext = nurl.path.split("/")
                if url.find("SAM.html")>0:
                    ListName = "[B][COLOR green]S[/COLOR][COLOR withe]a[/COLOR][COLOR red]M[/COLOR] [COLOR orange]  " + str(nu) + " [/COLOR][/B]"
                else:
                    listname = listnamext[-1].split(".m3u")
                    ListName = listname[0]
                    
                listurl = link['href']
                if string == "":
                    AddDir("[COLOR green]" + ListName + "[/COLOR]", listurl, 51, "http://findicons.com/files/icons/1331/matrix_rebooted/128/text_clipping_file.png", isFolder=True)
                else:
                    sch_m3u(listurl,string,ListName,live=live)
        
        if flink == 0:
            patron = '>(http:\/\/(.*?)\/.*?get.php.*?)<'
            matches = re.compile(patron, re.DOTALL).findall(data)
            
            for scrapedurl in matches:
                
                listurl = scrapedurl[0].replace("&amp;","&")
                listname = scrapedurl[0].split("/")[-2]
                xbmc.log("Finded url = " + listurl) 
                
                if string == "":
                    AddDir("[COLOR green]" + listname + "[/COLOR]", listurl, 51, "http://findicons.com/files/icons/1331/matrix_rebooted/128/text_clipping_file.png", isFolder=True)
                else:
                    sch_m3u(listurl,string,listname,live=live)
        
def OpenXML(url, string="",live=False):
    
    from xml.dom import minidom
    
    try:
        urldec = base64.decodestring(url)
        if common.check_url(urldec):
            url = urldec
    except:
        pass
    
    enckey=False
    urlrec = url
    
    if common.check_url(url):
        
        if '$$ref=' in url:
            enckey=url.split('$$ref=')[1].split('$$')[0]
            rp='$$ref=%s$$'%enckey
            url=url.replace(rp,"")
        
        data = common.cachepage(url,108000)
        
    else:
        f = open(url,'r')
        data = f.read().replace("\n\n", "")
        f.close()
        
    if enckey:
        import pyaes
        enckey=enckey.encode("ascii")
        print(enckey)
        missingbytes=16-len(enckey)
        enckey=enckey+(chr(0)*(missingbytes))
        print( repr(enckey))
        data=base64.b64decode(data)
        decryptor = pyaes.new(enckey , pyaes.MODE_ECB, IV=None)
        data=decryptor.decrypt(data).split('\0')[0]

    
    data = data.replace("&","&amp;").replace("&amp;amp;","&amp;")
    
    try:
        xmldoc = minidom.parseString(data)
        Data = xmldoc.getElementsByTagName('data')
        r = 0
        if  string == "":
            for d in Data:
                Type = d.getElementsByTagName("type")
                for node in Type:
                    nt = node.getAttribute('name')
                    if nt == "list":
                        r = 1
                        break
                    if nt == "folder":
                        r = 1
                        break
                
            if r==1:
                AddDir("[COLOR yellow][B]{0}[/B][/COLOR]".format(addons.VSlang(10250)), urlrec, 66, find, isFolder=True)
            
        for d in Data:
            Type = d.getElementsByTagName("type")
        
            for node in Type:
                nt = node.getAttribute('name')
                if nt == "channels":
                    mode = 3
                    icon = TVICO
                    isFolder=False                                
                elif nt == "list":
                    mode = 51
                    icon = iconlist
                    isFolder=True
                elif nt == "ylist":
                    mode = 93
                    icon = iconlist
                    isFolder=True

                itemlist = node.getElementsByTagName("item")
                
                Link = "" 

                for s in itemlist:

                    Name = s.getElementsByTagName("name")[0].childNodes[0].nodeValue.encode("UTF-8")
                    try:
                        Year = s.getElementsByTagName("year")[0].childNodes[0].nodeValue.encode("UTF-8")
                    except:
                        Year = ""                    
                    try:
                        Director = s.getElementsByTagName("director")[0].childNodes[0].nodeValue.encode("UTF-8")
                    except:
                        Director = ""
                    try:
                        Writer = s.getElementsByTagName("writer")[0].childNodes[0].nodeValue.encode("UTF-8")
                    except:
                        Writer = "" 
                    try:
                        Cast = s.getElementsByTagName("cast")[0].childNodes[0].nodeValue.encode("UTF-8")
                    except:
                        Cast = "" 
                    try:
                        Country = s.getElementsByTagName("country")[0].childNodes[0].nodeValue.encode("UTF-8")
                    except:
                        Country = "" 
                    try:
                        Genre = s.getElementsByTagName("genre")[0].childNodes[0].nodeValue.encode("UTF-8")
                    except:
                        Genre = ""
                    try:
                        Rating = str(float(s.getElementsByTagName("rating")[0].childNodes[0].nodeValue)).encode("UTF-8")
                    except:
                        Rating = ""
                    try:
                        Credit = str(float(s.getElementsByTagName("credit")[0].childNodes[0].nodeValue)).encode("UTF-8")
                    except:
                        Credit = ""
                    try:
                        Description = s.getElementsByTagName("description")[0].childNodes[0].nodeValue.encode("UTF-8")
                    except:
                        Description = ""
                    try:
                        Vid = s.getElementsByTagName("vid")[0].childNodes[0].nodeValue
                    except:
                        Vid = ""
                        pass
                    try:
                        Path = s.getElementsByTagName("path")[0].childNodes[0].nodeValue
                    except:
                        Path = ""
                        pass
                    try:
                        Link = s.getElementsByTagName("link")[0].childNodes[0].nodeValue
                    except:
                        Link = ""
                        pass

                    try:
                        Color = s.getElementsByTagName("color")[0].childNodes[0].nodeValue
                    except:
                        Color = ""
                        pass
                    try:
                        icon = s.getElementsByTagName("icon")[0].childNodes[0].nodeValue
                    except:
                        if not Link == "":
                            ext = "." + Link.split(".")[-1]
                            if bool(ext in EXTV):
                                icon = video
                            elif bool(ext in EXTA):
                                icon = audio
                    try:
                        fanart = s.getElementsByTagName("fanart")[0].childNodes[0].nodeValue
                    except:
                        fanart = ""
                    
                    if nt == "folder":
                        
                        if not Path == "":
                            if Path == "$download":
                                if not xbmcaddon.Addon('plugin.video.OTV_MEDIA').getSetting('download_path') == "":
                                    DD = xbmcaddon.Addon('plugin.video.OTV_MEDIA').getSetting('download_path')
                                else:
                                    DD = DFolder 
                                Link = DD
                            else:
                                Link = Path
                            mode = 164
                            icon = icondir
                            isFolder=True
                        else:
                            mode = 63
                            icon = icondir
                            isFolder=True 

                    elif nt == "ylist":
                        mode = 93
                        Link = Vid                        
                        icon = icondir
                        isFolder=True                        
                    
                    if icon == "video":
                        icon = video
                    if icon == "audio":
                        icon = audio
                    if icon == "folder":
                        icon = icondir
                    if icon == "list":    
                        icon = iconlist
                    if not Color == "" :
                        cname = "[COLOR " + Color + "][B]{0}[/B][/COLOR]".format(Name)
                    else:
                        cname = "{0}".format(Name)
                        
                    if nt == "list" and Link.startswith('page://'):
                        Link = Link.replace("page://","")
                        mode = 79    
                        
                    if string == "":    
                        AddDir(cname,Link,mode,icon,description=Description,isFolder=isFolder,background=fanart,genre=Genre,year=Year,director=Director,writer=Writer,cast=Cast,country=Country,rating=Rating,credit=Credit)
                    else:
                        sname = common.BBTagRemove(Name).replace("_"," ").replace("%20"," ").lower()
                        if mode == 3 and sname.find(string)>-1:
                            EXT = EXTV + EXTA
                            if not bool(ext in EXT) or not live:
                                if not bool(ext in EXT):
                                    FastDir(cname,Link,mode,icon,fanart=fanart,description=Description,res=True,isFolder=False)
                                else:
                                    AddDir(cname,Link,mode,icon,description=Description,isFolder=isFolder,background=fanart,genre=Genre,year=Year,director=Director,writer=Writer,cast=Cast,country=Country,rating=Rating,credit=Credit)
                        if mode == 151 or mode == 179:
                            sch_m3u(Link,string,sname,live=live)
                        if mode == 164:
                            PMFolder(Link,string,live=live)
                        if mode == 163:
                            OpenXML(Link,string,live=live)
                        if mode == 193:
                            Yplayl(Link,string,live=live)
    except:
        pass

def PMFolder( folder , string="",live=False):
    
    try:
        urldec = base64.decodestring(folder)
        if common.check_url(urldec):
            folder = urldec
    except:
        pass
    
    urlx = folder
    pw = ""
    
    if urlx.find("@")>-1:
        US = ""
        URL1 = urlx.split("@")[0]
    
        if urlx.startswith("http:"):
            proto = "http://"
        else:
            proto = "https://" 
    
        URL1 = urlx.replace("http://","").replace("https://","")
        us = URL1.split(":")[0]
        pw = URL1.split(":")[1]
        pw = pw.split("@")[0]
        
        datafile =  os.path.join( pwdir , base64.standard_b64encode(folder))
        pwm = ""
        usm = ""
        t = 0
        
        if os.path.isfile(datafile):
            f = open(datafile,'r')
            data = f.read().replace("\n\n", "")
            f.close() 
            pwm = find_single_match(data,"<password>([^<]+)</password>").strip()
            if not pwm == "": 
                pw = pwm
            usm = find_single_match(data,"<username>([^<]+)</username>").strip()
            if not usm == "": 
                us = usm
            folder = proto + us + ":" + pw + "@" + urlx.split("@")[1]
            
        if pw =="x" and string == "":
            if not us == "x":
                US = us
            stringa = GetKeyboardText("Enter username", US)
            if len(stringa) < 1:
                return
            us = stringa
            if not pw == "x":
                p = pw
            else:
                p = ""
                
            stringa = GetKeyboardText("Enter password", p)
            if len(stringa) < 1:
                return
            pw = stringa
            folder = proto + us + ":" + pw + "@" + urlx.split("@")[1]
            if os.path.isfile(datafile):
                os.remove(datafile)
                xbmc.sleep(1200)
            
        if not os.path.isfile(datafile) and string == "":
            content = "<username>" + us + "</username><password>" + pw + "</password>"
            common.write_file(datafile, content)
    
    DF =  folder
    dirs, files = xbmcvfs.listdir(DF)
    EXT = EXTL + EXTV + EXTA 
    
    files.sort()
    if  string == "":
        AddDir("[COLOR yellow][B]{0}[/B][/COLOR]".format(addons.VSlang(10250)), folder, 165, find, isFolder=True)
    
    
    if not xbmcaddon.Addon('plugin.video.OTV_MEDIA').getSetting('download_path') == "":
        DD = xbmcaddon.Addon('plugin.video.OTV_MEDIA').getSetting('download_path')
    else:
        DD = DFolder  
    
    if DF == DD and string == "":        
        src = os.path.join(xbmc.translatePath("special://userdata/addon_data" ), 'script.module.youtube.dl', 'tmp')
        AddDir("[COLOR red][B]{0}[/B][/COLOR]".format("Tmp"), src , 154, icondir, isFolder=True)
    
    for i in dirs:
        rf = format(i)
        cname = "[COLOR cyan][B]{0}[/B][/COLOR]".format(rf)
        
        if common.check_url(DF):
            url = DF  + rf + "/"
        else:
            url = os.path.join(DF, rf)

        url = url.replace("\r","").replace("\n","").strip()
        cname = cname.replace("%20"," ").replace("\r","").replace("\n","").strip()
        if string == "":
            AddDir(cname, url, 154, icondir, isFolder=True)
        else:
            PMFolder( url , string, live=live)
            
    for i in files:
        rf = format(i)
        ext = "." + rf.split(".")[-1]
        
        if ext == ".xml":
            
            Name = rf.replace("%20"," ").replace("\r","").replace("\n","").replace(".xml","").strip()
            Name = "[COLOR cyan][B]{0}[/B][/COLOR]".format(Name)
            
            if common.check_url(DF):
                url = DF + rf
            else:
                url = os.path.join(DF, rf)
            if string == "":
                AddDir(Name, url, 163, icondir, isFolder=True) 
            else:
                OpenXML(url,string,live=live)
    
    for i in files:    
        rf = format(i)
        ext = "." + rf.split(".")[-1]
        
        if bool(ext in EXT):
            
            Name = rf.replace("%20"," ").replace("\r","").replace("\n","").strip()
                
            if common.check_url(DF):
                url = DF + rf
            else:
                url = os.path.join(DF, rf)
		
            url = url.replace("\r","").replace("\n","").strip()

            if url.endswith(".m3u") or url.endswith(".txt") or url.endswith(".m3u8"):
                if string == "":
                    cname = "[COLOR green][B]{0}[/B][/COLOR]".format(Name)
                    AddDir(cname, url, 151, iconlist, isFolder=True)
                else:
                    sname = common.BBTagRemove(Name).replace("_"," ").replace("%20"," ").lower()
                    sch_m3u(url,string,sname,live=live)
            else:
                perc = -1
                p = ""
                EP = ""
                    
                if os.path.isfile(url + ".resume"):
                    EP = ".resume"
                elif os.path.isfile(url + ".stopped"):
                    EP = ".stopped"
                else:
                    perc = -1
                if not  EP == "":
                    PERC = common.ReadFile(url + EP).replace("\r","").split("\n")
                    perc = int(PERC[0])
                        
                if not perc <=0:
                    size = 0
                    size = os.stat(url).st_size
                        
                    if size > 0:
                        perc = round((100.0*size)/int(perc), 2)

                        col = "green"
                            
                        if perc <80:
                            col = "yellow"
                        if perc <55:
                            col = "orange"
                        if perc <35:
                            col = "orangered"
                        if perc <15:
                            col = "red"

                        p = " - [B][COLOR blue][ [COLOR " + col + "]" + str(perc) + "% [/COLOR]][/B][/COLOR]"
                
                elif not EP == "":
                    p = " - [B][COLOR blue][ [COLOR yellow] Download in progress [/COLOR]][/B][/COLOR]"

        
                if bool(ext in EXTV):
                    icon = video
                else:
                    icon = audio
                
                if string == "":    
                    cname = "[COLOR CCCCFFFF][B]{0}[/B][/COLOR]".format(Name) + p
                    AddDir(cname , url, 150 , icon, "", isFolder=False)
                else:
                    EXT1 = EXTV + EXTA 
                    if bool(ext in EXT1) and not live:
                        sname = common.BBTagRemove(Name).replace("_"," ").lower()
                        if sname.find(string)>-1:
                            cname = "[COLOR CCCCFFFF][B]{0}[/B][/COLOR]".format(Name) + p
                            AddDir(cname , url, 150 , icon, "", isFolder=False)
                        

def AddDir(name,url,mode,iconimage,description="",isFolder=True,background="",genre="",year="",director="",writer="",cast="",country="",rating="",credit=""):
    url = "https://findicons.com/search/search"
    url = url.replace('\n','')
    url = url.replace('\r','')
    url = url.strip()
    try:
        urlz = url.split("|")[1]
        #url = url.split("|")[0]
        #if urlz == "Player=HLS":
        #   url = url + '|' + urlz
    except:
        urlz = ""
    
    name = name.strip()
    if not mode == 32:
        name = common.GetEncodeString(name)
        
    EXTM = EXTV + EXTA
    
    u=sys.argv[0]+"?url="+Unquote_plus(url)+"&mode="+str(mode)+"&name="+Unquote_plus(name)+"&iconimage="+Unquote_plus(iconimage)+"&description="+Unquote_plus(description)
        
    liz = xbmcgui.ListItem(name)

    liz.setArt({'fanart': Addon.getAddonInfo('fanart')})
    liz.setArt({ 'thumb': iconimage})
    ext = ""
	
    if not background == "":
            liz.setProperty('fanart_image', background)
            
    if mode == 114 or mode == 121 or mode == 151 or mode == 154 or mode == 150 or mode == 160 or mode == 163 or mode == 164 or mode == 170 or mode == 179:
        items = [ ]
        
        if mode == 154:
            items.append(('Youtube-dl Control','XBMC.RunPlugin({0}?url={1}&name={2}&mode=80)'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(name))))
        
        if mode == 121 or mode == 163 or mode == 164 or mode == 170 or mode == 179:
            urlE = url
            try:
                urldec = base64.decodestring(url)
                if common.check_url(urldec):
                    url = urldec
            except:
                pass            
            
            if not mode == 164 and not mode == 163:
                items = [('{0}'.format(addons.VSlang(10008)) + name, 'XBMC.RunPlugin({0}?url={1}&name={2}&mode=55)'.format(sys.argv[0], Unquote_plus(urlE), Unquote_plus(name)))]
                items.append(('{0}'.format(addons.VSlang(10018)), 'XBMC.RunPlugin({0}?url={1}&name={2}&mode=161)'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(name))))
            else:
                items.append(('Youtube-dl Control','XBMC.RunPlugin({0}?url={1}&name={2}&mode=80)'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(name))))
            
            if url.find("@")>0:
                datafile = os.path.join( pwdir , base64.standard_b64encode(url) )
                if os.path.isfile(datafile):
                    items.append((addons.VSlang(10207), 'XBMC.RunPlugin({0}?url={1}&mode=56)'.format(sys.argv[0], Unquote_plus(url))))
            if mode == 163 or mode == 121 or mode == 170 or mode == 179:
                listDir = common.ReadList(playlistsFile4)
                for fold in listDir:
                    if not url == urlE:
                        t1 = fold["url"]
                        t2 = urlE
                    else:
                        t1 = fold["url"].lower()
                        t2 = url.lower()
                        
                    if t1 == t2:
                        e = ""
                        try:
                            e = fold["exclude"]
                        except:
                            pass
                        
                        if e == "yes":
                            items.append((addons.VSlang(10252), 'XBMC.RunPlugin({0}?url={1}&name={2}&mode=68)'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(name))))
                        else:
                            items.append((addons.VSlang(10251), 'XBMC.RunPlugin({0}?url={1}&name={2}&mode=67)'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(name))))
                
                TempName = base64.standard_b64encode(url)
                tmp = os.path.join(cdir, TempName)
            
                if os.path.isfile(tmp):            
                    items.append(('{0}'.format(addons.VSlang(10105)), 'XBMC.RunPlugin({0}?url={1}&name={2}&mode=94)'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(name))))
                 
        if mode == 4:
            
            if url.find("get.php?username=")>0 or name.lower().find("fast open")>-1 or name.lower().find("slow open")>-1 or name.lower().find("tv_channels")>-1 or name.lower().find("[iptv]")>-1:
                items.append(('Check List : [COLOR yellow]' + common.BBTagRemove(name) + '[/COLOR]', 'XBMC.RunPlugin({0}?url={1}&mode=90&iconimage={2}&name={3})'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(iconimage), Unquote_plus(name))))
                    
            items.append(('{0}'.format(addons.VSlang(10008)) + name, 'XBMC.RunPlugin({0}?url={1}&mode=22)'.format(sys.argv[0], Unquote_plus(url))))
            
            items.append(('{0}'.format(addons.VSlang(10018)), 'XBMC.RunPlugin({0}?url={1}&name={2}&mode=23)'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(name))))
            items.append(('{0}'.format(addons.VSlang(10019)), 'XBMC.RunPlugin({0}?url={1}&name={2}&mode=24)'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(name))))
            
            TempName = base64.standard_b64encode(url)
            tmp = os.path.join(cdir, TempName)
            
            if os.path.isfile(tmp):
                items.append(('{0}'.format(addons.VSlang(10105)), 'XBMC.RunPlugin({0}?url={1}&name={2}&mode=94)'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(name))))
            
        if mode ==51 or mode == 50:
            name = common.BBTagRemove(name)
            
            try:
                urldec = base64.decodestring(url)
                if common.check_url(urldec):
                    url = urldec
            except:
                pass
                
            if not common.check_url(url):
                items = [('{0}'.format(addons.VSlang(10205)) + ' : ' + name, 'XBMC.RunPlugin({0}?url={1}&name={2}&mode=52)'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(name)))]
            if url.find("get.php?username=")>0 or name.lower().find("fast open")>-1 or name.lower().find("slow open")>-1 or name.lower().find("tv_channels")>-1 or name.lower().find("[iptv]")>-1:
                items.append(('Check List : [COLOR yellow]' + name + '[/COLOR]', 'XBMC.RunPlugin({0}?url={1}&mode=90&iconimage={2}&name={3})'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(iconimage), Unquote_plus(name))))
            
            TempName = base64.standard_b64encode(url)
            tmp = os.path.join(cdir, TempName)
            
            if os.path.isfile(tmp):            
                items.append(('{0}'.format(addons.VSlang(10105)), 'XBMC.RunPlugin({0}?url={1}&name={2}&mode=94)'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(name))))
            
        if mode == 50:
            ext = url.split('.')[-1]
            namefile = urllib.unquote(os.path.basename(url)).replace("." + ext,"")
            if url.find("pornhd.com")>0:
                namefile = urllib.unquote(os.path.basename(url)).split('.')[-2]
            
            if os.path.isfile( url + ".stopped"):
                urlx = common.ReadFile(url + ".stopped").replace("\r","").split("\n")
                items.append((addons.VSlang(10213) + ' : ' + namefile, 'XBMC.RunPlugin({0}?url={1}&mode=7&iconimage={2}&name={3})'.format(sys.argv[0], Unquote_plus(urlx[1]), Unquote_plus(iconimage), Unquote_plus(namefile))))
            elif os.path.isfile( url + ".resume"):
                urlx = common.ReadFile(url + ".resume").replace("\r","").split("\n")
                items.append((addons.VSlang(10212) + ' : ' + namefile, 'XBMC.RunPlugin({0}?url={1}&mode=57&iconimage={2}&name={3})'.format(sys.argv[0], Unquote_plus(urlx[1]), Unquote_plus(iconimage), Unquote_plus(namefile))))
            
            items.append(('{0}'.format(addons.VSlang(10009)), 'XBMC.RunPlugin({0}?url={1}&mode=31&iconimage={2}&name={3})'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(iconimage), Unquote_plus(name))))
            
        if mode ==51 or mode == 50:
            if not common.check_url(url):
                if not os.path.isfile( url + ".stopped") and not os.path.isfile( url + ".resume"):
                    items.append(('{0}'.format(addons.VSlang(10018)), 'XBMC.RunPlugin({0}?url={1}&name={2}&mode=53)'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(name))))
            
            items.append(('Youtube-dl Control','XBMC.RunPlugin({0}?url={1}&name={2}&mode=80)'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(name))))
            items.append(('Refresh', 'Container.Refresh'))
        
        if mode == 50:
            if bool(ext in EXTV):
                liz.addContextMenuItems(items)
            else:
                liz.addContextMenuItems(items, replaceItems=True)
        else:
            liz.addContextMenuItems(items)
	
    
    if mode == 3 or mode == 32:
        liz.setProperty( "Video", "true")
        liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description,"Genre": genre, "Year" : year, "Director" : director, "Writer" : writer, "Cast" : cast.split(","), "Country" : country, "Rating": rating, "Credit": credit})
        liz.setProperty('IsPlayable', 'true')
        if mode == 3:
            items = [('{0}'.format(addons.VSlang(10009)), 'XBMC.RunPlugin({0}?url={1}&mode=31&iconimage={2}&name={3})'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(iconimage), Unquote_plus(name)))]
        else:
            items = [('{0}'.format(addons.VSlang(10010)), 'XBMC.RunPlugin({0}?url={1}&mode=33&iconimage={2}&name={3})'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(iconimage), Unquote_plus(name)))]
            items.append(('{0}'.format(addons.VSlang(10018)), 'XBMC.RunPlugin({0}?url={1}&name={2}&mode=169)'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(name))))
        ext = '.' + url.split('.')[-1]
        ref = 1
        
        if bool(ext in EXTM) or url.find("pornhd.com")>0:
            
            if url.find("pornhd.com")>0:
                ext = '.mp4'
            else:
                xbmcplugin.setContent(int(sys.argv[1]), 'movies')
            
            if common.check_url(url):
                name = name.replace(","," ")
                name = name.replace("  "," ")
                pname = common.BBTagRemove(name).replace(":","-").replace(".","-").replace("/","-")
                
                try:
                    pname = pname.split('[CR]')[-2]
                    ref = 0
                except:
                    pass
                
                pname = pname.strip()
                
                if not xbmcaddon.Addon('plugin.video.OTV_MEDIA').getSetting('download_path') == "":
                    dpath = xbmcaddon.Addon('plugin.video.OTV_MEDIA').getSetting('download_path')
                else:
                    dpath = DFolder
                            
                file = dpath + pname + ext
                 
                if ref == 0:

                    if os.path.isfile( file + ".stopped") and os.path.isfile( file):
                        items.append((addons.VSlang(10213) + ' : ' + pname, 'XBMC.RunPlugin({0}?url={1}&mode=6&iconimage={2}&name={3})'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(iconimage), Unquote_plus(pname))))
                        items.append((addons.VSlang(10213) +' : ' + pname, 'XBMC.RunPlugin({0}?url={1}&mode=171&iconimage={2}&name={3})'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(iconimage), Unquote_plus(pname))))
                    elif os.path.isfile( file + ".resume") and os.path.isfile( file):
                        items.append((addons.VSlang(10212) + ' : ' + pname, 'XBMC.RunPlugin({0}?url={1}&mode=172&iconimage={2}&name={3})'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(iconimage), Unquote_plus(pname))))
                    else:
                        items.append(('Download : ' + pname, 'XBMC.RunPlugin({0}?url={1}&mode=6&iconimage={2}&name={3})'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(iconimage), Unquote_plus(pname))))                
                
                else:
                    if os.path.isfile( file + ".stopped") and os.path.isfile( file):
                        items.append((addons.VSlang(10213) + ' : ' + pname, 'XBMC.RunPlugin({0}?url={1}&mode=7&iconimage={2}&name={3})'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(iconimage), Unquote_plus(pname))))
                        items.append((addons.VSlang(10214) +' : ' + pname, 'XBMC.RunPlugin({0}?url={1}&mode=58&iconimage={2}&name={3})'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(iconimage), Unquote_plus(pname))))
                    elif os.path.isfile( file + ".resume") and os.path.isfile( file):
                        items.append((addons.VSlang(10212) + ' : ' + pname, 'XBMC.RunPlugin({0}?url={1}&mode=57&iconimage={2}&name={3})'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(iconimage), Unquote_plus(pname))))
                    else:
                        items.append(('Download : ' + pname, 'XBMC.RunPlugin({0}?url={1}&mode=7&iconimage={2}&name={3})'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(iconimage), Unquote_plus(pname))))
                    items.append(('Refresh', 'Container.Refresh'))
        elif ext == ".html" or url.find("plugin.video.youtube")>0:
            xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        
        urldec = ""
        
        try:
            urldec = base64.decodestring(url)
            if common.check_url(urldec):
                url = urldec
        except:
            pass
        
        if url.find(".m3u8")>0 or urlz == "m3u8" or url.find("urhd.tv")>-1:
            items.append(('Play with HLS-Player','XBMC.RunPlugin({0}?url={1}&iconimage={2}&name={3}&mode=5)'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(iconimage), Unquote_plus(name))))
        
        if os.path.exists(ydldir) and not url.find("pornhd.com")>0:
            items.append(('Youtube-dl Control','XBMC.RunPlugin({0}?url={1}&name={2}&mode=80)'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(name))))

        # openload megahd nowvideo fastvideo rapidvideo nowdownload speedvideo streamin.to abysstream.com/
        if url.find("Player=HLS")>0 or url.find("openload.")>0 or url.find("megahd.")>0 or url.find("nowvideo.")>0 or url.find("fastvideo.")>0 or url.find("rapidvideo.")>0 or url.find("nowdownload.")>0 or url.find("speedvideo.")>0 or url.find("streamin.to")>0 or url.find("abysstream.com/")>0:
            liz.addContextMenuItems(items, replaceItems=True)
        else:
            liz.addContextMenuItems(items)
    if mode == 20:        
        items = [('{0}'.format(addons.VSlang(10120)) , 'XBMC.RunPlugin({0}?url={1}&mode=191)'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(name))),  
                        ('{0}'.format(addons.VSlang(10121)) , 'XBMC.RunPlugin({0}?url={1}&mode=192)'.format(sys.argv[0], Unquote_plus(url), Unquote_plus(name))) ]
        liz.addContextMenuItems(items , replaceItems=True)
    
    if mode == 30 or mode == 48 or mode == 49 or mode == 46 or mode == 34:
        liz.addContextMenuItems( [] , replaceItems=True)
    
    #xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)


def PM_index():
    
    AddDir("[COLOR yellow][B]{0}[/B][/COLOR]".format(addons.VSlang(10250)), "search" , 165, find, isFolder=True)
#    AddDir("[COLOR blue][B]{0}[/B][/COLOR]".format(addons.VSlang(10001)), "settings" , 120, "http://findicons.com/files/icons/1331/matrix_rebooted/128/new_folder.png", isFolder=False)
    
    if not xbmcaddon.Addon('plugin.video.OTV_MEDIA').getSetting('download_path') == "":
        DD = xbmcaddon.Addon('plugin.video.OTV_MEDIA').getSetting('download_path')
    else:
        DD = DFolder  
            
    AddDir("[COLOR cyan][B]{0}[/B][/COLOR]".format(addons.VSlang(10112)), DD , 160, "http://findicons.com/files/icons/1331/matrix_rebooted/128/drop_folder.png", isFolder=True)
    listDir = common.ReadList(playlistsFile4)
    
    for fold in listDir:
        name = "[COLOR cyan][B]{0}[/B][/COLOR]".format(fold["name"].encode("utf-8"))
        
        t = ""
        try:
            t = fold["type"]
        except:
            pass
        
        if t == "xml":
            mode = 170
        elif t == "page":
            mode = 179
        elif t == "pyt":
            mode = 193
        else:
            mode = 121
        
        AddDir(name, fold["url"].encode("utf-8"), mode, "http://findicons.com/files/icons/1331/matrix_rebooted/128/generic_folder_alt.png", isFolder=True)       
        
    list = common.ReadList(playlistsFile2)
    for channel in list:
        if channel["url"].find("://")>0:
            color = "FF00c100"
        else:
            color = "green"
            
        name = "[COLOR " + color + "][B]{0}[/B][/COLOR]".format(channel["name"].encode("utf-8"))
        AddDir(name, channel["url"].encode("utf-8"), 114, "http://findicons.com/files/icons/1331/matrix_rebooted/128/text_clipping_file.png", isFolder=True)
        
def ChangeName(name, listFile, key, title):
    
    list = common.ReadList(listFile)
    
    if not listFile == favoritesFile:
        name = common.BBTagRemove(name)
    
    string = GetKeyboardText(addons.VSlang(title), name)
    if len(string) < 1:
            return
    for channel in list:    
        if channel["url"] == url:
            channel["name"] = string
            break
        else:
            try:
                ure = base64.b64encode(url)
            except:
                ure = ""
            
            if channel["url"] == ure:
                channel["name"] = string
                break
                
    if common.SaveList(listFile, list):
            xbmc.executebuiltin("XBMC.Container.Refresh()")
		
def ChangeUrl(name, listFile, key, title):
        
    list = common.ReadList(listFile)
    name = re.sub('\[.*?]','',name)
	
    if not common.check_url(url):
        string = xbmcgui.Dialog().browse(int(1), addons.VSlang(10006), 'myprograms','.m3u8|.m3u')
        if not string:
            return
    else:
        string = GetKeyboardText(addons.VSlang(title), url)
            
    if len(string) < 1:
            return
    for channel in list:    
        if channel["url"] == url:
            channel["url"] = string
            break
    if common.SaveList(listFile, list):
            xbmc.executebuiltin("XBMC.Container.Refresh()")
	
def GetKeyboardText(title = "", defaultText = ""):
    
    keyboard = xbmc.Keyboard(defaultText, title)
    keyboard.doModal()
    text =  "" if not keyboard.isConfirmed() else keyboard.getText()
    return text

def GetSourceLocation(title, list):
    
    dialog = xbmcgui.Dialog()
    answer = dialog.select(title, list)
    return answer
	
def AddFavorites(url, iconimage, name):
    
    favList = common.ReadList(favoritesFile)
    for item in favList:
        if item["url"] == url:
            xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, name, addons.VSlang(10011), icon))
            return
        
    name = name.replace('\r','').replace('\r','').strip()
    url = url.replace('\n','').replace('\r','').strip()
	
    if not iconimage:
        iconimage = ""
    else:
        iconimage = iconimage.replace('\r','').replace('\n','').strip()
        
    data = {"url": url, "image": iconimage, "name": name }
    favList.append(data)
    common.SaveList(favoritesFile, favList)
    xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, name, addons.VSlang(10012), icon))
		
def ListFavorites():
    
    AddDir("[COLOR yellow][B]{0}[/B][/COLOR]".format(addons.VSlang(10013)), "favorites" ,34 ,os.path.join(addonDir, "resources", "images", "bright_yellow_star.png"), isFolder=False)
    if 'win32' or 'linux' or 'darwin' in sys.platform:
        AddDir("[COLOR red][B]{0}[/B][/COLOR]".format(addons.VSlang(10099)) + " - Press [ALT] + [F4] to close", "Netflix" ,48 ,os.path.join(addonDir, "resources", "images", "netflix.png"), isFolder=False)
    if 'win32' or 'linux' or 'darwin' in sys.platform:
        AddDir("[COLOR gold][B]{0}[/B][/COLOR]".format((addons.VSlang(10098))) + " - Press [ALT] + [F4] to close", "Offer" ,49 , os.path.join(addonDir, "resources", "images", "paypal.png"), isFolder=False)
	
    list = common.ReadList(favoritesFile)
    for channel in list:
        name = channel["name"].encode("utf-8")
        iconimage = channel["image"].encode("utf-8")
        if iconimage=="":
            iconimage = TVICO 
        
        AddDir(name, channel["url"].encode("utf-8"), 32, iconimage, isFolder=False) 
        #FastDir(name,channel["url"].encode("utf-8"),32,iconimage,isFolder=False)
        
def ListSub(lng):
    
    list = common.ReadList(lng)
    for item in list:
        mode =  2
        image = item.get('image', '')
        if not "http" in image:
                icon = os.path.join(addonDir, "resources", "images", image.encode("utf-8"))
        else:
                icon = image.encode("utf-8")
                
        try:
            name = int(item["name"])
            name = addons.VSlang(name)
        except:
            name = item["name"]
                
        cname = "[COLOR gold][B]{0}[/B][/COLOR]".format(name)
        AddDir(cname ,item["url"], mode , icon)

def ListTB(lg):
    
    ok = show_main(lg)

def RemoveFavorties(url):
    
    list = common.ReadList(favoritesFile) 
    for channel in list:
        if channel["url"].lower() == url.lower():
            list.remove(channel)
            break
			
    common.SaveList(favoritesFile, list)
    xbmc.executebuiltin("XBMC.Container.Refresh()")

def AddNewFavortie():
    
    chName = GetKeyboardText("{0}".format(addons.VSlang(10014))).strip()
    if len(chName) < 1:
            return
    chUrl = GetKeyboardText("{0}".format(addons.VSlang(10015))).strip()
    if len(chUrl) < 1:
            return
		
    favList = common.ReadList(favoritesFile)
    for item in favList:
            if item["url"].lower() == url.lower():
                    xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, chName, addons.VSlang(10011), icon))
                    return
			
    data = {"url": chUrl, "image": "", "name": chName.decode("utf-8")}
    favList.append(data)
    if common.SaveList(favoritesFile, favList):
            xbmc.executebuiltin("XBMC.Container.Update('plugin://{0}?mode=30&url=favorites')".format(AddonID))

############################################################################################
#    Modulo ricerca    

def sch_global(string,live=False):
    
    #0 - search in italian channels
    sch_m3u(os.path.join(chanDir, "it.txt"),string,addons.VSlang(10052),live=live)
    sch_m3u(os.path.join(chanDir, "vpnit.txt"),string,addons.VSlang(10051),live=live)
    sch_m3u(os.path.join(chanDir, "w_it.txt"),string,addons.VSlang(10054),live=live)
    
    # 1 - search in download folder
    if not xbmcaddon.Addon('plugin.video.OTV_MEDIA').getSetting('download_path') == "":
        DD = xbmcaddon.Addon('plugin.video.OTV_MEDIA').getSetting('download_path')
    else:
        DD = DFolder 
    
    PMFolder(DD,string,live=live)
    
    # 2 - search in m3ulist-index
    list = common.ReadList(playlistsFile2)
    for channel in list:
        url = channel["url"]
        sname = common.BBTagRemove(channel["name"]).replace("_"," ").replace("%20"," ").lower()
        sch_m3u(url,string,sname,live=live)

    # 3 - search in folder/xml-index
    listDir = common.ReadList(playlistsFile4)
    
    for fold in listDir:
        name = fold["name"]

        try:
            t = fold["type"]
        except:
            t = ""
        try:
            e = fold["exclude"]
        except:
            e = ""
        
        if e == "":
            if t == "xml":
                OpenXML(fold["url"],string,live=live)
            elif t == "page":
                findm3u(fold["url"],string,live=live)
            else:
                PMFolder(fold["url"],string,live=live)
        
def sch_folder(url,string):
    
    string = string.lower()
    PMFolder(url,string)

def sch_xml(url,string):
    
    string = string.lower()
    OpenXML(url,string)

def sch_m3u(url,string,sname,live=False):

    try:
        urldec = base64.decodestring(url)
        if common.check_url(urldec):
            url = urldec
    except:
        pass

    list = common.cachelist(url,cdir)
    
    for channel in list:
        name = channel["display_name"]
        name = common.BBTagRemove(name) 
        Name = name
        name = name.replace("_"," ").lower().strip()
        url = channel["url"].strip()
        ext = "." + url.split(".")[-1].strip()
        EXT = EXTV + EXTA
        
        if not bool(ext in EXT) or not live:
        
            if name.find(string)>-1:
                if channel.get("tvg_logo", ""):
                    if common.check_url(channel.get("tvg_logo", "")):
                        iconname = channel.get("tvg_logo", "")
                    else:
                        logo = channel.get("tvg_logo", "")
                        iconname = "https://kodilive.eu/logo/" + logo
                else :
                    iconname = TVICO

                listName = "  " + "[CR][I][COLOR blue][LIGHT]* {0}[/COLOR]".format(addons.VSlang(10004)) + " -->  [COLOR yellow]{0}[/COLOR][/I][/LIGHT]".format(sname)
                cname = "[COLOR orange][B]{0}[/B][/COLOR]".format(Name) + listName
                if live or not bool(ext in EXT):
                    FastDir(cname,url,3,iconname,res=True,isFolder=False)
                else:
                    AddDir(cname,url,3,iconname,isFolder=False)

def sch_exclude(url, listFile, key):
    
    list = common.ReadList(listFile)

    for channel in list:    
        if channel["url"].lower() == url.lower():
            channel["exclude"] = key
            break
        else:
            try:
                ure = base64.b64encode(url)
            except:
                ure = ""
            
            if channel["url"] == ure:
                channel["exclude"] = key
                break
            
    if common.SaveList(listFile, list):
        xbmc.executebuiltin("XBMC.Container.Refresh()")

##########################
# Specials Channels


def rsich(cid):
    pid = cid.split(":")[0]
    cid = cid.split(":")[1]
    url = "http://tp.srgssr.ch/akahd/token?acl=/i/" + cid +"/*"
    
    from random import randint
    a = str(randint(0,8))
    b = str(randint(0,256))
    c = str(randint(0,256))
    ip = "85."+a+'.'+b+'.'+c
    
    xbmc.log("random ip = "+ip)
    
    data = common.OpenURL(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko'})
    token = common.find_param('authparams":"(.*?)"',data)
    xbmc.log("RSI token = " + token)

    
    url = 'https://srgssruni' + pid +'ch-lh.akamaihd.net/i/' + cid + '/master.m3u8?' + token + '|X-Forwarded-For='+ip
    xbmc.log("RSI url = " + url)
    return url

def Opus(cid,headers={'Referer':'http://opus.re','User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.116 Chrome/48.0.2564.116 Safari/537.36'}):
    
    cid = cid.split("-$$")[1]
    cid1 = cid
    cid = cid.replace("_sd&","_hd&")
    
    if cid == "tf1":
        data = common.OpenURL('http://opus.re/wattf1.php?name=TF1')
        #xbmc.log("##### url tf1 = " + data)
        itemlink = common.find_param('file: *"([^",]+)',data)
        return itemlink
    else:
        url = "http://opus.re/index-PLAYLIST.php"
        
        data = common.OpenURL(url)
        #xbmc.log("##### url opus index = " + data,xbmc.LOGNOTICE)

        itemlink = common.find_param('opus.re/(.*?)/' + cid,data)
        xbmc.log("##### itemlink = " + itemlink,xbmc.LOGNOTICE)
        if cid == "arte":
            return "http://opus.re/" + itemlink + "/arte.m3u8"
        elif cid == "103":
            return "http://opus.re/" + itemlink + "/103.m3u8"
        elif cid == "101":
            return "http://opus.re/" + itemlink + "/101.m3u8"         
        else:
            data2 = common.OpenURL('http://opus.re/' + itemlink + "/" + cid + "/master.m3u8")
            
            try:
                item = common.find_param('opus.re/([^,]+)/2290000/index.m3u8',data2)
                itemlink =  item + '/2290000/index.m3u8' 
                return 'http://opus.re/' + itemlink
            except:
                return 'http://opus.re/' + itemlink + "/" + cid + "/master.m3u8"
                pass

def getIpBoxList(string="",live=False):
    ret=[]
    try:
        servers=common.cachepage("http://pastebin.com/raw/GrYKMHrF",3650)
        servers=servers.splitlines()

        import time
        for ln in servers:
            if not ln.startswith("##") and len(ln)>0:
                try:
                    print('ln',ln)
                    servername,surl=ln.split('$')
                    
                    if not servername.startswith("---"):
                        if '[gettext]' in surl:
                            surl,fileheaders,playheaders=surl.split('|')
                            surl = common.cachepage(surl.replace('[gettext]',''),3600)
                            if ' ' in surl or '>' in surl:
                                surl=surl.replace(' ','%20')
                                surl=surl.replace('>','%3E')
                                surl=surl.replace('<','%3C')
                            
                            try:
                                playheaders = playheaders.split("=")[1]
                                surl = surl + "|User-Agent=" + common.OpenURL(playheaders)
                            except:
                                pass
                            
                        if string == "":
                            typ = "- [COLOR yellow][mpeg][/COLOR]"
                            if surl.find("output=hls")>-1:
                                typ = "- [COLOR pink][hls][/COLOR]"
                                
                            AddDir("[B][COLOR green]" + servername + " List[/COLOR][/B] " + typ, surl, 51, iconlist, isFolder=True)
                        else:
                            sch_m3u(surl,string,servername,live=live)
                        
                except: traceback.print_exc(file=sys.stdout)
    except:
        traceback.print_exc(file=sys.stdout)

##########################
# Youtube Playlist

def Yplayl(url,string="",live=False):

    youdir = os.path.join(xbmc.translatePath("special://home/addons/"),'plugin.video.youtube')
    if not os.path.exists(youdir):
        if string == "":
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%("For this feature you need to install","[B][COLOR violet]Youtube video plugin[/COLOR][/B]", 6800, icon))
    else:
        
        if not string == "":
            listName = "  " + "[CR][I][COLOR blue][LIGHT]Youtube-Playlist[/COLOR] -->  [COLOR yellow]{0}[/COLOR][/I][/LIGHT]".format(url)

        url = "https://www.youtube.com/playlist?list=" + url    
        data = common.cachepage(url,1200,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko'})
        patron = 'data-video-id="([^"]+)(.*?)data-title="([^"]+)(.*?)data-thumb="([^"]+)'
        matches = re.compile(patron, re.DOTALL).findall(data)
        
        #from pytube import YouTube 
        
        for scrapedvid, sep, scrapedtitle, sep2, thumb in matches:
            scrapedtitle = common.decodeHtmlentities(scrapedtitle).strip()
            titolo = "[COLOR pink]" + scrapedtitle + "[/COLOR]"
            url = "plugin://plugin.video.youtube/play/?video_id=" + scrapedvid
            #url = 'http://www.youtube.com/watch?v=' + scrapedvid
            #yt = YouTube(url)
            #url = yt.filter('mp4')[-1]
            
            img = "https://i.ytimg.com/vi/" + scrapedvid + "/hqdefault.jpg"
            fanart = "https://i.ytimg.com/vi/" + scrapedvid + "/maxresdefault.jpg"        
            if not thumb.find("no_thumbnail")>-1:
                if string == "":
                    AddDir(titolo,url,3,img,background=fanart,isFolder=False)
                else:
                    sname = scrapedtitle.replace("_"," ").replace("%20"," ").lower()
                    if sname.find(string)>-1:
                        titolo = "[COLOR orangered]" + scrapedtitle + "[/COLOR]" + listName
                        AddDir(titolo,url,3,img,background=fanart,isFolder=False)

##########################
# Luci Rosse

def Pornazzi(url):
    
    if url == "index":
        urlbase = "http://www.pornhd.com/category"
        data = common.cachepage(urlbase,360000,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko'})
        patron = 'data-original="([^"]+)[^<]+[^<]+</span>(.*?)</a>'
        matches = re.compile(patron, re.DOTALL).findall(data)

        for scrapedimg, scrapedtitle in matches:
        
            scrapedtitle = common.decodeHtmlentities(scrapedtitle).strip()
            titolo = "[COLOR pink] " + scrapedtitle + "[/COLOR]"
            url = urlbase + "/" + scrapedtitle.replace(" ","-").lower() + "-videos"
            
            FastDir(titolo,url,77,scrapedimg,fanart="http://3da9975e9b4bda14573affe3f9f02618.lswcdn.net/343/Zy8RGV1LK7/1280x720new/37.jpg", isFolder=True)
    else:
        data = common.cachepage(url,360000,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko'})
        patron = 'src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7".*?data-original="([^"]+)[^<]+<[^<]+<[^<]+<[^<]+<[^<]+<[^<]+<[^<]+<[^<]+<[^<]+<[^<]+<[^<]+<[^<]+<.*?title" href="(.*?)">(.*?)</a>'
        urlbase = "http://www.pornhd.com"
        
        matches = re.compile(patron, re.DOTALL).findall(data)
 
        for scrapedimg, scrapedlink, scrapedtitle in matches:

            scrapedtitle = common.decodeHtmlentities(scrapedtitle).strip()
            titolo = "[COLOR gold] " + scrapedtitle + "[/COLOR]"          
            link = urlbase + scrapedlink
            fanart = scrapedimg.replace("320x180new","1280x720new")
            
            AddDir(titolo,link,3,scrapedimg,background=fanart, isFolder=False)
        
        n = re.search("Videos \(([^\),]+)", data) 
        N = int(int(n.group(1))/96)
        
        if not url.find("?page=")>-1:
            link = url + "?page=2"
            numb = 1
        else:
            urlb = url.split("?page=")
            link = urlb[0]
            numb = int(urlb[1])+1
            link = link + "?page=" + str(numb)
        
        if not numb>N:
            FastDir("[B] NEXT PAGE >>> [/B]",link,77,"http://c88016e5e72cbf2a8fd798c753f8a45a.lswcdn.net/139/fftJZJnQrF/320x180new/81.jpg",fanart="http://c88016e5e72cbf2a8fd798c753f8a45a.lswcdn.net/139/fftJZJnQrF/1280x720new/81.jpg", isFolder=True)
  
##########################
# Oggi in TV

def tvoggi(url):
    
    urlbase = "http://www.comingsoon.it/filmtv"
    
    #if url == "/":
    #    t = 159
    #else:
    #    t = 359
    
    data = common.OpenURL(urlbase + url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko'})
    
    patron = '<div class="col-xs-5 box-immagine">[^<]+<img src="([^"]+)[^<]+<[^<]+<[^<]+<[^<]+<[^<]+<.*?titolo">(.*?)</div>[^<]+<div class="h5 ora-e-canale">[^<]+<span>(.*?)</span><br />(.*?)<[^<]+</div>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedthumbnail, scrapedtitle, scrapetime, scrapedtv in matches:

        scrapedtitle = common.decodeHtmlentities(scrapedtitle).strip()
        titolo = scrapetime + " : [COLOR gold] " + scrapedtitle + "[/COLOR] - [COLOR orange] " + scrapedtv + "[/COLOR]"
        url = scrapedtv.lower() 
        url = url.replace("la2","la 2").replace("la1","la 1")
        
        FastDir(titolo,url,73,icon=scrapedthumbnail,fanart="http://www.ore12.net/wp-content/uploads/2016/08/cinema.jpg")

       
def SetteGiorniTV(day=""):
    if day == "":
        import datetime
        from datetime import date, timedelta
        start = date.today()
        icon = ""
        
        Link = ["/","/domani/","/dopodomani/","/giorno-3/","/giorno-4/","/giorno-5/","/giorno-6/"]
        Days = ["Oggi","Domani","Dopodomani","Fra 3 giorni","Fra 4 giorni","Fra 5 giorni","Fra 6 giorni"]
        
        AddDir("[COLOR gold][B]" + str(date.today()) + " - Film in TV " + Days[0] + "[/B][/COLOR]", Link[0], 75, icon, isFolder=True)
        for add in range(1, 7):
            future = start + timedelta(days=add)
            AddDir("[COLOR gold][B]" + str(future) + " - Film in TV " + Days[add] + "[/B][/COLOR]", Link[add], 75, icon, isFolder=True)
    else:
        if day == "/":
            AddDir("[COLOR red][B]ORA IN ONDA[/B][/COLOR]", day, 74, "http://a2.mzstatic.com/eu/r30/Purple/v4/3d/63/6b/3d636b8d-0001-dc5c-a0b0-42bdf738b1b4/icon_256.png", isFolder=True) 
        AddDir("[COLOR azure][B]Mattina[/B][/COLOR]", day + "?range=mt", 74, "http://www.creattor.com/files/23/787/morning-pleasure-icons-screenshots-17.png", isFolder=True)
        AddDir("[COLOR azure][B]Pomeriggio[/B][/COLOR]", day + "?range=pm", 74, "http://icons.iconarchive.com/icons/custom-icon-design/weather/256/Sunny-icon.png", isFolder=True)
        AddDir("[COLOR azure][B]Preserale[/B][/COLOR]", day + "?range=pr", 74, "https://s.evbuc.com/https_proxy?url=http%3A%2F%2Ftriumphbar.com%2Fimages%2Fhappyhour_icon.png&sig=ADR2i7_K2FSfbQ6b3dy12Xjgkq9NCEdkKg", isFolder=True)
        AddDir("[COLOR azure][B]Prima serata[/B][/COLOR]", day + "?range=ps", 74, "http://icons.iconarchive.com/icons/icons-land/vista-people/256/Occupations-Pizza-Deliveryman-Male-Light-icon.png", isFolder=True)
        AddDir("[COLOR azure][B]Seconda serata[/B][/COLOR]", day + "?range=ss", 74, "http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png", isFolder=True)
        AddDir("[COLOR azure][B]Notte[/B][/COLOR]", day + "?range=nt", 74, "http://icons.iconarchive.com/icons/oxygen-icons.org/oxygen/256/Status-weather-clear-night-icon.png", isFolder=True)
        
################################################################################################
# Ricerca aggiornamenti 

def checkforupdates(url,loc,aut):
    import ziptools
    xbmc.log('Start check for updates')
    try:
        data = urllib2.urlopen(url).read()
        xbmc.log('read xml remote data:' + data)
    except:
        data = ""
        xbmc.log('fail read xml remote data:' + url )
    try:
        f = open(loc,'r')
        data2 = f.read().replace("\n\n", "")
        f.close()
        xbmc.log('read xml local data:' + data2)
    except:
        data2 = ""
        xbmc.log('fail read xml local data')

    version_publicada = find_single_match(data,"<version>([^<]+)</version>").strip()
    tag_publicada = find_single_match(data,"<tag>([^<]+)</tag>").strip()

    version_local = find_single_match(data2,"<version>([^<]+)</version>").strip()
    tag_local = find_single_match(data,"<tag>([^<]+)</tag>").strip()

    try:
        numero_version_publicada = int(version_publicada)
        xbmc.log('number remote version:' + version_publicada)
        numero_version_local = int(version_local)
        xbmc.log('number local version:' + version_local)
    except:
        version_publicada = ""
        xbmc.log('number local version:' + version_local )
        xbmc.log('Check fail !@*')
            
    if version_publicada!="" and version_local!="":
        if (numero_version_publicada > numero_version_local):

            extpath = os.path.join(xbmc.translatePath("special://home/addons/")) 
            dest = addon_data_dir + '/lastupdate.zip'                
            UPDATE_URL = 'https://github.com/vania70/Kodi-Live-TV/raw/master/plugin.video.OTV_MEDIA-' + tag_publicada + '.zip'
            xbmc.log('START DOWNLOAD UPDATE:' + UPDATE_URL)
                
            DownloaderClass(UPDATE_URL,dest)  

            import ziptools
            unzipper = ziptools.ziptools()
            unzipper.extract(dest,extpath)
                
            line7 = 'New version installed .....'
            line8 = 'Version: ' + tag_publicada 
            xbmcgui.Dialog().ok('Kodi Live TV', line7, line8)
                
            if os.remove( dest ):
                xbmc.log('TEMPORARY ZIP REMOVED')
            xbmc.executebuiltin("UpdateLocalAddons")
            xbmc.executebuiltin("UpdateAddonRepos")
            xbmc.sleep(1500)

    url = REMOTE_VERSION_FILE2
    loc = LOCAL_VERSION_FILE2
        
    try:
        data = urllib2.urlopen(url).read()
        xbmc.log('read xml remote data:' + data)
    except:
        data = ""
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(AddonName,"Check for updates fail !", 3600, icon))
        xbmc.log('fail read xml remote data:' + url )
    try:
        f = open(loc,'r')
        data2 = f.read().replace("\n\n", "")
        f.close()
        xbmc.log('read xml local data:' + data2)
    except:
        data2 = ""
        xbmc.log('fail read xml local data')
            
    version_publicada = find_single_match(data,"<version>([^<]+)</version>").strip()
    tag_publicada = find_single_match(data,"<tag>([^<]+)</tag>").strip()

    version_local = find_single_match(data2,"<version>([^<]+)</version>").strip()
    dinamic_url = find_single_match(data,"<url>([^<]+)</url>").strip()
        
    try:
        numero_version_publicada = int(version_publicada)
        xbmc.log('number remote version:' + version_publicada)
        numero_version_local = int(version_local)
        xbmc.log('number local version:' + version_local)
    except:
        version_publicada = ""
        xbmc.log('number local version:' + version_local )
        xbmc.log('Check fail !@*')
        u = True
            
    if version_publicada!="" and version_local!="":
        if (numero_version_publicada > numero_version_local):

            extpath = os.path.join(xbmc.translatePath("special://home/addons/")) 
            dest = addon_data_dir + '/temp.zip'  
                    
            urllib.urlretrieve(dinamic_url,dest)
            xbmc.log('START DOWNLOAD PARTIAL UPDATE:' + dinamic_url) 
                    
            import ziptools
            unzipper = ziptools.ziptools()
            unzipper.extract(dest,extpath)
                    
            line7 = 'Plugin data updated .....'
            line8 = 'Description: ' + tag_publicada
            xbmcgui.Dialog().ok('Kodi Live TV', line7, line8)
                    
            if os.remove( dest ): 
                xbmc.log('TEMPORARY ZIP REMOVED')
            xbmc.executebuiltin("UpdateLocalAddons")
            xbmc.executebuiltin("UpdateAddonRepos")
            u = False
        else:
            xbmc.log('No partial updates are available' )
            u = True
                        
    if aut<1 and u:
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addons.VSlang(10106) + " :",addons.VSlang(10044), 4500, icon))
        xbmc.log('Check updates:No updates are available' )

# Ricerca automatica aggiornamenti
Tfile = os.path.join(addon_data_dir, 'time.txt')

if Addon.getSetting('autoupdate') == "true":

    if os.path.isfile(Tfile):
        t = time.time() - os.path.getmtime(Tfile)
        if t > 80000:
            try:
                checkforupdates(REMOTE_VERSION_FILE, LOCAL_VERSION_FILE,86400-t)
            except:
                pass
            common.write_file(Tfile  , '*')
    else:
        try:
            checkforupdates(REMOTE_VERSION_FILE, LOCAL_VERSION_FILE,0)
        except:
            pass
        common.write_file(Tfile  , '*')
    
###################

def Play_f4mProxy(url, name, iconimage):
    
    maxbitrate = Addon.getSetting('BitRateMax')
    if Addon.getSetting('use_simple') == "true":
        simpledownloader = True
    else:
        simpledownloader = False
    sys.path.insert(0, f4mProxy)
    from F4mProxy import f4mProxyHelper
    player=f4mProxyHelper()
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)
    
    if streamtype == "HLS":
        maxbitrate = 9000000
    player.playF4mLink(url, name, None, True, maxbitrate, simpledownloader, None, streamtype, False, None, None, None, iconimage)    
    
  
####################
def get_params():
	param = []
	paramstring = sys.argv[2]
	if len(paramstring)>= 2:
		params = sys.argv[2]
		cleanedparams = params.replace('?', '')
		if (params[len(params)-1] == '/'):
			params = params[0:len(params)-2]
		pairsofparams = cleanedparams.split('&')
		param = {}
		for i in range(len(pairsofparams)):
			splitparams = {}
			splitparams = pairsofparams[i].split('=')
			if (len(splitparams)) == 2:
				param[splitparams[0]] = splitparams[1]
	return param

params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None
station = None
user_id = None

try:
    url = Unquote_plus(params["url"])
except:
    pass
try:
    name = Unquote_plus(params["name"])
except:
    pass
try:
    iconimage = Unquote_plus(params["iconimage"])
except:
    pass
try:        
    mode = int(params["mode"])
except:
    pass
try:        
    user_id = params["userid"]
except:
    pass
try:        
    rec_id = params["recid"]
except:
    pass    
try:        
    station = Unquote_plus(params["station"])
except:
    pass    
    
try:        
    description = Unquote_plus(params["description"])
except:
    pass
try:
    streamtype = Unquote_plus(params["streamtype"])
except:
    pass    

if url and url.find("l=chit") >= 0:
    from teleboy import *
    ListTB("it")
    url = None
elif url and url.find("l=chfr") >= 0:
    from teleboy import *
    ListTB("fr")
    url = None
elif url and url.find("l=chde") >= 0:
    from teleboy import *
    ListTB("de")
    url = None
elif url and url.find("l=chen") >= 0:
    from teleboy import *
    ListTB("en")
    url = None
elif url and url.find("l=oggitv") >= 0:
    SetteGiorniTV()
    xbmcplugin.endOfDirectory(int(sys.argv[1]), succeeded=True)
    sys.exit()    
elif url and url.find("l=pornazzi") >= 0:
    Pornazzi("index")
    xbmc.executebuiltin("Container.SetViewMode(500)")
    xbmcplugin.endOfDirectory(int(sys.argv[1]), succeeded=True)
    sys.exit()     
if mode == None or url == None or len(url) < 1:
    Categories()
elif mode == 1:
    xml_settings = os.path.join(addon_data_dir, "settings.xml")
    if os.path.isfile(xml_settings):
        os.remove(xml_settings)
        sys.exit()
elif mode == 112:
    m3uCategory(url)
elif mode == 114 or mode == 151:
    m3uCategory(url,False)
elif mode == 163 or mode == 170:
    OpenXML(url)
elif mode == 113 or mode == 132:
    
    if url.startswith("opus") or url.startswith("enc"):
        PlayUrl(name, url, iconimage)
    elif url.startswith("plugin://") and not url.find("//plugin.video.youtube")>0:
        xbmc.executebuiltin("xbmc.RunPlugin("+url+")")
    elif url.find("openload.")>0:
        url = url.replace("/f/","/embed/")
        common.url_to_SOD(url,name,'openload','play')
    elif url.find("megahd.")>0:
        common.url_to_SOD(url,name,'megahd','play')
    elif url.find("nowvideo.")>0:
        url = url.replace("5nowvideo.com","nowvideo.li")
        url = url.replace("nowvideo.sx","nowvideo.li")
        common.url_to_SOD(url,name,'nowvideo','play')    
    elif url.find("fastvideo.")>0:
        common.url_to_SOD(url,name,'fastvideo','play')
    elif url.find("rapidvideo.")>0:
        common.url_to_SOD(url,name,'rapidvideo','play')
    elif url.find("nowdownload.")>0:
        common.url_to_SOD(url,name,'nowdownload','play')
    elif url.find("speedvideo.")>0:
        common.url_to_SOD(url,name,'speedvideo','play')
    elif url.find("streamin.to.")>0:
        common.url_to_SOD(url,name,'streamin','play')
    elif url.find("abysstream.com/")>0:
        common.url_to_SOD(url,name,'abysstream','play')
    elif url.find("vidto.me")>0:
        common.url_to_SOD(url,name,'vidtome','play')
    else:
        PlayUrl(name, url, iconimage)

elif mode == 5:   
    if url.find("urhd.tv")>0:
        try:
            url = common.urhd(url)
        except:
            pass
    if url.startswith("opus"):
        url = Opus(url)    
        
    Play_f4mProxy(url, name, iconimage)

elif mode == 116 or mode == 117:
    
    DF = xbmcaddon.Addon('plugin.video.OTV_MEDIA').getSetting('download_path')
    
    if not DF=='':  
        dpath = DF
    else:    
        dpath = DFolder
    
    ext = url.split('.')[-1]
    
    fileS = dpath + name + "." + ext + ".stopped"
    if not os.path.isfile(fileS):
        
        title = addons.VSlang(10203).encode('utf-8')
        string = GetKeyboardText(title, name)
        if len(string) >0:    
            common.StartDowloader(url,string,mode,DFolder)
    else:
        common.StartDowloader(url,name,mode,DFolder)
        
elif mode == 159:
    common.StartDowloader(url,name,mode,DFolder)                 
elif mode == 157 or mode == 172:
    common.StopDowloader(url,name,mode,DFolder)
elif mode == 158 or mode == 171:
    common.DeletePartialDowload(url,name,mode,DFolder)
elif mode == 10:
    # deleted
    sys.exit()
elif mode == 120:
    AddNewList()
elif mode == 121 or mode == 154 or mode == 160 or mode == 164:
    PMFolder( url )
elif mode == 122:
    RemoveFromLists(url)
elif mode == 123:
    ChangeName(name,playlistsFile2,"name",10004)
elif mode == 124:
    ChangeUrl(url,playlistsFile2,"url",10005)
elif mode == 161:
    ChangeName(name,playlistsFile4,"name",10004)        
elif mode == 169:
    ChangeName(name,favoritesFile,"name",10004)
elif mode == 125:
    importList()
elif mode == 126:
    if os.path.isfile( playlistsFile3 ) :
        if os.path.isfile( playlistsFile2 ) : os.remove( playlistsFile2 )
        shutil.copyfile( playlistsFile3, playlistsFile2 )
        xbmc.sleep ( 200 )
        os.remove( playlistsFile3 )
        xbmc.executebuiltin("XBMC.Container.Update('plugin://{0}')".format(AddonID))
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(AddonName,addons.VSlang(10125).encode('utf-8'), 3600, icon)) 
    else:
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(AddonName,addons.VSlang(10126).encode('utf-8'), 3600, icon))
elif mode == 130:
    ListFavorites()
elif mode == 131: 
    AddFavorites(url, iconimage, name)
elif mode == 155:
    RemoveDirFromLists(url,name)
elif mode == 156:
    os.remove( os.path.join(pwdir, base64.standard_b64encode(url))) 
    xbmc.executebuiltin("XBMC.Container.Refresh()")
elif mode == 133:
    RemoveFavorties(url)
elif mode == 34:
    AddNewFavortie()
elif mode == 35:
    ListSub(Italian)
elif mode == 36:
    ListSub(French)
elif mode == 37:
    ListSub(German)
elif mode == 38:
    ListSub(English)
elif mode == 139:
    PM_index()
elif mode == 40:
    common.DelFile(playlistsFile2)
    sys.exit()
elif mode == 41:
    common.DelFile(favoritesFile)
    sys.exit()
elif mode == 42:
    write_xml()
    sys.exit()
elif mode == 43:
    restore_xml()
    sys.exit()   
elif mode == 44:
    remove_xml()
    sys.exit()
elif mode == 45:        
    clean_cache()
    sys.exit()
elif mode == 46:       
    checkforupdates(REMOTE_VERSION_FILE, LOCAL_VERSION_FILE,0)
    if Addon.getSetting('autoupdate') == "true":
        common.write_file(Tfile , '*')        
    sys.exit()
elif mode == 47:
    xbmc.executebuiltin("StopPVRManager")
    xbmc.executebuiltin("StartPVRManager") 
    sys.exit()

elif mode == 150:
    print( '--- Playing "{0}". {1}'.format(name, url))
    listitem = xbmcgui.ListItem(path=url, thumbnailImage=iconimage)
    listitem.setInfo(type="Video", infoLabels={ "Title": name })
    xbmc.Player().play( url , listitem)
elif mode == 152:
    common.DeleteFile(url,name)
elif mode == 153:
    string = GetKeyboardText(addons.VSlang(10203).encode('utf-8'), name)
    if len(string) < 1:
        sys.exit()
    else:
        nurl = url.replace(name,string)
        xbmcvfs.rename(os.path.join(url) ,os.path.join(nurl))
        xbmc.executebuiltin("XBMC.Container.Refresh()")
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(name, addons.VSlang(10202).encode('utf-8'), 5200, icon))
        sys.exit()
elif mode == 162:
    cook = os.path.join(addonDir,'resources','cookie.dat')
    if os.path.isfile(cook):
        os.remove(cook)
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%("Kodi Live TV : ","Teleboy cookie has been deleted!", 4700, icon))
    sys.exit()
elif mode == 165 or mode == 181:
    title = addons.VSlang(10250).encode('utf-8')
    string = GetKeyboardText(title, "")
    if len(string) >0:
        string = string.lower()
        if url == "search":
            sch_global(string)
        elif mode == 181:
            findm3u(url, string)
        else:
            sch_folder(url,string)
elif mode == 166:
    title = addons.VSlang(10250).encode('utf-8')
    string = GetKeyboardText(title, "")
    if len(string) >0:
        sch_xml(url,string)

elif mode == 173:
    sch_global(url,live=True)
elif mode == 176:
    sch_global(name,live=False)
elif mode == 167:
    sch_exclude(url, playlistsFile4, "yes")
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%("Kodi Live TV : ","Folder " + name + " to global research excluded!", 4000, icon))
    sys.exit()
elif mode == 168:
    sch_exclude(url, playlistsFile4, "")
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%("Kodi Live TV : ","Folder " + name + " to global research included!", 4000, icon))
    sys.exit()
elif mode == 74:
    tvoggi(url)
elif mode == 75:    
    SetteGiorniTV(url)
elif mode == 77:
    Pornazzi(url)
    xbmc.executebuiltin("Container.SetViewMode(500)")
elif mode == 78:
    import FreeTV
    FreeTV.PlayOtherUrl ( url, name )

##########################
# Teleboy

elif mode == 27:
    from teleboy import *
    try:
        json = get_videoJson( user_id, station)
        if not json:
            exit( 1)

        title = json["data"]["epg"]["current"]["title"]
        url = json["data"]["stream"]["url"]
        if not url: 
            exit( 1)
        img = get_stationLogoURL( station )
        Player = xbmcaddon.Addon('plugin.video.kodilivetv').getSetting('player')
        if  Addon.getSetting('player') == "true":
            play_url2( url, title, img )  
        else:
            play_url( url, title, img )
    except:
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(AddonName, "Swiss IP needed. Your bags ready!", 3600, icon))
elif mode == 28:
    from teleboy import *
    show_recordings(user_id)
    #make_list()
elif mode == 29:
    from teleboy import *
    url = "stream/record/%s" % rec_id
    json    = fetchApiJson( user_id, url)
    title = json["data"]["record"]["title"]
    url   = json["data"]["stream"]["url"]
    img = REC_ICON
    play_url( url, title, img )
elif mode == 179:
    findm3u(url)
elif mode == 80:
    import control
elif mode == 190:
    TestCheck = ""
    TestCheck = common.find_lpanel(url)

    if not TestCheck == "":
        
        panel =  common.OpenURL(TestCheck,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko'})
        
        s = common.find_param('"status" *: *"([^",]+)',panel)
        if s == "":
            s = "unknown"
        status = "Status : " + s
        
        try:
            exp_date = "Exp. date : " + str(time.ctime(int(common.find_param('"exp_date" *: *"([^",]+)',panel))))
        except:
            exp_date = "Exp. date : unknown"
        try:    
            created_at = "Created at : " + str(time.ctime(int(common.find_param('"created_at" *: *"([^",]+)',panel))))
        except:
            created_at = "Created at : unknown"
            
        active_cons = "Active connections : " + common.find_param('"active_cons" *: *"([^",]+)',panel)
        max_connections = "Max connections : " + common.find_param('"max_connections" *: *"([^",]+)',panel) 
        
        Line = status + "\n" + created_at + "\n" + exp_date + "\n" + max_connections + " - " + active_cons
        
        common.OKmsg(name,Line)
elif mode == 91:
    zip_PM_data()
elif mode == 92:
    unzip_PM_data()
elif mode == 93:
    Yplayl(url)
elif mode == 94:
    TempName = base64.standard_b64encode(url)
    tmp = os.path.join(cdir, TempName)
    if os.path.isfile(tmp):
        common.DelFile(tmp)
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('[COLOR yellow]' +name + '[/COLOR]', 'Cache file was deleted!', 4000, icon))
        xbmc.executebuiltin("XBMC.Container.Refresh()")
###########################
#end directory
xbmcplugin.endOfDirectory(int(sys.argv[1]), succeeded=True)

