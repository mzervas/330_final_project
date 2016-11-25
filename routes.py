from flask import Flask, render_template, request, url_for, redirect
import sqlite3
import facebook
import test
import json
import urllib
import us
from forms import Login
from wtforms import TextField, TextAreaField, SubmitField
from urllib.request import urlopen

app = Flask(__name__)
app.secret_key = 'WebDesign'

strlist = []


conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()
logged_in = False
c.execute("DROP TABLE IF EXISTS users")
# Create table
c.execute("CREATE TABLE users (username VARCHAR(255), password VARCHAR(255), id INTEGER PRIMARY KEY);")
# ------------------------------------------
# Begin defining endpoints
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = Login()
    if len(strlist) == 0:
        def pretty(obj):
            return json.dumps(obj, sort_keys=True, indent=2)

        app_id = '960574354046426'
        app_secret = '28406d69054ebebffa22de1adb3904aa'
        access_token = form.token.data
        # access_token = 'EAANpoyUnPdoBAORvKsFYHsdldvViGZAtH7iz2xzhgi1EZCGC5SiYEoachtRmHhZBZCbzflMyTsmCeiTOOGEGiQ1S'

        graph = facebook.GraphAPI(access_token)
        user = graph.get_object("me?fields=name")
        musicfeed = graph.get_object("/"+user['id']+"/music", limit = 100)
        # musicdict = pretty(musicfeed)
        namelist = []
        for x in musicfeed['data']:
            bandnames = x['name']
            namelist.append(bandnames)
        sortednamelist = []
        for x in namelist:
            i = x.replace(' ', '-').lower().encode('utf-8')
            sortednamelist.append(i)
        print(sortednamelist)

        locationfeed = graph.get_object('/me?fields=location')
        # print(locationfeed)
        # medict = pretty(locationfeed)
        location = locationfeed['location']['name']
        # print(location)
        city = location.split(', ')[0].replace(' ', '-').lower()

        cnslist = []

        state = location.split(', ')[1]
        for x in us.states.mapping('name', 'abbr'):
            if x == state:
                sc = us.states.mapping('name', 'abbr')[x]

        biglist = []
        for band in sortednamelist:
            band = urllib.parse.quote(band)
            response = urllib.request.urlopen('http://api.seatgeek.com/2/events?venue.state='+sc+'&datetime_utc.gt=2015-11-03&performers.slug='+band+'&client_id=MTg1OTA2NnwxNDE3Nzk0MjAw').read().decode('utf-8')
            dumped = json.loads(response)
            for x in dumped['events']:
                for y in x['performers']:
                    if y['name'] in namelist:
                        biglist.append(x)

        correct_name_list = []
        for x in biglist:
            for y in x['performers']:
                if y['name'] in namelist:
                    correct_name_list.append(y['name'])

        dlist = []
        valist = []
        vllist = []
        venuelist = []
        for x in biglist:
        	date = x['datetime_local']
        	dlist.append(date)
        	address= x['venue']['address']
        	valist.append(address)
        	location2 = x['venue']['display_location']
        	vllist.append(location2)
        	venue = x['venue']['name']
        	venuelist.append(venue)

        for x in biglist:
        	date2 = x['datetime_local']
        	address = x['venue']['address']
        	location2 = x['venue']['display_location']
        	venue = x['venue']['name']
        	for y in x['performers']:
        		name = y['name']
        		if name in correct_name_list:
        			strings = "%s is coming to %s on %s at %s at %s." % (name, location2, date2[:10], venue, address)
        			strlist.append(str(strings))


        return render_template("home.html", strlist=strlist, logged_in=True, form=form, name=user['name'])
    return render_template("home.html", logged_in=logged_in)

@app.route('/login', methods=['GET', 'POST'])
def login():
    logged_in = False
    form = Login()
    # logged_in = True
    if form.validate_on_submit():
    #     c.execute("INSERT into users (username, password, id) VALUES (?, ?, NULL)", (form.email.data, form.password.data))
    #     conn.commit()
        logged_in = True
        # return(redirect(url_for('https://www.facebook.com/v2.8/dialog/oauth?client_id=960574354046426&redirect_uri=https://www.facebook.com/connect/login_success.html&scope=user_action.music,user_location', external=True)))
        return render_template("home.html", form=form, logged_in=True)

    # return(redirect(url_for('https://www.facebook.com/v2.8/dialog/oauth?client_id=960574354046426&redirect_uri=https://www.facebook.com/connect/login_success.html&scope=user_action.music,user_location', external=True)))
    return render_template("login.html", form=form)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("login.html"), 404














if __name__ == '__main__':	#Start the Development server
    app.run(debug=True)
