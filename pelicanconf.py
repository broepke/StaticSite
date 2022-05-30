#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Brian Roepke'
SITENAME = 'Data Knows All'
SITESUBTITLE = 'Machine Learning, Natural Language Processing, SQL, and More'
TAGLINE = 'Machine Learning, Natural Language Processing, SQL, and More'
SITEURL = 'https://www.dataknowsall.com'

# https://analytics.google.com/analytics/web
GOOGLE_ANALYTICS = 'G-W5GPXKDEPB'
# https://disqus.com/admin/
DISQUS_SITENAME = 'roepkeb'
# https://www.addthis.com/dashboard#profile-options/ra-617ff7ceb50a32be/general-settings
ADDTHIS_PUBID = 'ra-617ff7ceb50a32be'

RELATIVE_URLS = True
DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = True
USE_FOLDER_AS_CATEGORY = True 
DEFAULT_PAGINATION = 6

# https://github.com/gilsondev/pelican-clean-blog/
THEME='theme'
COLOR_SCHEME_CSS = 'tomorrow.css'
HEADER_COVER = 'images/home.jpg'

TIMEZONE = 'America/Los_Angeles'
DEFAULT_LANG = 'en'
# Used this if you want to have a custom static homepage and not blogroll
# INDEX_SAVE_AS = 'blog_index.html'

FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

PATH = 'content'
ARTICLE_PATHS = ['posts',]
PAGE_PATHS = ['pages',]
PLUGIN_PATHS=['pelican-plugins']
PLUGINS = ['render_math', 'gravatar', 'sitemap', 'seo']

MENUITEMS = (
    ('Résumé', '/pdf/cv.pdf'),
    ('Portfolio', '/pages/portfolio.html'),
    ('About', '/pages/about.html'),
    ('Subscribe', 'https://campaign.dataknowsall.com/subscribe'),
    # Similar to the above, uncomment these to have a custom static homepage
    # ('Blog', '/blog_index.html'),
    # ('Blog Home', '/index.html'),
)

# Social widget
SOCIAL = (
    ('twitter', 'https://twitter.com/broepke'),
    ('github', 'https://github.com/broepke'),
    ('linkedin','https://www.linkedin.com/in/broepke/')
)

# https://github.com/pelican-plugins/seo
SEO_REPORT = True
SEO_ENHANCER = True
SEO_ENHANCER_OPEN_GRAPH = True
SEO_ENHANCER_TWITTER_CARDS = True
SEO_ARTICLES_LIMIT = 50
SEO_PAGES_LIMIT = 50

# static paths will be copied without parsing their contents
STATIC_PATHS = ['images', 'extra/robots.txt', 'extra/favicon.ico', 'pdf', 'other']
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'}
}

# https://github.com/pelican-plugins/sitemap
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.8,
        'indexes': 0.1,
        'pages': 0.8
    },
    'changefreqs': {
        'articles': 'weekly',
        'indexes': 'weekly',
        'pages': 'monthly'
    }
}