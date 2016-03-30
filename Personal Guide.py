from flask import Flask, request, render_template
import urllib2, datetime, json
from werkzeug.debug import DebuggedApplication

app = Flask(__name__)
app.wsgi_app = DebuggedApplication(app.wsgi_app, True)
app.secret_key = "@#@$(CLXZXC>ASz?}{ax`"
app.config.from_pyfile('Personal Guide.ini', silent=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        city = request.form.get("city")
        if city == "":
            city = "Warsaw"
        return json.dumps(find_venue_by_city_name(city,""))

# current date
today = datetime.datetime.now()
today_date = str(today.strftime("%Y%m%d"))
# client data
client_id = "CXHY5LCAK45SPQMENVNXV11MJUQD50MJH4HT2OYI1MFLOPVX"
client_secret = "XUXPEY3DFLLG2E0P4VSLJ4E43ITUSKUVINWHTHKGC5JIPNQM"


@app.route("/search_venue/<lat_long>/<query>/")
def find_venue(lat_long, query):
    url = "https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&v={}&ll={}&query={}".format(
        client_id, client_secret, today_date, lat_long, query
    )
    venues_text = urllib2.urlopen(url).read()
    venues = json.loads(venues_text)
    return venues


def find_venue_by_city_name(near, query):
    url = "https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&v={}&near={}&query={}".format(
        client_id, client_secret, today_date, near, query
    )
    venues_text = urllib2.urlopen(url).read()
    venues = json.loads(venues_text)
    return venues


@app.route("/popular_sights/<lat_long>/")
def popular_sights(lat_long):
    url = "https://api.foursquare.com/v2/venues/explore?client_id={}&client_secret={}&v={}&ll={}&section=sights".format(
        client_id, client_secret, today_date, lat_long
    )
    print "url popular: " + url
    venues_text = urllib2.urlopen(url).read()
    venues = json.loads(venues_text)
    venues = venues['response']['groups'][0]['items']
    print venues
    print "-----------Miejsca:---------"
    for venue in venues:
        print venue['venue']['name'] + ' ' + str(venue['venue']['location']['lat']) + ' ' + str(venue['venue']['location']['lng'])
    return venues_text

@app.route("/popular_sights_for_map/<lat_long>/")
def popular_sights_for_map(lat_long):
    url = "https://api.foursquare.com/v2/venues/explore?client_id={}&client_secret={}&v={}&ll={}&section=sights".format(
        client_id, client_secret, today_date, lat_long
    )
    venues_text = urllib2.urlopen(url).read()
    venues = json.loads(venues_text)
    venues = venues['response']['groups'][0]['items']
    venues_for_map = []
    for venue in venues:
        venues_for_map.append({'name': venue['venue']['name'], 'lat': venue['venue']['location']['lat'], 'lng': venue['venue']['location']['lng']})
    return json.dumps(venues_for_map)


print find_venue("52.22,21.01", "Old town")
print popular_sights("52.22,21.01")

if __name__ == '__main__':
    app.run()
