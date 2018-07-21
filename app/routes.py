from flask import render_template_string, render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Beau'}
    result = ''
    with open('app/static/test.html','r') as htmlfile:
        result = str(htmlfile.read())
    return render_template_string(result,user=user,title='Home')