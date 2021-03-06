# -*- coding: utf-8 -*-

PY3 = False

try:
    import http.cookiejar as cookielib
    from urllib.parse import urlencode as Urlencode
    from urllib.parse import quote_plus as Quote_plus
    from urllib.parse import unquote as Unquote
    from urllib.parse import quote as Quote
    from urllib.parse import urlparse as Urlparse
    from urllib.parse import urljoin as Urljoin
    from urllib.parse import parse_qsl as Parse_qsl
    from urllib.parse import parse_qs as Parse_qs
    from urllib.error import HTTPError, URLError
    from urllib.request import Request
    from urllib.request import urlopen
    from urllib.request import HTTPCookieProcessor
    from urllib.request import build_opener
    from urllib.request import HTTPBasicAuthHandler
    from urllib.request import HTTPHandler
    from urllib.request import install_opener
    PY3 = True; unicode = str; unichr = chr; long = int; xrange = range
except:
    import cookielib
    from urllib import urlencode as Urlencode
    from urllib import quote_plus as Quote_plus
    from urllib import unquote as Unquote
    from urllib import quote as Quote
    from urlparse import urlparse as Urlparse
    from urlparse import urljoin as Urljoin
    from urlparse import parse_qsl as Parse_qsl
    from urlparse import parse_qs as Parse_qs
    from urllib2 import HTTPError, URLError
    from urllib2 import Request
    from urllib2 import urlopen
    from urllib2 import HTTPCookieProcessor
    from urllib2 import build_opener
    from urllib2 import HTTPBasicAuthHandler
    from urllib2 import HTTPHandler
    from urllib2 import install_opener


from resources.lib.comaddon import addon, dialog, VSlog
from resources.lib.util import urlEncode, Unquote

class cRequestHandler:
    REQUEST_TYPE_GET = 0
    REQUEST_TYPE_POST = 1
    DIALOG = dialog()
    ADDON = addon()

    def __init__(self, sUrl):
        self.__sUrl = sUrl
        self.__sRealUrl = ''
        self.__cType = 0
        self.__aParamaters = {}
        self.__aParamatersLine = ''
        self.__aHeaderEntries = []
        self.removeBreakLines(True)
        self.removeNewLines(True)
        self.__setDefaultHeader()
        self.__timeout = 30
        self.__bRemoveNewLines = False
        self.__bRemoveBreakLines = False
        self.__sResponseHeader = ''
        self.BUG_SSL = False

    def removeNewLines(self, bRemoveNewLines):
        self.__bRemoveNewLines = bRemoveNewLines

    def removeBreakLines(self, bRemoveBreakLines):
        self.__bRemoveBreakLines = bRemoveBreakLines

    def setRequestType(self, cType):
        self.__cType = cType

    def setTimeout(self, valeur):
        self.__timeout = valeur

    def addHeaderEntry(self, sHeaderKey, sHeaderValue):
        for sublist in self.__aHeaderEntries:
            if sHeaderKey in sublist:
                self.__aHeaderEntries.remove(sublist)
        aHeader = {sHeaderKey: sHeaderValue}
        self.__aHeaderEntries.append(aHeader)

    def addParameters(self, sParameterKey, mParameterValue):
        self.__aParamaters[sParameterKey] = mParameterValue

    def addParametersLine(self, mParameterValue):
        self.__aParamatersLine = mParameterValue

    #egg addMultipartFiled({'sess_id': sId, 'upload_type': 'url', 'srv_tmp_url': sTmp})
    def addMultipartFiled(self, fields):
        mpartdata = MPencode(fields)
        self.__aParamatersLine = mpartdata[1]
        self.addHeaderEntry('Content-Type', mpartdata[0] )
        self.addHeaderEntry('Content-Length', len(mpartdata[1]))

    # Je sais plus si elle gere les doublons
    def getResponseHeader(self):
        return self.__sResponseHeader

    # url after redirects
    def getRealUrl(self):
        return self.__sRealUrl

    def GetCookies(self):
        if not self.__sResponseHeader:
            return ''
        if 'Set-Cookie' in self.__sResponseHeader:
            import re

            #cookie_string = self.__sResponseHeader.getheaders('set-cookie')
            #c = ''
            #for i in cookie_string:
            #    c = c + i + ', '
            c = self.__sResponseHeader.get('set-cookie')

            c2 = re.findall('(?:^|,) *([^;,]+?)=([^;,\/]+?);', c)
            if c2:
                cookies = ''
                for cook in c2:
                    cookies = cookies + cook[0] + '=' + cook[1] + ';'
                cookies = cookies[:-1]
                return cookies
        return ''

    def request(self):
        # Supprimee car deconne si url contient ' ' et '+' en meme temps
        #self.__sUrl = self.__sUrl.replace(' ', '+')
        return self.__callRequest()

    def getRequestUri(self):
        return self.__sUrl + '?' + urlEncode(self.__aParamaters)

    def __setDefaultHeader(self):
        self.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0')
        self.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        self.addHeaderEntry('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7')

    def __callRequest(self):
        if self.__aParamatersLine:
            sParameters = self.__aParamatersLine
        else:
            sParameters = urlEncode(self.__aParamaters)

        if (self.__cType == cRequestHandler.REQUEST_TYPE_GET):
            if (len(sParameters) > 0):
                if (self.__sUrl.find('?') == -1):
                    self.__sUrl = self.__sUrl + '?' + str(sParameters)
                    sParameters = ''
                else:
                    self.__sUrl = self.__sUrl + '&' + str(sParameters)
                    sParameters = ''

        if (len(sParameters) > 0):
            oRequest = Request(self.__sUrl, sParameters)
        else:
            oRequest =Request(self.__sUrl)

        for aHeader in self.__aHeaderEntries:
            for sHeaderKey, sHeaderValue in list(aHeader.items()):
                oRequest.add_header(sHeaderKey, sHeaderValue)

        sContent = ''
        try:

            if self.BUG_SSL:
                VSlog('Retrying with SSL bug')
                import ssl
                gcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
                oResponse = urlopen(oRequest, timeout = self.__timeout, context=gcontext)
            else:
                oResponse = urlopen(oRequest, timeout = self.__timeout)

            sContent = oResponse.read()

            self.__sResponseHeader = oResponse.info()

            # compressed page ?
            if self.__sResponseHeader.get('Content-Encoding') == 'gzip':
                import zlib
                sContent = zlib.decompress(sContent, zlib.MAX_WBITS|16)

            # https://bugs.python.org/issue4773
            self.__sRealUrl = oResponse.geturl()
            self.__sResponseHeader = oResponse.info()

            oResponse.close()

        except HTTPError as e:
            if e.code == 503:

                # Protected by cloudFlare ?
                from resources.lib import cloudflare
                if cloudflare.CheckIfActive(e.read()):
                    self.__sResponseHeader = e.hdrs
                    cookies = self.GetCookies()
                    VSlog('Page protegee par cloudflare')
                    CF = cloudflare.CloudflareBypass()
                    sContent = CF.GetHtml(self.__sUrl, e.read(), cookies, sParameters, oRequest.headers)
                    self.__sRealUrl, self.__sResponseHeader = CF.GetReponseInfo()
                else:
                    sContent = e.read()
                    self.__sRealUrl = e.geturl()
                    self.__sResponseHeader = e.headers()

            else:
                try:
                    VSlog("%s (%d),%s" % (self.ADDON.VSlang(30205), e.code, self.__sUrl))
                    self.__sRealUrl = e.geturl()
                    self.__sResponseHeader = e.headers
                    sContent = e.read()
                except:
                    sContent = ''

            if not sContent:
                self.DIALOG.VSerror("%s (%d),%s" % (self.ADDON.VSlang(30205), e.code, self.__sUrl))
                return ''

        except URLError as e:
            if 'CERTIFICATE_VERIFY_FAILED' in str(e.reason) and self.BUG_SSL == False:
                self.BUG_SSL = True
                return self.__callRequest()

            self.DIALOG.VSerror("%s (%s),%s" % (self.ADDON.VSlang(30205), e.reason, self.__sUrl))
            return ''

        if (self.__bRemoveNewLines == True):
            sContent = sContent.replace("\n", "")
            sContent = sContent.replace("\r\t", "")

        if (self.__bRemoveBreakLines == True):
            sContent = sContent.replace("&nbsp;", "")

        return sContent

    def getHeaderLocationUrl(self):
        opened = urlopen(self.__sUrl)
        return opened.geturl()

# ******************************************************************************
# from https://github.com/eliellis/mpart.py
# ******************************************************************************


def MPencode(fields):
    import mimetypes
    random_boundary = __randy_boundary()
    content_type = "multipart/form-data, boundary=%s" % random_boundary

    form_data = []

    if fields:
        for (key, value) in fields.items():
            if not hasattr(value, 'read'):
                itemstr = '--%s\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n' % (random_boundary, key, value)
                form_data.append(itemstr)
            elif hasattr(value, 'read'):
                with value:
                    file_mimetype = mimetypes.guess_type(value.name)[0] if mimetypes.guess_type(value.name)[0] else 'application/octet-stream'
                    itemstr = '--%s\r\nContent-Disposition: form-data; name="%s"; filename="%s"\r\nContent-Type: %s\r\n\r\n%s\r\n' % (random_boundary, key, value.name, file_mimetype, value.read())
                form_data.append(itemstr)
            else:
                raise Exception(value, 'Field is neither a file handle or any other decodable type.')
    else:
        pass

    form_data.append('--%s--\r\n' % random_boundary)

    return content_type, ''.join(form_data)


def __randy_boundary(length=10, reshuffle=False):
    import string
    import random

    character_string = string.letters + string.digits
    boundary_string = []
    for i in range(0, length):
        rand_index = random.randint(0, len(character_string) - 1)
        boundary_string.append(character_string[rand_index])
    if reshuffle:
        random.shuffle(boundary_string)
    else:
        pass
    return ''.join(boundary_string)