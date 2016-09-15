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
	while(pos != std::string::npos) {
		base.replace(pos, find.length(), replace);
		pos = base.find(find);
	}
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

int fileToString(std::string filename, std::string * out) {
	if(out == NULL) {
		return -2;
	}
	std::ifstream file(filename);
	if(!file.is_open()) {
		return -1;
	}
	std::string line;
	std::string string;
	while(std::getline(file, line)) {
		string += line + "\n";
	}
	file.close();
	*out = string;
	return 0;
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
	std::string content;
	if(fileToString("pages/" + page.filename, &content) < 0) {
		return -2;
	}
	pageStr = replace(pageStr, "$MENU", pageMenu);
	pageStr = replace(pageStr, "$PAGE", content);
	pageStr = replace(pageStr, "$TITLE", page.title);
	std::ofstream pageFile("generated/" + page.filename);
	if(!pageFile.is_open()) {
		return -1;
	}
	pageFile << pageStr;
	pageFile.flush();
	pageFile.close();
	std::cout << "Wrote page " << page.filename << std::endl;
	return 0;
}

int loadPages() {
	std::ifstream pagesFile("pages.txt");
	if(!pagesFile.is_open()) {
		return -1;
	}
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
	return fileToString("template.html", &pageTemplate);
}

int main(int argc, char* argv[]) {
	bool error = false;
	if(loadPages() < 0) {
		std::cout << "Error loading pages.txt" << std::endl;
		error = true;
	}
	if(loadTemplate() < 0) {
		std::cout << "Error loading template.html" << std::endl;
		error = true;
	}
	if(error) {
		return -1;
	}
	buildMenu();
	for(size_t i = 0; i < pages.size(); i++) {
		if(buildPage(pages[i]) < 0) {
			std::cout << "Error writing page file generated/" << pages[i].filename << std::endl;
		}
	}
	return 0;
}
