from flask import Flask, render_template
from flask import request
from flask import jsonify

from utils.jwt import make_token

app = Flask(__name__)

# DB 연결
from pymongo import MongoClient
# from certifi import where
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://sparta:test@cluster0.3lyhcbq.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

# 크롤링
import requests
from bs4 import BeautifulSoup

# 숫자만 빼내기
import re

# -----------------


# 메인 페이지
@app.route('/')
def page_main():
    return render_template('index.html', **collect_distinct_items())

# (JH) 회원가입 페이지
@app.route('/signup')
def page_signup():
    return render_template('signup.html')

# (JH) 로그인 페이지
@app.route('/login')
def page_login():
    return render_template('login.html')

# (JE) 개인 프로필 페이지
@app.route('/profile/<user_id>')
def page_profile_me(user_id):
    return render_template('profile.html', user_id=user_id)

# 카드 등록 페이지
@app.route('/card/registration')
def page_card_registration():
    return render_template('card_registeration.html')

# 404 오류 핸들러 - 잘못된 페이지로의 접근
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# (JH) 유저 단일 조회 쿼리
@app.route('/api/users/<user_id>')
def query_users(user_id):
    result = db.user_list.find_one({'user_id': user_id}, {'_id': False})
    
    # 유저 조회가 이뤄지지 않았으면 오류 발생.
    if result is None:
        return {'msg': '존재하지 않는 유저입니다. 정확한 ID를 입력해주세요.', 'error_code': 'USER_NOT_FOUNDED'}, 406
    return {'result': result}

# (JH) 유저 단일 조회 쿼리 - ID값이 빈 값으로 넘어옴.
@app.route('/api/users/')
def query_users_without_id():
    return {'msg': '존재하지 않는 유저입니다. 정확한 ID를 입력해주세요.', 'error_code': 'USER_NOT_FOUNDED'}, 406

# (JH) 로그인 Query
@app.route('/api/login', methods=['POST'])
def query_login():
    id = request.form['id']
    pw = request.form['pw']
    
    # 만약 빈 값으로 넘어온 것이 있으면 입력 촉구 메시지 띄움.
    if id is None or not id.strip():
        return {'msg': 'ID 값이 빈 칸으로 넘어왔습니다. 입력해주십시오.', 'error_code': 'NULL_ID'}, 406
    if pw is None or not pw.strip():
        return {'msg': 'PW 값이 빈 칸으로 넘어왔습니다. 입력해주십시오.', 'error_code': 'NULL_PW'}, 406
    
    # 해당 유저 조회
    result = db.user_list.find_one({'user_id': id}, {'_id': False})
    # 만약 유저가 존재하지 않으면 로그인 실패
    if result is None:
        return {'msg': '존재하지 않는 유저입니다. 정확한 ID를 입력해주세요.', 'error_code': 'USER_NOT_FOUNDED'}, 406
    
    # pw 대조
    # 만약 비번이 틀리면 로그인 실패
    if result['user_pw'] != pw:
        return {'msg': '비밀 번호가 틀렸습니다. 정확한 Password를 입력해주세요.', 'error_code': 'WRONG_PASSWORD'}, 406
    
    # JWT 토큰 생성
    token = make_token(result)
    return {'msg': '로그인 성공', 'token': token}

# (JH) 회원가입 Query
@app.route('/api/signup', methods=['POST'])
def query_signup():
    id = request.form['id']
    pw = request.form['pw']
    name = request.form['name']
    
    # 만약 빈 값으로 넘어온 것이 있으면 입력 촉구 메시지 띄움.
    if id is None or not id.strip():
        return {'msg': 'ID 값이 빈 칸으로 넘어왔습니다. 입력해주십시오.', 'error_code': 'NULL_ID'}, 406
    if pw is None or not pw.strip():
        return {'msg': 'PW 값이 빈 칸으로 넘어왔습니다. 입력해주십시오.', 'error_code': 'NULL_PW'}, 406
    if name is None or not name.strip():
        return {'msg': 'NAME 값이 빈 칸으로 넘어왔습니다. 입력해주십시오.', 'error_code': 'NULL_NAME'}, 406
    
    # 해당 유저 조회
    result = db.user_list.find_one({'user_id': id})
    # 만약 존재한다면 회원 가입 실패. 이미 존재하는 유저라는 메시지 출력
    if result is not None:
        return {'msg': '이미 존재하는 유저입니다. 해당 ID로 로그인해주세요.', 'error_code': 'USER_ALREADY_EXISTED'}, 406
    
    # 해당 유저 저장.
    doc = {
        'user_nickname' : name,
        'user_id' : id,
        'user_pw' : pw,
        'has_card': 0,
    }
    db.user_list.insert_one(doc)
    return {'msg': '회원 가입 성공'}

# (JH) 중복 제거를 위한 func
def get_distinct_items(col):
    distinct_values = db.user_list.distinct(col)
    distinct_values = [
        i 
        for i in distinct_values 
        if i and i != 'undefined' and i != '선택'
        ]
    return distinct_values

# (JH) 각 칼럼마다 중복되지 않는 칼럼값 가져오기.
def collect_distinct_items():
    return {
        "cohort": get_distinct_items("cohort"),
        "mbti": get_distinct_items("MBTI"),
        "program": get_distinct_items("program"),
        "specialty": get_distinct_items("specialty"),
        "team": get_distinct_items("team"),
    }
    
# (JH) 특정 값에 일치하는 카드들 목록 load
@app.route('/api/<column>/<item>/cards')
def query_team_cards(column, item):
    result = list(db.user_list.find({column: item, 'has_card': 1}, {'_id':False}))
    return {"result": result}


# (YJ) 카드 등록
@app.route('/')
def home():
    return render_template('card_registeration.html')

# (Eric) extracting number from ogdescription for github repo count
# def extract_numbers(sentence):
#     numbers = re.findall(r'\d+', sentence)
#     return [int(number) for number in numbers]

def extract_number(sentence):
    match = re.search(r'\d+', sentence)
    if match:
        return int(match.group())
    else:
        return None  # If no number is found

@app.route("/register", methods=["POST"])
def register_post():
    # 유저 정보를 card_registration.html form에서 받기
    uid = request.form['uid']
    MBTI_receive = request.form['MBTI_give']
    location_receive = request.form['location_give']
    social_receive = request.form['social_give'] # social은 github
    specialty_receive = request.form['specialty_give']
    interest_receive = request.form['interest_give']
    program_receive = request.form['program_give']
    course_receive= request.form['course_give']
    cohort_receive = request.form['cohort_give']
    team_receive = request.form['team_give']
    image_receive = request.form['image_give']
    resolution_receive = request.form['resolution_give']
    target_industry_receive = request.form['targetindustry_give']
    
    # 크롤링: github 링크를 받아서 이미지 파일 추출하기
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(social_receive,headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    # Github 프로필 페이지에서 이미지 뽑아내기
    # <meta property="og:image" content="https://avatars.githubusercontent.com/u/12006951?v=4?s=400"> 200x200
    ogimage = soup.select_one('meta[property="og:image"]')['content']
    ogdesc = soup.select_one('meta[property="og:description"]')['content']
    
    image_github_url = ogimage
    repo_count = extract_number(ogdesc) # repository 수
    print(repo_count)

    # DB에 보낼 document구성
    doc = {
        'MBTI' : MBTI_receive,
        'location': location_receive,
        'social_list': social_receive,
        'specialty' : specialty_receive,
        'interest': interest_receive,
        'program' : program_receive,
        'course' : course_receive,
        'cohort' : cohort_receive,
        'team' : team_receive,
        'profile_image' : image_receive,
        'github_image_url': image_github_url,
        'github_repo_count': repo_count,
        'resolution' : resolution_receive,
        'target_industry': target_industry_receive,
        'has_card' : 1,
    }
    db.user_list.update_one({'user_id': uid},{'$set':doc})
    # 성공여부 추가, 성공 시 fuction 에 사용
    return jsonify({'result': 'success', 'msg': '저장 완료!'})


## (Eric) Profile Cards들을 리스팅
@app.route("/cards_get", methods=["GET"])
def cards_get():
    ## DB에서 영화를 가져다가 내려줘야한다
    all_user_cards = list(db.user_list.find({},{'_id':False}))

    # 내려주기
    return jsonify({'result':all_user_cards})


# JE 프로필 register 내용 출력하기
@app.route("/api/users/${user_id}", methods=["GET"])
def register_get():
    register_data = list(db.user_list.find({},{'_id':False}))
    return jsonify({'result':register_data})


# JE 댓글 저장하기
@app.route("/api/users/${user_id}/comment", methods=["POST"])
def comment_post(user_id):
    comment_receive = request.form['comment_give']

    comment_list = list(db.comment.find({}, {'_id': False}))
    count = len(comment_list) + 1
    doc = {
        'num':count,  #버킷 등록 시, db에서 특정 버킷을 찾기 위해 'num' 이라는 고유 값 부여
        'comment' :comment_receive,
        'user_id': user_id  #'done' key값을 추가 해 각 버킷의 완료 상태 구분(0 = 미완료, 1 = 완료)
    }
    db.comment.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})


# (JE) 개인 프로필 페이지 - 댓글 출력
@app.route('/profile/<user_id>/comments', methods=["GET"])
def profile_comments(user_id):
    user_comments = list(db.comment.find({'user_id': user_id}, {'_id': False}))
    return jsonify({'result': user_comments})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
 