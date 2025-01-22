from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def my_index():

    user = {'username': 'Miguel'}
    event_list = ['Event 1', 'Event 2', 'Event 3', 'Event 4', 'Event 5']
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]

    return render_template('index.html', title='Home', user=user, posts=posts, event_list=event_list)

@app.route('/about')
def my_about():
    return render_template('about.html', title='About')