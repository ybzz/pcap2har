import urlparse

# dpkt.http is buggy, so we use our modified replacement
from .. import dpkt_http_replacement as dpkt_http
from ..mediatype import MediaType
import message as http

from base64 import b64encode
import cgi
from requests_toolbelt.multipart import decoder, ImproperBodyPartContentException


class Request(http.Message):
    '''
    HTTP request. Parses higher-level info out of dpkt.http.Request
    Members:
    * query: Query string name-value pairs. {string: [string]}
    * host: hostname of server.
    * fullurl: Full URL, with all components.
    * url: Full URL, but without fragments. (that's what HAR wants)
    '''

    def __init__(self, tcpdir, pointer):
        http.Message.__init__(self, tcpdir, pointer, dpkt_http.Request)
        # get query string. its the URL after the first '?'
        uri = urlparse.urlparse(self.msg.uri)
        self.host = self.msg.headers['host'] if 'host' in self.msg.headers else ''
        fullurl = urlparse.ParseResult('http', self.host, uri.path, uri.params, uri.query, uri.fragment)
        self.fullurl = fullurl.geturl()
        self.url, frag = urlparse.urldefrag(self.fullurl)
        self.query = urlparse.parse_qs(uri.query, keep_blank_values=True)

        self.mediaType = None
        if 'content-type' in self.msg.headers:
            self.mediaType = MediaType(self.msg.headers['content-type'])
        self.postData = Request._postData(self.mediaType, self.msg.body)

    @classmethod
    def _postData(cls, mediaType, body):
        if mediaType and mediaType.mimeType() == 'multipart/form-data':
            try:
                multipart_data = decoder.MultipartDecoder(body, str(mediaType))
            except ImproperBodyPartContentException:
                return {}

            params = []
            default_type = None
            for part in multipart_data.parts:
                if 'Content-Disposition' not in part.headers:
                    continue

                if default_type is None:
                    default_type = part.headers.get('Content-Type')

                _, pdict = cgi.parse_header(part.headers['Content-Disposition'])

                p = dict(name=pdict.get('name'), contentType=part.headers.get('Content-Type', default_type))
                if pdict.get('filename'):
                    p['fileName'] = pdict.get('filename')

                if 'text/' in p['contentType']:
                    p['value'] = part.content
                else:
                    p['value'] = b64encode(part.content)

                params.append(p)

            return dict(mimeType=str(mediaType), params=params, comment='')

        return {}

