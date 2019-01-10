"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import Flask
from flask import flash
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import logging
from . import app
# Import module forms
from .module_authorization.forms import LoginForm, RegistrationForm,ContactUsForm,forgetPasswordForm
#from flask import current_app as app
from flask_login import current_user, login_required, login_user, logout_user

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
#app.secret_key = '/r/xd8}q/xde/x13/xe5F0/xe5/x8b/x96A64/xf2/xf8MK/xb1/xfdA7x8c'

#@app.before_first_request
#def logging_init():
#    print('@@@@@app.before_first_request')
#    logging.basicConfig(
#        datefmt = '%Y-%m-%d %H:%M:%S',
#        format = '%(asctime)s%%%(message)s',
#        filename = 'home/ganimides/routing.log',
#        level=logging.CRITICAL)
#    session['urls']=[]

@app.before_request
def init_vars():
    app.loginform=LoginForm()
    app.registrationform=RegistrationForm()
    contactusform=ContactUsForm()
    forgetpasswordform=forgetPasswordForm()
    if current_user.is_authenticated:
        print('@@@@app.before_request','current_user','IS-AUTHENTICATED')
        contactusform.firstName.data = current_user.firstName
        contactusform.lastName.data = current_user.lastName
        contactusform.company.data = current_user.company
        contactusform.jobTitle.data = current_user.jobTitle
        contactusform.email.data = current_user.email
        forgetpasswordform.email.data = current_user.email
    app.contactusform=contactusform
    app.forgetpasswordform=forgetpasswordform
    print('@@@@app.before_request','splash_form=',app.splash_form)
app.after_request
def init_vars_after_request(response):
    #print('@@@@app.after_request','init_vars_after_request')
#    try:
#        lp=app.splash_form
#    except:
#        app.splash_form='#BOBBISTARR#'
    print('@@@@app.after_request','splash_form=',app.splash_form)
    return response 

#def store_visited_urls(self):
    #self.session['urls'].append(request.url)
    #if len(session['urls']) > 5:
    #    session['urls'].pop(0)
    #session.modified = True
#    print('@@@@app.after_request',self.session['urls'])

@app.route('/')
def homepage():
    app.pages='home'
    app.lastpage='homepage'
    app.lastpage_html='page_templates/landing_page.html'
    print('HOME',request.method,request.url)
    #logging.critical('a request!')
    app.logger.info('%s logged in successfully', 'user.username')
    #session['username'] = "someuser"
    #session['urls'] = []
    return render_template(
        'page_templates/landing_page.html'
        ,title='home'
        #,pages=app.pages
        #,loginform=LoginForm()
        #,registrationform=RegistrationForm()
        #,contactusform=ContactUsForm()
        )

@app.route('/landingpage')
def landingpage():
    app.pages='landing page'
    app.lastpage='landingpage'
    app.lastpage_html='page_templates/landing_page.html'
    print('LANDINGPAGE',request.method,request.url)
    #logging.critical('LANDINGPAGE')
    #session['username'] = "someuser"
    #session['urls'] = []
    return render_template(
        'page_templates/landing_page.html'
        ,title='landing page'
        ,pages=app.pages
    )

@app.route('/language/<language>')
def set_language(language=None):
    print('LANGUAGE',request.method,request.url)
    session['language'] = language
    return redirect(url_for('homepage'))

@app.route('/contact')
def contact():
    app.pages='contact'
    app.lastpage='contact'
    app.lastpage_html='page_templates/contact.html'
    print('CONTACT',request.method,request.url)
    #data = []
    #if 'urls' in session:
    #    data = session['urls']

    return render_template(
        'page_templates/contact.html'
        ,title='Contact Info'
        ,pages=app.pages
        
    )

@app.route('/about')
def about():
    app.pages='about'
    app.lastpage='about'
    app.lastpage_html='page_templates/about.html'
    print('ABOUT',request.method,request.url)
    return render_template(
        'page_templates/about.html'
        ,title='about Ganimides'
        ,pages=app.pages
        
    )


@app.route('/company')
def company():
    app.pages='company'
    app.lastpage='company'
    app.lastpage_html='page_templates/company.html'
    print('COMPANY',request.method,request.url)
    return render_template(
        'page_templates/company.html'
        ,title='the company'
        ,pages=app.pages
        
    )

@app.route('/services')
def services():
    app.pages='services'
    app.lastpage='services'
    app.lastpage_html='page_templates/services.html'
    print('SERVICES',request.method,request.url)
    return render_template(
        'page_templates/services.html'
        ,title='services'
        ,pages=app.pages
        
    )

@app.route('/why')
def why():
    app.pages='why'
    app.lastpage='why'
    app.lastpage_html='page_templates/why.html'
    print('WHY',request.method,request.url)
    return render_template(
        'page_templates/why.html'
        ,title='why ganimides'
        ,pages=app.pages
        
    )

@app.route('/research')
def research():
    app.pages='research'
    app.lastpage='research'
    app.lastpage_html='page_templates/research.html'
    print('RESEARCH',request.method,request.url)
    return render_template(
        'page_templates/research.html'
        #,loginform=LoginForm()
        #,registrationform=RegistrationForm()
        #,contactusform=ContactUsForm()
        ,title='research'
        ,pages=app.pages
        
    )

@app.route('/academy')
def academy():
    app.pages='academy'
    app.lastpage='academy'
    app.lastpage_html='page_templates/academy.html'
    print('ACADEMY',request.method,request.url)
    return render_template(
        'page_templates/academy.html'
        #,loginform=LoginForm()
        #,registrationform=RegistrationForm()
        #,contactusform=ContactUsForm()
        ,title='BUSTEC ACADEMY'
        ,pages=app.pages
        
    )

@app.route('/knowledge')
def knowledge():
    app.pages='knowledge'
    app.lastpage='knowledge'
    app.lastpage_html='page_templates/knowledge.html'
    print('KNOWLEDGE',request.method,request.url)
    return render_template(
        'page_templates/knowledge.html'
        #,loginform=LoginForm()
        #,registrationform=RegistrationForm()
        #,contactusform=ContactUsForm()
        ,title='KNOWLEDGE CENTER'
        ,pages=app.pages
        
    )

@app.route('/prototypes')
def prototypes():
    app.pages='prototypes'
    app.lastpage='prototypes'
    app.lastpage_html='page_templates/prototypes.html'
    print('PROTOTYPES',request.method,request.url)
    return render_template(
        'page_templates/prototypes.html'
        ,title='prototypes'
        ,pages=app.pages
        
    )

@app.route('/cookies_policy')
def cookies_policy():
    app.pages='cookies policy'
    app.lastpage='cookies_policy'
    app.lastpage_html='page_templates/cookies_policy.html'
    print('COOKIES',request.method,request.url)
    return render_template(
        'page_templates/cookies_policy.html'
        ,title='cookies policy'
        ,pages=app.pages
        
    )

@app.route('/privacy_policy')
def privacy_policy():
    app.pages='privacy policy'
    app.lastpage='privacy_policy'
    app.lastpage_html='page_templates/privacy_policy.html'
    print('PRIVACY_POLICY',request.method,request.url)
    return render_template(
        'page_templates/privacy_policy.html'
        ,title='privacy policy'
        ,pages=app.pages
        
    )

@app.route('/terms_and_conditions')
def terms_and_conditions():
    app.pages='terms and conditions'
    app.lastpage='terms_and_conditions'
    app.lastpage_html='page_templates/terms_and_conditions.html'
    print('TERMS_AND_CONDITIONS',request.method,request.url)
    return render_template(
        'page_templates/terms_and_conditions.html'
        ,title='terms and conditions of use'
        ,pages=app.pages        
    )

@app.route('/myBank')
#@login_required
def myBank():
    app.pages=app.pages+" / " +"myBank"
    app.lastpage='myBank'
    app.lastpage_html='mybank/mybank_index.html'
    print('MYBANK',request.method,request.url)
    """Renders the app(myBank) home page."""
    return render_template(
        'mybank/mybank_index.html'
        ,title='myBank'
        ,pages=app.pages
        ,message='open banking prototype........'
    )

@app.route('/myGame')
def myGame():
    app.pages=app.pages+" / " +"myGame"
    app.lastpage='myGame'
    app.lastpage_html='myGame/myGame.html'
    print('MYGAME',request.method,request.url)
    """Renders the app(myBank) home page."""
    return render_template(
        'myGame/myGame.html'
        ,title='myGame'
        ,pages=app.pages
        ,message='gaming prototype........'
    )