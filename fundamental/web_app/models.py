from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey

# db = SQLAlchemy(app)
from sqlalchemy.orm import relationship, backref

db = SQLAlchemy()

class Page(db.Model):
    __tablename__ = 'page'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    slug = Column(String)
    content = Column(String)

    def __repr__(self):
        return self.title

class Menu(db.Model):
    __tablename__ = 'menu'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    order = Column(Integer)

    page_id = Column(Integer, ForeignKey('page.id'))
    page = relationship('Page', backref=backref('from menu'))

    def __repr__(self):
        return self.title


# db.create_all()