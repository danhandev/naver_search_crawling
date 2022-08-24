import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from final_data import final_data_dic
from tags import bakery_cafe, brunch_cafe, healing_cafe, instagram_cafe, new_cafe, view_cafe

# Use the application default credentials
cred = credentials.Certificate(
    r'C:\Users\danha\Documents\GitHub\naver_search_crawling\cafegation-firebase-admin.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

for data in final_data_dic.values():
    # auto increment id로 document 생성
    doc_ref = db.collection(u'cae').document()
    
    # 오픈 시간 월 ~ 일로 변환
    if '매일' in data['open_time']:
        open_time = data['open_time']['매일']
        data['open_time'] = {}

        for day in ['월', '화', '수', '목', '금', '토', '일']:
            data['open_time'][day] = open_time

    # tag 추가
    data['tags'] = []
    for i, cafe in enumerate([bakery_cafe.bakery_cafe, brunch_cafe.brunch_cafe, healing_cafe.healing_cafe, instagram_cafe.instagram_cafe, new_cafe.new_cafe, view_cafe.view_cafe]):
        if data['name'] in cafe:
            data['tags'].append(i+1)

    # firestore에 data 저장
    doc_ref.set({
        u'name': data['name'],
        u'images': data['images'],
        u'location': data['location'],
        u'menus': data['menus'],
        u'open_time': data['open_time'],
        u'rating': data['rating'],
        u'telephone': data['telephone'],
        u'tags': data['tags']
    })

# 데이터 확인용
# users_ref = db.collection(u'cae')
# docs = users_ref.stream()

# for doc in docs:
#     print(f'{doc.id} => {doc.to_dict()}')
