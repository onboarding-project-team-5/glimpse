# 식은 할당 대상이 될 수 없습니다? - 무슨 말인지 모르겠다
# post 문법 찾아보고 수정하기

from flask import Flask, render_template
app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://yungiDB:dbsrlelql@cluster0.bpcqzfd.mongodb.net/?retryWrites=true&w=majority')
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
# @app.route('/card/registration')
# def page_card_registration():
#     return render_template('card_registeration.html')

# 이미지 업로드 추가!!
@app.route("/register", methods=["POST"])
def register_post():
    nickname_receive = request.form['nickname_give']
    field_receive = request.form['field_give']
    github_receive= request.form['github_give']
    blog_receive = request.form['blog_give']
    location_receive = request.form['lacation_give']
    interest_receive = request.form['interest_give']
    MBTI_receive = request.form['MBTI_give']
    
    register_list = list(db.register.find({}, {'_id': False}))
    # 이미지 추가
    doc = {
        'nickname' = nickname_receive,
        'field' = field_receive,
        'github' = github_receive,
        'blog' = blog_receive,
        'location' = location_receive,
        'interest' = interest_receive,
        'MBTI' = MBTI_receive
    }

    db.cards.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})


# 404 오류 핸들러 - 잘못된 페이지로의 접근
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
 