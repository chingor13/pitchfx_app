from flask import Flask, Response
app = Flask(__name__)

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

import urllib2
import json

from HTMLParser import HTMLParser

# create a subclass and override the handler methods
class GamesParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.games = []
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            href = None
            name = None
            for name, value in attrs:
                if name == 'href':
                    href = value
                    self.games.append(href)
                    print "Adding link: ", href
    def handle_endtag(self, tag):
        print "End tag: ", tag
    def handle_data(self, data):
        print "Data: ", data

@app.route('/')
def hello():
    response = urllib2.urlopen('http://chingr.com/')
    print response.info()
    html = response.read()
    return html

@app.route('/games')
def games():
    url = 'http://gd2.mlb.com/components/game/mlb/year_2014/month_04/day_12/'
    resp = urllib2.urlopen(url)
    html = resp.read()
    parser = GamesParser()
    parser.feed(html)
    return Response(json.dumps({
        'games': parser.games
    }), mimetype='application/json')

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
