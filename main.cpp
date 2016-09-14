/*
Sobald mir das Dorfinternet Zugriff auf einen Compiler erlaubt soll dieses Programm folgendes können:
	- Eine Template Datei einlesen
	- "%MENU%" ersetzen mit einem korrekten Menu "<ul></ul>"
	- Markdown Dateien in dem Ordner Pages in Unterseiten verwandeln
	- index.md ist die Startseite, sie wird zu index.html
	- Der Dateiname der Seiten ist auch ihr Titel und ihr Name im Menü (ausser index.md)
	- Markdown Content ersetzt im Template "%PAGE%"
	- Aufrufen tut man das Programm im Root der Seite, es generiert die fertige statische Seite im Ordner "generated"
	- IDEE: Kein Markdown, einfach rohes HTML (erstmal) (möglicherweise Support für mehrere Formate)
*/

#include <iostream>
#include <fstream>
#include <vector>
#include <string>

class Page {
	public:
	Page(std::string newTitle, std::string newFilename) {
		title = newTitle;
		filename = newFilename;
	}
	std::string title;
	std::string filename;
};

std::vector<Page> pages;
std::string pageMenu;
std::string pageTemplate;

std::string replace(std::string base, std::string find, std::string replace) {
	std::size_t pos = base.find(find);
	base.replace(pos, find.length(), replace);
	return base;
}

std::string trim(std::string trimmed) {
	size_t begin = trimmed.find_first_not_of(' ');
	size_t end = trimmed.find_last_not_of(' ');
	if(end == std::string::npos) {
		end = trimmed.length();
	}
	if(begin == std::string::npos) {
		begin = 0;
	}
	return trimmed.substr(begin, end - begin + 1);
}

std::vector<std::string> split(std::string string, char delimiter) {
	std::vector<std::string> output;
	size_t delimpos = string.find(delimiter);
	if(delimpos == std::string::npos) {
		output.push_back(string);
		return output;
	}
	output.push_back(string.substr(0, delimpos));
	output.push_back(string.substr(delimpos + 1, string.length()));	
	return output;
}

int buildMenu() {
	pageMenu = "<ul>";
	for(size_t i = 0; i < pages.size(); i++) {
		std::string temp = "<li><a href='$FILE'>$TITLE</a></li>";
		temp = replace(temp, "$FILE", pages[i].filename);
		temp = replace(temp, "$TITLE", pages[i].title);
		pageMenu += temp;
	}
	pageMenu += "</ul>";
	return 0;
}

int buildPage(Page page) {
	std::string pageStr = pageTemplate;
	pageStr = replace(pageStr, "$MENU", pageMenu);
	pageStr = replace(pageStr, "$PAGE", "Hurensohn");
	pageStr = replace(pageStr, "$TITLE", page.title);
	std::ofstream pageFile("generated/" + page.filename);
	pageFile << pageStr;
	pageFile.flush();
	pageFile.close();
	std::cout << "Wrote page " << page.filename << std::endl;
	return 0;
}

int loadPages() {
	std::ifstream pagesFile("pages.txt");
	std::string line;
	while(std::getline(pagesFile, line)) {
		std::vector<std::string> values = split(line, '=');
		if(values.size() == 2) {
			std::string title = trim(values[0]);
			std::string filename = trim(values[1]);
			pages.push_back(Page(title, filename));
		}
	}
	pagesFile.close();
	return 0;
}

int loadTemplate() {
	std::ifstream templateFile("template.html");
	std::string line;
	while(std::getline(templateFile, line)) {
		pageTemplate += line + "\n";
	}
	templateFile.close();
	return 0;
}

int main(int argc, char* argv[]) {
	loadPages();
	loadTemplate();
	buildMenu();
	for(size_t i = 0; i < pages.size(); i++) {
		buildPage(pages[i]);
	}
}