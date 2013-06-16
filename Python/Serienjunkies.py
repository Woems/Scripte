#!/usr/bin/env python
import urllib2
import lxml.html
from StringIO import StringIO
import gzip
import time
import os
#xpath="//*[@id='download_mirrors']/a"
#xpath="id('content')//a[contains(@href,'download')]/@href"
xpath="id('content')//p/a[1][contains(@href,'download')]/@href"
url = "http://serienjunkies.org/serie/heroes/"

request=urllib2.Request(url)
request.add_header("User-Agent", "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11")
f = urllib2.urlopen(request)
print "* URL: "+f.geturl()
print "* Info:"
print f.info()
print "* GetCode:"
print f.getcode()
if f.info().get('Content-Encoding') == 'gzip':
  buf = StringIO( f.read())
  f = gzip.GzipFile(fileobj=buf)

#outfile = open('heros.html','w')
#outfile.write(f.read())
#outfile.close()

#print f.read()

tree = lxml.html.parse(f)
listings = tree.xpath(xpath)
for i in listings:
  print "Link: "+i
  #os.system("/usr/bin/firefox "+i)

  time.sleep(6)
#print listings
