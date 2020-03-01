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
    user = User(name=name)
    db.session.add(user)
    db.session.commit()

    ariticles = [
        {'title':'杀破狼','content':'111111111'},
        {'title':'扫毒','content':'222222222222'},
        {'title':'捉妖记','content':'33333333333'},
        {'title':'囧妈','content':'4444444444'},
        {'title':'葫芦娃','content':'55555555'},
        {'title':'玻璃盒子','content':'6666666'},
        {'title':'调酒师','content':'7777777'},
        {'title':'釜山行','content':'88888888'},
        {'title':'导火索','content':'99999999'}
    ]
    for a in ariticles:
        ariticle = Ariticles(title=a['title'],content=a['content'], author=User.query.first().id)
        db.session.add(ariticle)
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