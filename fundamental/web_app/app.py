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

    @app.route('/testdb')
    def testdb():
        from psycopg2 import connect

        conn = connect('dbname=flask_bootstrap user=choirul password=rahasia host=postgres')

        cur = conn.cursor()
        cur.execute('select * from page')
        id, title = cur.fetchone()

        conn.close()
        return 'Output table page {} - {}'.format(id, title)

    return app

# create_app().run('127.0.0.1', debug=True)
