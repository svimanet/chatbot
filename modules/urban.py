from bs4 import BeautifulSoup
import lxml.html
import requests

def urban(term):
	try:
		url = "http://urbandictionary.com/define.php?term={0}".format(term)
		resource = BeautifulSoup(requests.get(url).content, "lxml")
		content = resource.find('div', {"class":"meaning"}).text.strip()
		strlen = len(content)
		string = content
		splits = 1

		if strlen > 75:
			string = content.split(".")[0]
			for x in range(splits):
				if strlen > 20:
					string += content.split(".")[splits]
					splits += 1

			string += "."

		print(string)
		return string
	
	except Exception as e:
		return "Shit the bed, contact Maker!"



def define(term):
	try:
		url = "https://dictionary.com/browse/{}".format(term)
		resource = BeautifulSoup(requests.get(url).content, "lxml")
		content = resource.find('div', {"class":"def-content"})
		example = resource.find('div', {"class":"def-inline-example"})

		if content is None:
			content = "Couldn't find {}.".format(term)
			example = ""
		else: 
			content = content.text.strip()
			if example is None:
				example = "No example available."
			else:
				example = example.text.strip()

		string = "{0}&+{1}".format(content, example)
		print(string)
		return string

	except Exception as e:
		return e