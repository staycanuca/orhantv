# -*- coding: utf-8 -*-
from resources.lib.cconfig import ccConfig
from resources.lib.tools import logger
from resources.lib import common
import io, gzip, time, xbmcgui, re
import socket, os, sys, hashlib
try:
    from urlparse import urlparse
    from urllib import quote, urlencode
    from urllib2 import HTTPError, URLError, HTTPHandler, HTTPSHandler, HTTPCookieProcessor, build_opener, Request, urlopen
    from cookielib import LWPCookieJar, Cookie
    from httplib import HTTPSConnection, HTTPException
except ImportError:
    from urllib.parse import quote, urlencode, urlparse
    from urllib.error import HTTPError, URLError
    from urllib.request import HTTPHandler, HTTPSHandler, HTTPCookieProcessor, build_opener, Request, urlopen
    from http.cookiejar import LWPCookieJar, Cookie
    from http.client import HTTPSConnection, HTTPException


class cRequestHandler:
    def __init__(self, sUrl, caching=True, ignoreErrors=False, compression=True):
        self.__sUrl = sUrl
        self.__sRealUrl = ''
        self.__cType = 0
        self.__USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'
        self.__aParameters = {}
        self.__aResponses = {}
        self.__headerEntries = {}
        self.__cachePath = ''
        self._cookiePath = ''
        self.ignoreDiscard(False)
        self.ignoreExpired(False)
        self.caching = caching
        self.ignoreErrors = ignoreErrors
        self.compression = compression
        self.cacheTime = int(ccConfig().getSetting('cacheTime', 600))
        self.requestTimeout = int(ccConfig().getSetting('requestTimeout', 10))
        self.removeBreakLines(True)
        self.removeNewLines(True)
        self.__setDefaultHeader()
        self.setCachePath()
        self.__setCookiePath()
        self.__sResponseHeader = ''
        socket.setdefaulttimeout(self.requestTimeout)

    def removeNewLines(self, bRemoveNewLines):
        self.__bRemoveNewLines = bRemoveNewLines

    def removeBreakLines(self, bRemoveBreakLines):
        self.__bRemoveBreakLines = bRemoveBreakLines

    def addHeaderEntry(self, sHeaderKey, sHeaderValue):
        self.__headerEntries[sHeaderKey] = sHeaderValue

    def getHeaderEntry(self, sHeaderKey):
        if sHeaderKey in self.__headerEntries:
            return self.__headerEntries[sHeaderKey]

    def addParameters(self, key, value, Quote=False):
        if not Quote:
            self.__aParameters[key] = value
        else:
            self.__aParameters[key] = quote(str(value))
    def addParametersLine(self, mParameterValue):
        self.__aParamatersLine = mParameterValue


    def addResponse(self, key, value):
        self.__aResponses[key] = value

    def getResponseHeader(self):
        return self.__sResponseHeader

    def setRequestType(self, cType):
        self.__cType = cType

    def getRealUrl(self):
        return self.__sRealUrl

    def request(self):
        self.__sUrl = self.__sUrl.replace(' ', '+')
        return self.__callRequest()

    def getRequestUri(self):
        return self.__sUrl + '?' + urlencode(self.__aParameters)

    def __setDefaultHeader(self):
        self.addHeaderEntry('User-Agent', self.__USER_AGENT)
        self.addHeaderEntry('Accept-Language', 'de,en-US;q=0.7,en;q=0.3')
        self.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        if self.compression:
            self.addHeaderEntry('Accept-Encoding', 'gzip, deflate')

    def __callRequest(self):
        if self.caching and self.cacheTime > 0:
            sContent = self.readCache(self.getRequestUri())
            if sContent:
                return sContent
        cookieJar = LWPCookieJar(filename=self._cookiePath)
        try:
            cookieJar.load(ignore_discard=self.__bIgnoreDiscard, ignore_expires=self.__bIgnoreExpired)
        except Exception as e:
            logger.debug(e)
        if sys.version_info[0] == 2:
            sParameters = urlencode(self.__aParameters, True)
        else:
            sParameters = urlencode(self.__aParameters, True).encode()

        handlers = [HTTPHandler(), HTTPSHandler(), HTTPCookieProcessor(cookiejar=cookieJar)]
        if (2, 7, 9) <= sys.version_info < (2, 7, 11):
            handlers.append(newHTTPSHandler)
        opener = build_opener(*handlers)
        if len(sParameters) > 0:
            oRequest = Request(self.__sUrl, sParameters)
        else:
            oRequest = Request(self.__sUrl)

        for key, value in self.__headerEntries.items():
            oRequest.add_header(key, value)
        cookieJar.add_cookie_header(oRequest)
        try:
            oResponse = opener.open(oRequest)
        except HTTPError as e:
            if e.code == 503:
                oResponse = None
                if not oResponse:
                    logger.error('Failed Cloudflare aktiv Url: ' + self.__sUrl)
            if e.code == 403:
                data = e.fp.read()
                if 'DDOS-GUARD' in str(data):
                    opener = build_opener(HTTPCookieProcessor(cookieJar))
                    opener.addheaders = [('User-agent', self.__USER_AGENT), ('Referer', self.__sUrl)]
                    response = opener.open('https://check.ddos-guard.net/check.js')
                    if sys.version_info[0] == 2:
                        content = response.read()
                    else:
                        content = response.read().decode('utf-8').encode('utf-8', 'replace').decode('utf-8')
                    url2 = re.findall("Image.*?'([^']+)'; new", content)
                    url3 = urlparse(self.__sUrl)
                    url3 = '%s://%s/%s' % (url3.scheme, url3.netloc, url2[0])
                    opener = build_opener(HTTPCookieProcessor(cookieJar))
                    opener.addheaders = [('User-agent', self.__USER_AGENT), ('Referer', self.__sUrl)]
                    response = opener.open(url3)
                    content = response.read()
                    opener = build_opener(HTTPCookieProcessor(cookieJar))
                    opener.addheaders = [('User-agent', self.__USER_AGENT), ('Referer', self.__sUrl)]
                    oResponse = opener.open(self.__sUrl)

                    if not oResponse:
                        if not self.ignoreErrors:
                            logger.error('Failed DDOS-GUARD Url: ' + self.__sUrl)
                            return ''

            elif not self.ignoreErrors:
                xbmcgui.Dialog().ok('xStream', 'Fehler beim Abrufen der Url: {0} {1}'.format(self.__sUrl, str(e)))
                logger.error('HTTPError ' + str(e) + ' Url: ' + self.__sUrl)
                return ''
            else:
                oResponse = e
        except URLError as e:
            if not self.ignoreErrors:
                if hasattr(e.reason, 'args') and e.reason.args[0] == 1 and sys.version_info < (2, 7, 9):
                    xbmcgui.Dialog().ok('xStream', '{0}For this request is Python v2.7.9 or higher required.'.format(str(e.reason)))
                else:
                    xbmcgui.Dialog().ok('xStream', str(e.reason))
            logger.error('URLError ' + str(e.reason) + ' Url: ' + self.__sUrl)
            return ''
        except HTTPException as e:
            if not self.ignoreErrors:
                xbmcgui.Dialog().ok('xStream', str(e))
            logger.error('HTTPException ' + str(e) + ' Url: ' + self.__sUrl)
            return ''

        self.__sResponseHeader = oResponse.info()
        if self.__sResponseHeader.get('Content-Encoding') == 'gzip':
            sContent = gzip.GzipFile(fileobj=io.BytesIO(oResponse.read())).read()
            if sys.version_info[0] == 3:
                sContent = sContent.decode('utf-8').encode('utf-8', 'replace').decode('utf-8')
        else:
            if sys.version_info[0] == 2:
                sContent = oResponse.read()
            else:
                sContent = oResponse.read().decode('utf-8').encode('utf-8', 'replace').decode('utf-8')
        if 'lazingfast' in sContent:
            bf = cBF().resolve(self.__sUrl, sContent, cookieJar, self.__USER_AGENT)
            if bf:
                sContent = bf
            else:
                logger.error('Failed BF Url: ' + self.__sUrl)
        cookieJar.save(ignore_discard=self.__bIgnoreDiscard, ignore_expires=self.__bIgnoreExpired)
        if self.__bRemoveNewLines:
            sContent = sContent.replace('\n', '')
            sContent = sContent.replace('\r\t', '')
        if self.__bRemoveBreakLines:
            sContent = sContent.replace('&nbsp;', '')
        self.__sRealUrl = oResponse.geturl()
        oResponse.close()
        if self.caching and self.cacheTime > 0:
            self.writeCache(self.getRequestUri(), sContent)
        return sContent

    def getHeaderLocationUrl(self):
        opened = urlopen(self.__sUrl)
        return opened.geturl()

    def __setCookiePath(self):
        profilePath = common.profilePath
        cookieFile = os.path.join(profilePath, 'cookies')
        if not os.path.exists(cookieFile):
            os.makedirs(cookieFile)
        if not 'dummy' in self.__sUrl:
            cookieFile = os.path.join(cookieFile, urlparse(self.__sUrl).netloc.replace('.', '_') + '.txt')
            if not os.path.exists(cookieFile):
                file = open(cookieFile, 'w')
                file.close()
            self._cookiePath = cookieFile

    def getCookie(self, sCookieName, sDomain=''):
        cookieJar = LWPCookieJar()
        try:
            cookieJar.load(self._cookiePath, self.__bIgnoreDiscard, self.__bIgnoreExpired)
        except Exception as e:
            logger.error(e)
        for entry in cookieJar:
            if entry.name == sCookieName:
                if sDomain == '':
                    return entry
                elif entry.domain == sDomain:
                    return entry
        return False

    def setCookie(self, oCookie):
        cookieJar = LWPCookieJar()
        try:
            cookieJar.load(self._cookiePath, self.__bIgnoreDiscard, self.__bIgnoreExpired)
        except Exception as e:
            logger.error(e)
        cookieJar.set_cookie(oCookie)
        cookieJar.save(self._cookiePath, self.__bIgnoreDiscard, self.__bIgnoreExpired)

    def ignoreDiscard(self, bIgnoreDiscard):
        self.__bIgnoreDiscard = bIgnoreDiscard

    def ignoreExpired(self, bIgnoreExpired):
        self.__bIgnoreExpired = bIgnoreExpired

    def setCachePath(self, cache=''):
        if not cache:
            profilePath = common.profilePath
            cache = os.path.join(profilePath, 'htmlcache')
        if not os.path.exists(cache):
            os.makedirs(cache)
        self.__cachePath = cache

    def readCache(self, url):
        content = ''
        if sys.version_info[0] == 2:
            h = hashlib.md5(url).hexdigest()
        else:
            h = hashlib.md5(url.encode('utf8')).hexdigest()
        cacheFile = os.path.join(self.__cachePath, h)
        fileAge = self.getFileAge(cacheFile)
        if 0 < fileAge < self.cacheTime:
            try:
                if sys.version_info[0] == 2:
                    with open(cacheFile, 'r') as f:
                        content = f.read()
                else:
                    with open(cacheFile, 'rb') as f:
                        content = f.read().decode('utf8')
            except Exception:
                logger.error('Could not read Cache')
            if content:
                logger.info('read html for %s from cache' % url)
                return content
        return ''

    def writeCache(self, url, content):
        if sys.version_info[0] == 2:
            h = hashlib.md5(url).hexdigest()
        else:
            h = hashlib.md5(url.encode('utf8')).hexdigest()
        cacheFile = os.path.join(self.__cachePath, h)
        try:
            if sys.version_info[0] == 2:
                with open(cacheFile, 'w') as f:
                    f.write(content)
            else:
                with open(cacheFile, 'wb') as f:
                    f.write(content.encode('utf8'))
        except Exception:
            logger.error('Could not write Cache')

    @staticmethod
    def getFileAge(cacheFile):
        try:
            fileAge = time.time() - os.stat(cacheFile).st_mtime
        except Exception:
            return 0
        return fileAge

    def clearCache(self):
        files = os.listdir(self.__cachePath)
        for file in files:
            cacheFile = os.path.join(self.__cachePath, file)
            os.remove(cacheFile)


# python 2.7.9 and 2.7.10 certificate workaround
class newHTTPSHandler(HTTPSHandler):
    def do_open(self, conn_factory, req, **kwargs):
        conn_factory = newHTTPSConnection
        return HTTPSHandler.do_open(self, conn_factory, req)


class newHTTPSConnection(HTTPSConnection):
    def __init__(self, host, port=None, key_file=None, cert_file=None, strict=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, source_address=None, context=None):
        import ssl
        context = ssl._create_unverified_context()
        HTTPSConnection.__init__(self, host, port, key_file, cert_file, strict, timeout, source_address, context)


class cBF:
    def resolve(self, url, html, cookie_jar, user_agent):
        page = urlparse(url).scheme + '://' + urlparse(url).netloc
        j = re.findall('<script[^>]src="([^"]+)', html)
        if j:
            opener = build_opener(HTTPCookieProcessor(cookie_jar))
            opener.addheaders = [('User-agent', user_agent), ('Referer', url)]
            opener.open(page + j[0])
        a = re.findall('xhr\.open\("GET","([^,]+)",', html)
        if a:
            import random
            aespage = page + a[0].replace('" + ww +"', str(random.randint(700, 1500)))
            opener = build_opener(HTTPCookieProcessor(cookie_jar))
            opener.addheaders = [('User-agent', user_agent), ('Referer', url)]
            if sys.version_info[0] == 2:
                html = opener.open(aespage).read()
            else:
                html = opener.open(aespage).read().decode('utf-8').encode('utf-8', 'replace').decode('utf-8')
            cval = self.aes_decode(html)
            cdata = re.findall('cookie="([^="]+).*?domain[^>]=([^;]+)', html)
            if cval and cdata:
                c = Cookie(version=0, name=cdata[0][0], value=cval, port=None, port_specified=False, domain=cdata[0][1], domain_specified=True, domain_initial_dot=False, path="/", path_specified=True, secure=False, expires=time.time() + 21600, discard=False, comment=None, comment_url=None, rest={})
                cookie_jar.set_cookie(c)
                opener = build_opener(HTTPCookieProcessor(cookie_jar))
                opener.addheaders = [('User-agent', user_agent), ('Referer', url)]
                if sys.version_info[0] == 2:
                    return opener.open(url).read()
                else:
                    return opener.open(url).read().decode('utf-8').encode('utf-8', 'replace').decode('utf-8')

    def aes_decode(self, html):
        try:
            import pyaes
            keys = re.findall('toNumbers\("([^"]+)"', html)
            if keys:
                from binascii import hexlify, unhexlify
                msg = unhexlify(keys[2])
                key = unhexlify(keys[0])
                iv = unhexlify(keys[1])
                decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationCBC(key, iv))
                plain_text = decrypter.feed(msg)
                plain_text += decrypter.feed()
                return hexlify(plain_text).decode()
        except Exception as e:
            logger.error(e)
