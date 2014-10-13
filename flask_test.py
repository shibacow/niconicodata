#!/usr/bin/python
# -*- coding:utf-8 -*-


from flask import Flask,redirect,flash
from flask import current_app
from flask import render_template
from flaskext.wtf import Form
from wtforms import StringField,IntegerField,TextAreaField
from wtforms.validators import Required,NumberRange

app = Flask(__name__)
app.config['SECRET_KEY']='guest'
app.config['CSRF_ENABLED']=True
with app.app_context():
    app.logger.debug(current_app.name)

class MyForm(Form):
    name = StringField('name',validators=[Required()])
    number= IntegerField('number', validators=[NumberRange(min=0, max=10)])
    queryarea=TextAreaField('query')

@app.route("/")
def index():
    return 'Index Page'

@app.route('/submit',methods=('GET','POST'))
def submit():
    form=MyForm()
    if form.validate_on_submit():
        #app.logger.debug(dir(form))
        msg="name={} number={} query={}".format(form.name.data,form.number.data,form.queryarea.data)
        app.logger.debug(msg)
        return redirect('/sucess')
    flash('fuga')
    return render_template('submit.html',form=form)

@app.route('/sucess')
def sucess():
    return 'sucess'

if __name__ == "__main__":
    app.debug=True
    app.run(host='0.0.0.0')
