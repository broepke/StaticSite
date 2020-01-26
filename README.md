# StaticSite

Generated based on the tutorial from:  

https://www.fullstackpython.com/blog/generating-static-websites-pelican-jinja2-markdown.html

## Useful Commands  

* Use the `make html` to publish and update the output folder
* Run a local python web server running at by first `cd output` and
then `python -m http.server` which will be running at `localhost:8000`:
* Run the `make` command to see everything for this command
* Create new posts in the `content/posts` folder as `.markdown` files
* Useful tool to minify JS and CSS [Minifer.org](https://www.minifier.org)

### Markdown
Here is a great basic **Markdown** cheatsheet
https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet

Additionally, for **MultiMarkdown** which is supported many places, see here:
https://github.com/fletcher/MultiMarkdown/wiki/MultiMarkdown-Syntax-Guide

## Plugins

This site also uses a few Pelican Plugins.  Follow the instructions here:  
[Pelican Plugins on GitHub](https://github.com/getpelican/pelican-plugins)

Clone the following repo at the top level:  
`git clone --recursive https://github.com/getpelican/pelican-plugins`
