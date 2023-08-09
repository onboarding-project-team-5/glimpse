from flask import render_template

from db.mongo import db

def controller(app):
    
    # 카드 등록 페이지
    @app.route('/card/registration')
    def page_card_registration():
        return render_template('card_registeration.html')
