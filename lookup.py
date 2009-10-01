#!/usr/bin/env python
#coding=utf-8
"""
arXivToWiki
©2009 by Sven-S. Porst / earthlingsoft (ssp-web@earthlingsoft.net)
"""

from __future__ import with_statement
import cgi
import re
import urllib
from xml.etree import ElementTree
import xml.etree

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


"""
	Set up table of real names and crcg user names to create links to people's pages.
"""
people = dict({
"Laurent Bartholdi": "http://www.uni-math.gwdg.de/laurent/",
"Ralf Meyer": "http://www.uni-math.gwdg.de/rameyer/",
"Preda Mihailescu": "http://www.uni-math.gwdg.de/preda/",
"Samuel J. Patterson": "http://www.uni-math.gwdg.de/sjp/",
"Pablo Ramacher": "http://www.uni-math.gwdg.de/ramacher/",
"Karl-Henning Rehren": "http://www.theorie.physik.uni-goe.de/~rehren/",
"Thomas Schick": "http://www.uni-math.gwdg.de/schick/",
"Andreas Thom": "http://www.math.uni-leipzig.de/MI/thom/",
"Yuri Tschinkel": "http://www.uni-math.gwdg.de/tschinkel/",
"Ingo Witt": "http://www.uni-math.gwdg.de/iwitt/",
"Dorothea Bahns": "http://www.uni-math.gwdg.de/bahns/",
"Hannah Markwig": "User:Hannah",
"Chenchang Zhu": "User:Zhu",
"Anders Jensen": "User:Jensen",
"Alessandro Valentino": "http://www.uni-math.gwdg.de/sandro/",
"Hans-Christian Graf v. Bothmer": "User:Bothmer",
"Hans-Christian Graf von Bothmer": "User:Bothmer",
"Hans-Christian Bothmer": "User:Bothmer",
"Hans-Christian v. Bothmer": "User:Bothmer",
"Hans-Christian von Bothmer": "User:Bothmer",
"Thomas Markwig": "http://www.mathematik.uni-kl.de/~keilen/de/index.html",
"Eugenii Shustin": "http://www.math.tau.ac.il/~shustin/",
"Christian Böhning": "http://www.uni-math.gwdg.de/boehning/",
"Christian Boehning": "http://www.uni-math.gwdg.de/boehning/"
})




def prepareArXivID(ID):
	"""
		0909.1234-style ID => return unchanged
		09091234-style ID => return 0909.1234
		0606123-style ID => return math/0606123
		non-math/0606123-style ID => return unchanged
	"""
	myID = ID.strip()
	if  re.match(r"\d\d\d\d\.?\d\d\d\d$", myID) == None:
		""" 
			Not an 8 digit number: must be old style, if it doesn't contain an arXiv specifier, assume we're referring to math and prepend that. 
		"""
		startsWithDigit = re.match(r"\d", myID)
		if startsWithDigit != None:
			myID = "math/" + myID
	else:
		""" 
			Convenience: insert dot in the middle of a 8 digit number in case it was not entered.
		"""
		if re.match(r"\.", myID) == None:
			myID = re.sub(r"(\d\d\d\d)(\d\d\d\d)$", r"\1.\2", myID)
	
	return myID





def escapeHTML(inputString):
	"""
		Input: string
		Output: input string with < > & ' replaced by their HTML character entities
	"""
	ampRegexp = re.compile(r"&")
	ltRegexp = re.compile(r"<")
	gtRegexp = re.compile(r">")
	aposRegexp = re.compile(r"'")
	escapedString = ampRegexp.sub('&amp;', inputString)
	escapedString = ltRegexp.sub('&lt;', escapedString)
	escapedString = gtRegexp.sub('&gt;', escapedString)
	escapedString = aposRegexp.sub('&#39;', escapedString)

	return escapedString




def theForm():
	"""
		Returns HTML for the search form.
	"""
	return """
<form method="get" action="./lookup.py">
<p>
<input type="text" name="papers" class="papers" value='""" + escapeHTML(queryString) + """'>
<input type="submit" class="button" value="Retrieve Information">
</p>
</form>
"""



def pageHead():
	"""
		Returns HTML for the http header and the top of the HTML markup including CSS.
	"""

	return """Content-type: text/html; charset=UTF-8

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<title>Retrieve arXiv Information</title>
<meta name='generator' content='arXiv to Wiki converter for CRCG by earthlingsoft; ssp-web@earthlingsoft.net'>
<style type="text/css">
* { margin: 0em; padding: 0em; }
body { width: 40em; font-family: Georgia, Times, serif; line-height: 141%; margin:auto; background: #eee;}
#title { text-align:center; margin:2em 1em; }
p { margin: 0.5em 0em; }
h1 { font-size: 144%; margin: 0.5em;}
p.crcg { font-style: italic; }
form { display:block; margin: 1em; }
form p { text-align:center; } 
form input { font-size: 144%; }
form input.papers { width: 63%; margin-bottom: 6px; }
form input.button { position:relative; bottom: 3px; }
h2 { font-size: 121%; margin:2em 0em 1em 0em; position:relative; }
h2:before { content: "\\002767"; position: absolute; width: 1em; left:-1em; font-size: 360%; color: #999; }
h2.error:before { content: "\\002718"; color: #f33; }
textarea { width:100%; }
#foot { font-style:italic; text-align: center; margin: 3em 0em 1em 0em; border-top: #999 solid 1px; }
</style>
</head>
<body>
<div id="page">
<div id="title">
<h1>Retrieve arXiv Information</h1>
<p class="crcg">
<a href="http://www.crcg.de">Courant Research Centre ,Higher Order Structures in Mathematics‘</a>
</p>
</div>
<p>
This page helps you retrieve information from your <a href="http://www.arxiv.org/">arXiv</a> submissions for use on the Courant Centre <a href="http://92.51.147.127/wiki/index.php?title=Main_Page">publications wiki page</a>. Enter IDs – e.g. 0909.4913 – of the papers you want to add below and the page will give you the relevant information marked up ready to copy and paste it into the wiki.
</p>
""" + theForm()




def pageFoot():
	"""
		Returns HTML for the bottom of the page.
	"""

	return """<div id="foot">
<a href="http://www.crcg.de/">Courant Research Centre ,Higher Order Structures in Mathematics‘</a><br>
Georg-August-Universität Göttingen<br>
<a href="http://www.besserweb.de/website.php?id=42">Leave a Comment</a>
</div>	
</div>
</body>
</html>
"""




def markupForHTML(myDict):
	"""
		Input: dictionary with publication data.
		Output: HTML markup for publication data.
	"""
	authors = myDict["authors"]
	htmlauthors = []
	for author in authors:
		if people.has_key(author):
			address = people[author]
			if address.startswith("User:"):
				username = address.partition(":")[2]
				htmlauthors += ["<a href='http://www.crcg.de/index.php?title=User:" + username + "'>" + author + "</a>"]
			else:
				htmlauthors += ["<a href='" + address + "'>" + author + "</a>"]
		else:
			htmlauthors += [author]
			
	output = [", ".join(htmlauthors), ': “',  myDict["title"], '”, ', myDict["year"]]
	if myDict["journal"] != None:
		output += [", ", myDict["journal"]]
	output += ["; <a href='",  myDict["link"], "'>arXiv:", myDict["ID"], "</a>."]
	if myDict["DOI"] != None:
		output += [" DOI: <a href='http://dx.doi.org/", myDict["DOI"], "'>", myDict["DOI"], "</a>."]
	return "".join(output)




def markupForWiki(myDict):
	"""
		Input: dictionary with publication data.
		Output: Wiki markup for publication data.
	"""
	authors = myDict["authors"]
	wikiauthors = []
	for author in authors:
		if people.has_key(author):
			address = people[author]
			if address.startswith("User:"):
				username = address.partition(":")[2]
				wikiauthors += ["[[user:" + username + "|" + author + "]]"]
			else:
				wikiauthors += ["[[" + address + " " + author + "]]"]
		else:
			wikiauthors += [author]
	
	wikioutput = ["* ", ", ".join(wikiauthors), ': “', myDict["title"], '”, ', myDict["year"]]
	if myDict["journal"] != None:
			wikioutput += [", ", myDict["journal"]]
	wikioutput += ["; [", myDict["link"], " arXiv:", myDict["ID"], "]."]
	if myDict["DOI"] != None:
		wikioutput += [" DOI: [http://dx.doi.org/", myDict["DOI"], " ", myDict["DOI"], "]."]
	result = "".join(wikioutput)
	result = re.sub(r"\s+", r" ", result)
	return result




def markupForBibTeX(myDict):
	"""
		Input: dictionary with publication data.
		Output: BibTeX record for the preprint.
	"""
	bibTeXID = myDict["ID"]
	bibTeXAuthors = " and ".join(myDict["authors"])
	bibTeXTitle = myDict["title"]
	bibTeXYear = myDict["year"]
	
	bibTeXEntry = ["@misc{", bibTeXID, ",\nAuthor = {", bibTeXAuthors, "},\nTitle = {", bibTeXTitle, "},\nYear = {", bibTeXYear, "},\nEprint = {arXiv:", bibTeXID, "},\n"] 
	if myDict["journal"] != None:
		bibTeXEntry += ["Howpublished = {", myDict["journal"], "},\n"]
	if myDict["DOI"] != None:
		bibTeXEntry += ["Doi = {", myDict["DOI"], "},\n"]
	bibTeXEntry += ["}"]
	result = "".join(bibTeXEntry)
	return result




def markupForBibItem(myDict):
	"""
		Input: dictionary with publication data.
		Output: LaTeX \bibitem command for the publication
	"""
	bibTeXID = myDict["ID"]
	authors = myDict["authors"]
	authorstring = ""
	if len(authors) == 1:
		authorString = authors[0]
	else:
		lastAuthor = authors.pop(-1)
		authorString = ", ".join(authors) + " and " + lastAuthor
	
	title = myDict["title"]
	year = myDict["year"]

	bibItemCommand = ["\\bibitem{", bibTeXID, "}\n", authorString, ".\n\\newblock ", title, ", ", year]
	if myDict["journal"] != None:
		bibItemCommand += [",\n\\newblock ", myDict["journal"]]
	bibItemCommand += [";\n\\newblock arXiv:", bibTeXID, "."]
	if myDict["DOI"] != None:
		bibItemCommand += ["\n\\newblock DOI:", myDict["DOI"], "."]
	result = "".join(bibItemCommand)
	return result





def errorMarkup(errorText):
	"""
		Return markup for the error text received.
	"""
	return """<h2 class="error">An error occurred</h2>
<p>""" + errorText + """</p>
<p>If you think you entered a valid arXiv ID and you keep getting this error message, please accept our apologies and <a href="http://www.besserweb.de/website.php?id=42">let us know about it</a>.</p>
"""




"""
	MAIN SCRIPT *****************************************************************
"""

form = cgi.FieldStorage()
queryString = ""
if form.has_key("papers"):
	queryString = form["papers"].value
	papers = re.sub(r",", r" ", queryString).split()
print pageHead()


if form.has_key("papers"):
	arXivIDs = []
	for paperID in papers:
		arXivIDs += [prepareArXivID(paperID)]
	arXivURL = "http://export.arxiv.org/api/query?id_list=" + ",".join(arXivIDs)
	download = urllib.urlopen(arXivURL)
	download.encoding = "UTF-8"
	downloadedData = download.read()
	if downloadedData == None:
		print errorMarkup("The arXiv data could not be retrieved.")
	else:
		feed = xml.etree.ElementTree.fromstring(downloadedData)
		
		"""	Check for an error by looking at the title of the first paper """
		firstTitle = feed.find("{http://www.w3.org/2005/Atom}entry/{http://www.w3.org/2005/Atom}title")
		if firstTitle.text == "Error":
			print errorMarkup("The arXiv returned an error for the paper ID you requested. Any chance there may be a typo in there?")
		else:
			""" We got data and no error: Process it. """
			papers = feed.getiterator("{http://www.w3.org/2005/Atom}entry")
			output = []
			for paper in papers:
				authors = paper.getiterator("{http://www.w3.org/2005/Atom}author")
				theAuthors = []
				for author in authors:
					name = author.find("{http://www.w3.org/2005/Atom}name").text
					theAuthors += [name]
				theTitle = paper.find("{http://www.w3.org/2005/Atom}title").text
				theAbstract = paper.find("{http://www.w3.org/2005/Atom}summary").text.strip()
				links = paper.getiterator("{http://www.w3.org/2005/Atom}link")
				thePDF = ""
				theLink = ""
				for link in links:
					attributes = link.attrib
					if attributes.has_key("type"):
						linktype = attributes["type"]
					if linktype == "application/pdf":
						thePDF = attributes["href"]
					elif linktype == "text/html":
						theLink = attributes["href"]
				splitLink = theLink.split("/abs/")
				theID = splitLink[-1].split('v')[0]
				theLink = splitLink[0] + "/abs/" + theID
				theYear = paper.find("{http://www.w3.org/2005/Atom}published").text.split('-')[0]
				DOI = paper.find("{http://arxiv.org/schemas/atom}doi")
				theDOI = None
				extraRows = 0
				if DOI != None:
					theDOI = DOI.text
					extraRows += 1
				journal = paper.find("{http://arxiv.org/schemas/atom}journal_ref")
				theJournal = None
				if journal != None:
					theJournal = journal.text
					extraRows += 1
				
				publicationDict = dict({"authors": theAuthors, "title": theTitle, "abstract": theAbstract, "PDF": thePDF, "link": theLink, "ID": theID, "year": theYear, "DOI": theDOI, "journal": theJournal})
						
				output += ["<h2>arXiv: ", publicationDict["ID"], "</h2>\n"]
				output += ["<p class='paperinfo'>\n", markupForHTML(publicationDict), "</p>\n"]
				output += ["<p>Copy and paste the text below for the wiki:</p>\n<textarea class='wikiinfo' cols='70' rows='4'>\n", markupForWiki(publicationDict), "</textarea>\n"]
				output += ["<p>A simple-minded BibTeX entry for the paper:</p>\n<textarea class='bibtexinfo' cols='70' rows='", str(6 + extraRows), "'>\n", markupForBibTeX(publicationDict), "</textarea>\n"]
				output += ["<p>A simple-minded \bibitem-command for use in LaTeX:</p>\n<textarea class='bibiteminfo' cols='70' rows='", str(4+extraRows), "'>\n", markupForBibItem(publicationDict), "</textarea>\n"]
			print "".join(output)
		
print pageFoot()


