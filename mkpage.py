#!/usr/bin/env python3
from distutils.dir_util import copy_tree
from sys import exit
import os
import json
import datetime

class Site():
	def __init__(self, file):
		config = self.loadConfig(file)
		menu = self.buildMenu()
		if self.hasBlog():
			overview = self.buildBlogOverview()
		template = self.loadTemplate()

	def loadConfig(self, file):
		try:
			configFile = open(file, "r")
		except IOError:
			print("Error: No file: " + file + " found!")
			exit()
		self.config = json.load(configFile)

	def loadTemplate(self):
		try:
			templateFile = open(self.config["template"], "r")
		except IOError:
			print("Error: file " + self.config["template"] + " not found!")
			exit()
		self.template = templateFile.read()

	def buildMenu(self):
		menu = "<ul>"
		for page in self.config["pages"]:
			if not "hidden" in page or page["hidden"] == "false":
				menu += "<li><a href='" + page["file"] + "'>" + page["title"] + "</a></li>"
		menu += "</ul>"
		self.menu = menu

	def buildBlogOverview(self):
		overview = "<ul>"
		for post in self.config["blog"]["posts"]:
			overview += "<li><a href='" + post["file"] + "'>" + post["title"] + "</a></li>"
		overview += "</ul>"
		self.overview = overview

	def buildPage(self, folder, file, title):
		try:
			source = open(folder + "/" + file, "r")
		except IOError:
			print("Error: Failed to read " + folder + "/" + file)
			exit()
		try:
			dest = open("generated/" + file, "w")
		except IOError:
			print("Error: Failed to generate generated/" + file)
			exit()
		generated = self.template.replace("$CONTENT", source.read())
		generated = generated.replace("$MENU", self.menu)
		if self.hasBlog():
			generated = generated.replace("$BLOGOVERVIEW", self.overview)
		generated = generated.replace("$TITLE", self.config["title"])
		generated = generated.replace("$SUBTITLE", self.config["subtitle"])
		generated = generated.replace("$AUTHOR", self.config["author"])
		generated = generated.replace("$PAGETITLE", title)
		now = datetime.datetime.now()
		generated = generated.replace("$YEAR", str(now.year))
		dest.write(generated)
		return

	def buildPages(self):
		for page in self.config["pages"]:
			self.buildPage("pages", page["file"], page["title"])
		return

	def buildBlog(self):
		for post in self.config["blog"]["posts"]:
			self.buildPage("posts", post["file"], post["title"])
		return

	def hasBlog(self):
		return "blog" in self.config

	def copyAssets(self):
		if(os.path.isdir("assets")):
			copy_tree("assets", "generated")
		return

def mkpage():
	site = Site("page.json")

	if not os.path.isdir("generated"):
		os.makedirs("generated")
	site.buildPages()
	if site.hasBlog():
		site.buildBlog()
	site.copyAssets()
	return

mkpage()
