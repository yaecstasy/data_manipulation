from instagram.client import InstagramAPI

api = InstagramAPI(access_token="1526678063.915f951.bedceeb5fb524dac942a0a72035df295")

lon=-79.8868138
lat=40.3505527
count=1

distance=50

locations=api.location_search(distance,count,lat,lon)

for place in locations:
	print place.id
	print place.name
	recent_media, next= api.location_recent_media(location_id=place.id)
	print len(recent_media)
# for media in recent_media:
#     print media.tags