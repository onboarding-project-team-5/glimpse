from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://yungiDB:dbsrlelql@cluster0.bpcqzfd.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('card_registeration.html')

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
    db.cards.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=7007, debug=True)