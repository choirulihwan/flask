
from flask import Flask, render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from web_app.models import db, Page, Menu
from web_app.views import PageAdminView

def create_app():
    app = Flask(__name__)
    # app.config['DEBUG'] = True
    app.config.from_pyfile('settings.py')

    # import model
    db.init_app(app)

    #flask admin
    admin = Admin(app, name="Flask Bootsrap", template_mode='bootstrap3')

    admin.add_view(PageAdminView(Page, db.session))
    admin.add_view(ModelView(Menu, db.session))

    @app.route('/')
    @app.route('/<slug>')
    def index(slug=None):

        if slug is not None:
            page = Page.query.filter_by(slug=slug).first()
        else:
            page = Page.query.filter_by(is_homepage=True).first()

        content = ''
        if page is not None:
            content = page.content
        else:
            return 'Page not found for {} or homepage not set'.format(slug)

        menu = Menu.query.order_by('order').all()
        return render_template('index.html', TITLE='Flask bootstrap', CONTENT=content, MENU=menu)

    # @app.route('/about')
    # def about():
    #     return render_template('about.html', TITLE='Flask bootstrap')
    #
    # @app.route('/testdb')
    # def testdb():
    #     from psycopg2 import connect
    #
    #     conn = connect('dbname=flask_bootstrap user=choirul password=rahasia host=postgres')
    #
    #     cur = conn.cursor()
    #     cur.execute('select id, title from page')
    #     id, title = cur.fetchone()
    #
    #     conn.close()
    #     return 'Output table page {} - {}'.format(id, title)

    return app

# create_app().run('127.0.0.1', debug=True)
