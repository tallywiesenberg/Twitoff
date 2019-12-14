from decouple import config
from flask import Flask, render_template, request
from .model import User, Tweet, DB
from .twitter import *

def create_app():
    '''Create and configure an instance of the Flask application.'''
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['ENV'] = config('ENV')
    DB.init_app(app)

    @app.route('/')
    def root():
        users = User.query.all()
        return render_template('base.html', title='Homepage', users=users)
    
    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='DB Reset!', users=[])

    @app.route('/user/<username>')
    def load_user_tweets():
        return get_user_tweets(username)

    return app

if __name__ == "__main__":
	app = create_app()
	app.run(debug=True)