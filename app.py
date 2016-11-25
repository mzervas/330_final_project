import facebook
import test
import json
import urllib
# import urllib2

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

access_token = 'EAACEdEose0cBAMcvW9dFfg3VMdMrqhs0NaWYbhvADV7CM2CnXjcAGRjEJNMxS4i3iNIZCSVRubz3qZC5AdnhyIkcc7uto5iC2kSM1JtczY8K0AeoxTL7yFFZAJuIxZCZB9afd9UvS3ugvwV1DIcxuvdeEnhLFBzQwgCZAzfzjSRQZDZD'
graph = facebook.GraphAPI(access_token)
musicfeed = graph.get_object("/me/music", limit = 100)

musicdict = pretty(musicfeed)

namelist = []
for x in musicfeed['data']:
	bandnames = x['name']
	namelist.append(bandnames)

sortednamelist = sorted(namelist, key = lambda x: x)


nospacelist=[]
for x in sortednamelist:
	if ' ' in x:
		y = x.replace(' ','-')
		z = y.lower()
		nospacelist.append(z)


locationfeed = graph.get_object("/me")
medict = pretty(locationfeed)
location = locationfeed['location']['name']
city = location.split(', ')[0]

cnslist = []

if ' ' in city:
	y = city.replace(' ','-')
	z = y.lower()
	city = z

state = location.split(', ')[1]
if 'Missouri' in state: #I only did some states because I assumed most people's location on Facebook is Ann Arbor, since we're in Ann Arbor right now.
	sc = 'MO'
if 'Montana' in state:
	sc = 'MT'
if 'Nebraska' in state:
	sc = 'NE'
if 'Nevada' in state:
	sc = 'NV'
if 'New Hampshire' in state:
	sc = 'NH'
if 'New Jersey' in state:
	sc = 'NJ'
if 'New Mexico' in state:
	sc = 'NM'
if 'Ohio' in state:
	sc = 'OH'
if 'Virginia' in state:
	sc = 'VA'
if 'California' in state:
	sc = 'CA'
if 'Indiana' in state:
	sc = 'IN'
if 'Michigan' in state:
	sc = 'MI'
if 'Illinois' in state:
	sc = 'IL'
if 'New York' in state:
	sc = 'NY'
if 'Texas' in state:
	sc = 'TX'

# def fixchars(list):
# 	for x in list:
# 		if len(x.split('-')) > 7: #if there's so many words in the band name, it might not be a band name and might be a different type of page and will cause an error.
# 			list.remove(x)
# 		for y in x:
# 			if y == '&': #the url does not accept these characters.
# 				list.remove(x)
# 				return list
# 			elif y == '!':
# 				list.remove(x)
# 				return list
# 			elif y == '?':
# 				list.remove(x)
# 				return list
# 			elif y == '$':
# 				list.remove(x)
# 				return list
# 	return list
# fixedlist = fixchars(nospacelist)

for x in nospacelist:
	x.encode('utf-8').strip()
nospacelist.append('x8s9f$%')

biglist = []
for band in nospacelist:
	response = urllib.request.urlopen('http://api.seatgeek.com/2/events?venue.state='+sc+'&datetime_utc.gt=2015-11-03&performers.slug='+band+'&client_id=MTg1OTA2NnwxNDE3Nzk0MjAw').read()
    loaded = json.loads(response)
	for x in loaded['events']:
		for y in x['performers']:
			if y['name'] in namelist:
				biglist.append(x)


blist = []
for x in biglist:
	for y in x['performers']:
		if y['name'] in namelist:
			blist.append(y['name'])
print(blist)
# bd = {}
# for x in blist:
# 	if x in bd:
# 		bd[x] = bd[x] + 1
# 	else:
# 		bd[x] = 1
# blist = bd.keys()
# print blist

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

class DateTime:

	def __init__(self, astring):
		self.time = astring

	def gettime(self):
		return self.time

	def militaryto12(self):
		time1 = self.time[11:]
		time2 = int(time1[:2])
		if time2 > 12:
			return str(time2-12)+':'+time1[3:]+' PM'


newdlist = []
for x in dlist:
	one = DateTime(str(x))
	print(one)
	newdlist.append(one.militaryto12())

test.testEqual(one.militaryto12(), '6:30:00 PM')

strlist = []
for x in biglist:
	date2 = x['datetime_local']
	address = x['venue']['address']
	location2 = x['venue']['display_location']
	venue = x['venue']['name']
#	for d in newdlist:
		#date1 = d
	date3 = DateTime(str(date2))
	for y in x['performers']:
		name = y['name']
		if name in blist:
			strings = "%s is coming to %s on %s at %s at %s at %s." % (name, location2, date2[:10], date3.militaryto12(), venue, address)
			strlist.append(str(strings))


def mostcommonvenue(alist):
	d = {}
	vlist= []
	bestlist = []
	for x in alist:
		venue = x['venue']['name']
		vlist.append(venue)
	for y in vlist:
		if y in d:
			d[y]=d[y]+1
		else:
			d[y] = 1
	dk = d.keys()
	best = dk[0]
	for i in dk:
		if d[i] > d[best]:
			best = i
	for y in dk:
		if d[y] == d[best]:
			bestlist.append(y)
	return bestlist

test.testEqual(mostcommonvenue([{'venue':{'name':'Bill'}},{'venue':{'name':'Joe'}}, {'venue':{'name':'Joe'}}]), ['Joe'])
test.testEqual(type(mostcommonvenue([{'venue':{'name':'Joe'}}, {'venue':{'name':'Bill'}}, {'venue':{'name':'Joe'}}])), type(['Joe']))


def mostcommoncity(alist):
	d = {}
	clist = []
	bestlist = []
	for x in alist:
		venuecity = x['venue']['display_location']
		clist.append(venuecity)
	for y in clist:
		if y in d:
			d[y]=d[y]+1
		else:
			d[y] = 1
	dk = d.keys()
	best = dk[0]
	for i in dk:
		if d[i] > d[best]:
			best = i
	for y in dk:
		if d[y] == d[best]:
			bestlist.append(y)
	return bestlist

test.testEqual(mostcommoncity([{'venue':{'display_location':'y'}},{'venue':{'display_location':'x'}},{'venue':{'display_location':'x'}}]),['x'])

def nextyear(alist):
	new = [x for x in alist if '2015' in x]
	return new


#****** WRITING THE FILE *******#
for x in strlist:
	sortedstrlist = sorted(strlist, key = lambda y: y)
#print sortedstrlist[0]
st = "You have %d events coming near %s in the near future: \n" % (len(strlist), location)
outfile = open('testing.html','w')
outfile.write(st)

for x in sortedstrlist:
	outfile.write(x + '\n')

outfile.write('\n' + 'The most common venue(s) with concerts of bands that you have liked is: ')
for x in mostcommonvenue(biglist):
	outfile.write(x + ' ')

outfile.write('\n' + 'The most common city(ies) with venues of concerts of bands that you have liked is: ')

for x in mostcommoncity(biglist):
	outfile.write(x + ' ')

outfile.write('\n%d of these events are in 2015.' % (len(nextyear(strlist))))
