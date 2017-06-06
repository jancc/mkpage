#!/usr/bin/env python3
from distutils.dir_util import copy_tree
from sys import exit
import os
import json
import datetime
import argparse

class Site():
	def __init__(self, file, output):
		config = self.loadConfig(file)
		menu = self.buildMenu()
		self.output = output
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
			if not "hidden" in page or page["hidden"] == False:
				menu += "<li><a href='" + page["file"] + "'>" + page["title"] + "</a></li>"
		menu += "</ul>"
		self.menu = menu

	def buildBlogOverview(self):
		overview = "<ol reversed>"
		for post in self.config["blog"]["posts"]:
			overview += "<li><a href='" + post["file"] + "'>" + post["title"] + "</a></li>"
		overview += "</ol>"
		self.overview = overview

	def buildPage(self, folder, file, title):
		try:
			source = open(folder + "/" + file, "r")
		except IOError:
			print("Error: Failed to read " + folder + "/" + file)
			exit()
		try:
			dest = open(os.path.join(self.output, file), "w")
		except IOError:
			print("Error: Failed to generate " + self.output +  "/" + file)
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
		if not os.path.isdir(self.output):
			os.makedirs(self.output)
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
			copy_tree("assets", self.output)
		return

def mkpage():
	argparser = argparse.ArgumentParser(description="Very simple static site generator.")
	argparser.add_argument("-o", "--out",
						  help="Directory to output generated files (default: 'generated')",
						  default="generated")
	argparser.add_argument("-f", "--file",
						  help="Path to JSON file that describes your page (default: 'page.json')",
						  default="page.json")
	args = argparser.parse_args()

	site = Site(args.file, args.out)

	site.buildPages()
	if site.hasBlog():
		site.buildBlog()
	site.copyAssets()
	return

mkpage()
