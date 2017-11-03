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
		raise e
		return "Shit the bed, contact Maker!"
