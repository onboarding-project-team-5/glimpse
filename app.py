from flask import Flask, render_template
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

# 메인 페이지 - 유저리스트 카드 만들기
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

## Profile Cards들을 리스팅
@app.route("/movie", methods=["GET"])
def cards_get():
    ## DB에서 영화를 가져다가 내려줘야한다
    all_movies = list(db.movies.find({},{'_id':False}))

    # 내려주기
    return jsonify({'result':all_movies, 'msg': '리스팅 완료'})


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
 