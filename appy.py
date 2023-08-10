from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://yungiDB:dbsrlelql@cluster0.bpcqzfd.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

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

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)