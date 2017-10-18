MkPage
======

MkPage can glue together several sub-pages into a template and generate a consistent navigation.

Anything more and this project would reinvent the wheel, because Jekyll and/or Hugo already exist.

Usage
-----

To use MkPage you'll need to setup a directory in a certain way. It needs to contain:
- a pages.json file, which contains information about all pages you want to include
- a template.html file, which is your basic layout, where all other content will be copied into
- a "pages" subdirectory, which contains all your different pages
- (optional) an "assets" subdirectory, which contains all auxilary files you want to use (stylesheets, images, etc.)
- a "generated" subdirectory, in which your page will be generated

pages.json
---------

This file contains all pages you want to include. It has the following format:

    {
        "title": "Site",
        "subtitle": "My cool site",
        "author": "Me",
        "template": "template.html",
        "pages": [
            {
                "title": "home",
                "file": "index.html"
            },
            {
                "title": "the invisible man",
                "file": "invisble.html",
                "hidden": true
            }
        ]
    }

The hidden attribute can optionally be set. It allows you to generate pages, but not include them in your navigation.

template.html
-------------

This file should just be a regular html file, complete with &lt;html&gt; tags and a doctype.
Place "$MENU$" in your template, where you want your navigation to be (it is a &lt;ul&gt; filled with links).
The page's title will be placed at "$TITLE$" and the page's actual content will be placed at "$PAGE$".

pages
-----

A page file must only contain tags, that would make sense in it's position in the template. So no &lt;html&gt;, &lt;body&gt; or anything.