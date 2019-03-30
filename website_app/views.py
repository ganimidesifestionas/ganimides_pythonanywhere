"""
Routes and views for the flask application.
"""
#import logging
#from __future__ import unicode_literals
#import sqlite3
#from flask_paginate import Pagination, get_page_args
#import click
#click.disable_unicode_literals_warning = True


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
from flask import g, current_app

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
from .external_services.log_services import set_geolocation, client_IP, log_visit, log_page, log_route, log_splash_page, log_info, log_variable, RealClientIPA
from .external_services.token_services import generate_unique_sessionID
from .debug_services.debug_log_services import *

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
#how to get a config variable app.config.get('RECAPTCHA_PRIVATE_KEY'))
#how to get a config variable app.config.get('RECAPTCHA_PUBLIC_KEY'))
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
@app.teardown_request
def teardown(error):
    if hasattr(g, 'conn'):
        print('TEARDOWN !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!',error)
        g.conn.close()

@app.before_first_request
def init_cookies_etc_before_first_request():
    log_module_start('@app.before_first_request')
    log_info('SITE FIRST REQUEST !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    #this will make session cookies expired in 5 minutes
    #set app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)
    #session.permanent = True

    #1. init session cookies
    log_info('init session cookies')

    session['active_module'] = __name__
    session['urls'] = []
    session['pages'] = []
    clientIPA = client_IP()
    session['clientIPA'] = clientIPA
    session['visit'] = 0
    try:
        session['lastpageHTML'] = app.homepage_html
    except:
        session['lastpageHTML'] = 'page_templates/landing_page.html'
    session.modified = True

    #2. import splash forms objects
    log_info('init app (splash) forms')

    app.loginform = LoginForm()
    app.loginform.eyecatch.data = __name__
    app.registrationform = RegistrationForm()
    app.contactusform = ContactUsForm()
    app.forgetpasswordform = forgetPasswordForm()
    app.cookiesconsentform = CookiesConsentForm()
    log_variable('debug_log_services_eyecatch', debug_log_services_eyecatch)
    log_module_finish('@app.before_first_request')

@app.before_request
def set_cookies_etc_before_request():
    if request.base_url.lower().find('/static/') >= 0 :
        return

    log_request_start(request.base_url)
    log_start('@app.before_request')

    log_info('save necessary cookies')

    session['active_module'] = __name__
    if not session.get('sessionID'):
        token = generate_unique_sessionID()
        session['sessionID'] = token
        log_variable('@@@ NEW SESSION @@@', session.get('sessionID'))
        dt = datetime.now()
        strdt = dt.strftime("%Y-%m-%d %H:%M:%S")
        session['identityDT'] = strdt
        session['session_expiry'] = 60

    if 'identityDT' not in session:
        dt = datetime.now()
        strdt = dt.strftime("%Y-%m-%d %H:%M:%S")
        session['identityDT'] = strdt
        session['session_expiry'] = 60
        #log_info('*** new session started', session.get('identityDT'), session.get('session_expiry'))

    if not session.get('visit'):
        session['visit'] = 100
    session['visit'] = session.get('visit') + 1
    session['visitpoint_try'] = 0

    if 'urls' not in session:
        session['urls'] = []
    if 'pages' not in session:
        session['pages'] = []
    if 'clientIPA' not in session:
        clientIPA = client_IP()
        session['clientIPA'] = clientIPA
    if session['clientIPA'] !=  RealClientIPA():
        clientIPA = RealClientIPA()
        session['clientIPA'] = RealClientIPA()
    
    log_info('check session expiry')

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
        log_info('***session expired after 1 hour', duration_sec)
        app.logger.critical('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! SESSION EXPIRED !!! IP:{0}'.format(session.get('clientIPA')))
        session.pop('VisitID', None) # delete visitID
        session.pop('VisitNumber', None) # delete visitNumber
        session.pop('VisitPointID', None) # delete visitpointID
        session.pop('VisitPointNumber', None) # delete visitpointNumber
        session.pop('clientIPA', None) # delete clientIPA

    log_info('check cookies consent expiry')
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
    log_info('move authenticated user info to the (splash) forms')
    if current_user.is_authenticated:
        if app.forgetpasswordform:
            app.forgetpasswordform.email.data = current_user.email
        if app.contactusform:
            app.contactusform.firstName.data = current_user.firstName
            app.contactusform.lastName.data = current_user.lastName
            app.contactusform.company.data = current_user.company
            app.contactusform.jobTitle.data = current_user.jobTitle
            app.contactusform.email.data = current_user.email
            app.contactusform.contact_message.data = ''


    #3. log the visit in db
    log_info('log the visit in DB')
    log_visit()
    
    session.modified = True

    log_finish('@app.before_request')

@app.after_request
def set_cookies_after_request(response):
    log_start('@app.after_request')
    log_finish('@app.after_request')
    log_request_finish(request.base_url)
    return response

###########################################################################
###########################################################################
###########################################################################
### module functions
###########################################################################
###########################################################################
###########################################################################
def set_deviceandscreen_properties(width, height, devicepixelratio):
    session['screen_width'] = width
    session['screen_height'] = height
    session['device_pixelration'] = devicepixelratio
    session['splash_forms_width'] = str(width - 100)+'px'
    return
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

#############################################################
#############################################################
#############################################################
### client-to-server utilities:
#############################################################
#############################################################
#############################################################
@app.route('/location', methods=['POST'])
def location():
    latitude = request.json.get('latitude')
    longitude = request.json.get('longitude')
    session['geolocation'] = [latitude, longitude]
    log_variable('geolocation', session.get('geolocation'))
    set_geolocation(latitude, longitude)
    log_route('geolocation', 'geolocation')
    return('')
@app.route('/deviceandscreen', methods=['POST'])
def deviceandscreen():
    width = request.json.get('width')
    height = request.json.get('height')
    devicepixelratio = request.json.get('devicepixelratio')
    session['device'] = [width, height, devicepixelratio]
    log_variable('device', session.get('device'))
    set_deviceandscreen_properties(width, height, devicepixelratio)
    log_route('deviceandscreen', 'deviceandscreen')
    return('')

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
#############################################################
#############################################################
#############################################################
### test utilities:
#############################################################
#############################################################
#############################################################
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
    if session.get('geolocation'):
        try:
            lat = session.get('geolocation')[0] 
            lon = session.get('geolocation')[1] 
        except:
            lat = 0
            lon = 0
            return render_template('page_templates/terms_and_conditions.html')
    else:
        lat = -1
        lon = -1
        return render_template('page_templates/terms_and_conditions.html')

    log_info('-----lat,lon',lat,lon)
    #lat = session.get('geolocation')[0] 
    #lon = session.get('geolocation')[1] 

    # api_url = 'https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyCstqUccUQdIhV69NtEGuzASxBQX5zPKXY
    path = 'http://api.ipstack.com/{0}?access_key={1}'.format(clientip, '4022cfd2249c3431953ecf599152892e')
    path = 'https://maps.googleapis.com/maps/api/geocode/json?latlng={0},{1}&key={2}'.format(lat,lon,GOOGLE_MAPS_API_KEY)
    log_variable('apistack geolocation path', path)
    #print (path)
    r = requests.post(path)
    log_variable('request',r)
    #reply_code=r.status_code
    # if not r.status_code == requests.codes.ok:
    #response = {}
    if r:
        response = r.json()
        address_comps = response['results'][0]['address_components']
        types = ['locality', 'administrative_area_level_1', 'country', 'postal_code']
        filter_method = lambda x: len(set(x['types']).intersection(types))
        res=filter(filter_method, address_comps)
        for geoname in res:
            common_types = set(geoname['types']).intersection(set(types))
            log_info ('{} ({})'.format(geoname['long_name'], ', '.join(common_types)))
            # nam = ', '.join(common_types)
            # val = geoname['long_name']
            # print(nam, val)

        formatted_address = response['results'][0]['formatted_address']
        log_info ('{} ({})'.format(formatted_address, 'formatted address'))

        # #log_variable('apistack geolocation result', response)
        # log_info('==================================================')
        # #for key, value in response.items():
        #     #log_variable('---'+key, value)
        #     #log_info('------------------')
        # log_info('==================================================')
        # res= response['results']['address_components']
        # for item in res:
        #     log_variable('--- ---',item)
        #     for key, value in item.items():
        #         log_variable('--- --- ---'+key, value)

# import json
# import urllib2

# def get_geonames(lat, lng, types):
#     url = 'http://maps.googleapis.com/maps/api/geocode/json' + \
#             '?latlng={},{}&sensor=false'.format(lat, lng)
#     jsondata = json.load(urllib2.urlopen(url))
#     address_comps = jsondata['results'][0]['address_components']
#     filter_method = lambda x: len(set(x['types']).intersection(types))
#     return filter(filter_method, address_comps)

# lat, lng = 59.3, 18.1
# types = ['locality', 'administrative_area_level_1']

# # Display all geographical names along with their types
# for geoname in get_geonames(lat, lng, types):
#     common_types = set(geoname['types']).intersection(set(types))
#     print '{} ({})'.format(geoname['long_name'], ', '.join(common_types))

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
    
   #rootWindow = None
   #mapLabel = None

   #defaultLocation = "Mauna Kea, Hawaii"
   #mapLocation = defaultLocation
   #mapFileName = 'googlemap.gif'
    # https://maps.googleapis.com/maps/api/staticmap?center=Brooklyn+Bridge,New+York,NY&zoom=13&size=600x300&maptype=roadmap
    # &markers=color:blue%7Clabel:S%7C40.702147,-74.015794&markers=color:green%7Clabel:G%7C40.711614,-74.012318
    # &markers=color:red%7Clabel:C%7C40.718217,-73.998284
    # &key=YOUR_API_KEY

    #############static map
    key='&key='+GOOGLE_MAPS_API_KEY

    urlbase = "http://maps.google.com/maps/api/staticmap?"
    zoomLevel = 15
    mapType = "satellite" #"roadmap" #"terrain"
    width = 600
    height = 300
    markers  = "&markers=color:red|size:mid|label:VisitPoint|{},{}".format(lat,lon)
    args = "center={},{}&zoom={}&size={}x{}&format=gif{}".format(lat,lon,zoomLevel,width,height,markers)
    mapType = "&maptype={}".format(mapType)
    google_maps_url = urlbase+args+mapType+key
    return redirect(google_maps_url)
    
    #############dynamic map
    key='&key='+GOOGLE_MAPS_API_KEY
    urlbase = "https://www.google.com/maps/@?api=1&map_action=map"
    args = "&center={},{}&zoom={}&size={}x{}&format=gif{}".format(lat,lon,zoomLevel,width,height,markers)
    #&center=-33.712206,150.311941&zoom=12&basemap=terrain
    google_maps_url = urlbase+args+mapType+key
    return redirect(google_maps_url)

    # https://www.google.co.uk/maps/place/@{0},{1}".format(session.get('longitude'),session.get('longitude')) %}
    #     {% set href=href+"" %}
    #     <a target="_blank" href="{{href}}">
    #         <span style="font-weight:400" class="d-none d-lg-inline badge badge-pill badge-secondary">{{session.get('latitude')}},{{session.get('longitude')}}</span>
    #     </a>
    return render_template('page_templates/terms_and_conditions.html')

