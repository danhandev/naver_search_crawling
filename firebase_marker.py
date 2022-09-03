import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import googlemaps

# firebase_admin 보안 정보
cred = credentials.Certificate(
    r'C:\Users\danha\Documents\GitHub\naver_search_crawling\cafegation-firebase-admin.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

gmaps = googlemaps.Client("geocoding api 키")

# 정보를 입력할 collection 설정
users_ref = db.collection(u'cae')
# 'cae' collection의 모든 document들을 가져온다.
docs = users_ref.stream()

for doc in docs:
    location = doc.to_dict()['location']

    try:
        geocode_result = gmaps.geocode(location)[0]['geometry']['location']

        latitude = geocode_result['lat']
        longitude = geocode_result['lng']

        set_doc = users_ref.document(doc.id)
        set_doc.set({
            u'coordinate': [latitude, longitude],
        }, merge=True)

    except:
        print("경도 위도를 찾지 못함 : doc.to_dict()['name']")
