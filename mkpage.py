#!/usr/bin/env python3
from distutils.dir_util import copy_tree
from sys import exit
import os

class Page:
	def __init__(self, title, filename, hidden):
		self.title = title
		self.filename = filename
		self.hidden = hidden

def loadPagesList():
	pages = []
	try:
		pagesFile = open("pages.txt", "r")
	except IOError:
		print("Error: No pages.txt found!")
		exit()
	content = pagesFile.read()
	lines = content.splitlines()
	for line in lines:
		pagedata = line.split("=", 1)
		if len(pagedata) == 2:
			hidden = False
			if "[HIDDEN]" in pagedata[0]:
				hidden = True
				pagedata[0] = pagedata[0].replace("[HIDDEN]", "")
			page = Page(pagedata[0].strip(), pagedata[1].strip(), hidden)
			pages.append(page)
	return pages
	
def loadTemplate():
	try:	
		template = open("template.html", "r")
	except IOError:
		print("Error: No template.html found!")
		exit()
	return template.read()
	
def buildMenu(pages):
	menu = "<ul>"
	for page in pages:
		if not page.hidden:
			menu += "<li><a href='" + page.filename + "'>" + page.title + "</a></li>"
	menu += "</ul>"
	return menu
	
def buildPage(template, menu, page):
	try:
		source = open("pages/" + page.filename, "r")
	except IOError:
		print("Error: Failed to read pages/" + page.filename)
		exit()
	try:	
		dest = open("generated/" + page.filename, "w")
	except IOError:
		print("Error: Failed to generate generated/" + page.filename)
		exit()
	generated = template
	generated = generated.replace("$MENU", menu)
	generated = generated.replace("$TITLE", page.title)
	generated = generated.replace("$PAGE", source.read())
	dest.write(generated)
	return
	
def buildPages(template, menu, pages):
	if(not os.path.isdir("generated")):
		os.makedirs("generated")
	
	for page in pages:
		buildPage(template, menu, page)
	return
	
def copyAssets():
	if(os.path.isdir("assets")):
		copy_tree("assets", "generated")
	return
	
def mkpage():
	pages = loadPagesList()
	template = loadTemplate()
	menu = buildMenu(pages)
	buildPages(template, menu, pages)
	copyAssets()
	return
	
mkpage()
