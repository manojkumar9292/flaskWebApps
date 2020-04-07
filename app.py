from flask import Flask, render_template, request,session,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key='super-secret-key'
#app.config.update(
#    MAIL_SERVER='smtp.gmail.com',
#    MAIL_PORT='465',
#    MAIL_USE_SSL=True,
#    MAIL_USERNAME=params['gmail-user'],
#   MAIL_PASSWORD=params['gmail-password']
#)
#mail = Mail(app)

#replace below uri with prod uri
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sql9330142:sInQaajpWF@db4free.net:3306/sql9330142'
db = SQLAlchemy(app)


class Contacts(db.Model):
    '''
    sno, name phone_num, msg, date, email
    '''
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)

class Config(db.Model):
    '''
    sno,prod_uri, fb_uri,tw_uri,git_uri,heading_text,blogname,about_text
    '''
    sno = db.Column(db.Integer, primary_key=True)
    prod_uri = db.Column(db.String(100), nullable=False)
    fb_uri = db.Column(db.String(100), nullable=False)
    tw_uri = db.Column(db.String(100), nullable=False)
    git_uri = db.Column(db.String(120), nullable=False)
    heading_text = db.Column(db.String(100), nullable=True)
    blogname = db.Column(db.String(100), nullable=False)
    about_text = db.Column(db.String(100), nullable=False)
    midhead_text = db.Column(db.String(100), nullable=False)
    lefttop_text = db.Column(db.String(100), nullable=False)

class User(db.Model):
    '''
    sno, username, pass, pin
    '''
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    passwords = db.Column(db.String(20), nullable=False)
    pin = db.Column(db.Integer, primary_key=True)

class Posts(db.Model):
    '''
    sno, name phone_num, msg, date, email,img_file,category
    '''
    sno = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(30), nullable=False)
    content = db.Column(db.String(300), nullable=False)
    tagline = db.Column(db.String(120), nullable=False)
    img_file = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    category = db.Column(db.String(12), nullable=True)

cc=Config.query.filter_by().first() 
@app.route("/")
def home():
    posts= Posts.query.filter_by().all()
    ts=set([])
    for cat in posts:
        ts.add(cat.category)
    return render_template('index.html',posts=posts,ts=ts,cc=cc)

@app.route("/seg/<string:urls>",methods=['GET'])
def seg_url(urls):
    print(urls)
    posts = Posts.query.filter_by(category=urls).all()
    pcat= Posts.query.filter_by().all()
    tsg=set([])
    for cat in pcat:
        tsg.add(cat.category)
    return render_template('seg.html',posts=posts,tsg=tsg,cc=cc)

@app.route("/about")
def about():
    return render_template('about.html',cc=cc)

@app.route("/dashboard" ,methods=['GET', 'POST'])
def dashboard():
    users=User.query.filter_by().all()
    tused=[]
    for used in users:
        tused.append(used.username)
    if(('user' in session )and (session['user'] in tused)):
        posts = Posts.query.all()
        return render_template('dashboard.html',cc=cc, posts=posts)

    if request.method == 'POST':
        usernames = request.form.get('uname')
        userpass = request.form.get('pass')
        pass1=User.query.filter_by(username=usernames).first()
        if(usernames in tused and userpass==pass1.passwords):
            session['user'] = usernames
            posts = Posts.query.filter_by().all()
            return render_template('dashboard.html',cc=cc, posts=posts)
        
    return render_template('login.html',cc=cc)

@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name, phone_num = phone, msg = message, date= datetime.now(),email = email)
        db.session.add(entry)
        db.session.commit()
        #mail.send_message('New Message from blog'+ name,sender=email,recipients=[params['gmail-user']],
        #                 body = message + "\n" + phone
        #                )
        
    return render_template('contact.html',cc=cc)

@app.route("/post/<string:post_slug>",methods=['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', post=post,cc=cc)

@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/dashboard')


@app.route("/edit/<string:sno>", methods = ['GET', 'POST'])
def edit(sno):
    users=User.query.filter_by().all()
    tused=[]
    for used in users:
        tused.append(used.username)
    if('user' in session and session['user'] in tused):
        if request.method == 'POST':
            tlines = request.form.get('tline')
            slugs = request.form.get('slug')
            contents = request.form.get('content')
            category = request.form.get('category')
            date=datetime.now()
            if sno!='0':
                post = Posts.query.filter_by(sno=sno).first()
                post.slug = slugs
                post.content = contents
                post.tagline = tlines
                post.category=category
                post.img_file=0
                post.date = date
                db.session.commit()
                return redirect('/edit/'+ sno)
        post = Posts.query.filter_by(sno=sno).first()            
        return render_template('edit.html',post=post,cc=cc)
        

@app.route("/addpost/<string:sno>", methods = ['GET', 'POST'])
def addpost(sno):
    sn=Posts.query.filter_by().all()
    tsno=[]
    for snos in sn:
        tsno.append(snos.sno)
    maxsno=max(tsno)
    nextsno=maxsno+1
    users=User.query.filter_by().all()
    tused=[]
    for used in users:
        tused.append(used.username)
    if('user' in session and session['user'] in tused):
        if request.method == 'POST':
            #snos = request.form.get('sno')
            tlines = request.form.get('tline')
            slugs = request.form.get('slug')
            contents = request.form.get('content')
            category = request.form.get('category')
            date=datetime.now()
            if sno=='0':
                post = Posts(sno=nextsno,category=category,tagline=tlines,slug=slugs,content=contents,date=date,img_file=0)
                db.session.add(post)
                db.session.commit()
                return redirect('/addpost/'+ sno)
        return render_template('addpost.html',sno=sno,cc=cc)
@app.route("/delete/<string:sno>", methods = ['GET', 'POST'])
def delete(sno):
    users=User.query.filter_by().all()
    tused=[]
    for used in users:
        tused.append(used.username)
    if('user' in session and session['user'] in tused):
        post = Posts.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
    return redirect('/dashboard' )
       

