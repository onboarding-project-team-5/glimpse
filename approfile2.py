# 식은 할당 대상이 될 수 없습니다? - 무슨 말인지 모르겠다
# post 문법 찾아보고 수정하기

from flask import Flask, render_template
from flask import request
from flask import jsonify

from utils.jwt import make_token, decode_token

import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

from pymongo import MongoClient
# from certifi import where
import certifi

# JE 몽고db 맥북에서 연결되는 설정으로 변경
from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://sparta:test@cluster0.okucubo.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.dbsparta


# 메인 페이지
@app.route('/')
def page_main():
    return render_template('index.html')

# Yoonju 프로필 등록 페이지 - 유저리스트 카드 만들기
@app.route("/movie", methods=["POST"])
def cards_post():
    ## 1. url, comment + star 받기
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']
    star_receive = request.form['star_give']
    print(url_receive, comment_receive, star_receive)

    ## 2. 크롤링
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive,headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    # 여기에 코딩을 해서 meta tag를 먼저 가져와보겠습니다.
    # <meta content="스즈메의 문단속" property="og:title"/> 에서 "스즈메의 문단속""을 가져온다
    ogtitle = soup.select_one('meta[property="og:title"]')['content']
    ogimage = soup.select_one('meta[property="og:image"]')['content']
    ogdesc = soup.select_one('meta[property="og:description"]')['content']
    # print(ogtitle, ogimage, ogdesc)

    ## 3. DB에 넣기
    # 저장 - 예시
    doc = {
        'title': ogtitle,
        'image': ogimage,
        'desc': ogdesc,
        'comment': comment_receive,
        'star': star_receive
    }
    db.movies.insert_one(doc)
    
    return jsonify({'msg':'저장완료!'})

## (Eric) Profile Cards들을 리스팅
@app.route("/cards_get", methods=["GET"])
def cards_get():
    ## DB에서 영화를 가져다가 내려줘야한다
    all_user_cards = list(db.user_list.find({},{'_id':False}))

    # 내려주기
    return jsonify({'result':all_user_cards, 'msg': '카드 리스팅 완료'})


# (JH) 회원가입, 로그인 페이지
@app.route('/signup')
def page_signup():
    return render_template('signup.html')

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
        'user_name' : name,
        'user_id' : id,
        'user_pw' : pw,
    }
    db.user_list.insert_one(doc)
    return {'msg': '회원 가입 성공'}

# (JE) 개인 프로필 페이지
@app.route('/profile/me')
def page_profile_me():
    return render_template('profile.html')

# 카드 등록 페이지
@app.route('/card/registration')
def page_card_registration():
    return render_template('card_registeration.html')

# YJ 이미지 업로드 추가!!
@app.route("/register", methods=["POST"])
def register_post():
    nickname_receive = request.form['nickname_give']
    MBTI_receive = request.form['MBTI_give']
    location_receive = request.form['location_give']
    social_receive = request.form['social_give']
    specialty_receive = request.form['specialty_give']
    interest_receive = request.form['interest_give']
    program_receive = request.form['program_give']
    course_receive= request.form['course_give']
    cohort_receive = request.form['cohort_give']
    team_receive = request.form['team_give']
    image_receive = request.form['image_give']
    
    # 이미지 추가
    doc = {
        'user_nickname': nickname_receive,
        'MBTI' : MBTI_receive,
        'location': location_receive,
        'social_list': social_receive,
        'specialty' : specialty_receive,
        'interest': interest_receive,
        'program' : program_receive,
        'course' : course_receive,
        'cohort' : cohort_receive,
        'team' : team_receive,
        'image_receive' : image_receive
    }
    db.user_list.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})

# JE 프로필 register 내용 출력하기
@app.route("/register", methods=["GET"])
def register_get():
    register_data = list(db.user_list.find({},{'_id':False}))
    return jsonify({'result':register_data})


# JE 댓글 저장하기
@app.route("/comment", methods=["POST"])
def comment_post():
    comment_receive = request.form['comment_give']

    comment_list = list(db.comment.find({}, {'_id': False}))
    count = len(comment_list) + 1
    doc = {
        'num':count,  #버킷 등록 시, db에서 특정 버킷을 찾기 위해 'num' 이라는 고유 값 부여
        'comment' :comment_receive,
        'done' : 0   #'done' key값을 추가 해 각 버킷의 완료 상태 구분(0 = 미완료, 1 = 완료)
    }
    db.comment.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})

# JE 댓글 출력하기
@app.route("/comment", methods=["GET"])
def comment_get():
    all_comments = list(db.comment.find({}, {'_id': False}))
    return jsonify({'result': all_comments})


# 404 오류 핸들러 - 잘못된 페이지로의 접근
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
 