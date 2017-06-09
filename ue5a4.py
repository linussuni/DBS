# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import csv
import re
from collections import Counter


def countsSortedAlphabetically(counter, **kw):
	return sorted(counter.items(), **kw)

def countsSortedNumerically(counter, **kw):
	return sorted(counter.items(), key=lambda x:x[1], **kw)

# `from pprint import pprint as pp` is also useful
def printByLine(tuples):
	print( '\n'.join(' '.join(map(str,t)) for t in tuples) )

def getPage(url):
	r= requests.get(url)
	data = r.text
	spobj = BeautifulSoup(data, "lxml")
	return spobj

def main():

	fobj = open('heise-themen-https.csv', 'w')
	csvw = csv.writer(fobj)

	completetextstr = ""

	for page in range(0,4,1):

		heise_themen_url = "https://www.heise.de/thema/https?seite="+str(page)
		content = getPage(heise_themen_url).findAll('div', class_="keywordliste")
		for c in content:
			c = c.findAll("header")
			txt = [""]
			#itercontent = iter(content)
			#next(itercontent) #to exclude first header"alle Beitraege zu https"
			for t in c:
				txt.append(t.text.encode('utf-8'))

			csvw.writerow(txt)
			
			completetextstr += " ".join(txt)
			
	words = re.findall(ur'\w+', completetextstr, re.UNICODE)
	cap_words = [word.upper() for word in words]
	
	word_counts = Counter(cap_words)
	
	fobj.close()
	print("\nDONE ! heise.de/thema/https was scraped completely.\n")
	print("content:  "+completetextstr)
	printByLine(countsSortedNumerically(word_counts, reverse=True))
	#print(words)
	#print(word_counts)

if __name__ == '__main__':
	main()
