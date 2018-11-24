# -*- encoding:utf-8 -*-
# 这个 routes.py 文件主要进行url与相应网页的 map 功能

from flask import render_template
from app import app

@app.route('/')
def hello():
    user = {'username':'Daniel'}
    return render_template('indexSmart.html', user=user)

@app.route('/index')
def index():
    user = {'username':'Winchester'}
    return render_template('index.html', title='Home', user=user)

@app.route('/loopEg')
def loopEg():
    comments_list = [
        {'author': 'Mike', 'body': 'Good day is today.'},
        {'author': 'Tim', 'body': 'Beijing is a beautiful city!'}
    ]

    user = {'username': 'Winchester'}

    return render_template('loopEg.html', user=user, comments=comments_list)
