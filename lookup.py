#!/usr/bin/python2.5 
#coding=utf-8
"""
arXivToWiki v4
©2009-2010 Sven-S. Porst / earthlingsoft <ssp-web@earthlingsoft.net>
Das Skript benötigt Python 2.5.
"""

import cgi
import re
import urllib
from xml.etree import ElementTree
import xml.etree
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

maxpapers = 100



"""
	Load people information.
"""
execfile("people.py")




trailingRE = re.compile(r"(.*)v[0-9]*$")
newStyleRE = re.compile(r"\d\d\d\d\.?\d\d\d\d$")
sevenDigitsRE = re.compile(r"\d\d\d\d\d\d\d$")
oldStyleIDRE = re.compile(r"[a-z-]*/\d\d\d\d\d\d\d$")

def prepareArXivID(ID):
	"""
		first, strip potentially trailing version numbers like v4
		0909.1234-style ID => return unchanged
		09091234-style ID => return 0909.1234
		0606123-style ID => return math/0606123
		non-math/0606123-style ID => return unchanged
		anything else => return None
	"""
	myID = ID.strip()
	myID = trailingRE.sub(r"\1", myID)
	if  newStyleRE.match(myID) != None:
		""" An 8 digit number (new-style): insert dot in the middle in case it's not there already.	"""
		if re.match(r"\.", myID) == None:
			myID = re.sub(r"(\d\d\d\d)(\d\d\d\d)$", r"\1.\2", myID)
	elif sevenDigitsRE.match(myID) != None:
		""" Just seven digits: prepend math/ """
		myID = "math/" + myID
	elif oldStyleIDRE.match(myID) != None:
		myID = myID
	else:
		myID = None
	
	return myID





ampRegexp = re.compile(r"&")
ltRegexp = re.compile(r"<")
gtRegexp = re.compile(r">")
aposRegexp = re.compile(r"'")

def escapeHTML(inputString):
	"""
		Input: string
		Output: input string with < > & ' replaced by their HTML character entities
	"""
	escapedString = ampRegexp.sub('&amp;', inputString)
	escapedString = ltRegexp.sub('&lt;', escapedString)
	escapedString = gtRegexp.sub('&gt;', escapedString)
	escapedString = aposRegexp.sub('&#39;', escapedString)

	return escapedString




def theForm():
	"""
		Returns string with HTML for the search form.
		The form is pre-filled with the current query string.
	"""
	global format
	return """
<form method="get" action="./">
<p>
<input type="text" name="q" class="q" autofocus placeholder="09081234 OR courant_r_1" value='""" + escapeHTML(queryString) + """'>
<input type="hidden" name="format" id="formatinput" value='""" + format + """'>
<input type="submit" class="button" value="Retrieve Information">
</p>
</form>
"""



def pageHead():
	"""
		Returns string with HTML for the http header and the top of the HTML markup including CSS and JavaScript.
	"""
	global format
	title = "arXiv To Wiki"
	if runningFromBibTeXPath() == True:
		title ="arXiv To BibTeX"

	return """Content-type: text/html; charset=UTF-8

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<title>""" + title + """</title>
<meta name='generator' content='arXiv to Wiki/BibTeX Converter, 2009-2010 by Sven-S. Porst (ssp-web@earthlingsoft.net).'>
<meta name='description' content='A tool to create BibTeX, HTML or Wiki markup for papers on the mathematics and physics preprint arXiv.'>
<style type="text/css">
* { margin: 0em; padding: 0em; }
body { width: 40em; font-family: Georgia, Times, serif; line-height: 141%; margin:auto; background: #eee;}
.clear { clear:both; }
#title { text-align:center; margin:2em 1em; }
p { margin: 0.5em 0em; }
a { text-decoration: none; color: #00d; }
a:hover { text-decoration: underline; color: #00f; }
a:visited { color: #606; }
a.editlink { color: #b00;}
h1 { font-size: 144%; margin: 0.5em;}
a h1 { color: #000; }
p.crcg { font-style: italic; }
form { display:block; margin: 1em; }
form p { text-align:center; } 
form input { font-size: 121%; }
form input.q { width: 60%; margin-bottom: 6px; }
form input.button { position:relative; bottom: 3px; }
h2 { font-size: 121%; margin:2em 0em 1em 0em; position:relative; }
h2:before { content: "\\002767"; position: absolute; width: 1em; left:-1em; font-size: 360%; color: #999; }
h2.error:before { content: "\\002718"; color: #f33; }
ul { padding-left: 2em; }
ul li { margin-bottom: 0.5em; } 
.formatpicker { text-align: right; margin:1em 0em -1em 0em; }
.formatpicker ul { display: inline; list-style-type: none; padding: 0px; }
.formatpicker ul li { display: inline; margin-left: 0.5em; font-width: normal; padding: 0em; }
.format { display: none; }
textarea { width:100%; }
.warning { text-style: italic; font-style:italic; text-align:center; margin: 1em 0em; color: #900;}
#foot { font-style:italic; text-align: center; margin: 3em 0em 1em 0em; border-top: #999 solid 1px; }
</style>
<script type="text/javascript">
function showType(type) { 
var myType = type;
if (type != "wiki" && type != "bibtex" && type != "bibitem" && type != "html") { myType = "wiki"; }
var myTypes = new Array("wiki", "bibtex", "bibitem", "html");
document.getElementById("formatinput").value = myType;
var name;
for (var i = 0; i < myTypes.length; i++) {
	var name = myTypes[i]
	var linkID = name.concat("-link");
	if (name == myType) { 
		document.getElementById(name).style.display = "block";
		document.getElementById(linkID).style.fontWeight = "bold";
	}
	else {
		document.getElementById(name).style.display = "none";
		document.getElementById(linkID).style.fontWeight = "normal";		
	}
}
}
</script>
</head>
<body onload="javascript:showType('""" + format + """');">
<div id="page">
<div id="title">
<h1><a href="./">Retrieve arXiv Information</a></h1>
<p class="crcg">
<a href="http://www.crcg.de/">Courant Research Centre ,Higher Order Structures in Mathematics‘</a>
</p>
</div>
""" + theForm() 




def extraInfo():
	"""
		Returns string with HTML explaining what to enter into the form.
		Displayed beneath the search field on pages without results.
	"""
	return """
<p>
Use the form above to get information from your <a href="http://www.arxiv.org/">arXiv</a> submissions for use on the Courant Centre <a href="http://www.crcg.de/wiki/Publications">publications wiki page</a>. You can enter:
</p>
<ul>
<li>
<p>
one or several <em>paper IDs</em> like “0909.4913” or “0506203”.
</p>
</li><li>
<p>
your arXiv <em><a href="http://arxiv.org/help/author_identifiers">author ID</a></em> looking similar to “courant_r_1” to get a list of all your submitted papers. 
</p><p>
In case you do not have an arXiv author ID yet, go and <a href="http://arxiv.org/set_author_id">get one now</a>. To ensure completeness of the list created from that, please make sure that your co-authors correctly associated the paper to your arXiv account after submission.
</p><p>
Readymade links for <acronym title="Courant Research Centre Göttingen">CRCG</acronym> members: 
""" + memberLinks() + """.
</p><p>
Your name is missing in that list? <a href="http://arxiv.org/set_author_id">Get yourself an arXiv ID</a> and <a href="mailto:arXivToWiki@crcg.de?subject=My%20arXiv%20author%20ID">let us know</a>.
</p>
</ul>
<p>
"""



def memberLinks():
	"""
		Returns string with HTML containing links to look up all people with known arXiv author IDs.
	"""

	uniquemembers = dict()
	for person in people.iteritems():
		personName = person[0]
		personData = person[1]
		if personData.has_key(arXivID) and personData.has_key(default) and personData.has_key(crcg):
			personID = personData[arXivID]
			uniquemembers[personID] = personName

	links = []
	IDs = uniquemembers.keys()
	IDs.sort()
	for memberID in IDs:
		links += ["<a href='./?q=" + memberID + "'>" + uniquemembers[memberID] + "</a>"]
		
	return ", ".join(links)



def pageFoot():
	"""
		Returns string with HTML for the bottom of the page.
	"""
	foot = ["""<div id="foot">
<a href="http://www.crcg.de/">Courant Research Centre ,Higher Order Structures in Mathematics‘</a><br>
<a href="http://www.uni-goettingen.de/en/20693.html">Mathematisches Institut</a>,
<a href="http://www.uni-goettingen.de/en/1.html">Georg-August-Universität Göttingen</a><br>"""]
	if runningFromBibTeXPath() == True:
		foot += ["""Data provided by the <a href="http://arxiv.org/help/api/index">arXiv API</a> · Site made by <a href="http://earthlingsoft.net/ssp/design/">Sven-S. Porst</a><br>"""]
	foot += ["""<a href="http://www.besserweb.de/website.php?id=42">Leave a Comment</a>
</div>	
</div>
</body>
</html>
"""]
	return "".join(foot)




def htmlMarkup(items, type):
	"""
		Input: items - List of publication dictionaries.
		       type  - "Preprint" or "Publication".
		Output: Array of strings containing HTML markup with a heading and a textarea full of bibliographic information in HTML markup.
	"""
	markup = []
	if len(items) > 0:

		htmlMarkup = ["<ul>\n"]
		for item in items:
			htmlMarkup += ["<li>\n", escapeHTML(basicMarkupForHTMLEditing(item, type)), "\n</li>"]
		htmlMarkup += ["\n</ul>"]
		factor = 4
		if type == "Published":
			factor = 5
		markup = ["<textarea class='htmlinfo' cols='70' rows='", str( factor * len(items) + 2), "'>\n"] + htmlMarkup +  ["</textarea>\n"]
	return markup




def basicMarkupForHTMLEditing(myDict, type):
	"""
		Input: myDict - dictionary with publication data.
		       type   - "Preprint" or "Publication".
		Output: String with HTML markup for publication data.
	"""
	authors = myDict["authors"]
	htmlauthors = []
	for author in authors:
		if people.has_key(author):
			record = people[author]
			if record.has_key(URL):
				address = record[URL]
				htmlauthors += ["<a href='" + address + "'>" + author + "</a>"]
			else:
				htmlauthors += [author]
		else:
			htmlauthors += [author]
	output = [", ".join(htmlauthors), ': “',  myDict["title"], '”, ', myDict["year"]]
	if myDict["journal"] != None:
		output += [", ", myDict["journal"]]
	output += ["; <a href='",  myDict["link"], "'>arXiv:", myDict["ID"], "</a>."]
	if myDict["DOI"] != None:
		output += [" DOI: <a href='http://dx.doi.org/", myDict["DOI"], "'>", myDict["DOI"], "</a>."]
	
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
			htmlMarkup += [basicMarkupForHTMLEditing(item, type)]
		
		wikiMarkup[-1] = wikiMarkup[-1].strip("\n")
		factor = 3
		if type == "Published":
			factor = 4
		markup = ["<p>Preview:</p>\n", "<ul><li>" , "\n</li><li>".join(htmlMarkup), "</ul>\n", "<p class='clear'>Copy and paste the text below for the wiki:</p>\n", "<textarea class='wikiinfo' cols='70' rows='", str( factor * len(items)), "'>\n"] + wikiMarkup +  ["</textarea>\n"]
	return markup
	
	


wikiAddressRE = re.compile(r"http://www.crcg.de/wiki/(User:.*)")

def markupForWikiItem(myDict):
	"""
		Input: dictionary with publication data.
		Output: Wiki markup for publication data.
	"""
	authors = myDict["authors"]
	wikiauthors = []
	for author in authors:
		if people.has_key(author):
			record = people[author]
			if record.has_key(URL):
				address = record[URL]
				match = wikiAddressRE.match(address)
				if match != None:
					address = match.group(1)
					wikiauthors += ["[[" + address + "|" + author + "]]"]
				else:
					wikiauthors += ["[" + address + " " + author + "]"]
			else:
				wikiauthors += [author]
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




def bibTeXMarkup(items):
	"""
		Input: List of publication dictionaries.
		Output: Array of strings containing HTML markup with a heading and a textarea full of BibTeX records.
	"""
	markup = []
	if len(items) > 0:
		linecount = 0
		itemmarkup = []
		for item in items:
			bibtexmarkup = markupForBibTeXItem(item)
			itemmarkup += [bibtexmarkup]
			linecount += len(bibtexmarkup.split('\n'))
		markup += ["<textarea class='wikiinfo' cols='70' rows='", str(linecount + len(items) - 1), "'>\n", "\n\n".join(itemmarkup), "</textarea>\n"]
	return markup
	


def markupForBibTeXItem(myDict):
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
	result = "".join(bibItemCommand) + "\n"
	return result





def errorMarkup(errorText):
	"""
		Return markup for the error text received.
	"""
	return """<h2 class="error">No results</h2>
<p>""" + errorText + """</p>
<p>If you think you entered a valid arXiv ID and you keep getting this error message, please accept our apologies and <a href="http://www.besserweb.de/website.php?id=42">let us know about it</a>.</p>
"""



def runningFromBibTeXPath():
	result = False;
	if "REQUEST_URI" in os.environ:
		if os.environ["REQUEST_URI"].lower().find("bibtex") != -1:
			result = True
	return result





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






"""
	MAIN SCRIPT *****************************************************************
"""

form = cgi.FieldStorage()
queryString = ""
papers = []
personID = ""
if form.has_key("q"):
	queryString = form["q"].value
	papers = list(set(re.sub(r",", r" ", queryString).split()))
	""" for a single entry matching a regex we have an autor ID"""
	if len(papers) == 1:
		match = re.search(r"[a-z]*_[a-z]_[0-9]*", papers[0])
		if match != None:
			personID = match.string[match.start():match.end()]
format = "wiki"
if runningFromBibTeXPath() == True:
	format = "bibtex"
if form.has_key("format"):
	f = form["format"].value
	if f in ["wiki", "bibtex", "bibitem", "html"]:
		format = f
print pageHead()

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
		arXivURL = "http://export.arxiv.org/api/query?id_list=" + ",".join(arXivIDs) + "&max_results=" + str(maxpapers)
	else:
		arXivURL = "http://arxiv.org/a/" + personID + ".atom"
		
#	print arXivURL
	download = urllib.urlopen(arXivURL)
	download.encoding = "UTF-8"
	downloadedData = download.read()
	if downloadedData == None:
		print extraInfo()
		print errorMarkup("The arXiv data could not be retrieved.")
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
			
			print extraInfo()
			print errorMarkup("The arXiv did not return any results for the " + lookupSubject + " you entered. Any chance there may be a typo in there?")
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
			"""<li><a href='javascript:showType("wiki");' id='wiki-link' href='#'>Wiki</a></li>\n""", 
			"""<li><a href='javascript:showType("html");' id='html-link' href='#'>HTML</a></li>\n""", 
			"""<li><a onclick='javascript:showType("bibtex");' id='bibtex-link' href='#'>BibTeX</a></li>\n""", 
			"""<li><a href='javascript:showType("bibitem");' id='bibitem-link' href='#'>\\bibitem</a></li>\n""", 
			"</ul>\n</div>\n"]

			if len(papers) >= maxpapers:
				output += ["<div class='warning'>We can only process " + str(maxpapers) + " paper IDs at a time. " + str(len(papers) - maxpapers) + " of the IDs you entered were ignored.</div>"]

			journalrefnote = """<p><em>Please <a class="editlink" href="http://arxiv.org/user/" title="Go to arXiv user page where you can edit the information stored for your papers.">add the journal reference and <acronym title="Document Object Identifier">DOI</acronym> for your papers as soon as they are published</a>.</em></p>"""

			output += ["<div id='wiki'>\n"]
			if len(preprints) > 0:
				output += ["<h2>Preprints:</h2>\n", journalrefnote]
				output += wikiMarkup(preprints, "Preprint")
			if len(published) > 0:
				output += ["<h2>Published:</h2>\n"]
				output += wikiMarkup(published, "Published")
			output += ["</div>\n"]

			output += ["<div id='html'>\n"]
			if len(preprints) > 0:
				output += ["<h2>Preprints:</h2>\n", journalrefnote]
				output += htmlMarkup(preprints, "Preprint")
			if len(published) > 0:
				output += ["<h2>Published:</h2>\n"]
				output += htmlMarkup(published, "Published")
			output += ["</div>\n"]
	
			output += ["<div id='bibtex'>\n"]
			if len(preprints) > 0:
				output += ["<h2>Preprints:</h2>\n", journalrefnote]
				output += bibTeXMarkup(preprints)
			if len(published) > 0:
				output += ["<h2>Published:</h2>\n"]
				output += ["""<p>These BibTeX records are based on arXiv information only. You may prefer getting the more detailed records provided by <a href="http://ams.org/mathscinet/">MathSciNet</a> instead.</p>\n"""]
				output += bibTeXMarkup(published)
			output += ["</div>\n"]

			output += ["<div id='bibitem'>\n"]
			if len(preprints) > 0:
				output += ["<h2>Preprints:</h2>\n", journalrefnote]
				output += bibItemMarkup(preprints)
			if len(published) > 0:
				output += ["<h2>Published:</h2>\n"]
				output += bibItemMarkup(published)
			output += ["</div>\n"]
			
		if len(failedIDs) > 0:
			if len(failedIDs) == 1:
				print """<div class="warning">No paper with the ID “""" + failedIDs[0] + """” could be found on the arXiv.</div>\n""" 
			else:
				print """<div class="warning">The following paper IDs could not be found on the arXiv: """ + ", ".join(failedIDs) + """.</div>\n"""
			
		print "".join(output)
else:
	print extraInfo()	

print pageFoot()
