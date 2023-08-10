from flask import Flask, render_template, request, jsonify
app = Flask(__name__)


# 몽고db 맥북에서 연결되는 설정으로 변경
from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://sparta:test@cluster0.okucubo.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=ca)
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

@app.route("/mars", methods=["POST"])
def mars_post():
    name_receive = request.form['name_give']
    address_receive = request.form['address_give']
    size_receive = request.form['size_give']

    doc = {
        'name':name_receive,
        'address':address_receive,
        'size':size_receive
    }
    db.mars.insert_one(doc)

    return jsonify({'msg':'저장완료!'})

@app.route("/mars", methods=["GET"])
def mars_get():
    mars_data = list(db.mars.find({},{'_id':False}))
    return jsonify({'result':mars_data})

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']

    bucket_list = list(db.bucket.find({}, {'_id': False}))
    count = len(bucket_list) + 1
    doc = {
        'num':count,  #버킷 등록 시, db에서 특정 버킷을 찾기 위해 'num' 이라는 고유 값 부여
        'bucket' :bucket_receive,
        'done' : 0   #'done' key값을 추가 해 각 버킷의 완료 상태 구분(0 = 미완료, 1 = 완료)
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    all_buckets = list(db.bucket.find({}, {'_id': False}))
    return jsonify({'result': all_buckets})


# run 내용 편의를 위해 변경_배운걸로 사용
if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)

