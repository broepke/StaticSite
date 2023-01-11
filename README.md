# StaticSite

## Motivation

I started to build out this site because I wanted to play with AWS.  [This site](httpw://www.roepkeb.com) is hosted via an `S3` bucket's static web hosting capability and then fronted with the CDN `CloudFront`.  CloudFront, unlike direct S3 hosting also gives you the ability to use HTTPS and not just HTTP.  Nothing here is overly complex, but the `Pelican` framework is pretty slick and I've been experimenting with various customizations, themes, and plugins.  It's been interesting to see the behavior of the caching and TTL (default of 24 hours) and how you update the site.  

_Note: With S3 hosting you can force the cache to request updated items by versioning the filename or invalidating the cache.  Versioning the file name is much more cost effective._

## Install the following Packages

`pip install pelican`
`pip install markdown`

## Configure AWS CLI

To sync this to S3, the environment will have to have AWS CLI installed and configured.  
[AWS CLI V2](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)

[AWS CLI Configuration Quickstart](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)

## Working with this Site  

* Use the `make html` to publish and update the output folder
* Run a local python web server running at by first `cd output` and
then `python -m http.server` which will be running at `localhost:8000`:
* Run `make regenerate` to constantly regen each time a chagne is detected
* Run the `make` command to see everything for this command
* Create new posts in the `content/posts` folder as `.markdown` files
* Useful tool to minify JS and CSS [Minifer.org](https://www.minifier.org)

## Markdown

Here is a great basic **Markdown** cheatsheet
[Markdown cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)

Additionally, for **MultiMarkdown** which is supported many places, see here:
[Multi-Markdown Cheatshet](https://github.com/fletcher/MultiMarkdown/wiki/MultiMarkdown-Syntax-Guide)

## Plugins

This site also uses a few Pelican Plugins.  Follow the instructions here:  
[Pelican Plugins on GitHub](https://github.com/getpelican/pelican-plugins)

Clone the following repo at the top level:  
`git clone --recursive https://github.com/getpelican/pelican-plugins`

## Initial Starting Point

Generated originally based on the tutorial from:  

[How to Create Your First Static Site with Pelican and Jinja2](https://www.fullstackpython.com/blog/generating-static-websites-pelican-jinja2-markdown.html)


## Adding Canonical Link to Template

[Improve your Pelican based website SEO by adding canonical url](https://www.andreagrandi.it/2020/10/14/improve-pelican-based-website-seo-adding-canonical-url/)

```
    ...
    {% if article %}
        <link rel="canonical" href="{{ SITEURL }}/{{ article.url }}" />
    {% endif%}
</head>
```