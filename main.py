from flask import Flask
app = Flask(__name__)

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

import urllib2

from HTMLParser import HTMLParser

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print "Encountered a start tag:"
        print tag
    def handle_endtag(self, tag):
        print "Encountered an end tag :"
        print tag
    def handle_data(self, data):
        print "Encountered some data  :"
        print data

@app.route('/')
def hello():
    response = urllib2.urlopen('http://chingr.com/')
    print response.info()
    html = response.read()
    return html

@app.route('/games')
def games():
    url = 'http://gd2.mlb.com/components/game/mlb/year_2014/month_04/day_12/'
    html = urllib2.urlopen(url)
    parser = MyHTMLParser()
    parser.feed(html)
    return "Games page"

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
