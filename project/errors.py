from project import app
from flask import render_template

@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(400)  # 传入要处理的错误代码
def page_not_found(e):
    return render_template('errors/400.html'), 400

@app.errorhandler(500)  # 传入要处理的错误代码
def page_not_found(e):
    return render_template('errors/404.html'), 500