import facebook
import test
import json
import urllib
import us


def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

access_token = 'EAACEdEose0cBACjZBzMMTn7ZCOQzw3ZBtla0avFnxWGDu0JUEdwYSArqVwAmEvZAbF1X3kMm3PkW2YqhZCVYemAwMZCa3Ep3J3Ctl04hgsIfON7Vx7UPACM70yiyNawqZCHoe5ZBCtfHN4jyg7pYNFhuVQZBuvZCQ7S6RogoTTIvw0LQZDZD'
graph = facebook.GraphAPI(access_token)
musicfeed = graph.get_object("/me/music", limit = 100)

musicdict = pretty(musicfeed)

namelist = []
for x in musicfeed['data']:
    bandnames = x['name']
    namelist.append(bandnames)

sortednamelist = []
for x in namelist:
    i = x.replace(' ', '-').lower().encode('utf-8')
    sortednamelist.append(i)
# print(sortednamelist)

locationfeed = graph.get_object('/me')
medict = pretty(locationfeed)
location = locationfeed['location']['name']
city = location.split(', ')[0].replace(' ', '-').lower()

cnslist = []

state = location.split(', ')[1]
for x in us.states.mapping('name', 'abbr'):
    if x == state:
        sc = us.states.mapping('name', 'abbr')[x]

# for x in sortednamelist:
#     x.encode('utf-8').strip()
# sortednamelist.append('x8s9f$%')

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

strlist = []
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

st = "You have %d events coming near %s in the near future: \n" % (len(strlist), location)
outfile = open('testing.html','w')
outfile.write(st)

for x in strlist:
	outfile.write(x + '\n')
