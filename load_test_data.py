from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://sparta:test@cluster0.2f3ytju.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
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
    
    'profile_image' : 'https://www.nicepng.com/png/detail/933-9332131_profile-picture-default-png.png',
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
    
    'profile_image' : 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQrcZnEnLy7Ie31zOFTPNd_C8GCFnYvy-Thcg&usqp=CAU',
}

db.user_list.insert_one(doc)

print("load 완료")

# 꼭 DB URL 입력해주세요.
# 해당 파일과 동등한 위치에서 
# python load_test_data.py
# 라는 명령어를 terminal에서 입력하시면 됩니다.