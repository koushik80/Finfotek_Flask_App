from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed 
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length,EqualTo,Email

from wtforms import Form,TextAreaField, SubmitField, validators, ValidationError



class ContactForm(Form):
    name = StringField("Name", validators=[DataRequired("Please enter your name"),Length(min=3,max=20)])
    email = StringField("Email",validators=[DataRequired("Please enter your email address"),Email("Please enter your email address.")])
    subject = StringField("Subject", validators=[DataRequired("Please enter a subject"),Length(min=3,max=50)])
    message = TextAreaField("Message", validators=[DataRequired("Please enter a message"),Length(min=3,max=200)])
    submit = SubmitField("Send")


class RegistrationForm(FlaskForm):
    username = StringField(label='Username',validators=[DataRequired(),Length(min=3,max=20)])
    email = StringField(label='Email',validators=[DataRequired(),Email()])
    password = PasswordField(label='Password',validators=[DataRequired(),Length(min=6,max=16)])
    confirm_password = PasswordField(label='Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField(label='Sign Up')
    
    
class LoginForm(FlaskForm):
    email = StringField(label='Email',validators=[DataRequired(),Email()])
    password = PasswordField(label='Password',validators=[DataRequired(),Length(min=6,max=16)])
    submit = SubmitField(label='Login',validators=[DataRequired()])
    
    
class ResetRequestForm(FlaskForm):
    email = StringField(label='Email',validators=[DataRequired(),Email()])
    submit = SubmitField(label='Reset Password',validators=[DataRequired()])
    
    
class ResetPasswordForm(FlaskForm):
    password = PasswordField(label='Password',validators=[DataRequired(),Length(min=6,max=16)])
    confirm_password = PasswordField(label='Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField(label='Submit',validators=[DataRequired()])
   
        
class AccountUpdateForm(FlaskForm): 
    firstname = StringField(label='First Name',validators=[DataRequired(),Length(min=3,max=20)])
    lastname = StringField(label='Last Name',validators=[DataRequired(),Length(min=3,max=20)])
    username = StringField(label='Username',validators=[DataRequired(),Length(min=3,max=20)])
    email = StringField(label='Email',validators=[DataRequired(),Email()])
    picture=FileField(label="Update Profile Picture", validators=[FileAllowed(['jpg','png'])]) 
    submit= SubmitField(label='Update Account')     
        


        
    
    
    ##extra added   

class ChangePasswordForm(FlaskForm):
    password = PasswordField(label='Password',validators=[DataRequired(),Length(min=6,max=16)])
    confirm_password = PasswordField(label='Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit= SubmitField(label='Submit',validators=[DataRequired()] )
###extra added    
        