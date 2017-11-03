from bs4 import BeautifulSoup
import lxml.html
import urllib.request

def urban(term):
	url = "http://urbandictionary.com/define.php?term={0}".format(term)
	resource = BeautifulSoup(urllib.request.urlopen(url), "lxml")
	content = resource.find('div', {"class":"meaning"}).text.strip()
	strlen = len(content.split())
	string = content
	splits = 1

	if strlen > 75:
		string = content.split(".")[0]
		for x in range(splits):
			if strlen>20:
				string += content.split(".")[splits]
				splits += 1

		string += "."
	print(string)
	return string
