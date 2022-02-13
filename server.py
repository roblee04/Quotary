from flask import Flask, request, send_from_directory, redirect, render_template, url_for, jsonify, session, flash
# import cv2
import os
import random
from typing import Sequence, Optional
from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:////tmp/quote.db', echo=True, connect_args={"check_same_thread": False})
Session = sessionmaker()
Base = declarative_base()
Session.configure(bind=engine)
random.seed()

class QuoteInfo(Base):
    __tablename__ = 'quoteinfo'

    quote = Column(String, primary_key=True)
    title = Column(String)
    theme = Column(String)
    pdf = Column(String)
    # quantity = Column(Integer)

    # def quote(self):
    #     return [self.quote]
    def to_list(self):
        return [self.quote, self.title, self.theme, self.pdf]


Base.metadata.create_all(engine)

class Database:
    def __init__(self):
        self.session = Session()

    def store(self, entity: QuoteInfo) -> None:
        try:
            self.session.add(entity)
            self.session.commit()
        except:
            print("We tried to add something that already exists!")
            self.session.rollback()

    def fetchall(self) -> Sequence[QuoteInfo]:
        return self.session.query(QuoteInfo).all()

    def fetch_if_exists(self, name: str) -> Optional[QuoteInfo]:
        return self.session.query(QuoteInfo).filter(QuoteInfo.name == name).first()

    def save(self) -> None:
        self.session.commit()

db = Database()


app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = 'a\xd0x\x0f\x97\xa2\x86\x7fy3\\\xa0\xfe\xcc"\x19\x15\n\xc5+\xd6\x99hb'


@app.route("/" , methods = ['GET'])
def hello_world():
    list = db.fetchall()
    all = []
    for item in list:
        all.append(item.to_list())
    index = random.randint(0,len(all)-1)
    session['index'] = index
    return render_template("page.html", row = all[index])

@app.route("/" , methods = ['POST'])
def contact():
    return redirect(url_for('info'))



@app.route("/info", methods = ['GET'])
def info():
    list = db.fetchall()
    all = []
    for item in list:
        all.append(item.to_list())
    index = session.get('index', None)
    return render_template("info.html", row = all[index])

@app.route("/info", methods = ['POST'])
def back():
    return redirect(url_for('hello_world'))




@app.route("/add", methods = ['GET'])
def addhome():
    return render_template('add.html')

@app.route("/add", methods = ['POST'])
def add():
    quote = request.form.get('quote')
    title = request.form.get('title')
    themes = request.form.get('themes')
    pdf = request.form.get('pdf')

    # if not quote:
    #     flash('Quote is blank!')
    # elif not title:
    #     flash('Title is blank!')
    # elif not themes:
    #     flash('Themes is blank!')
    # elif not pdf:
    #     flash('PDF is blank!')
    # else:
    a = QuoteInfo(quote = quote, title = title, theme = themes, pdf = pdf)
    db.store(a)

    return render_template('add.html')
