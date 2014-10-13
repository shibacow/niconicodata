#!/usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask,redirect,flash
from flask import current_app
from flask import render_template
from flaskext.wtf import Form
from wtforms import StringField,IntegerField,TextAreaField
from wtforms.validators import Required,NumberRange
import sys
import os
_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_dir)
import bq_client
import time
import pprint

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
      bq=bq_client.BQClient()
      sql=form.queryarea.data
      bq.insertQuery(sql)
      while not bq.isStatusDone():
         time.sleep(1)
      is_ok,results,errors=bq.getResults()
      if is_ok:
         for r in results:
            msg=pprint.pformat(r)
            app.logger.debug(msg)
      else:
         msg=pprint.pformat(errors)
         app.logger.error(msg)
   return render_template('submit.html',form=form)

@app.route('/sucess')
def sucess():
    return 'sucess'

if __name__ == "__main__":
    app.debug=True
    app.run(host='0.0.0.0')
