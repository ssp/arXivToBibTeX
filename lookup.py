#!/usr/bin/env python
#coding=utf-8
"""
arXivToBibTeX / arXivToWiki v7.2
©2009-2020 Sven-S. Porst / earthlingsoft <ssp-web@earthlingsoft.net>

Service available at: https://arxiv2bibtex.org
Source code available at: https://github.com/ssp/arXivToBibTeX

Originally created for Courant Research Centre
‘Higher Order Structures in Mathematics’ at the
Mathematics Institute at the University of Göttingen.

Links for form submission refer to the folder of the current path without a
further filename:
	/?q=searchTerm

Your server setup (.htaccess file) needs to make sure that these requests are
redirected to the script.
"""

import cgi
import re
import urllib
from urlparse import urlparse
from xml.etree import ElementTree
import xml.etree
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#for debugging
#import cgitb
#cgitb.enable()

maxpapers = 100

trailingRE = re.compile(r"(.*)v[0-9]*$")
newStyleRE = re.compile(r"\d{4}\.?\d{4,}$")
sevenDigitsRE = re.compile(r"\d{7}$")
oldStyleIDRE = re.compile(r"[a-z-]+/\d{7}$")
paperIDRE = re.compile(r"([a-z-]+/\d{7}|\d{4}\.\d{4,})")



def prepareArXivID(ID):
	"""
		first, strip potentially trailing version numbers like v4
		0909.1234 or 1504.12345-style ID => return unchanged
		09091234 or 159412345-style ID => return 0909.1234 or 1504.12345
		0606123-style ID => return math/0606123
		non-math/0606123-style ID => return unchanged
		anything else => return None
	"""
	myID = ID.strip()
	myID = trailingRE.sub(r"\1", myID)
	if newStyleRE.match(myID) != None:
		""" An 8+ digit number (new-style): insert dot in the middle in case it's not there already.	"""
		if re.match(r"\.", myID) == None:
			myID = re.sub(r"(\d\d\d\d)(\d\d\d\d+)$", r"\1.\2", myID)
	elif sevenDigitsRE.match(myID) != None:
		""" Just seven digits: prepend math/ """
		myID = "math/" + myID
	elif oldStyleIDRE.match(myID) != None:
		myID = myID
	else:
		myID = None

	return myID


def extractPapersFromArXivUriPath(path):
	"""
		An arXiv URL was entered, extract the last component(s) as the paper ID
		Match both old math.ph/9902123 and new 1705.12345 style path segments
	"""
	paperIDMatch = paperIDRE.search(path)
	if paperIDMatch != None:
		return paperIDMatch.string[paperIDMatch.start(1):paperIDMatch.end(1)]



def printAll(output):
	print output



def printHtml(html, outputformat):
	if outputformat == "html":
		print html




def printPublicationsRaw(publications, format, outputformat):
	if outputformat == "raw":
		if format == "html":
			print "\n\n".join(map(lambda publication: basicMarkupForHTMLEditing(publication), publications))
		elif format == "bibtex" or format == "biblatex":
			print "\n\n".join(map(lambda publication: markupForBibTeXItem(publication, format), publications))
		elif format == "bibitem":
			print "\n\n".join(map(lambda publication: markupForBibItem(publication), publications))
		elif format == "wiki":
			print "\n".join(map(lambda publication: markupForWikiItem(publication), publications))




def escapeHTML(inputString):
	"""
		Input: string
		Output: input string with < > & " replaced by their HTML character entities
	"""
	return cgi.escape(inputString, True)



def theForm(format, queryString):
	"""
		Returns string with HTML for the search form.
		The form is pre-filled with the current query string.
	"""
	return '''
<form method="get" action="./">
<p>
<input type="text" name="q" class="q" autofocus="autofocus" placeholder="1510.01797 or courant_r_1" value="''' + escapeHTML(queryString) + '''"/>
<input type="hidden" name="format" id="formatinput" value="''' + escapeHTML(format) + '''"/>
<input type="submit" class="button" value="Retrieve Information"/>
</p>
</form>
'''



def outputformatToMimeType(outputformat):
	if outputformat == "html":
		return "text/html"
	elif outputformat == "bibtex" or outputformat == "biblatex":
		return "application/x-bibtex"
	else:
		return "text/plain"



def pageHead(queryString, format, outputformat):
	"""
		Returns string with HTML for the http header and the top of the HTML markup including CSS and JavaScript.
	"""
	if outputformat == "raw":
		return "Content-type: " + outputformatToMimeType(outputformat) + "; charset=UTF-8\n"
	else:
		title = "arXiv To Wiki"
		if isRunningFromBibTeXURI():
			title = "arXiv To BibTeX"
		elif isRunningFromHTMLURI():
			title = "arXiv to HTML"

		return """Content-type: text/html; charset=UTF-8

<!DOCTYPE html>
<html lang="en">
<head>
<title>""" + title + """</title>
<meta name='generator' content='arXiv to Wiki/BibTeX Converter, 2009-2015 by Sven-S. Porst (ssp-web@earthlingsoft.net).'/>
<meta name='description' content='Create BibTeX, HTML or Wiki markup for papers on the mathematics and physics preprint arXiv.'/>
<style>
* { margin: 0em; padding: 0em; }
body { width: 40em; font-family: Georgia, Times, serif; line-height: 141%; margin:auto; background: #eee;}
.clear { clear:both; }
#title { text-align:center; margin:3em 1em; }
p { margin: 0.5em 0em; }
a { text-decoration: none; color: #00d; }
a:hover { text-decoration: underline; color: #00f; }
a:visited { color: #606; }
a.editlink { color: #b00;}
h1 { font-size: 144%; margin: 0.5em;}
a h1 { color: #000; }
form { display:block; margin: 1em; }
form p { text-align:center; }
form input { font-size: 121%; }
form input.q { width: 60%; margin-bottom: 1em; }
form input.button { position:relative; bottom: 3px; }
h2 { font-size: 121%; margin:2em 0em 1em 0em; position:relative; }
h2:before { content: "\\002767"; position: absolute; width: 1em; left:-1em; font-size: 360%; color: #999; }
h2.error:before { content: "\\002718"; color: #f33; }
ul { padding-left: 2em; }
ul li { margin-bottom: 0.5em; }
.formatpicker { text-align: right; margin:1em 0em -1em 0em; }
.formatpicker ul { display: inline; list-style-type: none; padding: 0px; }
.formatpicker ul li { display: inline; margin-left: 0.5em; font-weight: normal; padding: 0em; }
.format { display: none; }
textarea { width:100%; }
.warning { font-style:italic; text-align:center; margin: 1em 0em; color: #900;}
#foot { font-size: 80%; font-style:italic; text-align: center; margin: 3em 0em 1em 0em; padding-top: 0.2em; border-top: #999 solid 1px; }
</style>
<script>
//<![CDATA[
function showType(type) {
	var myTypes = ["bibtex", "biblatex", "bibitem", "html", "wiki"];
	var myType = (!type || myTypes.indexOf(type) === -1) ? "wiki" : type;
	document.getElementById("formatinput").value = myType;
	for (var i = 0; i < myTypes.length; i++) {
		var name = myTypes[i]
		var linkID = name.concat("-link");
		if (name === myType) {
			document.getElementById(name).style.display = "block";
			document.getElementById(linkID).style.fontWeight = "bold";
		}
		else {
			document.getElementById(name).style.display = "none";
			document.getElementById(linkID).style.fontWeight = "normal";
		}
	}
}
//]]>
</script>
</head>
<body onload="javascript:showType('""" + format + """');">
<div id="page">
<div id="title">
<h1><a href="./">Retrieve arXiv Information</a></h1>
</div>
""" + theForm(format, queryString)




def extraInfo():
	"""
		Returns string with HTML explaining what to enter into the form.
		Displayed beneath the search field on pages without results.
	"""
	return """
<p>
Use the form above to get information for <a href="https://www.arxiv.org/">arXiv</a> submissions
for use in BibTeX, on web pages or in Wikis. You can enter:
</p>
<ul>
<li>
<p>
one or several <em>paper IDs</em> like “1510.01797” or “math/0506203”.
</p>
</li><li>
<p>
your <a href="https://arxiv.org/help/author_identifiers">arXiv <em>author ID</em></a>
looking similar to “grafvbothmer_h_1” to get a list of all your submitted papers.
</p>
</li>
<li>
<p>
your <a href="https://orcid.org">ORCID ID</a> looking similar to “0000-0003-0136-444X”
which you should register with your arXiv-account.
</p>
</li>
</ul>
"""



def pageFoot():
	"""
		Returns string with HTML for the bottom of the page.
	"""
	return """<div id="foot">
	Data from <a href="https://arxiv.org/help/api/index">arXiv API</a>
	· Site by <a href="https://earthlingsoft.net/ssp">Sven-S. Porst</a>
	· <a href="https://github.com/ssp/arXivToWiki/issues">Feedback</a>
</div>
</div>
</body>
</html>
"""




def htmlMarkup(items, type):
	"""
		Input: items - List of publication dictionaries.
		       type  - "Preprint" or "Published".
		Output: Array of strings containing HTML markup with a heading and a textarea full of bibliographic information in HTML markup.
	"""
	markup = []
	if len(items) > 0:

		htmlMarkup = ["<ul>\n"]
		for item in items:
			htmlMarkup += ["<li>\n", escapeHTML(basicMarkupForHTMLEditing(item)), "\n</li>"]
		htmlMarkup += ["\n</ul>"]
		factor = 4
		if type == "Published":
			factor = 5
		markup = ["<textarea class='htmlinfo' cols='70' rows='", str( factor * len(items) + 2), "'>\n"] + htmlMarkup +  ["</textarea>\n"]
	return markup




def basicMarkupForHTMLEditing(myDict):
	"""
		Input: myDict - dictionary with publication data.
		Output: String with HTML markup for publication data.
	"""
	authors = myDict["authors"]
	htmlauthors = []
	for author in authors:
		htmlauthors += [author]
	output = [", ".join(htmlauthors), ': “',  myDict["title"], '”, ', myDict["year"]]
	if myDict["journal"] != None:
		output += [", ", myDict["journal"]]
	output += ["; <a href='",  myDict["link"], "'>arXiv:", myDict["ID"], "</a>."]
	if myDict["DOI"] != None and len(myDict["DOI"]) > 0:
		dois = []
		for DOI in myDict["DOI"]:
			dois += ["<a href='https://dx.doi.org/" + DOI + "'>" + DOI + "</a>"]
		output += [" DOI: ", ", ".join(dois), "."]

	return "".join(output)




def wikiMarkup(items, type):
	"""
		Input: items - List of publication dictionaries.
		       type  - "Preprint" or "Publication".
		Output: Array of strings containing HTML markup with a heading and a textarea full of bibliographic information in Wiki markup.
	"""
	markup = []
	if len(items) > 0:

		wikiMarkup = []
		htmlMarkup = []
		for item in items:
			wikiMarkup += [markupForWikiItem(item), "\n\n"]
			htmlMarkup += [basicMarkupForHTMLEditing(item)]

		wikiMarkup[-1] = wikiMarkup[-1].strip("\n")
		factor = 3
		if type == "Published":
			factor = 4
		markup = ["<p>Preview:</p>\n", "<ul><li>" , "\n</li><li>".join(htmlMarkup), "</li></ul>\n", "<p class='clear'>For copy and pasting to a Wiki:</p>\n", "<textarea class='wikiinfo' cols='70' rows='", str( factor * len(items)), "'>\n"] + wikiMarkup +  ["</textarea>\n"]
	return markup




def markupForWikiItem(myDict):
	"""
		Input: dictionary with publication data.
		Output: Wiki markup for publication data.
	"""
	authors = myDict["authors"]
	wikiauthors = []
	for author in authors:
		wikiauthors += [author]

	wikioutput = ["* ", ", ".join(wikiauthors), ': “', myDict["title"], '”, ', myDict["year"]]
	if myDict["journal"] != None:
		wikioutput += [", ", myDict["journal"]]
	wikioutput += ["; [", myDict["link"], " arXiv:", myDict["ID"], "]."]
	if myDict["DOI"] != None and len(myDict["DOI"]) > 0 :
		dois = []
		for DOI in myDict["DOI"]:
			dois += ["[https://dx.doi.org/" + DOI + " " + DOI + "]"]
		wikioutput += [" DOI: ", ", ".join(dois) , "."]
	result = "".join(wikioutput)
	result = re.sub(r"\s+", r" ", result)
	return result




def bibTeXMarkup(items, format):
	"""
		Input: List of publication dictionaries.
		Output: Array of strings containing HTML markup with a heading and a textarea full of BibTeX records.
	"""
	markup = []
	if len(items) > 0:
		linecount = 0
		itemmarkup = []
		for item in items:
			bibtexmarkup = markupForBibTeXItem(item, format)
			itemmarkup += [bibtexmarkup]
			linecount += len(bibtexmarkup.split('\n'))
		markup += ["<textarea class='wikiinfo' cols='70' rows='", str(linecount + len(items) - 1), "'>\n", "\n\n".join(itemmarkup), "</textarea>\n"]
	return markup



def markupForBibTeXItem(myDict, format):
	"""
		Input: dictionary with publication data.
		Output: BibTeX record for the preprint.
	"""
	bibTeXID = myDict["ID"]
	bibTeXAuthors = " and ".join(myDict["authors"])
	bibTeXTitle = myDict["title"]
	bibTeXYear = myDict["year"]

	hasDOI = myDict["DOI"] != None and len(myDict["DOI"]) > 0
	hasJournal = myDict["journal"] != None
	isPublished = hasJournal or hasDOI

	publicationType = ("@online" if format == "biblatex" else "@misc") if not isPublished else "@article"

	eprintPrefix = "" if format == "biblatex" else "arXiv:"
	bibTeXEntry = [publicationType, "{", bibTeXID, ",\nAuthor = {", bibTeXAuthors, "},\nTitle = {", bibTeXTitle, "},\nYear = {", bibTeXYear, "},\nEprint = {", eprintPrefix, bibTeXID, "},\n"]
	if format == "biblatex":
		bibTeXEntry += ["Eprinttype = {arXiv},\n"]
	if hasJournal:
		bibTeXEntry += ["Howpublished = {", myDict["journal"], "},\n"]
	if hasDOI:
		bibTeXEntry += ["Doi = {", " ".join(myDict["DOI"]), "},\n"]
	bibTeXEntry += ["}"]
	result = "".join(bibTeXEntry)
	return result



def bibItemMarkup(items):
	"""
		Input: List of publication dictionaries.
		Output: Array of strings containing HTML markup with a heading and a textarea full of \bibitem commands.
	"""
	markup = []
	if len(items) > 0:
		linecount = 0
		itemmarkup = []
		for item in items:
			bibItem = markupForBibItem(item)
			itemmarkup += [bibItem]
			linecount += len(bibItem.split('\n'))
		markup = ["<p>Simple-minded \\bibitems:</p>\n", "<textarea class='wikiinfo' cols='70' rows='", str(linecount + 3), "'>\\begin{thebibliography}\n\n", "\n".join(itemmarkup), "\n\end{thebibliography}</textarea>\n"]
	return markup


def markupForBibItem(myDict):
	"""
		Input: dictionary with publication data.
		Output: LaTeX \bibitem command for the publication
	"""
	bibTeXID = myDict["ID"]
	authors = myDict["authors"]
	authorString = ""
	if len(authors) == 1:
		authorString = authors[0]
	elif len(authors) > 1:
		firstAuthors = authors[:-1]
		lastAuthor = authors[-1]
		authorString = ", ".join(firstAuthors) + " and " + lastAuthor

	title = myDict["title"]
	year = myDict["year"]

	bibItemCommand = ["\\bibitem{", bibTeXID, "}\n", authorString, ".\n\\newblock ", title, ", ", year]
	if myDict["journal"] != None:
		bibItemCommand += [",\n\\newblock ", myDict["journal"]]
	bibItemCommand += [";\n\\newblock arXiv:", bibTeXID, "."]
	if myDict["DOI"] != None and len(myDict["DOI"]) > 0:
		bibItemCommand += ["\n\\newblock DOI: ", " ".join(myDict["DOI"]), "."]
	result = "".join(bibItemCommand) + "\n"
	return result





def errorMarkup(errorText):
	"""
		Return markup for the error text received.
	"""
	return """<h2 class="error">No results</h2>
<p>""" + errorText + """</p>
<p>If you think you entered a valid arXiv ID and you keep getting this error message, please accept our apologies and <a href="https://github.com/ssp/arXivToWiki/issues">let me know</a>.</p>
"""



def isRunningFromBibTeXURI():
	return isInRequestURI("bibtex")

def isRunningFromHTMLURI():
	return isInRequestURI("html")

def isInRequestURI(string):
	return isInEnvironment("REQUEST_URI", string) or isInEnvironment("HTTP_HOST", string)

def isInEnvironment(fieldName, string):
	if fieldName in os.environ:
		if os.environ[fieldName].lower().find(string) != -1:
			return True
	return False


IDCleanerRE = re.compile(r"[^0-9]*([0-9]*)\.?([0-9]*)")

def comparePaperDictionaries (firstPaper, secondPaper):
	"""
		Compare paper dictionaries.
		Earlier years are smaller.
		Smaller IDs within a year are smaller.
	"""
	comparisonResult = 0
	if firstPaper.has_key("year") and firstPaper.has_key("ID") and secondPaper.has_key("year") and secondPaper.has_key("ID"):
		comparisonResult = cmp(firstPaper["year"], secondPaper["year"])

		if comparisonResult == 0:
			cleanedFirstID = int(IDCleanerRE.sub(r"\1\2", firstPaper["ID"]))
			cleanedSecondID = int(IDCleanerRE.sub(r"\1\2", secondPaper["ID"]))
			comparisonResult = cmp(cleanedFirstID, cleanedSecondID)

	return comparisonResult



def processCgi(form):
	queryString = ""
	papers = []
	personID = ""
	if form.has_key("q"):
		queryString = form["q"].value
		papers = list(set(re.sub(r",", r" ", queryString).split()))
		""" 
			for a single entry matching a regex we have an arXiv or ORCID autor ID
			see https://arxiv.org/help/author_identifiers
		"""
		if len(papers) == 1:
			arxivAuthorIDRegex = r"([a-z]*_[a-z]_[0-9]*)"
			orcidIDRegex = r"((https://orcid.org/)?\d\d\d\d-\d\d\d\d-\d\d\d\d-\d\d\d[0-9X])"
			authorMatch = re.search(arxivAuthorIDRegex + "|" + orcidIDRegex, papers[0])
			if authorMatch != None:
				personID = authorMatch.string[authorMatch.start():authorMatch.end()]
			urlParts = urlparse(queryString)
			if urlParts.netloc == "arxiv.org":
				fromUriPath = extractPapersFromArXivUriPath(urlParts.path)
				if fromUriPath != None:
					papers = [fromUriPath]

	outputformat = "html"
	if form.has_key("outputformat"):
		of = form["outputformat"].value
		if of in ["html", "raw"]:
			outputformat = of

	format = "wiki"
	if isRunningFromBibTeXURI():
		format = "bibtex"
	elif isRunningFromHTMLURI():
		format = "html"
	if form.has_key("format"):
		f = form["format"].value
		if f in ["wiki", "bibtex", "biblatex", "bibitem", "html"]:
			format = f

	printAll(pageHead(queryString, format, outputformat))

	if form.has_key("q"):
		failedIDs = []
		if personID == "":
			arXivIDs = []
			for paperID in papers:
				processedID = prepareArXivID(paperID)
				if processedID != None:
					arXivIDs += [processedID]
				else:
					failedIDs += [paperID]
			arXivURL = "https://export.arxiv.org/api/query?id_list=" + ",".join(arXivIDs) + "&max_results=" + str(maxpapers)
		else:
			arXivURL = "https://arxiv.org/a/" + personID + ".atom"

		download = urllib.urlopen(arXivURL)
		download.encoding = "UTF-8"
		downloadedData = download.read()
		if downloadedData == None:
			printHtml(extraInfo(), outputformat)
			printHtml(errorMarkup("The arXiv data could not be retrieved."), outputformat)
		else:
			publications = []
			feed = xml.etree.ElementTree.fromstring(downloadedData)
			output = []

			"""	Check for an error by looking at the title of the first paper: errors are marked by 'Error', empty feeds don't have a title """
			firstTitle = feed.find("{http://www.w3.org/2005/Atom}entry/{http://www.w3.org/2005/Atom}title")
			if firstTitle == None or firstTitle.text == "Error":
				lookupSubject = "paper ID"
				if personID == "" and len(papers) > 1:
					lookupSubject = "paper IDs"
				elif personID != "":
					lookupSubject = "author ID"

				printHtml(extraInfo(), outputformat)
				printHtml(errorMarkup("The arXiv did not return any results for the " + lookupSubject + " you entered. Any chance there may be a typo in there?"), outputformat)
			else:
				""" We got data and no error: Process it. """
				papersiterator = feed.getiterator("{http://www.w3.org/2005/Atom}entry")
				for paper in papersiterator:
					titleElement = paper.find("{http://www.w3.org/2005/Atom}title")
					if titleElement == None:
						continue
					theTitle = re.sub(r"\s*\n\s*", r" ", titleElement.text)
					authors = paper.getiterator("{http://www.w3.org/2005/Atom}author")
					theAuthors = []
					for author in authors:
						name = author.find("{http://www.w3.org/2005/Atom}name").text
						theAuthors += [name]
					theAbstract = paper.find("{http://www.w3.org/2005/Atom}summary").text.strip()

					links = paper.getiterator("{http://www.w3.org/2005/Atom}link")
					thePDF = ""
					theLink = ""
					for link in links:
						attributes = link.attrib
						if attributes.has_key("href"):
							linktarget = attributes["href"]
							linktype = attributes["type"] if attributes.has_key("type") else None
							linktitle = attributes["title"] if attributes.has_key("title") else None
						if linktype == "application/pdf":
							thePDF = linktarget
						elif linktype == "text/html":
							theLink = linktarget
					splitLink = theLink.split("/abs/")
					theID = splitLink[-1].split('v')[0]
					theLink = splitLink[0] + "/abs/" + theID

					theYear = paper.find("{http://www.w3.org/2005/Atom}published").text.split('-')[0]

					theDOIs = []
					DOIs = paper.getiterator("{http://arxiv.org/schemas/atom}doi")
					for DOI in DOIs:
						theDOIs += [DOI.text]

					journal = paper.find("{http://arxiv.org/schemas/atom}journal_ref")
					theJournal = None
					if journal != None:
						theJournal = journal.text

					publicationDict = dict({
						"ID": theID,
						"authors": theAuthors,
						"title": theTitle,
						"abstract": theAbstract,
						"year": theYear,
						"PDF": thePDF,
						"link": theLink,
						"DOI": theDOIs,
						"journal": theJournal})
					publications += [publicationDict]

				preprintIDs = []
				preprints = []
				publishedIDs = []
				published = []

				publications.sort(comparePaperDictionaries, None, True)

				for publication in publications:
					if publication["journal"] != None:
						published += [publication]
						publishedIDs += [publication["ID"]]
					else:
						preprints += [publication]
						preprintIDs += [publication["ID"]]

				output += ["<div class='formatpicker'>Format:<ul class='outputtypes'>\n",
				"""<li><a href='javascript:showType("bibtex");' id='bibtex-link'>BibTeX</a></li>\n""",
				"""<li><a href='javascript:showType("biblatex");' id='biblatex-link'>BibLaTeX</a></li>\n""",
				"""<li><a href='javascript:showType("bibitem");' id='bibitem-link'>\\bibitem</a></li>\n""",
				"""<li><a href='javascript:showType("html");' id='html-link'>HTML</a></li>\n""",
				"""<li><a href='javascript:showType("wiki");' id='wiki-link'>Wiki</a></li>\n""",
				"</ul>\n</div>\n"]

				if len(papers) >= maxpapers:
					output += ["<div class='warning'>We can only process " + str(maxpapers) + " paper IDs at a time. " + str(len(papers) - maxpapers) + " of the IDs you entered were ignored.</div>"]

				journalrefnote = """<p><em>Please <a class="editlink" href="https://arxiv.org/user/" title="Go to arXiv user page where you can edit the information stored for your papers.">add the journal reference and <abbr title="Document Object Identifier">DOI</abbr> for your papers as soon as they are published</a>.</em></p>"""

				output += ["<div id='bibtex'>\n"]
				if len(preprints) > 0:
					output += ["<h2>Preprints:</h2>\n", journalrefnote]
					output += bibTeXMarkup(preprints, "bibtex")
				if len(published) > 0:
					output += ["<h2>Published:</h2>\n"]
					output += ["""<p>These BibTeX records are based on arXiv information only. You may prefer getting the more detailed records provided by <a href="https://mathscinet.ams.org/mathscinet/">MathSciNet</a> instead.</p>\n"""]
					output += bibTeXMarkup(published, "bibtex")
				output += ["</div>\n"]

				output += ["<div id='biblatex'>\n"]
				if len(preprints) > 0:
					output += ["<h2>Preprints:</h2>\n", journalrefnote]
					output += bibTeXMarkup(preprints, "biblatex")
				if len(published) > 0:
					output += ["<h2>Published:</h2>\n"]
					output += ["""<p>These BibLaTeX records are based on arXiv information only. You may prefer getting the more detailed records provided by <a href="https://mathscinet.ams.org/mathscinet/">MathSciNet</a> instead.</p>\n"""]
					output += bibTeXMarkup(published, "biblatex")
				output += ["</div>\n"]

				output += ["<div id='bibitem'>\n"]
				if len(preprints) > 0:
					output += ["<h2>Preprints:</h2>\n", journalrefnote]
					output += bibItemMarkup(preprints)
				if len(published) > 0:
					output += ["<h2>Published:</h2>\n"]
					output += bibItemMarkup(published)
				output += ["</div>\n"]

				output += ["<div id='html'>\n"]
				if len(preprints) > 0:
					output += ["<h2>Preprints:</h2>\n", journalrefnote]
					output += htmlMarkup(preprints, "Preprint")
				if len(published) > 0:
					output += ["<h2>Published:</h2>\n"]
					output += htmlMarkup(published, "Published")
				output += ["</div>\n"]

				output += ["<div id='wiki'>\n"]
				if len(preprints) > 0:
					output += ["<h2>Preprints:</h2>\n", journalrefnote]
					output += wikiMarkup(preprints, "Preprint")
				if len(published) > 0:
					output += ["<h2>Published:</h2>\n"]
					output += wikiMarkup(published, "Published")
				output += ["</div>\n"]


			if len(failedIDs) > 0:
				if len(failedIDs) == 1:
					printHtml("""<div class="warning">No paper with the ID “""" + failedIDs[0] + """” could be found on the arXiv.</div>\n""", outputformat)
				else:
					printHtml("""<div class="warning">The following paper IDs could not be found on the arXiv: """ + ", ".join(failedIDs) + """.</div>\n""", outputformat)

			printHtml("".join(output), outputformat)
			printPublicationsRaw(publications, format, outputformat)
	else:
		printHtml(extraInfo(), outputformat)

	printHtml(pageFoot(), outputformat)


"""
	MAIN SCRIPT *****************************************************************
"""
form = cgi.FieldStorage()
processCgi(form)
