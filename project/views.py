from flask import request, flash, render_template, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user
from project import db,app
from project.models import User, Ariticles



# base
@app.route("/base")
def base():
    return render_template('base.html')


# 首页
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
        # 获取表单的数据
        title = request.form.get('title')
        year = request.form.get('year')

        # 验证title，year不为空，并且title长度不大于60，year的长度不大于4
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('输入错误')  # 错误提示
            return redirect(url_for('index'))  # 重定向回主页

        movie = Ariticles(title=title, year=year)  # 创建记录
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash('数据创建成功')
        return redirect(url_for('index'))

    ariticles = Ariticles.query.all()
    return render_template('index.html', ariticles=ariticles)


# 编辑电影信息页面
@app.route('/ariticle_id/edit/<int:ariticle_id>', methods=['GET', 'POST'])
@login_required
def edit(ariticle_id):
    ariticle = Ariticles.query.get_or_404(ariticle_id)

    if request.method == 'POST':
        title = request.form['title']
        ariticle.title = title
        db.session.commit()
        flash('电影信息已经更新')
        return redirect(url_for('index'))
    return render_template('edit.html', ariticle=ariticle_id)

@app.route('/settings',methods=['GET','POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name)>20:
            flash('输入错误')
            return redirect(url_for('settings'))

        current_user.name = name
        db.session.commit()
        flash('设置name成功')
        return redirect(url_for('index'))

    return render_template('settings.html')

# 删除信息
@app.route('/ariticle/delete/<int:ariticle_id>', methods=['POST'])
@login_required
def delete(ariticle_id):
    ariticle = Ariticles.query.get_or_404(ariticle_id)
    db.session.delete(ariticle)
    db.session.commit()
    flash('删除数据成功')
    return redirect(url_for('index'))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('输入错误')
            return redirect(url_for('login'))
        user = User.query.first()
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登录用户
            flash('登录成功')
            return redirect(url_for('index'))  # 登录成功返回首页
        flash('用户名或密码输入错误')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('退出登录')
    return redirect(url_for('index'))

@app.route("/publish", methods=['GET', 'POST'])
def publish():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
        # 获取表单的数据
        title = request.form.get('title')
        content = request.form.get('content')

        # 验证title，year不为空，并且title长度不大于60，year的长度不大于4
        if not title or len(title) > 60:
            flash('输入错误')  # 错误提示
            return redirect(url_for('index'))  # 重定向回主页

        ariticles = Ariticles(title=title, content=content,author=current_user.id)  # 创建记录
        db.session.add(ariticles)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash('数据创建成功')
        return redirect(url_for('index'))
    return render_template('publish.html')

