from flask import render_template

from db.mongo import db

def controller(app):
    
    # 개인 프로필 페이지
    @app.route('/profile/me')
    def page_profile_me():
        return render_template('profile.html')
