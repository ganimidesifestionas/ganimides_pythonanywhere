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
from flask import jsonify

# Import the app object from the main app module __INIT__
from . import app
# Import the database object from the main app module
from . import db

# Import module forms
from .module_authorization.forms import LoginForm, RegistrationForm, ContactUsForm, forgetPasswordForm
from .forms import CookiesConsentForm
from .models import Visit, Visitor, Page_Visit
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import func
from .external_services.log_services import *

###########################################################################
###########################################################################
###########################################################################
### functions
###########################################################################
###########################################################################
###########################################################################
# def log_page(pageName, pageFunction, pageTemplate='', pageTemplate_page='', page_form=''):
#     # if startNewRoute == 1:
#     #     session['pages_history'] = pageName
#     # else:
#     #     session['pages_history'] = session['pages_history'] + ">"+ pageName
#     session['lastpage'] = pageFunction
#     session['lastpageURL'] = request.url
#     if pageTemplate:
#         session['lastpageHTML'] = pageTemplate
#     session['pageID'] = pageName.upper()
#     if not 'pages' in session:
#         session['pages'] = []
#     session['pages'].append(pageName)
#     if len(session['pages']) > 9:
#         session['pages'].pop(0)

#     for p in range(1, len(session['pages'])):
#         if p == 1:
#             session['pages_history'] = session['pages'][p-1]
#         else:
#             session['pages_history'] = session['pages_history'] + ">"+ session['pages'][p-1]

#     session.modified = True
#     print(client_IP(), 'page', session['pageID'], request.method, request.url, '### '+__name__+' ###')
#     log_page_visit(pageName, request.url, 'page', pageFunction, pageTemplate, pageTemplate_page, page_form)

# def log_route(routeName, routeFunction='', routeTemplate='', routeTemplate_page='', route_form=''):
#     session['routeID'] = routeName.upper()
#     if not 'pages' in session:
#         session['pages'] = []
#     session['pages'].append(routeName)
#     if len(session['pages']) > 9:
#         session['pages'].pop(0)
#     for p in range(1, len(session['pages'])):
#         if p == 1:
#             session['pages_history'] = session['pages'][p-1]
#         else:
#             session['pages_history'] = session['pages_history'] + ">"+ session['pages'][p-1]

#     session.modified = True
#     print(client_IP(), 'route', session['routeID'], request.method, request.url, '### '+__name__+' ###')
#     log_page_visit(routeName, request.url, 'route', routeFunction, routeTemplate, routeTemplate_page, route_form)

# def log_splash_page(pageName, pageFunction, pageTemplate='',pageTemplate_page='', page_form=''):
#     #session['splashpage'] = pageFunction
#     pageID = pageName.upper()
#     if not 'pages' in session:
#         session['pages'] = []

#     session['pages'].append(pageName)
#     if len(session['pages']) > 9:
#         session['pages'].pop(0)

#     for p in range(1, len(session['pages'])):
#         if p == 1:
#             session['pages_history'] = session['pages'][p-1]
#         else:
#             session['pages_history'] = session['pages_history'] + ">"+ session['pages'][p-1]

#     session.modified = True
#     print(client_IP(), 'splash-page, pageID', request.method, request.url, '#'+__name__+'#')
#     log_page_visit(pageName, request.url, 'splash_page', pageFunction, pageTemplate, pageTemplate_page, page_form)

# def log_info(msg):
#     print('   ', msg)

# def log_variable(name='', value=''):
#     msg = '{0}={1}'.format(name, value)
#     print('   ', msg)

# def client_IP():
#     if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
#         clientip = request.environ['REMOTE_ADDR']
#     else:
#         clientip = request.environ['HTTP_X_FORWARDED_FOR']
#     return clientip

# def log_visit():
#     ## visitor
#     visitor = Visitor.query.filter_by(ipa=client_IP()).first()
#     if not visitor:
#         #find nextvisitorNum
#         max_id = db.session.query(func.max(Visitor.id)).scalar()
#         log_variable('last visitor id', max_id)
#         nextvisitorNum = 1
#         if max_id:
#             last_visitor = Visitor.query.filter_by(id=max_id).first()
#             log_variable('last visitor', last_visitor)
#             if last_visitor:
#                 log_variable('last visitor visitorNumber', last_visitor.visitorNumber)
#                 if last_visitor.visitorNumber:
#                     nextvisitorNum = last_visitor.visitorNumber + 1

#         visitor = Visitor(
#             ipa=client_IP()
#             , visitDT=datetime.now()
#             , visitorNumber=nextvisitorNum
#             , visitsCount=1
#             )
#         # add visit to the database
#         db.session.add(visitor)
#         db.session.commit()
#         visitor = Visitor.query.filter_by(ipa=client_IP()).first()
#         session['VisitorID'] = visitor.id
#         session.modified = True
#         log_variable('new visitor', visitor)
#     else:
#         log_variable('visitor',visitor)
#         if not 'VisitorID' in session:
#             session['VisitorID'] = visitor.id
    
#     log_variable('VisitorID', session['VisitorID'])

#     ## visit
#     if not 'VisitNumber' in session and not 'VisitID' in session :
#         max_id = db.session.query(func.max(Visit.id)).scalar()
#         log_variable('last visit id', max_id)
#         visitNum = 0
#         if max_id:
#             last_visit = Visit.query.filter_by(id=max_id).first()
#             log_variable('last visit', last_visit)
#             if last_visit:
#                 log_variable('last visit visitNumber', last_visit.visitNumber)
#                 if last_visit.visitNumber:
#                     visitNum = last_visit.visitNumber

#         visitNum = visitNum + 1

#         visit = Visit(
#             ipa=client_IP()
#             , visitDT=datetime.now()
#             , visitNumber=visitNum
#             , visitor_ID=visitor.id
#             #, session_ID=visitor.id
#             )
#         # add visit to the database
#         visitor.visitsCount = visitor.visitsCount + 1
#         db.session.add(visit)
#         db.session.commit()
#         vid = db.session.query(func.max(Visit.id)).filter_by(ipa=client_IP())
#         visit = Visit.query.filter_by(id=vid).first()
#         session['VisitNumber'] = visitNum
#         session['VisitID'] = visit.id
#         session.modified = True

#         flash('You are Visitor # {0}. Thanks for visiting us!'.format(visitNum,),'success')
#         log_variable('new visit', visit)

#     log_variable('VisitID', session['VisitID'])

# def log_page_visit(pageName, pageURL, pageType, pageFunction='', pageTemplate='', pageTemplate_page='', pageTemplate_form=''):
#     if 'language' in session:
#         lang = session['language']
#     else:
#         lang = session.get('language',request.accept_languages.best_match(app.config['LANGUAGES'].keys()))

#     page_visit = Page_Visit(
#         page=pageName
#         , pageURL=pageURL
#         , pageType=pageType
#         , pageLanguage=lang
#         , pageFunction=pageFunction
#         , pageTemplate=pageTemplate
#         , pageTemplate_page=pageTemplate_page
#         , pageTemplate_form=pageTemplate_form
#         )

#     if 'VisitorID' in session:
#         page_visit.visitor_ID = session['VisitorID']
#     if 'VisitID' in session:
#         page_visit.visit_ID = session['VisitID']

#     db.session.add(page_visit)
#     db.session.commit()

##########################################
#put this after @ decorator
##########################################
#how to get a config variable app.config.get('GOOGLE_RECAPTCHA_SITE_KEY'))
#how to get a config variable app.config.get('GOOGLE_RECAPTCHA_SECRET_KEY'))

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

#varPageName = request.args.get('url')
#alert(varPageName)
###########################################################################
###########################################################################
###########################################################################
### define the routes, accepted methods (GET/POST) and the service function
###########################################################################
###########################################################################
###########################################################################
#app.secret_key = '/r/xd8}q/xde/x13/xe5F0/xe5/x8b/x96A64/xf2/xf8MK/xb1/xfdA7x8c'
#############################################################
#############################################################
#############################################################
@app.before_first_request
def init_cookies():
    print('##########################################')
    print('##########################################')
    print('##########################################')
    print('##########################################')
    print('###'+__name__+'###', 'before_first_request')
    print('##########################################')
    print('##########################################')
    print('##########################################')
    print('##########################################')
    #this will make session cookies expired in 5 minutes
    # set app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)
    session.permanent = True

    session['active_module'] = __name__
    session['urls'] = []
    session['pages'] = []
    clientIPA = client_IP()
    session['clientIPA'] = clientIPA

    try:
        session['lastpageHTML'] = app.homepage_html
    except:
        session['lastpageHTML'] = 'page_templates/landing_page.html'
        
    session.modified = True

    ### import splash forms objects
    app.loginform = LoginForm()
    app.loginform.eyecatch.data = __name__
    app.registrationform = RegistrationForm()
    app.contactusform = ContactUsForm()
    app.forgetpasswordform = forgetPasswordForm()
    app.cookiesconsentform = CookiesConsentForm()
    #print('   ', app.cookiesconsentform)
    #print('   ', '!!! splash forms objects loaded in app. will be made avalaible from server...')
    #log_visit()

@app.before_request
def set_cookies():
    #print('###'+__name__+'###', 'before_request')
    session['active_module'] = __name__
    if not 'urls' in session:
        session['urls'] = []
    session['urls'].append(request.url)
    if len(session['urls']) > 9:
        session['urls'].pop(0)
    if not 'pages' in session:
        session['pages'] = []
    if not 'clientIPA' in session:
        clientIPA = client_IP()
        session['clientIPA'] = clientIPA

    if current_user.is_authenticated:
        if app.forgetpasswordform:
            app.forgetpasswordform.email.data = current_user.email
        if app.contactusform:
            app.contactusform.firstName.data = current_user.firstName
            app.contactusform.lastName.data = current_user.lastName
            app.contactusform.company.data = current_user.company
            app.contactusform.jobTitle.data = current_user.jobTitle
            app.contactusform.email.data = current_user.email
            app.contactusform.contact_message.data = 'xxxx'
    session.modified = True
    log_visit()

@app.after_request
def set_cookies_after_request(response):
    #print('###'+__name__+'###', 'after_request')
    return response

###########################################################################
###########################################################################
###########################################################################
### module functions
###########################################################################
###########################################################################
###########################################################################

#############################################################
#############################################################
#############################################################
### routes and pages
#############################################################
#############################################################
#############################################################
@app.route('/')
def homepage():
    page_name = 'home'
    page_function = 'homepage'
    page_template = 'page_templates/landing_page.html'
    log_page(page_name, page_function, page_template)
    return render_template('page_templates/landing_page.html')

@app.route('/landingpage')
def landingpage():
    page_name = 'landingpage'
    page_function = 'landingpage'
    page_template = 'page_templates/landing_page.html'
    log_page(page_name, page_function, page_template)
    return render_template('page_templates/landing_page.html')

@app.route('/contact')
def contact():
    page_name = 'contact'
    page_function = 'contact'
    page_template = 'page_templates/contact.html'
    log_page(page_name, page_function, page_template)
    return render_template('page_templates/contact.html')

@app.route('/about')
def about():
    page_name = 'about'
    page_function = 'about'
    page_template = 'page_templates/about.html'
    log_page(page_name, page_function, page_template)
    return render_template('page_templates/about.html')

@app.route('/company')
def company():
    page_name = 'company'
    page_function = 'company'
    page_template = 'page_templates/company.html'
    log_page(page_name, page_function, page_template)
    return render_template('page_templates/company.html')

@app.route('/services')
def services():
    page_name = 'services'
    page_function = 'services'
    page_template = 'page_templates/services.html'
    log_page(page_name, page_function, page_template)
    return render_template('page_templates/services.html')

@app.route('/why')
def why():
    page_name = 'why'
    page_function = 'why'
    page_template = 'page_templates/why.html'
    log_page(page_name, page_function, page_template)
    return render_template('page_templates/why.html')

@app.route('/research')
def research():
    page_name = 'research'
    page_function = 'research'
    page_template = 'page_templates/research.html'
    log_page(page_name, page_function, page_template)
    return render_template('page_templates/research.html')

@app.route('/academy')
def academy():
    page_name = 'academy'
    page_function = 'academy'
    page_template = 'page_templates/academy.html'
    log_page(page_name, page_function, page_template)
    return render_template('page_templates/academy.html')

@app.route('/knowledge')
def knowledge():
    page_name = 'knowledge'
    page_function = 'knowledge'
    page_template = 'page_templates/knowledge.html'
    log_page(page_name, page_function, page_template)
    return render_template('page_templates/knowledge.html')

@app.route('/prototypes')
def prototypes():
    page_name = 'prototypes'
    page_function = 'prototypes'
    page_template = 'page_templates/prototypes.html'
    log_page(page_name, page_function, page_template)
    return render_template('page_templates/prototypes.html')

@app.route('/cookies_policy')
def cookies_policy():
    page_name = 'cookies policy'
    page_function = 'cookies_policy'
    page_template = 'page_templates/cookies_policy.html'
    log_page(page_name, page_function, page_template)
    return render_template('page_templates/cookies_policy.html')

@app.route('/privacy_policy')
def privacy_policy():
    page_name = 'privacy policy'
    page_function = 'privacy_policy'
    page_template = 'page_templates/privacy_policy.html'
    log_page(page_name, page_function, page_template)
    return render_template('page_templates/privacy_policy.html')

@app.route('/terms_and_conditions')
def terms_and_conditions():
    page_name = 'terms and conditions'
    page_function = 'terms_and_conditions'
    page_template = 'page_templates/terms_and_conditions.html'
    log_page(page_name, page_function, page_template)
    return render_template('page_templates/terms_and_conditions.html')

@app.route('/language/<language>')
def set_language(language=None):
    log_route('change language', 'set_language')
    session['language'] = language
    #log_variable('language', session['language'])
    log_info('language set to {0}'.format(language))
    return redirect(session['lastpageURL'])

@app.route('/cookiesconsentform', methods=['GET', 'POST'])
def cookiesconsentform():
    page_name = 'cookiesconsentform-splash-form'
    page_function = 'cookiesconsentform'
    page_form = 'splash_form_cookiesconsent.html'
    log_splash_page(page_name, page_function, '', '', page_form)

    form = CookiesConsentForm()
    if not(form.validate_on_submit()):
        dummy = 1 
    else:    
        ## add contactmessage to the database
        #db.session.add(contactmessage)
        #db.session.commit()
        session['cookies_consent'] = "YES"
        flash('Thank You. Your data are protected','success')
        #OK
        return render_template(
            session['lastpageHTML']
            )
    return render_template(
        session['lastpageHTML']
        , cookiesconsentform=form
        , splash_form='cookiesconsent'
        )

#############################################################
#############################################################
#############################################################
### prototypes: 
#############################################################
#############################################################
#############################################################
@app.route('/myBank')
@login_required
def myBank():
    page_name = 'myBank-prototype'
    page_function = 'myBank'
    page_template = 'myBank/myBank_index.html'
    page_form = ''
    log_page(page_name, page_function, page_template,'',page_form)
    return render_template(
        'mybank/mybank_index.html'
        ,title='myBank'
        ,message='open banking prototype........'
    )

@app.route('/myGame')
def myGame():
    page_name = 'myGame-prototype'
    page_function = 'myGame'
    page_template = 'myGame/myGame.html'
    page_form = ''
    log_page(page_name, page_function, page_template,'',page_form)
    return render_template(
        'myGame/myGame.html'
        ,title='myGame'
        ,message='gaming prototype........'
    )

