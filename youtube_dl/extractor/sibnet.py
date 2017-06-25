# coding: utf-8
from __future__ import unicode_literals

import re

from .common import InfoExtractor

class SibnetIE(InfoExtractor):
    _VALID_URL = r'(?:https?://)?video\.sibnet\.ru/video(?P<id>\d+).*'
    
    def _real_extract(self, url):
        mobj = re.match(self._VALID_URL, url)
        video_id = mobj.group('id')
        
        webpage = self._download_webpage(url, video_id)
        self.report_extraction(video_id)
        
        format_url = self._html_search_regex(r'src:\s*"(?P<mpd>.+)\.mpd"', webpage, 'mpd')
        format_url = 'https://video.sibnet.ru/' + format_url + '.mpd'
        
        formats = []
        formats.extend(self._extract_mpd_formats(format_url, video_id))
        self._sort_formats(formats)
        
        video_title = self._html_search_regex(r'<meta property="og:title" content="(.+?)"', webpage, 'title')
        
        return {
            'id': video_id,
            'title': video_title,
            'formats': formats
        }
