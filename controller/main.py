from flask import render_template

from db.mongo import db

def controller(app):
    
    # 메인 페이지
    @app.route('/')
    def page_main():
        return render_template('index.html')
