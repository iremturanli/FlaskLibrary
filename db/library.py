from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
import datetime

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////home/turkai/Masaüstü/workplace/Flask/library/flasklibrarymodify/db/library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False 

db=SQLAlchemy(app)


class Library(db.Model):

    BookID=db.Column(db.Integer,primary_key=True)
    BookName=db.Column(db.String,nullable=False)
    Yearofpublication=db.Column(db.String,nullable=False)
    AuthorName=db.Column(db.String,nullable=False)
    Category=db.Column(db.String,nullable=False)
    Addp=db.Column(db.String,nullable=False)
    Book=db.relationship("Log",backref='library')

    def __init__(self,BookName,Yearofpublication,AuthorName,Category,Addp):
        self.BookName=BookName
        self.Yearofpublication=Yearofpublication
        self.AuthorName=AuthorName
        self.Category=Category
        self.Addp=Addp


    def addClass(self):
        db.session.add(self)
        db.session.commit()


class Log(db.Model):

    BookID_log=db.Column(db.Integer,primary_key=True)
    Date=db.Column(db.String,nullable=False)
    Library_id=db.Column(db.Integer,db.ForeignKey('library.BookID'))
    Info=db.Column(db.String)
    Name=db.Column(db.String)
    OldVersion=db.Column(db.String)
    NewVersion=db.Column(db.String)

    def __init__(self,Library_id,Info,Name,OldVersion,NewVersion):
        self.Date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.Library_id=Library_id
        self.Info=Info
        self.Name=Name
        self.OldVersion=OldVersion
        self.NewVersion=NewVersion

    def addClass(self):
        db.session.add(self)
        db.session.commit()



db.create_all()

##addhtmlye gonder
Books=Library.query.all()
Logrecords=Log.query.all()

