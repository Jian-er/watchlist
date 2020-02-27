from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    name = 'Akihi'
    movies = [
        {'title': 'python', 'year': '2003'},
        {'title': 'C', 'year': '2018'},
        {'title': 'java', 'year': '2016'},
        {'title': '囧妈', 'year': '2020'},
        {'title': '葫芦娃', 'year': '1989'},
        {'title': '玻璃盒子', 'year': '2020'},
        {'title': '调酒师', 'year': '2020'},
        {'title': '釜山行', 'year': '2017'},
        {'title': '导火索', 'year': '2005'},
        {'title': '叶问', 'year': '2015'}
    ]
    return render_template('index.html', name=name, movies=movies)