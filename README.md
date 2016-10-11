MkPage
======

MkPage helps you generate static websites with several pages and a navigation.

Usage
-----

To use MkPage you'll need to setup a directory in a certain way. It needs to contain:
- a pages.txt file, which contains information about all pages you want to include
- a template.html file, which is your basic layout, where all other content will be copied into
- a "pages" subdirectory, which contains all your different pages
- (optional) an "assets" subdirectory, which contains all auxilary files you want to use (stylesheets, images, etc.)
- a "generated" subdirectory, in which your page will be generated

pages.txt
---------

This file contains all pages you want to include. It has the following format:
    Title = name.html
    About Me = about.html
    Downloads = downloads.html
    [HIDDEN]Pacman = pacman.html

The [HIDDEN] flag can be added. It allows you to generate pages, but not include them in your navigation.

template.html
-------------

This file should just be a regular html file, complete with <html> tags and a doctype.
Place "$MENU" in your template, where you want your navigation to be (it is a <ul> filled with links).
The page's title will be placed at "$TITLE" and the page's actual content will be placed at "$PAGE".

pages
-----

A page file must only contain tags, that would make sense in it's position in the template. So no <html>, <body> or anything.
