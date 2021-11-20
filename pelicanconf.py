#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Brian Roepke'
SITENAME = 'roepkeb'
SITEURL = 'https://www.roepkeb.com'
# https://analytics.google.com/analytics/web
GOOGLE_ANALYTICS = 'UA-309309-9'
# https://disqus.com/admin/
DISQUS_SITENAME = 'roepkeb'
# https://www.addthis.com/dashboard#profile-options/ra-617ff7ceb50a32be/general-settings
ADDTHIS_PUBID = 'ra-617ff7ceb50a32be'

RELATIVE_URLS = False

DISPLAY_PAGES_ON_MENU = True

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
COLOR_SCHEME_CSS = 'tomorrow.css'
HEADER_COVER = 'images/home.jpg'

# Social widget
SOCIAL = (('twitter', 'https://twitter.com/broepke'),
          ('github', 'https://github.com/broepke'),
          ('linkedin','https://www.linkedin.com/in/broepke/'))


# static paths will be copied without parsing their contents
STATIC_PATHS = ['images', 'extra/robots.txt', 'extra/favicon.ico']
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'}
}

DEFAULT_PAGINATION = 6

PLUGIN_PATHS=['pelican-plugins']
PLUGINS = ['render_math', 'gravatar']


DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False
USE_FOLDER_AS_CATEGORY = True 
PATH = 'content'
ARTICLE_PATHS = ['posts',]
PAGE_PATHS = ['pages',]

MENUITEMS = (
    ('Resume', '/pages/resume.html'),
)