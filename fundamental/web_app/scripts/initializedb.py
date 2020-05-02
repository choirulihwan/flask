import sys,os

sys.path.append(os.getcwd() + '/web_app')

from app import create_app
from models import Page, db, Menu

app = create_app()

with app.app_context():
    page = Page()
    page.title = 'Homepage'
    page.slug = 'home'
    page.content = "<h1>Bismillah</h1>"
    page.is_homepage = True
    db.session.add(page)
    db.session.commit()

    menu = Menu()
    menu.title = 'Homepage'
    menu.order = 1
    menu.page_id = page.id
    db.session.add(menu)
    db.session.commit()

    page = Page()
    page.title = 'About'
    page.slug = 'about'
    page.content = "<h1>Ini About page</h1>"
    page.is_homepage = False
    db.session.add(page)
    db.session.commit()

    menu = Menu()
    menu.title = 'About us'
    menu.order = 10
    menu.page_id = page.id
    db.session.add(menu)
    db.session.commit()
