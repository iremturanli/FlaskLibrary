from flask import Flask,render_template,url_for,redirect
from flask import Flask
from werkzeug import useragents
from flask_sqlalchemy import SQLAlchemy 
from flask import request
from db.library import Library, books,logrecords
import hashlib as hasher

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////home/turkai/Masaüstü/workplace/Flask/library/flasklibrarymodify/db/library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False 


db=SQLAlchemy(app)





@app.route("/",methods=["GET","POST"])
def index():
    try:
        if request.method == 'POST':

            isim=request.form.get('name')
            password=request.form.get('passw')
            # sifreleyici.update(password.encode())
            # cikti=sifreleyici.hexdigest()
            cikti=hasher.sha224(password.encode()).hexdigest()
           
            uye=Uye.query.filter_by(uye_kullaniciadi=isim,uye_sifre=cikti).first()

            if uye.uye_kullaniciadi==isim and uye.uye_sifre==cikti:
                return redirect(url_for('add'))

            else:
                mesaj="Hatalı giriş!,Tekrar deneyiniz."
                return render_template("index.html",mesaj=mesaj)            
        else:  
                 mesaj="Hoşgeldiniz."
                 return render_template("index.html",mesaj=mesaj)
    except:
        mesaj="Hatalı giriş,Tekrar deneyiniz."
        return render_template("index.html",mesaj=mesaj)


@app.route("/signup",methods=["GET","POST"])
def signup():
        username=request.form.get('uname')
        print(username)
  
    
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
        
            isim=request.form.get('name')
            sifre=request.form.get('psw')
            cikti=hasher.sha224(sifre.encode()).hexdigest()
           
            uye=Uye.query.filter_by(uye_kullaniciadi=isim,uye_sifre=cikti).first()
            if uye.uye_kullaniciadi==isim and uye.uye_sifre==cikti and uye.uye_durum==True:
                return redirect(url_for('log'))
            else:
                mesaj="Bu sayfaya erişiminiz bulunmamaktadır."
                return render_template("access.html",mesaj=mesaj)
        else:
            mesaj="Yönetici sayfasına hoşgeldiniz."
            return render_template("access.html",mesaj=mesaj)
              

    except:    
         mesaj="Hatalı giriş,tekrar deneyiniz."
         return render_template('access.html',mesaj=mesaj)




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

   
# iremt=Uye(uye_kullaniciadi="iremt",uye_sifre="1234567890",uye_durum=1)
# print(iremt.uye_sifre)
# iremt.uye_sifre=hasher.sha224(iremt.uye_sifre.encode()).hexdigest()
# iremt.addClass()
   
# user=Uye(uye_kullaniciadi="user",uye_sifre="12345",uye_durum=0)
# sifreleyici.update(user.uye_sifre.encode())
# cikti=sifreleyici.hexdigest()
# user.uye_sifre=cikti
# user.addClass()
   

# members=Uye.query.all()
# for i in range(len(members)):
#     sifreler=members[i].uye_sifre
#     sifreleyici.update(sifreler.encode())
#     cikti=sifreleyici.hexdigest()
#     print(cikti)
#     members[i].uye_sifre=cikti
#     db.session.commit()
 
   



if __name__=="__main__":
    app.run(debug=True)
    # app.run(host='192.168.1.97',debug=True, port=5000)
