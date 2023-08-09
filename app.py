from flask import Flask, render_template
app = Flask(__name__)

from pymongo import MongoClient
from certifi import where

DB_URL = '{DB URL 기입하시면 되요}'
client = MongoClient(DB_URL, tlsCAFile=where())

db = client.dbsparta


# 메인 페이지
@app.route('/')
def page_main():
    return render_template('index.html')

# 회원가입, 로그인 페이지
@app.route('/signup')
def page_signup():
    return render_template('signup.html')

# 개인 프로필 페이지
@app.route('/profile/me')
def page_profile_me():
    return render_template('profile.html')

# 카드 등록 페이지
@app.route('/card/registration')
def page_card_registration():
    return render_template('card_registeration.html')

# 404 오류 핸들러 - 잘못된 페이지로의 접근
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
 