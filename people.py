#!/usr/bin/python2.5 
#coding=utf-8
"""
people.py
arXivToWiki v4.1
©2009-2010 Sven-S. Porst / earthlingsoft <ssp-web@earthlingsoft.net>

List of people and their web pages for automatic linking in arXivToWiki.
"""


"""
	Set up table of real names pointing to a dictionary with
		URL     -> full web page URL for the person
		arXivID -> arXiv ID for the person
		default -> key whose existense indicates this is the default entry for the person in question
		crcg	-> indicates that this person is a proper CRCG member and will be explicitly listed as such
		
	Be sure to precede the name string with a u, e.g. u"Carl Müller".
"""

URL = "URL"
arXivID = "arXivID"
default = "default"
crcg = "crcg"

people = dict({
u"Dorothea Bahns":                   dict(URL="http://www.uni-math.gwdg.de/bahns/", arXivID="bahns_d_1", default="", crcg=""),
u"D. Bahns":                         dict(URL="http://www.uni-math.gwdg.de/bahns/", arXivID="bahns_d_1", crcg=""),
u"Laurent Bartholdi":                dict(URL="http://www.uni-math.gwdg.de/laurent/", arXivID="bartholdi_l_1", default="", crcg=""),
u"L. Bartholdi":                     dict(URL="http://www.uni-math.gwdg.de/laurent/", arXivID="bartholdi_l_1", crcg=""),
u"Valentin Blomer":                  dict(URL="http://www.uni-math.gwdg.de/blomer/", default="", crcg=""),
u"Hans-Christian Graf v. Bothmer":   dict(URL="http://www.crcg.de/wiki/User:Bothmer", arXivID="grafvbothmer_h_1", default="", crcg=""),
u"Hans-Christian Graf von Bothmer":  dict(URL="http://www.crcg.de/wiki/User:Bothmer", arXivID="grafvbothmer_h_1", crcg=""),
u"Hans-Christian Bothmer":           dict(URL="http://www.crcg.de/wiki/User:Bothmer", arXivID="grafvbothmer_h_1", crcg=""),
u"Hans-Christian v. Bothmer":        dict(URL="http://www.crcg.de/wiki/User:Bothmer", arXivID="grafvbothmer_h_1", crcg=""),
u"Hans-Christian von Bothmer":       dict(URL="http://www.crcg.de/wiki/User:Bothmer", arXivID="grafvbothmer_h_1", crcg=""),
u"H.-Chr. Graf von Bothmer":         dict(URL="http://www.crcg.de/wiki/User:Bothmer", arXivID="grafvbothmer_h_1", crcg=""),
u"H. -Chr. Graf von Bothmer":        dict(URL="http://www.crcg.de/wiki/User:Bothmer", arXivID="grafvbothmer_h_1", crcg=""),
u"H.-C. Graf v. Bothmer":            dict(URL="http://www.crcg.de/wiki/User:Bothmer", arXivID="grafvbothmer_h_1", crcg=""),
u"Jörg Brüdern":                     dict(default="", crcg=""),
u"Arne Buchholz":                    dict(URL="http://www.crcg.de/wiki/User:Buchholz", default="", crcg=""),
u"Dzmitry Dudko":                    dict(default="", crcg=""),
u"Łukasz Grabowski":                 dict(arXivID="grabowski_l_1", default="", crcg=""),
u"Lukasz Grabowski":                 dict(arXivID="grabowski_l_1", crcg=""),
u"Nils Hansen":                      dict(default="", crcg=""),
u"Bernd Hoffmann":                   dict(default="", crcg=""),
u"Anders Jensen":                    dict(URL="http://www.crcg.de/wiki/User:Jensen", arXivID="jensen_a_1", default ="", crcg=""),
u"Anders N. Jensen":                 dict(URL="http://www.crcg.de/wiki/User:Jensen", crcg=""),
u"A. N. Jensen":                     dict(URL="http://www.crcg.de/wiki/User:Jensen", crcg=""),
u"Anders Nedergaard Jensen":         dict(URL="http://www.crcg.de/wiki/User:Jensen", crcg=""),
u"Alexander Kahle":                  dict(default="", crcg=""),
u"Du Li":                            dict(URL="http://www.crcg.de/wiki/User:Lidu", default="", crcg=""),
u"Hannah Markwig":                   dict(URL="http://www.crcg.de/wiki/User:Hannah", arXivID="markwig_h_1", default="", crcg=""),
u"H. Markwig":                       dict(URL="http://www.crcg.de/wiki/User:Hannah", arXivID="markwig_h_1", crcg=""),
u"Thomas Markwig": 	                 dict(URL="http://www.mathematik.uni-kl.de/~keilen/de/index.html", default="", crcg=""),
u"Thomas Keilen": 	                 dict(URL="http://www.mathematik.uni-kl.de/~keilen/de/index.html", default="", crcg=""),
u"Holger Knuth":                     dict(default="", crcg=""),
u"Jakob Kröker":                     dict(URL="http://www.crcg.de/wiki/User:Kroeker", default="", crcg=""),
u"Ralf Meyer":                       dict(URL="http://www.uni-math.gwdg.de/rameyer/", arXivID="meyer_r_1", default="", crcg=""),
u"Preda Mihăilescu":                 dict(URL="http://www.uni-math.gwdg.de/preda/", default="", crcg=""),
u"Preda Mihailescu":                 dict(URL="http://www.uni-math.gwdg.de/preda/", crcg=""),
u"Patrick Neumann":                  dict(default="", crcg=""),
u"P. Neumann":   	                 dict(crcg=""),
u"Samuel J. Patterson":              dict(URL="http://www.uni-math.gwdg.de/sjp/", default="", crcg=""),
u"Alexander Pavlov":                 dict(default="", crcg=""),
u"Alexander A. Pavlov":              dict(crcg=""),
u"A. A. Pavlov":                     dict(crcg=""),
u"Ulrich Pennig":                    dict(default="", crcg=""),
u"U. Pennig":                        dict(crcg=""),
u"Gabriele Ranieri":                 dict(default="", crcg=""),
u"Karl-Henning Rehren":              dict(URL="http://www.theorie.physik.uni-goe.de/~rehren/", arXivID="rehren_k_1", default="", crcg=""),
u"K. -H. Rehren":                    dict(URL="http://www.theorie.physik.uni-goe.de/~rehren/", arXivID="rehren_k_1", crcg=""),
u"Thomas Schick":                    dict(URL="http://www.uni-math.gwdg.de/schick/", arXivID="schick_t_1", default="", crcg=""),
u"T. Schick":                        dict(URL="http://www.uni-math.gwdg.de/schick/", arXivID="schick_t_1", crcg=""),
u"Franziska Schroeter":              dict(URL="http://www.crcg.de/wiki/User:Franzi", crcg=""),
u"Giorgio Trentinaglia":             dict(default="", crcg=""),
u"Luca Tomassini":                   dict(default="", crcg=""),
u"Alessandro Valentino":             dict(URL="http://www.uni-math.gwdg.de/sandro/", arXivID="valentino_a_1", default="", crcg=""),
u"Stefan Wiedmann":                  dict(URL="http://www.uni-math.gwdg.de/wiedmann/", arXivID="wiedmann_s_1", default="", crcg=""),
u"Ingo Witt":                        dict(URL="http://www.uni-math.gwdg.de/iwitt/", default="", crcg=""),
u"Jochen Zahn":                      dict(default="", crcg=""),
u"Chenchang Zhu":                    dict(URL="http://www.crcg.de/wiki/User:Zhu", arXivID="zhu_c_1", default="", crcg=""),
u"C. Zhu":                           dict(URL="http://www.crcg.de/wiki/User:Zhu", arXivID="zhu_c_1", crcg=""),


## external members not listed on the start page
u"Christian Böhning":                dict(URL="http://www.uni-math.gwdg.de/boehning/", default=""),
u"Detlev Buchholz":                  dict(default=""),
u"Pablo Ramacher":                   dict(URL="http://www.uni-math.gwdg.de/ramacher/", default=""),
u"Yunhe Sheng":                      dict(default=""),
u"Andreas Thom":                     dict(URL="http://www.math.uni-leipzig.de/MI/thom/", default=""),
u"Yuri Tschinkel":                   dict(URL="http://www.uni-math.gwdg.de/tschinkel/", default=""),


## extra convenience entries for related people who are not CRCG-members
u"Christoph Wockel":				dict(URL="http://wockel.eu/", arXivID="wockel_c_1", default=""),
u"Sven-S. Porst":					dict(URL="http://earthlingsoft.net/ssp/", arXivID="porst_s_1", default="")
})

