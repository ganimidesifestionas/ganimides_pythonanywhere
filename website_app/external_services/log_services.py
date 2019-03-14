from datetime import datetime
import requests

#from flask import Flask
from flask import flash
#from flask import render_template
from flask import request
from flask import session
#from flask import logging
#from flask import jsonify
from sqlalchemy import func
import sqlalchemy

# Import the app from the parent folder (assumed to be the app)
from .. import app
# Import the database object from the main app module
from .. import db

# Import module forms
#from .module_authorization.forms import LoginForm, RegistrationForm, ContactUsForm, forgetPasswordForm
#from .forms import CookiesConsentForm
from .. models import Visit, VisitPoint, Page_Visit
#from flask_login import current_user#, login_required#, login_user, logout_user
from .geolocation_services import get_geolocation_info_from_IP, get_geolocation_info
from .debug_log_services import *

def RealClientIPA():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        clientipa = request.environ['REMOTE_ADDR']
    else:
        clientipa = request.environ['HTTP_X_FORWARDED_FOR']
    if request.headers.get('X-Real-IP') is None:
        realclientipa = clientipa
    else:
        realclientipa = request.headers.get('X-Real-IP')
    return realclientipa

def client_IP():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        clientipa = request.environ['REMOTE_ADDR']
        #print('clientIP from request.environ[REMOTE_ADDR]', clientipa)
    else:
        clientipa = request.environ['HTTP_X_FORWARDED_FOR']
        #print('clientIP from request.environ[HTTP_X_FORWARDED_FOR]', clientipa)

    #session['clientIPA'] = clientipa
    #app.logger.critical('client IPA is {}'.format(clientipa))
    if request.headers.get('X-Real-IP') is None:
        realclientipa = clientipa
    else:
        realclientipa = request.headers.get('X-Real-IP')
        #print('clientIP from request.headers.get(X-Real-IP)(pythonanywhere)', realclientipa)
        #app.logger.critical('###real client IPA is {}'.format(realclientipa))

    session['clientIPA'] = realclientipa
    #app.logger.critical('###client IPA is {0}/{1}'.format(clientipa, realclientipa))
    return realclientipa

#from mod_python import apache
#print('###'+__name__+'###1', session['clientIPA'], request.get_remote_host(apache.REMOTE_NOLOOKUP))
#print('###'+__name__+'###1', session['clientIPA'], request.environ.get('HTTP_X_REAL_IP'))
#print('###'+__name__+'###2', session['clientIPA'], request.environ.get('REMOTE_ADDR'))
#print('###'+__name__+'###3', session['clientIPA'], request.remote_addr)


def get_client_info_dictionary():
    log_module_start('get_client_info_dictionary')
    clientDictionary = {}
    if 'language' in session:
        lang = session['language']
    else:
        lang = session.get('language', request.accept_languages.best_match(app.config['LANGUAGES'].keys()))    
    clientDictionary.update({'lang' : lang})

    if not session.get('clientIPA'):
        clientip = client_IP()
    else:
        clientip = session.get('clientIPA')
    clientDictionary.update({'clientip' : clientip})

    if session.get('geolocation'):
        try:
            lat = session.get('geolocation')[0] 
            lon = session.get('geolocation')[1] 
        except:
            lat = 0
            lon = 0
    else:
        lat = -1
        lon = -1
    clientDictionary.update({'lat' : lat})
    clientDictionary.update({'lon' : lon})
    log_variable('clientDictionary',clientDictionary)
    log_module_finish('get_client_info_dictionary')
    return clientDictionary

def set_geolocation_from_ip_on_visitpoint(ip, visitpoint):
    log_module_start('set_geolocation_from_ip_on_visitpoint')

    ipa_info = get_geolocation_info_from_IP(ip)
    if ipa_info:
        visitpoint.geolocation_type = 'IP'
        visitpoint.iptype = ipa_info['type']
        visitpoint.continent_code = ipa_info['continent_code']
        visitpoint.continent_name = ipa_info['continent_name']
        visitpoint.country_code = ipa_info['country_code']
        visitpoint.country_name = ipa_info['country_name']
        visitpoint.region_code = ipa_info['region_code']
        visitpoint.region_name = ipa_info['region_name']
        visitpoint.city = ipa_info['city']
        visitpoint.zip = ipa_info['zip']
        visitpoint.postal_code = ipa_info['zip']
        visitpoint.latitude = ipa_info['latitude']
        visitpoint.longitude = ipa_info['longitude']
        visitpoint.location = ipa_info['location'] # this is a dictionary in json format
        # visitpoint.timezone = ipa_info['timezone']
        # visitpoint.currency = ipa_info['currency']
        # visitpoint.connection = ipa_info['connection']
        # visitpoint.security = ipa_info['security']
        log_module_finish('set_geolocation_from_ip_on_visitpoint')

def set_geolocation_info_on_visitpoint(lat,lon,visitpoint):
    log_module_start('set_geolocation_info_on_visitpoint')
    geolocation_info = get_geolocation_info(lat, lon)
    if geolocation_info:
        visitpoint.geolocation_type = 'geolocation'
        #visitpoint.iptype = geolocation_info['type']
        #visitpoint.continent_code = geolocation_info['continent_code']
        #visitpoint.continent_name = geolocation_info['continent_name']
        #visitpoint.country_code = geolocation_info['country_code']
        if geolocation_info.get('country_name'):
            visitpoint.country_name = geolocation_info['country_name']
        #visitpoint.region_code = geolocation_info['region_code']
        if geolocation_info.get('region_name'):
            visitpoint.region_name = geolocation_info['region_name']
        if geolocation_info.get('city'):
            visitpoint.city = geolocation_info['city']
        if geolocation_info.get('zip'):
            visitpoint.zip = geolocation_info['zip']
            visitpoint.postal_code = geolocation_info['zip']
        visitpoint.latitude = geolocation_info['latitude']
        visitpoint.longitude = geolocation_info['longitude']
        if geolocation_info.get('address'):
            visitpoint.address = geolocation_info['address']
        #visitpoint.location = geolocation_info['location'] # this is a dictionary in json format
        # visitpoint.timezone = geolocation_info['timezone']
        # visitpoint.currency = geolocation_info['currency']
        # visitpoint.connection = geolocation_info['connection']
        # visitpoint.security = geolocation_info['security']
    log_module_finish('set_geolocation_info_on_visitpoint')
# def xget_IPA_info(clientip):
#     print('###'+__name__+'###', 'get_IPA_info', 'clientip =',clientip)
#     if not clientip:
#         clientip=client_IP()
#     if not session.get('clientIPA'):
#         session['clientIPA'] = clientip
#     if clientip=='127.0.0.1':
#         clientip = '213.149.173.194'
#     #print('###'+__name__+'###', 'get_client_info5', 'clientip =',clientip)
#     ################################################################
#     ### ipstack access key
#     ################################################################
#     #IPSTACK_API_ACCESSKEY = '4022cfd2249c3431953ecf599152892e'
#     #IPSTACK_URL = 'http://api.ipstack.com/'
#     #IPSTACK_URL_CMD = 'http://api.ipstack.com/{0}?access_key={1}'
#     path = 'http://api.ipstack.com/{0}?access_key={1}'.format(clientip, '4022cfd2249c3431953ecf599152892e')
#     log_variable('apistack geolocation path', path)
#     r = requests.post(path)
#     #print(r)
#     #reply_code=r.status_code
#     # if not r.status_code == requests.codes.ok:
#     #response = {}
#     if r:
#         response = r.json()
#         log_variable('apistack geolocation result', response)
#         # for key, value in response.items():
#         #     log_variable('---'+key, value)
#         # loc = response['location']
#         # for key, value in loc.items():
#         #     log_variable('--- ---'+key, value)
#         return response
#     else:
#         return None
#     #res = response.json()
#         #print(res)
#     #r = requests.post(api_url,headers=headers,data=payload)
#     #reply_code=r.status_code

# def xget_geolocation_info(visitpoint):
#     geolocationDictionary = {}
#     if session.get('geolocation'):
#         try:
#             lat = session.get('geolocation')[0] 
#             lon = session.get('geolocation')[1] 
#             geolocationDictionary.update({'latitude' : lat})
#             geolocationDictionary.update({'longitude' : lon})
#         except:
#             log_info('geolocation latitude or longitude invalid....')
#             return None
#     else:
#         log_info('geolocation not provided....')
#         return None

#     visitpoint.latitude = lat
#     visitpoint.longitude = lon
#     log_variable('visitpoint.latitude',visitpoint.latitude)
#     log_variable('visitpoint.longitude',visitpoint.longitude)

#     GOOGLE_MAPS_API_KEY = 'AIzaSyCstqUccUQdIhV69NtEGuzASxBQX5zPKXY'
#     # api_url = 'https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyCstqUccUQdIhV69NtEGuzASxBQX5zPKXY
#     path = 'https://maps.googleapis.com/maps/api/geocode/json?latlng={0},{1}&key={2}'.format(lat,lon,GOOGLE_MAPS_API_KEY)
#     log_variable('apistack geolocation path', path)
#     r = requests.post(path)
#     print(r)
#     #reply_code=r.status_code
#     # if not r.status_code == requests.codes.ok:
#     #response = {}
#     if r:
#         response = r.json()
#         log_variable('GEOLOCATION',response)
#         status = response.get('status')
#         log_variable('status',status)
#         types = [
#               'locality'
#             , 'sublocality'
#             , 'sublocality_level_1'
#             , 'neighborhood'
#             , 'route'
#             , 'premise'
#             , 'administrative_area_level_1'
#             , 'postal_code'
#             , 'country'
#             , 'street_address'
#         ]
#         results = response.get('results')
#         #log_variable('results',results)
#         for res in results:
#             typ = res.get('types')
#             #log_variable('---types',typ)
#             compos = res.get('address_components')
#             #log_variable('--- --- components', compos)

#             fnd = 0
#             for t in typ:
#                 if t in types:
#                     fnd = 1
#             if fnd == 0:
#                 for t in typ:
#                     log_variable('--- --- XXX ---types_of_visitpoint',t)

#             if 'street_address' in typ:
#                 val = res.get('formatted_address') #res.response['results'][i]['formatted_address']
#                 nam = 'address'
#                 #log_variable('--- --- address',val)
#                 geolocationDictionary.update({'address' : val})

#             #address_comps = response['results'][0]['address_components']
#             address_comps = compos
#             filter_method = lambda x: len(set(x['types']).intersection(types))
#             compo = filter(filter_method, address_comps)
#             #log_variable('--- --- compo',compo)

#             for geoname in compo:
#                 #log_variable('--- --- +++ geoname',geoname)
#                 common_types = set(geoname['types']).intersection(set(types))
#                 nam = ', '.join(common_types)
#                 val = geoname['long_name']
#                 print('ooo ooo ooo', nam,'-->', val)
#                 if 'country' in geoname['types']:
#                     geolocationDictionary.update({'country_name' : val})
#                     visitpoint.country_name = val
#                     log_variable('--- --- ---visitpoint.country_name',visitpoint.country_name)
#                 if 'administrative_area_level_1' in geoname['types']:
#                     geolocationDictionary.update({'region_name' : val})
#                     visitpoint.region_name = val
#                     log_variable('--- --- ---visitpoint.region_name',visitpoint.region_name)
#                 if 'neighborhood'  in geoname['types']:
#                     geolocationDictionary.update({'region_name' : val})
#                     visitpoint.region_name = val
#                     log_variable('--- --- ---visitpoint.region_name',visitpoint.city)
#                 if 'sublocality' in geoname['types']:
#                     #geolocationDictionary.update({'sublocality?' : val})
#                     #visitpoint.region_name = val
#                     log_variable('--- --- ---visitpoint.xxxxx????',val)

#                 if 'locality' in geoname['types']:
#                     geolocationDictionary.update({'city' : val})
#                     visitpoint.city = val
#                     log_variable('--- --- ---visitpoint.city',visitpoint.city)
#                 if 'postal_code' in geoname['types']:
#                     geolocationDictionary.update({'zip' : val})
#                     visitpoint.zip = val
#                     log_variable('--- --- ---visitpoint.zip',visitpoint.zip)

#         #     visitpoint.iptype = res['type']
#         #     visitpoint.continent_code = res['continent_code']
#         #     visitpoint.continent_name = res['continent_name']
#         #     visitpoint.country_code = res['country_code']
#         #     visitpoint.country_name = res['country_name']
#         #     visitpoint.region_code = res['region_code']
#         #     visitpoint.region_name = res['region_name']
#         #     visitpoint.city = res['city']
#         #     visitpoint.zip = res['zip']
#         #     visitpoint.latitude = res['latitude']
#         #     visitpoint.longitude = res['longitude']
#         #     visitpoint.location = res['location'] # this is a dictinary in json format
#         #     # visitpoint.timezone = res['timezone']
#         #     # visitpoint.currency = res['currency']
#         #     # visitpoint.connection = res['connection']
#         #     # visitpoint.security = res['security']
#         return geolocationDictionary

def get_next_visitpointNumber():
    max_id = db.session.query(func.max(VisitPoint.id)).scalar()
    #log_variable('last visitpoint id', max_id)
    nextvisitpointNum = 1
    if max_id:
        last_visitpoint = VisitPoint.query.filter_by(id=max_id).first()
        #log_variable('last visitpoint', last_visitpoint)
        if last_visitpoint:
            #log_variable('last visitpoint visitpointNumber', last_visitpoint.visitpointNumber)
            if last_visitpoint.visitpointNumber:
                nextvisitpointNum = last_visitpoint.visitpointNumber + 1
    #log_variable('next visitpoint Number', nextvisitpointNum)
    return nextvisitpointNum

def get_next_visitNumber():
    max_id = db.session.query(func.max(Visit.id)).scalar()
    #log_variable('last visit id', max_id)
    nextvisitNum = 1
    if max_id:
        last_visit = Visit.query.filter_by(id=max_id).first()
        #log_variable('last visit', last_visit)
        if last_visit:
            #log_variable('last visit visitNumber', last_visit.visitNumber)
            if last_visit.visitNumber:
                nextvisitNum = last_visit.visitNumber + 1
    #log_variable('next visit Number', nextvisitNum)
    return nextvisitNum

##########################################################################################################
def log_visitpoint():
    #print('###'+__name__+'###', 'log_visitpoint [start]', 'session clientIPA=',session.get('clientIPA'))
    log_module_start('log_visitpoint')

    clientDictionary = get_client_info_dictionary()
    clientip = clientDictionary['clientip']
    lat = clientDictionary['lat']
    lon = clientDictionary['lon']   

    ##################################################################
    ##################################################################
    ##################################################################
    # 1st database access-check if connection is alive
    ##################################################################
    #print('###'+__name__+'###', 'log_visitpoint_before_1stquery')
    if not session.get('visitpoint_try'):
        session['visitpoint_try'] = 0
    session['visitpoint_try'] = session.get('visitpoint_try') + 1

    #app.logger.critical('###{0}-{1}###!!!{2}!!!before_1stquery--session[clientIPA]={3}'.format(session.get('visit'),session.get('visitpoint_try'),'log_visitpoint', session.get('clientIPA')))
    #db.session.remove()
    #app.logger.critical('###{0}-{1}##SESSION-ALIVE#!!!{2}!!!before_1stquery--session[clientIPA]={3}'.format(session.get('visit'),session.get('visitpoint_try'),'log_visitpoint', session.get('clientIPA')))
    try:
        ok=1
        #visitpoint = VisitPoint.query.filter_by(ip=clientip).first()
        visitpoint = VisitPoint.query.filter_by(ip=clientip, latitude=lat, longitude=lon).first()
    except (sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.DBAPIError) as e:
        ok=0
        visitpoint = None
        # handle exception "e", or re-raise appropriately.
        app.logger.critical('###{0}###!!!{1}!!!EEEEEEERRRRRRRRRRROOOOOOOOORRRRRRRRRR --session[clientIPA]={2}'.format(session.get('visit'),'log_visitpoint', session.get('clientIPA')))
        #db.session.rollback()
        db.session.remove()
        app.logger.critical('###{0}###!!!{1}!!!EEEEEEERRRRRRRRRRROOOOOOOOORRRRRRRRRR --session[clientIPA]={2}'.format(session.get('visit'),'log_visitpoint', session.get('clientIPA')))
        raise
    #app.logger.critical('####################{0}#####!!!{1}!!!after_1stquery --session[clientIPA]={2}'.format(session.get('visit'),'log_visitpoint', session.get('clientIPA')))
    #print('###'+__name__+'###', 'log_visitpoint_after_1stquery')
    ##################################################################
    ##################################################################
    ##################################################################
    if not visitpoint:
        #make new visitpoint
        nextvisitpointNum = get_next_visitpointNumber()
        visitpoint = VisitPoint(
            ip=clientip
            , latitude=lat
            , longitude=lon
            , visitDT=datetime.now()
            , visitpointNumber=nextvisitpointNum
            , visitsCount=1
            #, primarykey=clientip+'|'+str(lat)+'|'+str(lon)
        )
        set_geolocation_from_ip_on_visitpoint(clientip, visitpoint)
        set_geolocation_info_on_visitpoint(lat, lon, visitpoint)
        db.session.add(visitpoint)
        db.session.commit()
        # print('###'+__name__+'###---->', '***new visitpoint***', visitpoint.id)
        # visitpoint = VisitPoint.query.filter_by(ip=clientip, latitude=lat, longitude=lon).first()
        # print('###'+__name__+'###<----', '***new visitpoint***', visitpoint.id)

        session['VisitPointID'] = visitpoint.id
        session['VisitPointNumber'] = visitpoint.visitpointNumber
        #for display on screens
        session['continent_name'] = visitpoint.continent_name
        session['country_name'] = visitpoint.country_name
        session['region_name'] = visitpoint.region_name
        session['city'] = visitpoint.city
        session['latitude'] = str(visitpoint.latitude)
        session['longitude'] = str(visitpoint.longitude)
        session.modified = True
        log_info('*** new visitpoint')
    else:
        log_info('*** existing visitpoint')
        if 'VisitPointID' not in session or 'VisitPointNumber' not in session:
            session['VisitPointID'] = visitpoint.id
            session['VisitPointNumber'] = visitpoint.visitpointNumber
            session['continent_name'] = visitpoint.continent_name
            session['country_name'] = visitpoint.country_name
            session['region_name'] = visitpoint.region_name
            session['city'] = visitpoint.city
            session['latitude'] = str(visitpoint.latitude)
            session['longitude'] = str(visitpoint.longitude)
            session.modified = True
    #print('###'+__name__+'###','log_visitpoint [finish]', visitpoint)
    log_module_finish('log_visitpoint')
    return visitpoint
##########################################################################################################
def log_visit(visitpoint=None):
    log_module_start('log_visit')
    if 'VisitID' not in session:
        visitpoint = log_visitpoint()
        # if not visitpoint or ('VisitPointID' not in session) or not session.get('VisitPointID') or not session.get('clientIPA'):
        #     print('###'+__name__+'###', 'log_visit [no visitpoint]')
        #     visitpoint = log_visitpoint()
        nextvisitNum = get_next_visitNumber()
        #clientDictionary = get_client_info_dictionary()
        #clientip = clientDictionary['clientip']
        #lat = clientDictionary['lat']
        #lon = clientDictionary['lon']   
        visit = Visit(
            visitDT=datetime.now()
            , visitNumber=nextvisitNum
            , visitpoint_ID=visitpoint.id
            , sessionID=session.get('sessionID')
            #, ip=clientip
            #, latitude=lat
            #, longitude=lon
        )
        visitpoint.visitsCount = visitpoint.visitsCount + 1
        db.session.add(visit)
        db.session.commit()
        # print('###'+__name__+'###---->', '***new visit***', visit.id)
        # visitid = db.session.query(func.max(Visit.id)).filter_by(visitNumber=nextvisitNum)
        # visit = Visit.query.filter_by(id=visitid).first()
        # print('###'+__name__+'###<----', '***new visit***', visit.id)
        session['VisitNumber'] = visit.visitNumber
        session['VisitID'] = visit.id
        session.modified = True
        flash('You are Visit # {1}/{0}. Thanks for visiting us!'.format(visitpoint.visitpointNumber, visit.visitNumber,), 'success')
        log_info('*** new visit')
    else:
        log_info('*** existing visit')
        #print('###'+__name__+'###', '***existing visit')
        visitid = session['VisitID']
        visit = Visit.query.filter_by(id=visitid).first()
        if 'VisitNumber' not in session:
            session['VisitNumber'] = visit.visitNumber
    #print('###'+__name__+'###', 'log_visit [finish]', visit)
    log_module_finish('log_visit')
    return visit
##########################################################################################################
def log_page_visit(pageType, pageID, pageURL, pageFunction='', pageTemplate='', pageTemplate_page='', pageTemplate_form=''):
    log_module_start('log_page_visit')

    visit = log_visit()
    #visitid=visit.id
    visitid=session.get('VisitID')
    #make sure is numeric
    try:
        dummy = visitid -1
    except:
        visitid=1

    clientDictionary = get_client_info_dictionary()
    lang = clientDictionary['lang']
    page_visit = Page_Visit(
        pageID=pageID
        , request_method=request.method
        , pageURL=pageURL
        , pageType=pageType
        , pageLanguage=clientDictionary['lang']
        , pageFunction=pageFunction
        , pageTemplate=pageTemplate
        , pageTemplate_page=pageTemplate_page
        , pageTemplate_form=pageTemplate_form
        , visit_ID=visitid
        , sessionID=session.get('sessionID')
    )
    db.session.add(page_visit)
    db.session.commit()
    session['page_visit_id'] = page_visit.id
    #print('###'+__name__+'###', 'log_page_visit [finish]', page_visit)
    log_module_finish('log_page_visit')
##########################################################################################################
def set_geolocation(latitude, longitude):
    set_log_suffix_timestamp(0)
    set_log_suffix(__name__,'')
    log_module_start('set_geolocation')
    #print('###'+__name__+'###', 'set_geolocation [start]')
    session['geolocation'] = [latitude, longitude]
    visitpoint = log_visitpoint()
    if 'VisitID' not in session:
        visit = log_visit(visitpoint)
    else:
        visitid = session['VisitID']
        visit = Visit.query.filter_by(id=visitid).first()
        visitpoint_ID = visitpoint.id
        db.session.commit()
    set_geolocation_info_on_visitpoint(latitude, longitude, visitpoint)
    #print('###'+__name__+'###', 'set_geolocation [finish]',visit, visitpoint)
    log_module_finish('set_geolocation')
##########################################################################################################
##########################################################################################################
##########################################################################################################
### log functions used in rootes and views
##########################################################################################################
##########################################################################################################
##########################################################################################################
def log_page(pageName, pageFunction, pageTemplate='', pageTemplate_page='', page_template_form=''):
    pageID = pageName.upper().replace('_', '-').replace(' ', '-')
    session['pageID'] = pageID
    session['lastpage'] = pageFunction
    session['lastpageURL'] = request.url
    if pageTemplate:
        session['lastpageHTML'] = pageTemplate
    if 'pages' not in session:
        session['pages'] = []
    if 'urls' not in session:
        session['urls'] = []

    if pageName not in session['pages']:
        session['pages'].append(pageName)
        session['urls'].append(request.url)
        
    if len(session['pages']) > 9:
        session['pages'].pop(0)
        session['urls'].pop(0)

    session.modified = True
    w1 = 'page ['
    msg = '{} {} [{}] [{}] {} <--{}'.format(
        session['clientIPA']
        , 'page'
        , session['pageID']
        , request.method
        , request.url
        , session.get('active_module')
        )
    print(msg)
    #print(session['clientIPA'], 'page', session['pageID'], request.method, request.url, '<--'+session.get('active_module'))
    log_page_visit('page', pageID, request.url, pageFunction, pageTemplate, pageTemplate_page, page_template_form)
    #app.logger.info('--%s page:%s %s %s %s', session['clientIPA'], session['pageID'], request.method, request.url, '### '+__name__+' ###')
    #app.logger.info('***page={0}***ip={1}***visit={2}***'.format(pageID, session.get('clientIPA'), session.get('VisitNumber')))

def log_route(pageName, pageFunction='', pageTemplate='', pageTemplate_page='', page_template_form=''):
    routeID = pageName.upper().replace('_', '-').replace(' ', '-')
    print(session['clientIPA'], 'route', routeID, request.method, request.url, '<--'+session.get('active_module'))
    log_page_visit('route', routeID, request.url, pageFunction, pageTemplate, pageTemplate_page, page_template_form)
    #app.logger.info('--%s route:%s %s %s %s', session['clientIPA'], session['routeID'], request.method, request.url, '### '+__name__+' ###')
    #app.logger.info('***route={0}***ip={1}***visit={2}***'.format(routeID, session.get('clientIPA'), session.get('VisitNumber')))

def log_splash_page(pageName, pageFunction, pageTemplate='', pageTemplate_page='', page_template_form=''):
    pageID = pageName.upper().replace('_', '-').replace(' ', '-')
    print(session['clientIPA'], 'splash-page', pageID, request.method, request.url, '<--'+session.get('active_module'))
    log_page_visit('splash_page', pageID, request.url, pageFunction, pageTemplate, pageTemplate_page, page_template_form)
    #app.logger.info('***splash={0}***ip={1}***visit={2}***'.format(pageID, session.get('clientIPA'), session.get('VisitNumber')))

# def log_info(msg):
#     print('   ', msg)

# def log_variable(name='', value=''):
#     msg = '{0}={1}'.format(name, value)
#     print('   ', 'var', msg)

# def log_url_param(name='', value=''):
#     msg = '{0}={1}'.format(name, value)
#     print('   ', 'url-param', msg)

# def log_module_start(module_name):
#     print(app.modules_stack, 'start', module_name)
#     app.modules_stack.append(module_name)

# def log_module_finish(module_name):
#     print(app.modules_stack, 'finish', module_name)
#     app.modules_stack.pop(len(app.modules_stack))


if __name__ == '__main__':
    log_info('test.....')
    log_variable('test', 'test')
