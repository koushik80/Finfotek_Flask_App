from typing import Any
from finfotek import app,db,bcrypt, mail
from flask import render_template, url_for,redirect,flash,request,Flask
from finfotek.forms import AccountUpdateForm, RegistrationForm,LoginForm, ResetRequestForm, ResetPasswordForm, ChangePasswordForm
from finfotek.models import User, UserDetails
from flask_login import login_user,logout_user,current_user,login_required
from flask_mail import Message,Mail
import os

from finfotek.forms import ContactForm


@app.route('/')

@app.route('/index')
def index():
    return render_template('index.html',title='Home')

@app.route('/layouts')
def layouts():
    return render_template('layouts.html',title='Layouts')


@app.route('/about')
def about():
    return render_template('about.html',title='About')

def save_image(picture_file):
    picture_name=picture_file.filename
    picture_path=os.path.join(app.root_path,'static/profile_pics', picture_name)
    picture_file.save(picture_path)
    return picture_name

@app.route('/account',methods=['POST','GET'])
@login_required
def account():
    form=AccountUpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            image_file=save_image(form.picture.data)
            current_user.image_file=image_file
        current_user.username=form.username.data
        current_user.email=form.email.data
        user_details=UserDetails(firstname=form.firstname.data,lastname=form.lastname.data,user_id=current_user.id)
        db.session.add(user_details)
        db.session.commit()
        return redirect(url_for('account'))
    elif request.method=="GET":
        form.username.data=current_user.username
        form.email.data=current_user.email
        form.firstname.data=current_user.details[-1].firstname
        form.lastname.data=current_user.details[-1].lastname
    image_url=url_for('static',filename='profile_pics/'+current_user.image_file)
    return render_template('account.html',title='Account',legend='ACCOUNT DETAILS',form=form,image_url=image_url)

@app.route('/blog')
def blog():
    return render_template('blog.html',title='Blog')




@app.route('/price')
def price():
    return render_template('price.html',title='Price')

@app.route('/services')
def services():
    return render_template('services.html',title='Services')

@app.route('/single')
def single():
    return render_template('single.html',title='Featured Article')


@app.route('/register',methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form=RegistrationForm()
    if form.validate_on_submit():
        encrypted_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=encrypted_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created successfully for {form.username.data}', category='success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)


@app.route('/login',methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            flash(f'Login successful for {form.email.data}''!', category='success')
            return redirect(url_for('account'))
        else:
            flash(f'Login unsuccessful for {form.email.data}', category='danger')
    return render_template('login.html',title='Login',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

def send_mail(user):
    token=user.get_token()
    msg=Message('Password Reset Request',recipients=[user.email],sender='noreply@finfotek.com')
    msg.body=f''' To reset your password please follow the link below.

    {url_for('reset_token',token=token,_external=True)}

    If you didn't send a password reset request, please ignore this message.

    '''
    mail.send(msg)

@app.route('/reset_password',methods=['GET','POST'])
def reset_request():
    form=ResetRequestForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user:
            send_mail(user)
        flash('Reset request sent. Check your mail.','success')
        return redirect (url_for('login'))
    return render_template('reset_request.html',title='Reset Request',form=form,legend="RESET PASSWORD")

@app.route('/reset_password/<token>',methods=['GET', 'POST'])
def reset_token(token):
    user=User.verify_token(token)
    if user is None:
        flash('That is invalid token or expired. Please try again.','warning')
        return redirect(url_for('reset_request'))

    form=ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password=hashed_password
        db.session.commit()
        flash('Password changed! Please login!','success')
        return redirect(url_for('login'))
    return render_template('change_password.html',title='Change Password', legend="CHANGE PASSWORD",form=form)

## extra added

@app.route('/change_password',methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm()
    return render_template('change_password.html',title='Change Password',form=form)
##extra added

##contact form
@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()

  if request.method == 'POST':

    if form.validate():
      db.session.commit()  
      flash('All fields are required.')
      return render_template('contact.html', form=form)
  
    else:
       msg = Message(form.subject.data, sender='finfotek80@gmail.com', recipients=['unsatisfiedsoul@gmail.com'])
       msg.body = """
       From: %s <%s>
      %s
      """ % (form.name.data, form.email.data, form.message.data)
       mail.send(msg)
       
       return render_template('contact.html', success=True)

  elif request.method == 'GET':
    return render_template('contact.html', form=form)
