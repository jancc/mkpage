#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from distutils.dir_util import copy_tree
from sys import exit
import os
import json
import datetime
import argparse

__version__ = "0.2.0"

class Site():
	def __init__(self, file, output, workingDirectory):
		self.output = output
		self.workingDirectory = workingDirectory
		config = self.loadConfig(os.path.join(workingDirectory, file))
		template = self.loadTemplate()

	"""
	Load the config json file and parse using inbuild json
	parsing functionality.
	"""
	def loadConfig(self, file):
		try:
			configFile = open(file, "r")
		except IOError:
			print("Error: No file: " + file + " found!")
			exit()
		self.config = json.load(configFile)

	"""
	Load the template html file, in which all other files will be embedded
	"""
	def loadTemplate(self):
		configFilename = os.path.join(self.workingDirectory, self.config["template"])
		try:
			templateFile = open(configFilename, "r")
		except IOError:
			print("Error: file " + configFilename + " not found!")
			exit()
		self.template = templateFile.read()

	"""
	Parse the optional hidden attribute of a page
	"""
	def isHidden(self, page):
		try:
			return page["hidden"]
		except KeyError:
			return False

	"""
	Prepare menu as a simple unnumbered HTML list with links.
	The current page isn't a link however.
	"""
	def buildMenu(self, currentPage):
		menu = "<ul>"
		for page in self.config["pages"]:
			if not self.isHidden(page) and page != currentPage:
				menu += "<li><a href='" + page["file"] + "'>" + page["title"] + "</a></li>"
			elif not self.isHidden(page):
				menu += "<li><a class='nav_active' href='" + page["file"] + "'>" + page["title"] + "</a></li>"
		menu += "</ul>"
		return menu

	"""
	Prepare a single page by first putting it inside the template and then
	loading all other definitions.
	"""
	def buildPage(self, folder, page):
		try:
			source = open(folder + "/" + page["file"], "r")
		except IOError:
			print("Error: Failed to read " + folder + "/" + page["file"])
			exit()
		try:
			dest = open(os.path.join(self.output, page["file"]), "w")
		except IOError:
			print("Error: Failed to generate " + self.output +  "/" + page["file"])
			exit()
		generated = self.template.replace("$PAGE$", source.read())
		menu = self.buildMenu(page)
		generated = generated.replace("$MENU$", menu)
		generated = generated.replace("$TITLE$", self.config["title"])
		generated = generated.replace("$SUBTITLE$", self.config["subtitle"])
		generated = generated.replace("$AUTHOR$", self.config["author"])
		generated = generated.replace("$PAGETITLE$", page["title"])
		now = datetime.datetime.now()
		generated = generated.replace("$YEAR$", str(now.year))
		dest.write(generated)
		return

	"""
	Build all pages that are defined in the config.
	"""
	def buildPages(self):
		if not os.path.isdir(self.output):
			os.makedirs(self.output)
		for page in self.config["pages"]:
			self.buildPage(os.path.join(self.workingDirectory, "pages"), page)
		return

	"""
	Copy all files in the "assets" folder into the generated folder.
	"""
	def copyAssets(self):
		if(os.path.isdir(os.path.join(self.workingDirectory, "assets"))):
			copy_tree(os.path.join(self.workingDirectory, "assets"), self.output)
		return

def mkpage():
	argparser = argparse.ArgumentParser(description="Very simple static site generator.")
	argparser.add_argument("-o", "--out",
						  help="Directory to output generated files (default: 'generated')",
						  default="generated")
	argparser.add_argument("-f", "--file",
						  help="Path to JSON file that describes your page (default: 'page.json')",
						  default="page.json")
	argparser.add_argument("-d", "--directory",
						  help="Path to directory that includes your files (default: current directory)",
						  default=os.getcwd())
	args = argparser.parse_args()

	site = Site(args.file, args.out, args.directory)

	site.buildPages()
	site.copyAssets()
	return

if __name__ == "__main__":
	mkpage()
