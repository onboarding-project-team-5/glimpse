from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient('{DB URL 입력하시면 되요}', tlsCAFile=ca)
db = client.dbsparta

doc = {
    'user_id' : 'mrhong',
    'user_pw' : '1234',
    'user_nickname': 'thief', # 닉네임
    
    'MBTI' : 'ENTJ', # mbti
    'location': 'seoul', # 지역
    'social_list': [{'facebook': 'fb.com/abc', 'github': 'github.com'} ],
    'specialty' : 'spring', # 주특기 
    'interest': ['tennis', 'swimming'], # 관심사
    
    'likes': 10, # 좋아요 
    
    'program' : '항해',
    'course' : '웹개발 종합반', 
    'cohort' : 16,
    'team' : [5,10,11],
}

db.user_list.insert_one(doc)

doc = {
    'user_id' : 'young',
    'user_pw' : '1234',
    'user_nickname': 'happy', # 닉네임
    
    'MBTI' : 'INTP', # mbti
    'location': 'seoul', # 지역
    'social_list': [{'facebook': 'fb.com/abc', 'github': 'github.com'} ],
    'specialty' : 'Node.js', # 주특기 
    'interest': ['tennis', 'swimming'], # 관심사
    
    'likes': 20, # 좋아요 
    
    'program' : '항해',
    'course' : '웹개발 종합반', 
    'cohort' : 16,
    'team' : [2,9,11],
}

db.user_list.insert_one(doc)

print("load 완료")

# 해당 파일과 동등한 위치에서 
# python load_test_data.py
# 라는 명령어를 terminal에서 입력하시면 됩니다.