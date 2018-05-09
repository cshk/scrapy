"""
    根据urlsha过滤
"""

import hashlib
from scrapy.dupefilters import RFPDupeFilter
from scrapy.utils.url import canonicalize_url


class URLSha1Filter(RFPDupeFilter):

    def __init__(self, path=None, debug=False):
        self.url_seen = set()
        RFPDupeFilter.__init__(self, path)

    def request_seen(self, request):
        fp = hashlib.sha1()
        fp.update((canonicalize_url(request.url).encode('utf-8')))
        url_sha1 = fp.hexdigest()
        if url_sha1 in self.url_seen:
            return True
        else:
            self.url_seen.add(url_sha1)