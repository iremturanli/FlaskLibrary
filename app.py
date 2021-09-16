from flask import Flask,render_template,url_for,redirect
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request
from db.library import *
from db.library import Library,Log,books,logrecords
import hashlib as hasher

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////home/turkai/Masaüstü/workplace/Flask/library/flasklibrarymodify/db/library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


db=SQLAlchemy(app)

@app.route("/",methods=["GET","POST"])
def index():
    try:
        if request.method == 'POST':

            name=request.form.get('name')
            password=request.form.get('passw')
            cikti=hasher.sha224(password.encode()).hexdigest()

            uye=Uye.query.filter_by(uye_kullaniciadi=name,uye_sifre=cikti).first()

            if uye.uye_kullaniciadi==name and uye.uye_sifre==cikti:
                return redirect(url_for('add'))

            else:
                message="Wrong username or password,Try again."
                return render_template("index.html",message=message)
        else:
                 message="Welcome."
                 return render_template("index.html",message=message)
    except:
        message="Wrong username or password,Try again."
        return render_template("index.html",message=message)



@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        username=request.form.get('uname')
        password=request.form.get('psword')
        cikti=hasher.sha224(password.encode()).hexdigest()
        if 'status' in request.form:
            status=request.form['status']

        member=Uye(uye_kullaniciadi=username,uye_sifre=cikti,uye_durum=status)
        if member.uye_durum=='1':
            member.uye_durum=True
            mesaj="Your account has been successfully created!"
            member.addClass()

            return render_template("signup.html",mesaj=mesaj)
            #  return redirect(url_for('index'))

        else:
            member.uye_durum=False
            mesaj="Your account has been successfully created!"
            member.addClass()

            return render_template("signup.html",mesaj=mesaj)
        #    return redirect(url_for('index'))

    else:
        return render_template("signup.html")




@app.route("/add",methods=["GET"])
def add():

    uyeler=Uye.query.all()
    return render_template("add.html",books=books,uye=uyeler)


@app.route("/log",methods=["GET","POST"])
def log():
    return render_template("log.html",logrecords=logrecords)


@app.route("/access",methods=["GET","POST"])
def access():

    try:
        if request.method == 'POST':

            name=request.form.get('name')
            password=request.form.get('psw')
            cikti=hasher.sha224(password.encode()).hexdigest()

            uye=Uye.query.filter_by(uye_kullaniciadi=name,uye_sifre=cikti).first()
            if uye.uye_kullaniciadi==name and uye.uye_sifre==cikti and uye.uye_durum==True:
                return redirect(url_for('admin'))
            else:
                message="You do not have permission to access."
                return render_template("access.html",message=message)
        else:
            message="Welcome to admin page!"
            return render_template("access.html",message=message)


    except:
         message="Wrong password or username."
         return render_template('access.html',message=message)



@app.route("/admin", methods=["POST","GET"])
def admin():
    admins=db.session.query(Uye).filter(Uye.uye_durum==True).all()

    if request.method=="POST":
        selectAdmin=request.form.get('select')
        return render_template("admin.html",selectAdmin=selectAdmin,books=books)
 


    return render_template("admin.html",books=books,admins=admins)


@app.route("/add/delete/<string:id>",methods=["GET","POST"])
def adminDelete(id):
   
    db.session.query(Library).filter(Library.BookID==id).delete()
    db.session.commit()
    lg=Log(Library_id=id,Info='Book Deleted',Name=None,OldVersion=None,NewVersion=None)#ismial
    lg.addClass()
    db.session.commit()
    return redirect(url_for('admin'))


@app.route("/add/update/<string:id>",methods=["POST","GET"])
def adminUpdate(id):
    olddata=db.session.query(Library).filter(Library.BookID==id).one()
    oldBookname=olddata.BookName
    oldYearofPublication=olddata.Yearofpublication
    oldAuthorname=olddata.AuthorName
    oldCategory=olddata.Category
    oldAddp=olddata.Addp

    if request.method=="POST":
        UpdateBookName=request.values.get('bname')
        UpdateYear=request.values.get('yname')
        UpdateAuthorName=request.values.get('aname')
        UpdateCategory=request.values.get('cname')
        UpdatePerson=request.values.get('pname')

        l1=db.session.query(Library).filter(Library.BookID==id).one()
        l1.BookName=UpdateBookName
        l1.Yearofpublication=UpdateYear
        l1.AuthorName=UpdateAuthorName
        l1.Category=UpdateCategory
        l1.Addp=UpdatePerson
        db.session.commit()
        lg=Log(Library_id=id,Info='Book updated',Name=None,OldVersion="{},{},{},{},{}".format(oldBookname,oldYearofPublication,oldAuthorname,oldCategory,oldAddp),NewVersion="{},{},{},{},{}".format(UpdateBookName,UpdateYear,UpdateAuthorName,UpdateCategory,UpdatePerson))
        lg.addClass()
        db.session.commit()
        return render_template('update.html')
    else:
        return render_template('update.html')



class Uye(db.Model):

    uye_id=db.Column(db.Integer,primary_key=True)
    uye_kullaniciadi=db.Column(db.String,nullable=False)
    uye_sifre=db.Column(db.String,nullable=False)
    uye_durum=db.Column(db.Boolean,nullable=False)

    def __init__(self,uye_kullaniciadi,uye_sifre,uye_durum):

        self.uye_kullaniciadi=uye_kullaniciadi
        self.uye_sifre=uye_sifre
        self.uye_durum=uye_durum

    def addClass(self):
        db.session.add(self)
        db.session.commit()

db.create_all()


if __name__=="__main__":
    app.run(debug=True)
    # app.run(host='192.168.1.97',debug=True, port=5000)
