#!/usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask
app = Flask(__name__)
from flask import render_template

@app.route("/")
def index():
    return 'Index Page'

@app.route("/hello")
@app.route("/hello/<name>")
def hello(name=None):
    return render_template('hello.html',name=name)

@app.route('/user/<username>')
def show_user_profile(username):
    return "User {}".format(username)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return "Post %d" % post_id
@app.route('/projects/')
def projecsts():
    return 'The Project Page'

@app.route('/about')
def about():
    return 'the about page'

if __name__ == "__main__":
    app.debug=True
    app.run(host='0.0.0.0')
