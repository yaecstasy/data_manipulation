# //1526678063.915f951.bedceeb5fb524dac942a0a72035df295
# //1497158604.73e896a.041f75b9d36940c084214a5f0141fdd8
# //1497158604.915f951.9fe2738dca34431ba78a350b7d1e2dd3
# //1526678063.e3c4e2f.242f1ae2c5514c369d0cb037204429e2
# //1530119206.915f951.60a0632d13304c6c9152f15165b85385
# //first:
# //pip install python-instagram
from instagram.client import InstagramAPI

api = InstagramAPI(access_token="1526678063.915f951.bedceeb5fb524dac942a0a72035df295")
print api.location(location_id="305429").name
recent_media,next = api.location_recent_media(location_id="305429")
for media in recent_media:
    print media.tags