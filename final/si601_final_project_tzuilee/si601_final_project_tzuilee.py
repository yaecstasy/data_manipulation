import simplejson as json
import re,string
from instagram.client import InstagramAPI

api = InstagramAPI(access_token="1526678063.915f951.bedceeb5fb524dac942a0a72035df295")

def check_name(yelp,instagram):
	for c in string.punctuation:
		yelp = yelp.replace(c,"")

	yelpSplit=yelp.split()	  
	for name in yelpSplit:
		foo=re.compile(name)
		if foo.search(instagram):
			return True
	return False		

infile=open('yelp_academic_dataset_business.json','rU')

state="PA"
places=[]
for line in infile:
	data=json.loads(line)
	if data['state']== "PA":
		categories=data['categories']
		if categories:
			for category in categories:
				if category=='Restaurants' and data['review_count']>=10:
					name=data['name']
					lon=data['longitude']
					lat=data['latitude']
					stars=data['stars']
					review_counts=data['review_count']
					places.append([name,lon,lat,stars,review_counts])

distance=2
count=1
combine=[]

for i in range(len(places)):
	lon=places[i][1]
	lat=places[i][2]
	stars=places[i][3]
	review_counts=places[i][4]
	yelp_name=places[i][0]
	location=api.location_search(distance,count,lat,lon)

	for place in location:
		if check_name(yelp_name,place.name):
			recent_media, next= api.location_recent_media(location_id=place.id)
			if len(recent_media)!=0:
				combine.append([yelp_name,stars,review_counts,len(recent_media)])			

outfile = open('finalProjectPA_WI.csv','w')
outfile.write('Name,Yelp_stars,Yelp_review,Instagram_checkin\n')

for item in combine:
	line=item[0]+','+str(item[1])+','+str(item[2])+','+str(item[3])
	outfile.write(unicode(line).encode('utf-8')+'\n')
outfile.close()



