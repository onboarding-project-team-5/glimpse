from flask import render_template

from db.mongo import db

def controller(app):
    
    # 404 오류 핸들러 - 잘못된 페이지로의 접근
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
