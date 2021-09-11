#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Brian Roepke'
SITENAME = 'roepkeb'
SITEURL = 'https://www.roepkeb.com'
GOOGLE_ANALYTICS = 'UA-309309-9'
DISQUS_SITENAME = "roepkeb"

RELATIVE_URLS = False

PATH = 'content'

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# https://github.com/gilsondev/pelican-clean-blog/
THEME='theme'
COLOR_SCHEME_CSS = 'monokai.css'
HEADER_COVER = 'images/home.jpg'

# Social widget
GITHUB_URL = 'http://github.com/broepke'
TWITTER_URL = 'http://twitter.com/broepke'
LINKEDIN_URL = 'https://www.linkedin.com/in/broepke/'

# static paths will be copied without parsing their contents
STATIC_PATHS = ['images', 'extra/robots.txt', 'extra/favicon.ico']
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'}
}

DEFAULT_PAGINATION = 6

PLUGIN_PATHS=['pelican-plugins']
PLUGINS = ['render_math']
