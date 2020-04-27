from flask import Flask, render_template


def create_app():
    app = Flask(__name__)
    # app.config['DEBUG'] = True
    app.config.from_pyfile('settings.py')

    @app.route('/')
    def index():
        return render_template('index.html', TITLE='Flask bootstrap')

    @app.route('/about')
    def about():
        return render_template('about.html', TITLE='Flask bootstrap')

    return app

# create_app().run('127.0.0.1', debug=True)
