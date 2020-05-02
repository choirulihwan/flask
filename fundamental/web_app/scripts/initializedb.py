import sys,os

sys.path.append(os.getcwd() + '/web_app')

from app import create_app
from models import Page, db

app = create_app()

with app.app_context():
    page = Page()
    page.title = 'Homepage'
    page.slug = 'home'
    page.is_homepage = True

    db.session.add(page)
    db.session.commit()
