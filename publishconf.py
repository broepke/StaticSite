#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import sys

sys.path.append(".")
from pelicanconf import *

RELATIVE_URLS = False

FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/{slug}.atom.xml"

DELETE_OUTPUT_DIRECTORY = True
