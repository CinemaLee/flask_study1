from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() # db사용을 위한 변수.


class Fcuser(db.Model):
    __tablename__ = 'fcuser'
    id=db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(64))
    userid = db.Column(db.String(32))
    username = db.Column(db.String(8))