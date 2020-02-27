import unittest

from project import app, db
from project.models import Movie, User

class ProjectTestCase(unittest.TestCase):

    # 测试固件
    def setUp(self):
        # 更新配置
        app.config.update(
            TESTING = True,
            SQLALCHEMY_DATABASE_URL = 'sqlte:///:memory:'
        )

        db.create_all()
        user = User(username='Test', name='Test')
        user.set_password('123456')
        movie = Movie(title='test mvoie',year='2020')

        db.session.add_all([user,movie])
        db.session.commit()

        self.client = app.test_client()  # 测试客户端
        self.runner = app.test_cli_runner()  # 创建测试命令运行器

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # 测试app是否存在
    def test_app_exist(self):
        self.assertIsNotNone(app)

    # 测试程序是否处于测试模式
    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING'])

    # 测试404
    def test_404_page(self):
        response = self.client.get('/sdfafadfsf')
        data = response.get_data(as_text=True)
        self.assertIn('404 - 页面跑丢了', data)
        self.assertIn('返回首页', data)
        self.assertEqual(response.status_code, 404)

    # 测试主页
    def test_index_page(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertIn('Test的电影列表', data)
        self.assertIn('test mvoie', data)
        self.assertEqual(response.status_code, 200)

    # 登陆 （辅助删除，编辑，添加功能）
    def test_login(self):
        self.client.post('/login',data=dict(
            username = 'Test',
            password = '123456'
        ), follow_redirects=True)

    # 删除
    def test_delte_item(self):
        self.test_login()

        response = self.client.post("/movie/delete/1",follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('删除数据成功', data)

    # 添加
    def test_add_item(self):
        self.test_login()

        response = self.client.post('/', data=dict(
            title = 'AAA',
            year = '2020'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('数据创建成功', data)

    # 编辑
    def test_edit_item(self):
        self.test_login()

        response = self.client.post('/movie/edit/1', data=dict(
            title = 'BBB',
            year = '2019'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('电影信息已经更新', data)
        self.assertIn('BBB', data)

    # 修改名字
    def test_updata_name_item(self):
        self.test_login()

        response = self.client.post('/settings', data=dict(name='Test_two'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('设置name成功', data)


if __name__ == '__main__':
    unittest.main()