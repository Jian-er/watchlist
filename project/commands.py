import click

from project.models import User, Ariticles
from project import db, app


# 注册命令
@app.cli.command()
@click.option('--drop', is_flag=True, help='Crete after drop')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("初始化数据库")

# 自定义命令forge，把数据写入数据库
@app.cli.command()
def forge():
    db.create_all()
    name = "Akihi"
    movies = [
        {'title':'杀破狼','year':'2003'},
        {'title':'扫毒','year':'2018'},
        {'title':'捉妖记','year':'2016'},
        {'title':'囧妈','year':'2020'},
        {'title':'葫芦娃','year':'1989'},
        {'title':'玻璃盒子','year':'2020'},
        {'title':'调酒师','year':'2020'},
        {'title':'釜山行','year':'2017'},
        {'title':'导火索','year':'2005'},
        {'title':'叶问','year':'2015'}
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Ariticles(title=m['title'],year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('数据导入完成')

# 生成管理员用户
@app.cli.command()
@click.option('--username', prompt=True, help='用户名')
@click.option('--password', prompt=True, help='密码', confirmation_prompt=True, hide_input=True)
def admin(username, password):
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo("更新用户")
        user.username = username
        user.set_password(password)
    else:
        click.echo('创建用户')
        user = User(username=username, name='Akihi')
        user.set_password(password)
        db.session.add(user)
    db.session.commit()
    click.echo('完成')