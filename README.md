# StaticSite

## Motivation

I started to build this out based on wanting to play wiht AWS a little more.  This site is hosted via an `S3` bucket's static web hosting capability and then fronted with the CDN 'CloudFront'.  CloudFront, unlike direct S3 hosting also gives you the abilty to use HTTPS and not just HTTP.  Nothing here is overly complex, but the `Pelican` framework is pretty slick and I've been experimenting with various customizations, themes, and plugins.

## Working with this Site  

* Use the `make html` to publish and update the output folder
* Run a local python web server running at by first `cd output` and
then `python -m http.server` which will be running at `localhost:8000`:
* Run the `make` command to see everything for this command
* Create new posts in the `content/posts` folder as `.markdown` files
* Useful tool to minify JS and CSS [Minifer.org](https://www.minifier.org)

## Markdown Cheatsheet:
While markdown is a reallys simple 'language', I find from time to time I want a good reference.  I found this one to be excellent.  Covers most of the base Markdown specification and a few other tips. 

https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet

## Plugins

This site also uses a few Pelican Plugins.  Follow the instructions here:  
[Pelican Plugins on GitHub](https://github.com/getpelican/pelican-plugins)

Clone the following repo at the top level:  
`git clone --recursive https://github.com/getpelican/pelican-plugins`

## Initial Starting Point

Generated originally based on the tutorial from:  

https://www.fullstackpython.com/blog/generating-static-websites-pelican-jinja2-markdown.html
