# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import csv
import re
from collections import Counter

#****************************************************************
#von Stackoverflow außschließlich optische Funktion
def countsSortedNumerically(counter, **kw):
	return sorted(counter.items(), key=lambda x:x[1], **kw)

def printByLine(tuples):
	print( '\n'.join(' '.join(map(str,t)) for t in tuples) )
#****************************************************************


def getPage(url):#genauso wie im Beispiel
	r= requests.get(url)
	data = r.text
	spobj = BeautifulSoup(data, "lxml")
	return spobj

def main():

	fobj = open('heise-themen-https.csv', 'w')
	csvw = csv.writer(fobj) #es wird eine csv geschrieben
			#ja sie wird nicht benutzt, diente aber dem zweck eine anfängliche
		#Übersicht zu haben ob das richtige raus kommt und für das Erfolgsgefühl

	completetextstr = ""#string aller Wörter um diese später in liste zu bringen

	for page in range(0,4,1): #iteriere durch die 4 Seiten

		heise_themen_url = "https://www.heise.de/thema/https?seite="+str(page)
		content = getPage(heise_themen_url).findAll('div', class_="keywordliste")
				#die Überschriften stehen immer im div mit der class keyw...
		for c in content:
			c = c.findAll("header")
			txt = [""]
			#itercontent = iter(content)
			#next(itercontent) #to exclude first header"alle Beitraege zu https"
			#funktionierte leider nicht wie gewünscht
			for t in c:
				txt.append(t.text.encode('utf-8'))

			csvw.writerow(txt)
			
			completetextstr += " ".join(txt)
	
	#alle Wörter werden gelistet			
	words = re.findall(ur'\w+', completetextstr, re.UNICODE) 
	#großmachen der wörter für weniger unterschiede
	cap_words = [word.upper() for word in words]
	#counter für die Wörter	
	word_counts = Counter(cap_words)
	
	fobj.close()
	print("\nDONE ! heise.de/thema/https was scraped completely.\n")
	print("content:  "+completetextstr) #schöne Übersicht über alle Überschriften
	printByLine(countsSortedNumerically(word_counts, reverse=True))
		#schöne Darstellung der verwendeten Wörter

if __name__ == '__main__':
	main()
