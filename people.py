#coding=utf-8
"""
people.py
arXivToWiki v1
©2009 by Sven-S. Porst / earthlingsoft (ssp-web@earthlingsoft.net)

List of people and their web pages for automatic linking in arXivToWiki.
"""


"""
	Set up table of real names pointing to a dictionary with
		URL     -> full web page URL for the person
		arXivID -> arXiv ID for the person
		
	Be sure to precede the name string with a u, e.g. u"Carl Müller".
"""

URL = "URL"
arXivID = "arXiv ID"

people = dict({
u"Laurent Bartholdi":                dict(URL="http://www.uni-math.gwdg.de/laurent/", arXivID="bartholdi_l_1"),
u"L. Bartholdi":                     dict(URL="http://www.uni-math.gwdg.de/laurent/", arXivID="bartholdi_l_1"),
u"Ralf Meyer":                       dict(URL="http://www.uni-math.gwdg.de/rameyer/", arXivID="meyer_r_1"),
u"R. Meyer":                         dict(URL="http://www.uni-math.gwdg.de/rameyer/", arXivID="meyer_r_1"),
u"Preda Mihailescu":                 dict(URL="http://www.uni-math.gwdg.de/preda/"),
u"Samuel J. Patterson":              dict(URL="http://www.uni-math.gwdg.de/sjp/"),
u"Pablo Ramacher":                   dict(URL="http://www.uni-math.gwdg.de/ramacher/"),
u"Karl-Henning Rehren":              dict(URL="http://www.theorie.physik.uni-goe.de/~rehren/"),
u"Thomas Schick":                    dict(URL="http://www.uni-math.gwdg.de/schick/", arXivID="schick_t_1"),
u"T. Schick":                        dict(URL="http://www.uni-math.gwdg.de/schick/", arXivID="schick_t_1"),
u"Andreas Thom":                     dict(URL="http://www.math.uni-leipzig.de/MI/thom/"),
u"Yuri Tschinkel":                   dict(URL="http://www.uni-math.gwdg.de/tschinkel/"),
u"Ingo Witt":                        dict(URL="http://www.uni-math.gwdg.de/iwitt/"),
u"Dorothea Bahns":                   dict(URL="http://www.uni-math.gwdg.de/bahns/"),
u"Hannah Markwig":                   dict(URL="http://www.crcg.de/wiki/User:Hannah", arXivID="markwig_h_1"),
u"H. Markwig":                       dict(URL="http://www.crcg.de/wiki/User:Hannah", arXivID="markwig_h_1"),
u"Chenchang Zhu":                    dict(URL="http://www.crcg.de/wiki/User:Zhu", arXivID="zhu_c_1"),
u"C. Zhu":                           dict(URL="http://www.crcg.de/wiki/User:Zhu", arXivID="zhu_c_1"),
u"Anders Jensen":                    dict(URL="http://www.crcg.de/wiki/User:Jensen"),
u"Anders Nedergaard Jensen":         dict(URL="http://www.crcg.de/wiki/User:Jensen"),
u"Alessandro Valentino":             dict(URL="http://www.uni-math.gwdg.de/sandro/", arXivID="valentino_a_1"),
u"Hans-Christian Graf v. Bothmer":   dict(URL="http://www.crcg.de/wiki/User:Bothmer", arXivID="grafvbothmer_h_1"),
u"Hans-Christian Graf von Bothmer":  dict(URL="http://www.crcg.de/wiki/User:Bothmer", arXivID="grafvbothmer_h_1"),
u"Hans-Christian Bothmer":           dict(URL="http://www.crcg.de/wiki/User:Bothmer", arXivID="grafvbothmer_h_1"),
u"Hans-Christian v. Bothmer":        dict(URL="http://www.crcg.de/wiki/User:Bothmer", arXivID="grafvbothmer_h_1"),
u"Hans-Christian von Bothmer":       dict(URL="http://www.crcg.de/wiki/User:Bothmer", arXivID="grafvbothmer_h_1"),
u"H.-Chr. Graf von Bothmer":         dict(URL="http://www.crcg.de/wiki/User:Bothmer", arXivID="grafvbothmer_h_1"),
u"H. -Chr. Graf von Bothmer":        dict(URL="http://www.crcg.de/wiki/User:Bothmer", arXivID="grafvbothmer_h_1"),
u"H.-C. Graf v. Bothmer":            dict(URL="http://www.crcg.de/wiki/User:Bothmer", arXivID="grafvbothmer_h_1"),
u"Thomas Markwig": 	                 dict(URL="http://www.mathematik.uni-kl.de/~keilen/de/index.html"),
u"Thomas Keilen": 	                 dict(URL="http://www.mathematik.uni-kl.de/~keilen/de/index.html"),
u"Eugenii Shustin":                  dict(URL="http://www.math.tau.ac.il/~shustin/"),
u"Christian Böhning":                dict(URL="http://www.uni-math.gwdg.de/boehning/"),
u"Jakob Kröker":                     dict(URL="http://www.crcg.de/wiki/User:Kroeker")
})
