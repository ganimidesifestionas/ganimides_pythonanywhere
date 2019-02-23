"""
Routes and views for the flask application.
"""
#import logging
from datetime import datetime
from datetime import timedelta
#import time
#import googlemaps
from datetime import datetime

import requests
#import json

#from flask import Flask
from flask import flash
from flask import render_template
from flask import request
from flask import redirect
#from flask import url_for
from flask import session
#from flask import logging
#from flask import jsonify
from flask_login import current_user, login_required #, login_user, logout_user

# Import the app object from the main app module __INIT__
from . import app

# Import module forms
from .module_authorization.forms import LoginForm, RegistrationForm, ContactUsForm, forgetPasswordForm
from .forms import CookiesConsentForm
#from .models import Visit, VisitPoint, Page_Visit
#from sqlalchemy import func
from .external_services.log_services import client_IP, log_visit, log_page, log_route, log_splash_page, log_info, log_variable, RealClientIPA

###########################################################################
###########################################################################
###########################################################################
### functions
###########################################################################
###########################################################################
###########################################################################
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
def init_cookies_etc_before_first_request():
    print('##########################################')
    print('###'+__name__+'###', 'before_first_request')
    print('##########################################')

    #this will make session cookies expired in 5 minutes
    # set app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)
    #session.permanent = True

    #1. init session cookies
    session['active_module'] = __name__
    session['urls'] = []
    session['pages'] = []
    clientIPA = client_IP()
    session['clientIPA'] = clientIPA
    session['visit'] = 0
    app.logger.critical('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! SITE FIRST REQUEST !!! IP:{0}'.format(session.get('clientIPA')))
    try:
        session['lastpageHTML'] = app.homepage_html
    except:
        session['lastpageHTML'] = 'page_templates/landing_page.html'

    session.modified = True

    #2. import splash forms objects
    app.loginform = LoginForm()
    app.loginform.eyecatch.data = __name__
    app.registrationform = RegistrationForm()
    app.contactusform = ContactUsForm()
    app.forgetpasswordform = forgetPasswordForm()
    app.cookiesconsentform = CookiesConsentForm()
    print('##########################################--finished')

@app.before_request
def set_cookies_etc_before_request():
    #print(request.base_url)
    #print(request.base_url.lower().find('/static/'))
    if request.base_url.lower().find('/static/') >= 0 :
        return
    print('##########################################')
    print('###'+__name__+'###', 'before_request')
    print('##########################################-start')
    if not session.get('visit'):
        session['visit'] = 100
    session['visit'] = session.get('visit') + 1
    session['visitpoint_try'] = 0

    #1. set session cookies
    session['active_module'] = __name__

    if 'identityDT' not in session:
        dt = datetime.now()
        strdt = dt.strftime("%Y-%m-%d %H:%M:%S")
        session['identityDT'] = strdt
        session['session_expiry'] = 60
        print('###'+__name__+'###', '***New session started')
    else:
        strdt = session['identityDT']
        t1 = datetime.strptime(strdt, "%Y-%m-%d %H:%M:%S")
        t2 = datetime.now()
        duration = t2 - t1
        duration_sec = duration.total_seconds()
        session['session_expiry'] = duration_sec
        if duration_sec >= 60*60:
            dt = datetime.now()
            strdt = dt.strftime("%Y-%m-%d %H:%M:%S")
            session['identityDT'] = strdt
            session['session_expiry'] = 60*60
            print('###'+__name__+'###', '***session expired after 1 hour')
            app.logger.critical('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! SESSION EXPIRED !!! IP:{0}'.format(session.get('clientIPA')))
            session.pop('VisitID', None) # delete visitID
            session.pop('VisitNumber', None) # delete visitNumber
            session.pop('VisitorID', None) # delete visitpointID
            session.pop('VisitorNumber', None) # delete visitpointNumber
            session.pop('clientIPA', None) # delete clientIPA

    if 'urls' not in session:
        session['urls'] = []
    session['urls'].append(request.url)
    if len(session['urls']) > 9:
        session['urls'].pop(0)

    if 'pages' not in session:
        session['pages'] = []

    if 'clientIPA' not in session:
        clientIPA = client_IP()
        session['clientIPA'] = clientIPA
        #print('###'+__name__+'###', '***new clientIPA session cookie : ',session['clientIPA'])

    if session['clientIPA'] !=  RealClientIPA():
        clientIPA = RealClientIPA()
        session['clientIPA'] = RealClientIPA()
        #print('###'+__name__+'###', '***changed clientIPA session cookie : ',session['clientIPA'])

    #from mod_python import apache
    #print('###'+__name__+'###1', session['clientIPA'], request.get_remote_host(apache.REMOTE_NOLOOKUP))

    # print('###'+__name__+'###1', session['clientIPA'], request.environ.get('HTTP_X_REAL_IP'))
    # print('###'+__name__+'###2', session['clientIPA'], request.environ.get('REMOTE_ADDR'))
    # print('###'+__name__+'###3', session['clientIPA'], request.remote_addr)

    #force get
    #clientIPA = client_IP()
    #session['clientIPA'] = clientIPA
    #print('###'+__name__+'###', 'client IP :',session['clientIPA'])

    if 'cookies_consent_time' in session:
        strdt = session['cookies_consent_time']
        t1 = datetime.strptime(strdt, "%Y-%m-%d %H:%M:%S")
        t2 = datetime.now()
        duration = t2 - t1
        duration_sec = duration.total_seconds()
        #duration_min = divmod(duration_sec, 60)[0]
        #print('XXXX-check-duration',duration_sec, duration_min)
        if duration_sec >= 0:
            session['cookies_consent'] = 'EXPIRED'
            app.logger.critical('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! COOKIES CONSENT EXPIRED !!! IP:{0}'.format(session.get('clientIPA')))
        else:
            session['cookies_consent'] = 'YES'
    else:
        session['cookies_consent'] = 'NO'

    #2. init spash forms with authenticated user info
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

    #3. log the visit in db
    log_visit()
    session['request_started'] = 'YES'
    print('##########################################--finished')

@app.after_request
def set_cookies_after_request(response):
    #print('###'+__name__+'###', 'after_request')
    #session['request_started'] = 'NO'
    #print('##########################################--finished')
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
    print('###'+__name__+'###homepage-1')
    log_page(page_name, page_function, page_template)
    print('###'+__name__+'###homepage-2')
    return render_template('page_templates/landing_page.html')

@app.route('/landingpage')
def landingpage():
    page_name = 'landingpage'
    page_function = 'landingpage'
    page_template = 'page_templates/landing_page.html'
    print('###'+__name__+'###landingpage-1')
    log_page(page_name, page_function, page_template)
    print('###'+__name__+'###landingpage-2')
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
    print('###'+__name__+'###company-1')
    log_page(page_name, page_function, page_template)
    print('###'+__name__+'###company-2')
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
    log_info('language set to {0}'.format(language))
    return redirect(session['lastpageURL'])

@app.route('/cookiesconsentform/<answer>', methods=['GET', 'POST'])
def cookiesconsentform(answer):
    page_name = 'cookiesconsentform-splash-form'
    page_function = 'cookiesconsentform'
    page_form = 'splash_form_cookiesconsent.html'
    log_splash_page(page_name, page_function, '', '', page_form)
    if answer.upper() == 'AGREE':
        dt = datetime.now() + timedelta(days=31)
    else:
        #dt = datetime.now() + timedelta(seconds=60)
        dt = datetime.now() + timedelta(days=1)
    strdt = dt.strftime("%Y-%m-%d %H:%M:%S")
    session['cookies_consent_time'] = strdt
    session['cookies_consent'] = 'YES'
    flash('Thank You. Your data are protected', 'success')
    return redirect(session.get('lastpageURL'))

@app.route('/test_cookiesconsent')
def test_cookiesconsent():
    dt = datetime.now() - timedelta(days=111)
    strdt = dt.strftime("%Y-%m-%d %H:%M:%S")
    session['cookies_consent_time'] = strdt
    session['cookies_consent'] = 'NO'
    return redirect(session.get('lastpageURL'))

@app.route('/test_google_api')
def test_google_api():
    page_name = 'terms and conditions'
    page_function = 'terms_and_conditions'
    page_template = 'page_templates/terms_and_conditions.html'
    log_page(page_name, page_function, page_template)
    clientip = '213.149.173.194'
    GOOGLE_MAPS_API_KEY='AIzaSyCstqUccUQdIhV69NtEGuzASxBQX5zPKXY'
    lat = 34.684100
    lon = 33.037900
    # api_url = 'https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyCstqUccUQdIhV69NtEGuzASxBQX5zPKXY
    path = 'http://api.ipstack.com/{0}?access_key={1}'.format(clientip, '4022cfd2249c3431953ecf599152892e')
    path = 'https://maps.googleapis.com/maps/api/geocode/json?latlng={0},{1}&key={2}'.format(lat,lon,GOOGLE_MAPS_API_KEY)
    log_variable('apistack geolocation path', path)
    #print (path)
    r = requests.post(path)
    print(r)
    #reply_code=r.status_code
    # if not r.status_code == requests.codes.ok:
    #response = {}
    if r:
        response = r.json()
        log_variable('apistack geolocation result', response)
        # for key, value in response.items():
        #     log_variable('---'+key, value)
        # loc = response['location']
        # for key, value in loc.items():
        #     log_variable('--- ---'+key, value)

    # gmaps = googlemaps.Client(key='AIzaSyCstqUccUQdIhV69NtEGuzASxBQX5zPKXY')
    # # Geocoding an address
    # geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
    # log_variable('geocode_result', geocode_result)

    # # Look up an address with reverse geocoding
    # reverse_geocode_result = gmaps.reverse_geocode((34.6841, 33.0379))
    # log_variable('reverse_geocode_result', reverse_geocode_result)

    # # Request directions via public transit
    # now = datetime.now()
    # directions_result = gmaps.directions("Sydney Town Hall",
    #                                     "Parramatta, NSW",
    #                                     mode="transit",
    #                                     departure_time=now)
    # log_variable('directions_result', directions_result)
    return render_template('page_templates/terms_and_conditions.html')
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
    log_page(page_name, page_function, page_template, '', page_form)
    return render_template(
        'mybank/mybank_index.html'
        , title='myBank'
        , message='open banking prototype........'
    )

@app.route('/myGame')
def myGame():
    page_name = 'myGame-prototype'
    page_function = 'myGame'
    page_template = 'myGame/myGame.html'
    page_form = ''
    log_page(page_name, page_function, page_template, '', page_form)
    return render_template(
        'myGame/myGame.html'
        , title='myGame'
        , message='gaming prototype........'
    )
