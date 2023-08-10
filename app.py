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

DB_URL = '{DB URL 기입하시면 되요}'
ca = certifi.where()
# client = MongoClient(DB_URL, tlsCAFile=where())
client = MongoClient('mongodb+srv://sparta:test@cluster0.2f3ytju.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta


# 메인 페이지
@app.route('/')
def page_main():
    return render_template('index.html')

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
    }
    db.user_list.insert_one(doc)
    return {'msg': '회원 가입 성공'}



# (YJ) 카드 등록
@app.route("/register", methods=["POST"])
def register_post():
    nickname_receive = request.form['nickname_give']
    field_receive = request.form['field_give']
    github_receive= request.form['github_give']
    blog_receive = request.form['blog_give']
    location_receive = request.form['location_give']
    interest_receive = request.form['interest_give']
    MBTI_receive = request.form['MBTI_give']
    
    register_list = list(db.register.find({}, {'_id': False}))
    # 이미지 추가
    doc = {
        'nickname' : nickname_receive,
        'field' : field_receive,
        'github' : github_receive,
        'blog' : blog_receive,
        'location' : location_receive,
        'interest' : interest_receive,
        'MBTI' : MBTI_receive
    }

    db.cards.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})


## (Eric) Profile Cards들을 리스팅
@app.route("/cards_get", methods=["GET"])
def cards_get():
    ## DB에서 영화를 가져다가 내려줘야한다
    all_user_cards = list(db.user_list.find({},{'_id':False}))

    # 내려주기
    return jsonify({'result':all_user_cards})


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
 