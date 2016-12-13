#!/usr/bin/env python3
from distutils.dir_util import copy_tree
from sys import exit
import os
import json
import datetime

class Page:
	def __init__(self, title, filename, hidden):
		self.title = title
		self.filename = filename
		self.hidden = hidden

def loadSiteConfig():
	try:
		siteFile = open("page.json", "r")
	except IOError:
		print("Error: No pages.json found!")
		exit()
	return json.load(siteFile)

def loadTemplate(site):
	try:
		template = open(site["template"], "r")
	except IOError:
		print("Error: file " + site["template"] + " not found!")
		exit()
	return template.read()

def buildMenu(site):
	menu = "<ul>"
	for page in site["pages"]:
		if not "hidden" in page or page["hidden"] == "false":
			menu += "<li><a href='" + page["file"] + "'>" + page["title"] + "</a></li>"
	menu += "</ul>"
	return menu

def buildPage(template, menu, page, site):
	try:
		source = open("pages/" + page["file"], "r")
	except IOError:
		print("Error: Failed to read pages/" + page["file"])
		exit()
	try:
		dest = open("generated/" + page["file"], "w")
	except IOError:
		print("Error: Failed to generate generated/" + page["file"])
		exit()
	generated = template
	generated = generated.replace("$MENU", menu)
	generated = generated.replace("$TITLE", site["title"])
	generated = generated.replace("$SUBTITLE", site["subtitle"])
	generated = generated.replace("$AUTHOR", site["author"])
	generated = generated.replace("$PAGETITLE", page["title"])
	generated = generated.replace("$PAGE", source.read())
	now = datetime.datetime.now()
	generated = generated.replace("$YEAR", str(now.year))
	dest.write(generated)
	return

def buildPages(template, menu, site):
	if(not os.path.isdir("generated")):
		os.makedirs("generated")

	for page in site["pages"]:
		buildPage(template, menu, page, site)
	return

def copyAssets():
	if(os.path.isdir("assets")):
		copy_tree("assets", "generated")
	return

def mkpage():
	site = loadSiteConfig()
	template = loadTemplate(site)
	menu = buildMenu(site)
	buildPages(template, menu, site)
	copyAssets()
	return

mkpage()
