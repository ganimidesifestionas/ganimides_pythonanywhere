"""
Controllers (Routes) and views for the flask application.(authorization)
"""
import os
import requests
import json
import time
import inspect
from datetime import datetime

# Import flask dependencies
from flask import Flask
from flask import flash
from flask import render_template
from flask import request, make_response, jsonify, redirect, url_for
from flask import g, session, abort, Response
from flask import Blueprint

from flask import current_app as app
from flask_login import current_user, login_required, login_user, logout_user
#from flask import after_request

# Import password / encryption helper tools
#from werkzeug import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from .. external_services.email_services import send_email
from .. external_services.token_services import generate_confirmation_token, confirm_token, generate_mobileconfirmation_code

# Import module forms
from . forms import LoginForm, RegistrationForm, PasswordChangeForm, mobileConfirmationForm, UserProfileDisplayForm, UserProfileChangeForm,emailConfirmationForm,PasswordReSetForm,forgetPasswordForm,ContactUsForm,AvatarUploadForm

# Import module models (i.e. User)
from . models import Subscriber,ContactMessage,User

#from .. import db

# Define the blueprint: 'authorization', set its url prefix: app.url/authorization
authorization = Blueprint('authorization', __name__, url_prefix='/authorization')
#from . import module_authorization as authorization

from .. import db
# Import the database object from the main app module
#from app import db


#from flask_recaptcha import ReCaptcha


#from serializer import serializer
#from myApp import db, login_manager
#from myApp import db
#from . models import Subscriber,ContactMessage
#from . import authorization
#from . forms import LoginForm, RegistrationForm, SubscriberForm, PasswordChangeForm, mobileConfirmationForm, UserProfileDisplayForm, UserProfileChangeForm,emailConfirmationForm,PasswordReSetForm,forgetPasswordForm,ContactUsForm,AvatarUploadForm
#from . import authorization
#from json2html import *
#from .. models import Subscriber,ContactMessage
#db=sqlalchemy(app)
#from werkzeug.utils import secure_filename
#from ..external_services.python_debug_utilities.python_debug_utilities import *
#from myApp.external_services.email_services import send_email
#from myApp.external_services.token_services import generate_confirmation_token,confirm_token,generate_mobileconfirmation_code
#from .. service_bus import *
#from flask import Flask, redirect, url_for, session, request
#from flask_oauth import OAuth
#from . import auth
#from . import app
#recaptcha = ReCaptcha(app=app)
#app1=current_app.app_context()._get_current_object()
#app1=current_app.app_context()
#app2=app1._get_current_object()
#app1 = app._get_current_object()



###########################################################################
###########################################################################
###########################################################################
### functions used
###########################################################################
###########################################################################
###########################################################################

def init_active_menuoptions():
    app.login_active=''
    app.register_active=''
    app.help_active=''

def init_form_options():
    try:
        dummy=app.lastpage
    except:
        app.lastpage='homepage'
    try:
        dummy=app.lastpage_html
    except:
        app.lastpage_html='page_templates/landing_page.html'
    try:
        dummy=app.pages
    except:
        app.pages='homepage'

def getConfig(key):
    with app.app_context():
        if key in app.config:
            return app.config.get(key)
        else:
            raise Exception("config key:"+key+" not found...")

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (getattr(form, field).label.text,error),'error')


def send_mobileconfirmation_sms(code):
    """ Send a mobile confirmation Code via SMS
    """
    subscriber = Subscriber.query.filter_by(id=current_user.id).first()
    subscriber.mobileConfirmationCode=code
    subscriber.mobileConfirmationCodeDT=datetime.now()
    subscriber.mobileConfirmed=False
    subscriber.mobileConfirmedDT=None
    db.session.commit()
    sms_message = render_template('autorization/sms_templates/sms_mobile_confirmation.html', verification_code=code)
    smsfrom = 'Ganimides'
    #result=send_sms(subscriber.mobile,smsfrom,sms_message)
    subject = "please confirm your mobile"
    result=send_email(subscriber.email,subject,sms_message)
    return(result)

def send_email_test(email):
    """ Send a test email
    """
    token = generate_confirmation_token(email)
    confirm_url = url_for('authorization.emailconfirm', token=token, _external=True)
    html = render_template('autorization/email_templates/email_confirmation_email.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    result=send_email(email, subject, html)
    return result

def send_emailconfirmation_email(email):
    """ Send an email confirmation email
    """
    subscriber = Subscriber.query.filter_by(email=email).first()
    if not(subscriber):
        return 'email not found'
    subscriber.emailConfirmed=False
    subscriber.emailConfirmedDT=None
    db.session.commit()
    token = generate_confirmation_token(subscriber.email)
    confirm_url = url_for('authorization.emailconfirm', token=token, _external=True)
    html = render_template('autorization/email_templates/email_confirmation_email.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    result=send_email(subscriber.email, subject, html)
    return result

def send_passwordreset_email(parEmail):
    """ Send a password reset email
    """
    token = generate_confirmation_token(parEmail)
    confirm_url = url_for('authorization.passwordresetverification', token=token, _external=True)
    html = render_template('autorization/email_templates/email_passwordreset_email.html', confirm_url=confirm_url)
    subject = "Password Reset"
    result=send_email(parEmail, subject, html)
    return result

def send_messagereceiveconfirmation_email(paremail,parcontactid):
    """ Send an email to confirm message receive
    """
    tokenStr=str(parcontactid)+'-'+paremail
    token = generate_confirmation_token(tokenStr)
    confirm_url = url_for('authorization.contactemailverification', token=token, _external=True)
    html = render_template('autorization/email_templates/email_messagereceive_confirmation.html', confirm_url=confirm_url,referenceid=parcontactid)
    subject = "message receive confirmation"
    result=send_email(paremail, subject, html)
    return result

def is_human(captcha_response):
    """ Validating recaptcha response from google server
        Returns True captcha test passed for submitted form else returns False.
    """
    secret=app.config.get('RECAPTCHA_SECRET_KEY')
    #print('   ###GOOGLE_RECAPTCHA_CHECKBOX_SECRETKEY=',secret)
    payload = {'response':captcha_response, 'secret':secret}
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
    response_text = json.loads(response.text)
    return response_text['success']

def fillin_profile_forms(subscriber,profileDisplayForm,profileChangeForm,emailConfirmForm,mobileConfirmForm,passwordchangeForm,avatarUploadForm):
    print('   @@@fillin_profile_forms--->')
    #profileDisplayForm = UserProfileDisplayForm()
    #profileChangeForm = UserProfileChangeForm()
    #emailConfirmForm = emailConfirmationForm()
    #mobileConfirmForm = mobileConfirmationForm()
    #passwordchangeForm=passwordchangeForm()
    #avatarUploadForm=AvatarUploadForm()

    print('   ---userid=',current_user.id)
    subscriber = Subscriber.query.filter_by(id=current_user.id).first()
    print('   ---subscriber=',subscriber)
    # handle nulls
    if not(subscriber.firstName):
        subscriber.firstName=''
        #db.session.commit()
    if not(subscriber.lastName):
        subscriber.lastName=''
        #db.session.commit()
    if not(subscriber.mobile):
        subscriber.mobile=''
        #db.session.commit()
    if not(subscriber.userName):
        subscriber.userName=''
        #db.session.commit()

    profileDisplayForm.email.data=subscriber.email
    profileDisplayForm.firstName.data=subscriber.firstName
    profileDisplayForm.lastName.data=subscriber.lastName
    profileDisplayForm.company.data=subscriber.company
    profileDisplayForm.jobTitle.data=subscriber.jobTitle
    profileDisplayForm.mobile.data=subscriber.mobile
    profileDisplayForm.userName.data = subscriber.userName
    profileDisplayForm.registered.data = str(subscriber.registeredDT)
    profileDisplayForm.termsAgreed.data=str(subscriber.agreeTermsDT)
    profileDisplayForm.mailingListSignUp.data = str(subscriber.mailingListSignUpDT)
    profileDisplayForm.lastLogin.data = str(subscriber.lastLoginDT)
    profileDisplayForm.mobileConfirmed.data = str(subscriber.mobileConfirmedDT)
    profileDisplayForm.emailConfirmed.data = str(subscriber.emailConfirmedDT)
    print('   ---profileDisplayForm=',profileDisplayForm);

    profileChangeForm.email.data = subscriber.email
    profileChangeForm.firstName.data = subscriber.firstName
    profileChangeForm.lastName.data = subscriber.lastName
    profileChangeForm.company.data=subscriber.company
    profileChangeForm.jobTitle.data=subscriber.jobTitle
    profileChangeForm.mobile.data=subscriber.mobile
    profileChangeForm.userName.data = subscriber.userName
    profileChangeForm.mailingListSignUp.data=subscriber.mailingListSignUp
    print('   ---profileChangeForm=',profileChangeForm);

    emailConfirmForm.email.data = subscriber.email
    print('   ---emailConfirmForm=',emailConfirmForm);
    mobileConfirmForm.mobile.data = subscriber.mobile
    mobileConfirmForm.mobile_token.data = ''
    print('   ---mobileConfirmForm=',mobileConfirmForm);

    passwordchangeForm.email.data = subscriber.email
    print('   ---passwordchangeForm=',passwordchangeForm);
    
    avatarUploadForm.photo.data=subscriber.avatarImageFile
    print('   ---avatarUploadForm=',avatarUploadForm);

    return('OK')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
###########################################################################
###########################################################################
###########################################################################

##########################################
#put this after @ decorator
##########################################
#how to get a config variable app.config.get('GOOGLE_RECAPTCHA_CHECKBOX_SITE_KEY'))
#how to get a config variable app.config.get('GOOGLE_RECAPTCHA_CHECKBOX_SECRET_KEY'))

#request.method:              GET
#request.url:                 http://127.0.0.1:5000/alert/dingding/test?x=y
#request.base_url:            http://127.0.0.1:5000/alert/dingding/test
#request.url_charset:         utf-8
#request.url_root:            http://127.0.0.1:5000/
#str(request.url_rule):       /alert/dingding/test
#request.host_url:            http://127.0.0.1:5000/
#request.host:                127.0.0.1:5000
#request.script_root:
#request.path:                /alert/dingding/test
#request.full_path:           /alert/dingding/test?x=y

#request.args:                ImmutableMultiDict([('x', 'y')])
#request.args.get('x'):       y
##########################################


#varPageName = request.args.get('url')
#alert(varPageName)
#print('xxxrequestxxxxxxx',varPageName)
#print('xxxqqqqxxxxxxx',e)
#return render_template('404.html'), 404
#print ('xxxx:',request)
###########################################################################
###########################################################################
###########################################################################
### define the routes, accepted methods (GET/POST) and the service function
###########################################################################
###########################################################################
###########################################################################
#@authorization.after_request
#def store_visted_urls():
#    session['urls'].append(request.url)
#    if(len[session['urls']) > 5:
#        session['urls'].pop(0)
#    session.modified = True

#@authorization.after_request

#@authorization.route('/pictures/<path:imagefile>')
#def pathtoimage(imagefile):
    #print('request-/:',request.url)
#    return request.url+'/'+imagefile

@authorization.route('/', methods=['GET', 'POST'])
def homepageredirect():
    return redirect(url_for('homepage'))

@authorization.route('/contactemailverification/<token>')
#@login_required
def contactemailverification(token):
    app.pages=app.pages+" / " +"email verification"
    print('CONTACT-EMAIL-VERIFICATION',request.method," token=",token,request.url)
    try:
        tokenStr = confirm_token(token,3600)
    except:
        flash('The link is invalid or has expired.Retry', 'warning')
        return redirect(url_for('homepage'))

    if not(tokenStr):
        flash('The link is invalid or has expired.Retry', 'warning')
        return redirect(url_for('homepage'))

    print('tokenStr',tokenStr)
    x=tokenStr.split('-',1)
    contactID=x[0]
    print('CONTACT-ID',contactID)
    contactmessage=ContactMessage.query.filter_by(id=contactID).first_or_404()
    if not(contactmessage):
        flash('The link is invalid or has expired.Retry', 'warning')
        return redirect(url_for('homepage'))
    contactmessage.confirmed=True
    contactmessage.confirmedDT=datetime.now()
    db.session.commit()
    flash('Your Message has been received. We will contact You ASAP.', 'success')
    subscriber = Subscriber.query.filter_by(email=contactmessage.email).first()
    if subscriber is None:
        # add as subscriber
        subscriber = Subscriber(
            email=contactmessage.email
            ,firstName=contactmessage.firstName
            ,lastName=contactmessage.lastName
            ,jobTitle=contactmessage.jobTitle
            ,company=contactmessage.company
            ,registeredDT=datetime.now()
            )
        subscriber.mobile=''
        subscriber.userName=''
        subscriber.confirmed=None
        subscriber.confirmedDT=None

        db.session.add(subscriber)
        db.session.commit()
        flash('You email has been registered!','success')
    else:
        if not(subscriber.emailConfirmed):
            #confirm the susbscriber
            subscriber.emailConfirmed = True
            subscriber.emailConfirmedDT = datetime.now()
            #db.session.add(subscriber)
            db.session.commit()
            flash('You have confirmed your Email. Thanks!', 'success')

    return redirect(url_for('homepage'))

@authorization.route('/myBank')
@login_required
def myBank():
    app.pages=app.pages+" / " +"my Bank"
    print('MYBANK',request.method,request.url)
    """Renders the app(myBank) home page."""
    return render_template(
        'mybank/mybank_index.html'
        ,title='myBank'
        ,pages=app.pages
        ,message='open banking prototype........'
    )

@authorization.route('/myGame')
def myGame():
    print('MYGAME',request.method,request.url)
    """Renders the app(myBank) home page."""
    return render_template(
        'myGame/myGame.html'
        ,title='myGame'
        ,pages=app.pages
        ,message='gaming prototype........'
    )

@authorization.route('/register', methods=['GET', 'POST'])
def register():
    app.pages="register"
    print('REGISTER',request.method,request.url)
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            captcha_response = request.form['g-recaptcha-response']
        except:
            captcha_response = '????'
        if not(is_human(captcha_response)):
            # Log invalid attempts
            flash('Sorry ! Bots are not allowed.','error')
        else:
            # Process request here
            print('   ###',"Recaptcha OK, Login Details submitted successfully.")
            #flash('Recaptcha OK, Login Details submitted successfully.','success')
            subscriber = Subscriber.query.filter_by(email=form.email.data).first()
            if subscriber :
                flash('You are already registered!','warning')
                return redirect(url_for('authorization.login'))
            
            subscriber = Subscriber(
                email=form.email.data
                ,firstName=form.firstName.data
                ,lastName=form.lastName.data
                ,password=form.password.data
                ,registeredDT=datetime.now()
                ,userName=form.userName.data
                ,mobile=form.mobile.data
                )
            #subscriber.mobile=''
            #subscriber.userName=''
            if subscriber.userName:
                if Subscriber.query.filter_by(userName=subscriber.userName).first():
                    subscriber.userName=subscriber.userName+'01'

            print('###--->subscriber-add to db')
            # add subscriber to the database
            db.session.add(subscriber)
            print('###--->subscriber-commit db')
            db.session.commit()
            flash('You have successfully registered!','success')
            print('###--->add subscriber ok')
            #flash("invalid email or password",'error')

            # genereate an email activation code
            result=send_emailconfirmation_email(subscriber.email)
            if result!='OK':
                #error_text=result.dumps()
                ErrorMsg='Failed to send confirmation email. Request a New Confirmation Email'
                flash(ErrorMsg, 'error')
            else:
                flash('an activation email has been sent to {}.'.format(subscriber.email),'warning')
                flash('open this email and click the provided link in order to activate Your account','info')
                print(' activation email send.###redirect to login')
                return redirect(url_for('authorization.login'))
    else:
        # flash the errors if not already registered
        is_already_registered=False
        for msg in form.email.errors:
            if "is already in use" in msg:
                is_already_registered=True
        if not(is_already_registered):
            flash_errors(form)

    # load registration template
    return render_template('authorization/authorization_forms_template.html'
                            ,login_form=LoginForm()
                            ,registration_form=form
                            ,activeTAB='register'
                            ,title='login/Register'
                            ,formPage='form_register.html'
                           )

@authorization.route('/login', methods=['GET', 'POST'])
def login():
    init_active_menuoptions()
    app.pages="login"
    app.login_active='active'
    print('LOGIN',request.method,request.url)
    try:
        dummy=app.lastpage
    except:
        app.lastpage='homepage'
    print('LOGIN',request.method,'lastpage',app.lastpage)
    print('LOGIN',request.method,'splash_form',app.splash_form)
    #if request.method=='POST':
    #    app.splash_form='login'
    form = LoginForm()
    if form.validate_on_submit():
        print('LOGIN',request.method,'NO-ERRORS----')
        #print('recaptcha=',form.recaptcha)
        #recaptcha method1 OK. thanks google
        #captcha_response = request.form['g-recaptcha-response']
        #print('   captcha_response = ',captcha_response)
        try:
            captcha_response = request.form['g-recaptcha-response']
        except:
            captcha_response = '????'
        if not(is_human(captcha_response)):
           # Log invalid attempts
            flash("Sorry ! Bots are not allowed.",'error')
        else:
           #Process request here
           #print('   ###',"Recaptcha OK, Login Details submitted successfully.")
           #flash("Recaptcha OK, Login Details submitted successfully.",'success')
           subscriber = Subscriber.query.filter_by(email=form.email.data).first()
           #print('   ###----',"Subscriber",subscriber)
           if subscriber is None:
                #form.email.errors.append("invalid email or password")
                #form.password.errors.append("invalid email or password")
                flash("invalid email or password",'error')
           else:
               if not(subscriber.emailConfirmed):
                    #print('   ###----EMAIL NOT CONFIRMED',subscriber.email)
                    #form.email.errors.append("please Activate Your Email before Login")
                    flash("please Activate Your Email before Login","error")
                    return redirect(url_for('authorization.emailconfirmrequest', email=subscriber.email))
               else:
                    if subscriber.verify_password(form.password.data):
                        subscriber.lastLoginDT=datetime.now()
                        db.session.commit()
                        # login the user
                        login_user(subscriber)
                        flash('You have successfully logged-in as {}.'.format(form.email.data),'success')
                        # redirect to the appropriate dashboard page
                        #app.splash_form=''
                        if subscriber.isAdmin:
                            return redirect(url_for('authorization.admin_dashboard'))
                        else:
                            # SUCCESS!!! send to the last page
                            return redirect(url_for(app.lastpage))
                    else:
                        #form.email.errors.append("invalid email or password")
                        #form.password.errors.append("invalid email or password")
                        flash("invalid email or password",'error')
    else:    
        print('LOGIN',request.method,'--ERRORS--')
        #app.splash_form='login'
        #print('==============SPLASH_FORM= ',app.splash_form)
        #return redirect(url_for(app.lastpage))

    #print('LOGIN',request.method,'splash_form',app.splash_form)
    #load login page
    return render_template('authorization/authorization_forms_template.html'
                            ,login_form=form
                            ,registration_form=RegistrationForm()
                            ,activeTAB='login'
                            ,title='login'
                            ,formPage='form_login.html'
                           )


@authorization.route('/login_or_register/<action_tab>', methods=['GET', 'POST'])
def login_or_register(action_tab):
    app.pages="login or register"
    print('LOGIN_OR_REGISTER',request.method,'action_tab=',action_tab,request.url)
    form = LoginForm()
    if form.validate_on_submit():
        subscriber = Subscriber.query.filter_by(email=form.email.data).first()
        if subscriber is None:
            form.email.errors.append("invalid email or password")
            form.password.errors.append("invalid email or password")
        else:
            if not(subscriber.verify_password(form.password.data)):
                form.email.errors.append("invalid email or password")
                form.password.errors.append("invalid email or password")
            else:
                subscriber.lastLoginDT=datetime.now()
                db.session.commit()
                # login the user
                login_user(subscriber)
                # redirect to the appropriate dashboard page
                if subscriber.isAdmin:
                    return redirect(url_for('authorization.admin_dashboard'))
                else:
                    return redirect(url_for('homepage'))
    # load login/registration template
    return render_template('authorization/authorization_forms_template.html'
                            ,login_form=form
                            ,registration_form=RegistrationForm()
                            ,activeTAB=action_tab
                            ,title='login/Register'
                            ,formPage='login_or_register.html'
                           )

@authorization.route('/logout')
@login_required
def logout():
    app.pages=app.pages+" / " +"logout"
    print('LOGOUT',request.method,request.url)
    logout_user()
    flash('You have successfully logged out.','success')
    try:
        dummy=app.lastpage
    except:
        app.lastpage='homepage'
    # redirect to lastpage or login page
    return redirect(url_for(app.lastpage))


@authorization.route('/userprofile')
@login_required
def userprofile():
    app.pages="user profile"
    print('PROFILE',request.method,request.url)

    # fill-in the forms from the DB
    profileDisplayForm = UserProfileDisplayForm()
    profileChangeForm = UserProfileChangeForm()
    emailConfirmForm = emailConfirmationForm()
    mobileConfirmForm = mobileConfirmationForm()
    passwordchangeForm=PasswordChangeForm()
    avatarUploadForm=AvatarUploadForm()

    #print('---userID=',current_user.id)
    subscriber = Subscriber.query.filter_by(id=current_user.id).first()
    result=fillin_profile_forms(subscriber,profileDisplayForm,profileChangeForm,emailConfirmForm,mobileConfirmForm,passwordchangeForm,avatarUploadForm)
    form=profileDisplayForm
    varTitle='User Profile : '+subscriber.firstName+' '+subscriber.lastName
    mobileconfirmed=True
    if subscriber.mobile and not(subscriber.mobileConfirmed):
        mobileconfirmed=False
    # load userprofile template
    return render_template('page_templates/userprofile.html'
                            ,userprofiledisplay_form=profileDisplayForm
                            ,userprofilechange_form=profileChangeForm
                            ,passwordchange_form=passwordchangeForm
                            ,mobileconfirmation_form=mobileConfirmForm
                            ,emailconfirmation_form=emailConfirmForm
                            ,avatarupload_form=avatarUploadForm
                            ,activeTAB='userprofile'
                            ,title=varTitle
                            ,pages=app.pages
                            ,mobileconfirmed=mobileconfirmed
                            ,emailconfirmed=subscriber.emailConfirmed
                           )

@authorization.route('/userprofilechange', methods=['GET', 'POST'])
@login_required
def userprofilechange():
    app.pages=app.pages+" / " +"change"
    print('PROFILECHANGE',request.method,request.url)

    # fill-in the forms from the DB
    profileDisplayForm = UserProfileDisplayForm()
    profileChangeForm = UserProfileChangeForm()
    emailConfirmForm = emailConfirmationForm()
    mobileConfirmForm = mobileConfirmationForm()
    passwordchangeForm=PasswordChangeForm()
    avatarUploadForm=AvatarUploadForm()
    #print('---userID=',current_user.id)
    subscriber = Subscriber.query.filter_by(id=current_user.id).first()
    result=fillin_profile_forms(subscriber,profileDisplayForm,profileChangeForm,emailConfirmForm,mobileConfirmForm,passwordchangeForm,avatarUploadForm)
    varTitle='User Profile : '+subscriber.firstName+' '+subscriber.lastName
    varActiveTAB='userprofilechange'

    if request.method == 'GET':
        form=profileChangeForm

    if request.method == 'POST':
        form=UserProfileChangeForm()
        if form.validate_on_submit():
            varActiveTAB='userprofile'

            email_change=False
            mobile_change=False
            if subscriber.email != form.email.data:
                email_change=True
            if subscriber.mobile != form.mobile.data:
                mobile_change=True

            print('   ###email_change',email_change)
            print('   ###mobile_change',mobile_change)

            print('   ###email',subscriber.email,form.email.data)
            print('   ###firstName',subscriber.firstName,form.firstName.data)
            print('   ###lastName',subscriber.lastName,form.lastName.data)
            print('   ###mobile',subscriber.mobile,form.mobile.data)
            print('   ###jobTitle',subscriber.jobTitle,form.jobTitle.data)
            print('   ###company',subscriber.company,form.company.data)
            print('   ###mailingListSignUp',subscriber.mailingListSignUp,form.mailingListSignUp.data)

            if (
                not(mobile_change)
            and not(email_change)
            and subscriber.firstName == form.firstName.data
            and subscriber.lastName == form.lastName.data
            and subscriber.jobTitle == form.jobTitle.data
            and subscriber.company == form.company.data
            and subscriber.mailingListSignUp == form.mailingListSignUp.data
            and subscriber.userName == form.userName.data
            ):
                flash('Nothing changed in Your profile!','info')
                print('   NO-CHANGES')
                return redirect(url_for('authorization.userprofile'))


            # get field values from form
            subscriber.email=form.email.data
            subscriber.firstName = form.firstName.data
            subscriber.lastName = form.lastName.data
            subscriber.mobile = form.mobile.data
            subscriber.jobTitle = form.jobTitle.data
            subscriber.company = form.company.data
            subscriber.mailingListSignUp = form.mailingListSignUp.data
            subscriber.userName = form.userName.data

            #fixes
            #subscriber.emailConfirmed=True
            #subscriber.emailConfirmedDT=datetime.now()
            #subscriber.mailingListSignUpDT=datetime.now()
            #subscriber.registeredDT=datetime.now()
            #subscriber.lastLoginDT=datetime.now()
            #subscriber.agreeTermsDT=datetime.now()

            if not(subscriber.mailingListSignUp):
               subscriber.mailingListSignUpDT=None
            else:
                if not(subscriber.mailingListSignUpDT):
                    subscriber.mailingListSignUpDT=datetime.now()

            if email_change:
                subscriber.emailConfirmed=False
                subscriber.emailConfirmedDT=None
            if mobile_change:
                subscriber.mobileConfirmed=False
                subscriber.mobileConfirmedDT=None

            print('   ###emailConfirmed',subscriber.emailConfirmed)
            print('   ###mobileConfirmed',subscriber.mobileConfirmed)

            # update DB
            print('   ###update DB--->')
            db.session.commit()
            flash('You have successfully changed your profile!','success')
            print('   DATABASE UPDATED')

            if email_change:
                print('   ###email_change....')
                result=send_emailconfirmation_email(subscriber.email)
                if result=='OK':
                    flash('a confirmation email has been sent to {}.'.format(subscriber.email),'warning')
                    flash('open this email and click the provided link in order to confirm Your new email','info')
                else:
                    #error_text=result.dumps()
                    ErrorMsg='Failed to send confirmation email. Request a New Confirmation Email'
                    flash(ErrorMsg, 'error')

            if mobile_change:
                print('   ###mobile_change....')
                subscriber = Subscriber.query.filter_by(id=current_user.id).first()
                code=generate_mobileconfirmation_code(subscriber.mobile)
                subscriber.mobileConfirmationCode=code
                subscriber.mobileConfirmationCodeDT=datetime.now()
                subscriber.mobileConfirmed=False
                subscriber.mobileConfirmedDT=None
                db.session.commit()
                result=send_mobileconfirmation_sms(code)
                if result=='OK':
                    flash('a confirmation code has been sent via sms to {}. Use this code to confirm your mobile'.format(subscriber.mobile), 'success')
                else:
                    #error_text=result.dumps()
                    ErrorMsg='Failed to send confirmation code via sms. Request a new mobile confirmation Code'
                    flash(ErrorMsg, 'error')

            if email_change:
                print('########FORCE LOGOUT')
                logout_user()
                # redirect to the login page
                return redirect(url_for('authorization.login'))

            if mobile_change:
                return redirect(url_for('authorization.mobileconfirm'))

            return redirect(url_for('authorization.userprofile'))

    print('   ###activeTAB',varActiveTAB)
    # load userprofile template
    return render_template('page_templates/userprofile.html'
                            ,userprofiledisplay_form=profileDisplayForm
                            ,userprofilechange_form=form
                            ,passwordchange_form=passwordchangeForm
                            ,mobileconfirmation_form=mobileConfirmForm
                            ,emailconfirmation_form=emailConfirmForm
                            ,avatarupload_form=avatarUploadForm
                            ,activeTAB=varActiveTAB
                            ,title=varTitle
                            ,pages=app.pages
                            )

@authorization.route('/passwordchange', methods=['GET', 'POST'])
@login_required
def passwordchange():
    app.pages=app.pages+" / " +"password change"
    print('PASSWORDCHANGE',request.method,request.url)
    # fill-in the forms from the DB
    profileDisplayForm = UserProfileDisplayForm()
    profileChangeForm = UserProfileChangeForm()
    emailConfirmForm = emailConfirmationForm()
    mobileConfirmForm = mobileConfirmationForm()
    passwordchangeForm=PasswordChangeForm()
    avatarUploadForm=AvatarUploadForm()
    #print('---userID=',current_user.id)
    subscriber = Subscriber.query.filter_by(id=current_user.id).first()
    result=fillin_profile_forms(subscriber,profileDisplayForm,profileChangeForm,emailConfirmForm,mobileConfirmForm,passwordchangeForm,avatarUploadForm)
    form=passwordchangeForm
    varTitle='User Profile : '+subscriber.firstName+' '+subscriber.lastName
    varActiveTAB='passwordchange'

    if form.validate_on_submit():

        if form.old_password.data==form.new_password.data:
           form.new_password.errors.append("new password must be different than the current")
        else:
            if not(subscriber.verify_password(form.old_password.data)):
               form.old_password.errors.append("Invalid password")
            else:
                subscriber.password=form.new_password.data
                db.session.commit()
                flash('You have successfully changed your password.','success')
                logout_user()
                flash('login with your new password.','info')
                # redirect to the login page
                return redirect(url_for('authorization.login'))

    print('   ###activeTAB',varActiveTAB)
    # load userprofile template
    return render_template('page_templates/userprofile.html'
                            ,userprofiledisplay_form=profileDisplayForm
                            ,userprofilechange_form=profileChangeForm
                            ,passwordchange_form=form
                            ,mobileconfirmation_form=mobileConfirmForm
                            ,emailconfirmation_form=emailConfirmForm
                            ,avatarupload_form=avatarUploadForm
                            ,activeTAB=varActiveTAB
                            ,title=varTitle
                            ,pages=app.pages
                            )


@authorization.route('/upload_avatar', methods=['GET','POST'])
@login_required
def upload_avatar():
    app.pages=app.pages+" / " +"upload avatar"
    print('UPLOAD-AVATAR',request.method,request.url)
    subscriber = Subscriber.query.filter_by(id=current_user.id).first()
    varTitle='User Profile : '+subscriber.firstName+' '+subscriber.lastName
    varActiveTAB='avatarupload'
    # fill-in the forms from the DB
    profileDisplayForm = UserProfileDisplayForm()
    profileChangeForm = UserProfileChangeForm()
    emailConfirmForm = emailConfirmationForm()
    mobileConfirmForm = mobileConfirmationForm()
    passwordchangeForm=PasswordChangeForm()
    avatarUploadForm=AvatarUploadForm()
    subscriber = Subscriber.query.filter_by(id=current_user.id).first()
    result=fillin_profile_forms(subscriber,profileDisplayForm,profileChangeForm,emailConfirmForm,mobileConfirmForm,passwordchangeForm,avatarUploadForm)
    if request.method == 'GET':
        form=avatarUploadForm
    if request.method == 'POST':
        form=AvatarUploadForm()
    #if form.validate_on_submit():
    if request.method == 'POST':
        print('---emptyAvatarType=',form.emptyAvatarType.data)
        print('---photo=',form.photo.data)
        print('---files=',request.files)
        if 'photo' not in request.files and form.emptyAvatarType.data in (['M','F']):
            subscriber.avatarImageFile='../../static/images/icon_user_woman.png'
            if form.emptyAvatarType.data=='M':
                subscriber.avatarImageFile='../../static/images/icon_user_man.png'
            db.session.commit()
            flash('Your Picture has been set to an empty {} avatar.'.format(form.emptyAvatarType.data),'success')
            #success redirect to userprofile
            return redirect(url_for('authorization.userprofile'))

        # check if the post request has the file part
        # photo is the filefield defined in the form
        print('---->valid-continue')
        if 'photo' not in request.files:
            flash('select an empty avatar or an image file','error')
            print('--->photo not in request.files')
            #form.photo.errors.append("No photo file ...")
        else:
            print('---photo is there')
            file = request.files['photo']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                print('--->file.filename==""')
                flash('No photo file selected','error')
                #form.photo.errors.append("No photo file selected")

            print('---photo selected')
            print('   ','file=',file.filename)
            if not(file):
                flash('is not a file. system error-retry','error')
                print('---is not a file')
            else:
                if not(allowed_file(file.filename)):
                    print('--->not(allowed_file(file.filename)')
                    flash('this file format is not allowed for security reasons','error')
                    #form.photo.errors.append("this file format is not allowed for security reasons")
                else:
                    filename = secure_filename(file.filename)
                    print('   ','secure_filename=',filename)
                    fullpathfile = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    print('   ','fullpathfile1=',fullpathfile)
                    fullpathfile = os.path.join(app.root_path ,app.config['UPLOAD_FOLDER'], filename)
                    print('   ','fullpathfile2=',fullpathfile)
                    fullpathfile = os.path.join(app.root_path ,'static/avatars', filename)
                    print('   ','fullpathfile3=',fullpathfile)
                    file.save(fullpathfile)
                    subscriber.avatarImageFile='../../static/avatars/'+filename
                    db.session.commit()
                    #success redirect to userprofile
                    return redirect(url_for('authorization.userprofile'))

    print('   ###activeTAB',varActiveTAB)
    # load userprofile template
    return render_template('page_templates/userprofile.html'
                            ,userprofiledisplay_form=profileDisplayForm
                            ,userprofilechange_form=profileChangeForm
                            ,passwordchange_form=passwordchangeForm
                            ,mobileconfirmation_form=mobileConfirmForm
                            ,emailconfirmation_form=emailConfirmForm
                            ,avatarupload_form=form
                            ,activeTAB=varActiveTAB
                            ,title=varTitle
                            ,pages=app.pages
                            )

#    return render_template('page_templates/avatar_upload.html'
#                        ,avatarupload_form=form
#                        ,title='upload your avatar picture'
#                        ,pages=app.pages
#                        )

@authorization.route('/mobileconfirm', methods=['GET', 'POST'])
@login_required
def mobileconfirm():
    app.pages=app.pages+" / " +"mobile confirm"
    print('MOBILECONFIRM',request.method,request.url)

    form = mobileConfirmationForm()
    subscriber = Subscriber.query.filter_by(id=current_user.id).first()
    varTitle='User Profile : '+subscriber.firstName+' '+subscriber.lastName
    if request.method == 'GET':
        form.mobile.data = subscriber.mobile
        form.mobile_token.data = ''
        if subscriber.mobileConfirmed:
           flash('mobile already confirmed.', 'error')

    if request.method == 'POST':
        #print('---mobile=',form.mobile.data)
        if form.validate_on_submit():
            subscriber = Subscriber.query.filter_by(mobile=form.mobile.data).first_or_404()
            #print('---mobileConfirmed=',subscriber.mobileConfirmed)
            if subscriber.mobileConfirmed:
                #flash('mobile already confirmed.', 'info')
                form.mobile.errors.append("mobile already confirmed")
            else:
                token=form.mobile_token.data
                #print('---token=',form.mobile_token.data)
                #print('---codeHash=',subscriber.mobileConfirmationCodeHash)
                #print('++++++',subscriber.mobileConfirmationCodeDT,datetime.now(),datetime.now()-subscriber.mobileConfirmationCodeDT)
                tdelta=datetime.now()-subscriber.mobileConfirmationCodeDT
                #print('++++++days=',tdelta.days)
                #print('++++++secs=',tdelta.seconds)
                #return td.days, td.seconds//3600, (td.seconds//60)%60
                if tdelta.days>0 or tdelta.seconds>60*10:
                    #print('---code has expired. Request a new mobile confirmation code')
                    form.mobile_token.errors.append("Code has expired. Request a new mobile confirmation Code")
                else:
                    #if form.mobile_token.data!=subscriber.mobileConfirmationCode:
                    if not(subscriber.verify_mobileConfirmationCode(form.mobile_token.data)):
                        #print('---token is NOT-OK')
                        form.mobile_token.errors.append("Invalid Code. Retry or Request a new mobile confirmation Code")
                    else:
                        #print('---token is OK')
                        subscriber.mobileConfirmed=True
                        subscriber.mobileConfirmedDT=datetime.now()
                        db.session.commit()
                        #print('---DATABASE update')
                        flash('You have successfully confirmed your mobile.','success')
                        return redirect(url_for('authorization.userprofile'))

    # load userprofile template
    return render_template('page_templates/mobileconfirmation.html'
                        ,form=form
                        ,title='mobile confirmation'
                        ,pages=app.pages
                        ,alreadyconfirmed=subscriber.mobileConfirmed
                        )

@authorization.route('/sendconfirmationsms', methods=['POST','GET'])
def send_confirmation_sms():
    app.pages=app.pages+" / " +"send verification sms"
    print('SENDCONFIRMATIONSMS',request.method,request.url)
    subscriber = Subscriber.query.filter_by(id=current_user.id).first()
    code=generate_mobileconfirmation_code(subscriber.mobile)
    subscriber.mobileConfirmationCode=code
    subscriber.mobileConfirmationCodeDT=datetime.now()
    subscriber.mobileConfirmed=False
    subscriber.mobileConfirmedDT=None
    db.session.commit()
    result=send_mobileconfirmation_sms(code)
    #token = generate_mobileconfirmation_token(subscriber.mobile)
    ##print('   @@@token=',token)
    #subscriber.mobileConfirmationCode=token
    #subscriber.mobileConfirmationCodeDT=datetime.now()
    #db.session.commit()
    ##print('   @@@DB UPDATED')
    #sms_message = render_template('page_templates/sms_mobile_confirmation.html', verification_code=token)
    #smsfrom = 'Ganimides'
    ##result=send_sms(subscriber.mobile,smsfrom,sms_message)
    #subject = "please confirm your mobile"
    #result=send_email(subscriber.email,subject,sms_message)
    if result=='OK':
        flash('a confirmation code has been sent via sms to {}. Use this code to confirm your mobile'.format(subscriber.mobile), 'success')
        return redirect(url_for('authorization.mobileconfirm'))
    else:
        #error_text=result.dumps()
        ErrorMsg='Failed to send confirmation code via sms. Request a new mobile confirmation Code'
        flash(ErrorMsg, 'error')
        return redirect(url_for('authorization.mobileconfirm'))

@authorization.route('/emailconfirmrequest/<email>', methods=['GET', 'POST'])
#@login_required
def emailconfirmrequest(email):
    app.pages=app.pages+" / " +"email verification request"
    print('EMAILCONFIRMREQUEST',request.method,request.url)
    form = emailConfirmationForm()
    form.email.data = email
    #subscriber = Subscriber.query.filter_by(email=current_user.email).first()
    subscriber = Subscriber.query.filter_by(email=email).first()
    if subscriber is None:
        form.email.errors.append("invalid email")
        varTitle='User Profile : ???'
    else:
        form.email.data = subscriber.email
        varTitle='User Profile : '+subscriber.firstName+' '+subscriber.lastName
    if request.method == 'GET':
        if subscriber.emailConfirmed:
           flash('email already confirmed.', 'error')

    if request.method == 'POST':
        #print('---mobile=',form.mobile.data)
        if form.validate_on_submit():
            subscriber = Subscriber.query.filter_by(email=form.email.data).first_or_404()
            #print('---mobileConfirmed=',subscriber.mobileConfirmed)
            if subscriber.emailConfirmed:
                #flash('mobile already confirmed.', 'info')
                form.email.errors.append("email already confirmed")
            else:
                subscriber.emailConfirmed=False
                subscriber.emailConfirmedDT=None
                db.session.commit()
                result=send_emailconfirmation_email(subscriber.email)
                if result=='OK':
                    flash('an email confirmation link has been sent to {}'.format(subscriber.email),'warning')
                    flash('please open this email and click the provided link to activate Your new email','info')
                    return redirect(url_for('authorization.userprofile'))
                else:
                    #error_text=result.dumps()
                    ErrorMsg='Failed to send confirmation email'
                    flash(ErrorMsg, 'error')

    # load userprofile template
    return render_template('page_templates/emailconfirmation.html'
                        ,form=form
                        ,title='email confirmation'
                        ,pages=app.pages
                        ,alreadyconfirmed=subscriber.emailConfirmed
                        )
@authorization.route('/sendconfirmationemail', methods=['POST','GET'])
def send_confirmation_email():
    app.pages=app.pages+" / " +"send confirmation email"
    print('SENDCONFIRMATIONEMAIL',request.method,request.url)
    form = emailConfirmationForm()
    subscriber = Subscriber.query.filter_by(email=form.email.data).first()
    if subscriber is None:
        form.email.errors.append("invalid email")
        varTitle='User Profile : ???'
    else:
        form.email.data = subscriber.email
        varTitle='User Profile : '+subscriber.firstName+' '+subscriber.lastName
    if request.method == 'GET':
        if subscriber.emailConfirmed:
           flash('email already confirmed.', 'error')
    #subscriber = Subscriber.query.filter_by(id=current_user.id).first()
    subscriber.emailConfirmed=False
    subscriber.emailConfirmedDT=None
    db.session.commit()
    result=send_emailconfirmation_email(subscriber.email)
    if result=='OK':
        flash('an activation link has been sent to {}'.format(subscriber.email),'warning')
        flash('please open this email and click the provided link to activate Your new email','info')
    else:
        #error_text=result.dumps()
        ErrorMsg='Failed to send confirmation email'
        flash(ErrorMsg, 'error')

    return redirect(url_for('authorization.login'))

@authorization.route('/sendtestemail', methods=['POST','GET'])
def sendtestemail():
    app.pages=app.pages+" / " +"send test email"
    print('SEND_TEST_EMAIL',request.method,request.url)
    test_email='philippos.leandrou@gmail.com'
    result=send_email_test(test_email)
    if result=='OK':
        flash('an activation link has been sent to {}'.format(test_email),'warning')
        flash('please open this email and click the provided link to activate Your new email','info')
    else:
        #error_text=result.dumps()
        ErrorMsg='Failed to send confirmation email'
        flash(ErrorMsg, 'error')

    return redirect(url_for('authorization.login'))

@authorization.route('/confirm/<token>')
#@login_required
def emailconfirm(token):
    print('CONFIRM',request.method," token=",token,request.url)
    try:
        email = confirm_token(token,3600)
    except:
        flash('The confirmation link is invalid or has expired.Retry', 'warning')
        return redirect(url_for('authorization.userprofile'))

    if not(email):
        flash('The confirmation link is invalid or has expired.Retry', 'warning')
        return redirect(url_for('authorization.userprofile'))

    user = Subscriber.query.filter_by(email=email).first_or_404()
    if user.emailConfirmed:
        flash('Email already confirmed. Please login.', 'info')
    else:
        user.emailConfirmed = True
        user.emailConfirmedDT = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your Email. Thanks!', 'success')

    return redirect(url_for('authorization.login'))

@authorization.route('/passwordresetverification/<token>')
#@login_required
def passwordresetverification(token):
    print('PASSWORDRESETVERICATION',request.method," token=",token,request.url)
    try:
        email = confirm_token(token,3600)
    except:
        flash('The password reset link is invalid or has expired.Retry', 'warning')
        return redirect(url_for('authorization.login'))

    if not(email):
        flash('The password reset link is invalid or has expired.Retry', 'warning')
        return redirect(url_for('authorization.login'))

    subscriber = Subscriber.query.filter_by(email=email).first_or_404()
    if not(subscriber):
        flash('The password reset link is invalid or has expired.Retry', 'warning')
        return redirect(url_for('authorization.login'))

    subscriber.passwordReset=True
    db.session.commit()
    flash('Your Password has been reset. Please define Your password.', 'success')
    return redirect(url_for('authorization.password_reset',email=email))

@authorization.route('/passwordreset/<email>', methods=['GET', 'POST'])
def password_reset(email=''):
    print('PASSWORDRESET',request.method,request.url,'email=',email)
    form = PasswordReSetForm()
    varTitle='Password Reset'
    form.email.data=email
    # special case retrieve the email from the currently login user
    if email=='*':
        subscriber = Subscriber.query.filter_by(id=current_user.id).first()
        email=subscriber.email

    subscriber = Subscriber.query.filter_by(email=form.email.data).first_or_404()
    if not(subscriber):
        flash('invalid email. Retry','error')
    if form.validate_on_submit():
        subscriber.password=form.new_password.data
        subscriber.passwordReset=False
        db.session.commit()
        flash('You have successfully reset your password.','success')
        flash('login with your new password.','info')
        # redirect to the login page
        return redirect(url_for('authorization.login'))

    # load passsword reset template
    return render_template('authorization/authorization_forms_template.html'
                            ,form=form
                            ,title=varTitle
                            ,formPage='form_password_reset.html'
                            ,passwordreset=subscriber.passwordReset
                            )



###########################################################
###################splash forms############################
###########################################################
@authorization.route('/loginForm', methods=['GET','POST'])
def loginForm():
    init_form_options()
    init_active_menuoptions()
    print('LOGIN-FORM',request.method,request.url)
    print('LOGIN-FORM',request.method,'lastpage',app.lastpage)
    print('LOGIN-FORM',request.method,'lastpage_html',app.lastpage_html)
    form = LoginForm()
    print('LOGIN-FORM',request.method,'form',form)
    print('LOGIN-FORM',request.method,'email',form.email.data)
    # if request.method=='POST':
    #     print('LOGIN-FORM',request.method,'action',request.form['action'])
    #     if request.form['action'] == 'forget_password':
    #         print('LOGIN-FORM',request.method,'FORGET PASSWORD REQUESTED')
    #         return redirect(url_for('authorization.forgetpassword',email=form.email.data))

    if not(form.validate_on_submit()):
        print('LOGIN-FORM',request.method,'FORM INPUT HAS ERRORS')
    else:    
        print('LOGIN-FORM',request.method,'FORM INPUT IS OK')
        print('LOGIN-FORM',request.method,'SERVER SIDE VALIDATION START')
        print('LOGIN-FORM',request.method,'buttons',form.forgetPassword.data,form.submit.data)
        #check which sibmit button was pushed
        if form.forgetPassword.data:
            print('LOGIN-FORM',request.method,'FORGET PASSWORD REQUESTED')
            #return redirect(url_for('authorization.forgetpassword',email=form.email.data))
            return render_template(
                app.lastpage_html
                ,forgetpasswordform=forgetPasswordForm()
                ,activeTAB='forgetpassword'
                ,splash_form='forgetpassword'
                )
        else:
            print('LOGIN-FORM',request.method,'LOGIN REQUESTED')

        try:
            captcha_response = request.form['g-recaptcha-response']
        except:
            captcha_response = '???'
        if not(is_human(captcha_response)):
            flash("Sorry ! Bots are not allowed.",'error')
        else:
            print('LOGIN-FORM',request.method,'RECAPTCHA OK. check subscriber')
            #flash("Recaptcha OK, Login Details submitted successfully.",'success')
            subscriber = Subscriber.query.filter_by(email=form.email.data).first()
            #print('   ###----',"Subscriber",subscriber)
            if subscriber is None:
                print('LOGIN-FORM',request.method,'subscriber NOT FOUND')
                flash("invalid email or password",'error')
            else:
                print('LOGIN-FORM',request.method,'subscriber found')
                if not(subscriber.emailConfirmed):
                    print('LOGIN-FORM',request.method,'subscriber email NOT confirmed yet',subscriber.email)
                    flash("please Activate Your Email before Login","error")
                    return redirect(url_for('authorization.emailconfirmrequest', email=subscriber.email))
                else:
                    print('LOGIN-FORM',request.method,'subscriber email OK',subscriber.email)
                    if not(subscriber.verify_password(form.password.data)):
                        print('LOGIN-FORM',request.method,'subscriber password ERROR',subscriber.email)
                        flash("invalid email or password",'error')
                    else:
                        print('LOGIN-FORM',request.method,'all OK',subscriber.email)
                        subscriber.lastLoginDT=datetime.now()
                        db.session.commit()
                        print('LOGIN-FORM',request.method,'lastloginDT commit in DB')
                        # login the user
                        login_user(subscriber)
                        print('LOGIN-FORM',request.method,'subscriber login')
                        flash('You have successfully logged-in as {}.'.format(form.email.data),'success')
                        # redirect to the appropriate dashboard page
                        print('LOGIN-FORM',request.method,'OK redirect')
                        if subscriber.isAdmin:
                            print('LOGIN-FORM',request.method,'subscriber is Admin. goto admin_dashboard')
                            # SUCCESS!!! send to the admin page
                            return redirect(url_for('authorization.admin_dashboard'))
                        else:
                            print('LOGIN-FORM',request.method,'goto lastpage',app.lastpage)
                            # SUCCESS!!! send to the last page
                            return redirect(url_for(app.lastpage))

    print('LOGIN-FORM','RETURN',app.lastpage_html,'with splash_form','login')
    return render_template(
        app.lastpage_html
        ,loginform=form
        ,activeTAB='login'
        ,splash_form='login'
        )
@authorization.route('/registrationForm', methods=['GET','POST'])
def registrationForm():
    init_form_options()
    init_active_menuoptions()
    print('REGISTRATION-FORM',request.method,request.url)
    print('REGISTRATION-FORM',request.method,'lastpage',app.lastpage)
    print('REGISTRATION-FORM',request.method,'lastpage_html',app.lastpage_html)
    form = RegistrationForm()
    if not(form.validate_on_submit()):
        print('REGISTRATION-FORM',request.method,'FORM INPUT HAS ERRORS')
    else:    
        print('REGISTRATION-FORM',request.method,'FORM INPUT IS OK')
        print('REGISTRATION-FORM',request.method,'SERVER SIDE VALIDATION START')
        try:
            captcha_response = request.form['g-recaptcha-response']
        except:
            captcha_response = '???'
        if not(is_human(captcha_response)):
            flash("Sorry ! Bots are not allowed.",'error')
        else:
            print('REGISTRATION-FORM',request.method,'RECAPTCHA OK. check subscriber')
            #flash("Recaptcha OK, Login Details submitted successfully.",'success')
            subscriber = Subscriber.query.filter_by(email=form.email.data).first()
            if subscriber :
                flash('You are already registered!','warning')
                print('REGISTRATION-FORM',request.method,'subsrciber already registered. redirect to login')
                return redirect(url_for('authorization.loginForm'))
            
            print('REGISTRATION-FORM',request.method,'subsrciber record build')
            subscriber = Subscriber(
                email=form.email.data
                ,firstName=form.firstName.data
                ,lastName=form.lastName.data
                ,password=form.password.data
                ,registeredDT=datetime.now()
                ,userName=form.userName.data
                ,mobile=form.mobile.data
                )
            if subscriber.userName:
                if Subscriber.query.filter_by(userName=subscriber.userName).first():
                    subscriber.userName=subscriber.userName+'01'
                    print('REGISTRATION-FORM',request.method,'subsrciber username set to ',subscriber.userName)

            # add subscriber to the database
            db.session.add(subscriber)
            print('REGISTRATION-FORM',request.method,'subsrciber added to DB')
            db.session.commit()
            print('REGISTRATION-FORM',request.method,'subsrciber added to DB. commit OK')
            flash('You have successfully registered!','success')
            print('REGISTRATION-FORM',request.method,'subsrciber added OK')

            # genereate an email activation code
            print('REGISTRATION-FORM',request.method,'send email to ',subscriber.email)
            result=send_emailconfirmation_email(subscriber.email)
            if result!='OK':
                #error_text=result.dumps()
                print('REGISTRATION-FORM',request.method,'send email FAILED',result)
                ErrorMsg='Failed to send confirmation email. Request a New Confirmation Email'
                flash(result, 'error')
            else:
                flash('an activation email has been sent to {}.'.format(subscriber.email),'warning')
                flash('open this email and click the provided link in order to activate Your account','info')
                print('REGISTRATION-FORM',request.method,'activation email send.redirect to login',result)
                return redirect(url_for(app.lastpage))
    
    # flash the errors if not already registered
    is_already_registered=False
    for msg in form.email.errors:
        if "is already in use" in msg:
            is_already_registered=True
    if not(is_already_registered):
        flash_errors(form)

    print('REGISTRATION-FORM','RETURN',app.lastpage_html,'with splash_form','registration')
    return render_template(
        app.lastpage_html
        ,registrationform=form
        ,activeTAB='registration'
        ,splash_form='registration'
        )

@authorization.route('/contactForm', methods=['GET', 'POST'])
def contactForm():
    init_form_options()
    #app.pages=app.pages+" / " +"contact_form"
    print('CONTACT-FORM',request.method,request.url)
    print('CONTACT-FORM',request.method,'lastpage',app.lastpage)
    print('CONTACT-FORM',request.method,'lastpage_html',app.lastpage_html)
    form = ContactUsForm()
    if not(form.validate_on_submit()):
        print('CONTACT-FORM',request.method,'FORM INPUT HAS ERRORS')
    else:    
        print('CONTACT-FORM',request.method,'FORM INPUT IS OK')
        print('CONTACT-FORM',request.method,'SERVER SIDE VALIDATION START')
        contactmessage = ContactMessage(
                            email=form.email.data,
                            message=form.contact_message.data,
                            firstName=form.firstName.data,
                            lastName=form.lastName.data,
                            company=form.company.data,
                            jobTitle=form.jobTitle.data,
                            mobile="",
                            receivedDT=datetime.now()
                            )
        ## add contactmessage to the database
        db.session.add(contactmessage)
        db.session.commit()
        flash('Thank You. Your contact reference is {}'.format(contactmessage.id),'success')
        result=send_messagereceiveconfirmation_email(form.email.data,contactmessage.id)
        if result=='OK':
            flash('a receive confirmation email has been sent to {}'.format(form.email.data), 'info')
            flash('please open this email and click the provided link to confirm Your email','info')
        else:
            #error_text=result.dumps()
            ErrorMsg='Failed to send message receive email. Retry'
            flash(ErrorMsg, 'error')
        return redirect(url_for(app.lastpage))

    print('CONTACT-FORM','RETURN',app.lastpage_html,'with splash_form','contactus')
    return render_template(
        app.lastpage_html
        ,contactusform=form
        ,splash_form='contactus'
        )

@authorization.route('/forgetpassword/<email>', methods=['GET', 'POST'])
def forgetpassword(email=''):
    #app.pages=app.pages+" / " +"forget password"
    print('FORGETPASSWORD',request.method,request.url,'email',email)
    form = forgetPasswordForm()
    form.email.data=email
    print('FORGETPASSWORD',request.method,form)
    print('FORGETPASSWORD',request.method,'email',form.email.data)
    print('---email=',form.email.data)
    if form.validate_on_submit():
        #print('recaptcha=',form.recaptcha)
        # recaptcha method1 OK. thanks google
        captcha_response = request.form['g-recaptcha-response']
        #print('   captcha_response = ',captcha_response)
        if not(is_human(captcha_response)):
            # Log invalid attempts
            flash("Sorry ! Bots are not allowed.",'error')
        else:
            # Process request here
            #print('   ###',"Recaptcha OK, Login Details submitted successfully.")
            #flash("Recaptcha OK, Login Details submitted successfully.",'success')
            subscriber = Subscriber.query.filter_by(email=form.email.data).first()
            if subscriber is None:
                flash("invalid email",'error')
            else:
                result=send_passwordreset_email(subscriber.email)
                if result=='OK':
                    flash('a password reset link has been sent to {}'.format(subscriber.email),'warning')
                    flash('please open this email and click the provided link to reset Your Password','info')
                else:
                    #error_text=result.dumps()
                    ErrorMsg='Failed to send password reset email. Retry'
                    flash(ErrorMsg, 'error')

    # load passsword_forget template
    print('FORGETPASSWORD','RETURN',app.lastpage_html,'with splash_form','forgetpassword')
    #return render_template('authorization/authorization_forms_template.html'
    #                        app.lastpage_html
    #                        ,forgetpasswordform=form
    #                        ,formPage='form_forget_splash.html'
    #                        ,splashform='forgetpassword'
    #                        )
    return render_template(
        app.lastpage_html
        ,forgetpasswordform=form
        ,splash_form='forgetpassword'
        )



#@authorization.route('/fblogin')
#def loginwithfb():
#    return facebook.authorize(callback=url_for('facebook_authorized',
#        next=request.args.get('next') or request.referrer or None,
#        _external=True))


#@authorization.route('/fblogin/authorized')
#@facebook.authorized_handler
#def facebook_authorized(resp):
#    if resp is None:
#        return 'Access denied: reason=%s error=%s' % (
#            request.args['error_reason'],
#            request.args['error_description']
#        )
#    session['oauth_token'] = (resp['access_token'], '')
#    me = facebook.get('/me')
#    return 'Logged in as id=%s name=%s redirect=%s' % \
#        (me.data['id'], me.data['name'], request.args.get('next'))


#@facebook.tokengetter
#def get_facebook_oauth_token():
#    return session.get('oauth_token')

#@app.after_request
#def store_visited_urls():
#    session['urls'].append(request.url)
#    if len(session['urls']) > 5:
#        session['urls'].pop(0)
#    session.modified = True