import os,sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'klasdjlaksd'

db = SQLAlchemy(app)

login_manager = LoginManager(app)   # 实例化扩展类
@login_manager.user_loader
def load_user(user_id):   # 创建用户加载回调函数，接受用户ID作为参数
    from  project.models import User
    user = User.query.get(int(user_id))
    return user

login_manager.login_view = 'login'
login_manager.login_message = '没有登陆'

@app.context_processor  # 模板上下文处理函数
def inject_user():
    from project.models import User
    user = User.query.first()
    return dict(user=user)

from project import views,errors,commands