from flask import render_template

from db.mongo import db

def controller(app):
    
    # 회원가입, 로그인 페이지
    @app.route('/signup')
    def page_signup():
        return render_template('signup.html')
