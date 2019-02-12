"""
Routes and views for the flask application.
"""
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

# Import the app from the parent folder (assumed to be the app)
from .. import app
# Import the database object from the main app module
from .. import db

# Import module forms
#from .module_authorization.forms import LoginForm, RegistrationForm, ContactUsForm, forgetPasswordForm
#from .forms import CookiesConsentForm
from .. models import Visit, VisitPoint, Page_Visit
#from flask_login import current_user#, login_required#, login_user, logout_user

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
    #app.logger.info('client IPA is {}'.format(clientipa))
    if request.headers.get('X-Real-IP') is None:
        realclientipa = clientipa
    else:
        realclientipa = request.headers.get('X-Real-IP')
        #print('clientIP from request.headers.get(X-Real-IP)(pythonanywhere)', realclientipa)
        #app.logger.info('###real client IPA is {}'.format(realclientipa))

    session['clientIPA'] = realclientipa
    #app.logger.info('###client IPA is {0}/{1}'.format(clientipa, realclientipa))
    return realclientipa

def get_client_info(clientip):
    print('###'+__name__+'###', 'get_client_info', 'session clientIPA=',session.get('clientIPA'))
    if not session.get('clientIPA'):
        clientip=client_IP()
        print('###'+__name__+'###', 'get_client_info', 'session clientIPA(recalc)=',session.get('clientIPA'))
    ################################################################
    ### ipstack access key
    ################################################################
    #IPSTACK_API_ACCESSKEY = '4022cfd2249c3431953ecf599152892e'
    #IPSTACK_URL = 'http://api.ipstack.com/'
    #IPSTACK_URL_CMD = 'http://api.ipstack.com/{0}?access_key={1}'
    if clientip=='127.0.0.1':
        clientip = '213.149.173.194'

    path = 'http://api.ipstack.com/{0}?access_key={1}'.format(clientip, '4022cfd2249c3431953ecf599152892e')
    log_variable('apistack geolocation path', path)
    r = requests.post(path)
    #print(r)
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

        return response
    else:
        return None
    #res = response.json()
        #print(res)
    #headers = {
    #    'accept': 'application/json'
    #}
    #payload = {
    #    'code': authorization_code,
    #    'client_id': api_params['client_id'],
    #    'client_secret': api_params['client_secret'],
    #    'grant_type': 'authorization_code',
    #    'scope': 'UserOAuth2Security'
    #}

    #r = requests.post(api_url,headers=headers,data=payload)
    #reply_code=r.status_code

    # if not r.status_code == requests.codes.ok:
    #     authorization_token=None
    #     error_text=r.text
    #     error_code=1
    # else:
    #     authorization_token = response['access_token']
    # def ip(self):
    # 	return self.res['ip']

    # def hostname(self):
    # 	return self.res['hostname']

    # def type(self):
    # 	return self.res['type']

    # def continent_code(self):
    # 	return self.res['continent_code']

    # def continent_name(self):
    # 	return self.res['continent_name']

    # def country_code(self):
    # 	return self.res['country_code']

    # def country_name(self):
    # 	return self.res['country_name']

    # def region_code(self):
    # 	return self.res['region_code']

    # def region_name(self):
    # 	return self.res['region_name']

    # def city(self):
    # 	return self.res['city']

    # def zip(self):
    # 	return self.res['zip']

    # def latitude(self):
    # 	return self.res['latitude']

    # def longitude(self):
    # 	return self.res['longitude']

    # def location(self):
    # 	return self.res['location'].json()

    # def timezone(self):
    # 	return self.res['timezone'].json()

    # def currency(self):
    # 	return self.res['currency'].json()

    # def connection(self):
    # 	return self.res['connection'].json()

    # def security(self):
    # 	return self.res['security'].json()
    #return response
###########################################################################
###########################################################################
###########################################################################
### log functions used in rootes and views
###########################################################################
###########################################################################
###########################################################################
def log_page(pageName, pageFunction, pageTemplate='', pageTemplate_page='', page_template_form=''):
    pageID = pageName.upper().replace('_', '-').replace(' ', '-')
    session['pageID'] = pageID
    session['lastpage'] = pageFunction
    session['lastpageURL'] = request.url
    if pageTemplate:
        session['lastpageHTML'] = pageTemplate
    if 'pages' not in session:
        session['pages'] = []
    session['pages'].append(pageName)
    if len(session['pages']) > 9:
        session['pages'].pop(0)

    for p in range(1, len(session['pages'])):
        if p == 1:
            session['pages_history'] = session['pages'][p-1]
        else:
            session['pages_history'] = session['pages_history'] + ">"+ session['pages'][p-1]


    session.modified = True
    print(session['clientIPA'], 'page', session['pageID'], request.method, request.url, '<--'+session.get('active_module'))
    #log_page_visit('page', pageID, request.url, pageFunction, pageTemplate, pageTemplate_page, page_template_form)
    #app.logger.info('--%s page:%s %s %s %s', session['clientIPA'], session['pageID'], request.method, request.url, '### '+__name__+' ###')

def log_route(pageName, pageFunction='', pageTemplate='', pageTemplate_page='', page_template_form=''):
    pageID = pageName.upper().replace('_', '-').replace(' ', '-')
    session['routeID'] = pageID
    # if 'pages' not in session:
    #     session['pages'] = []
    # session['pages'].append(pageName)
    # if len(session['pages']) > 9:
    #     session['pages'].pop(0)
    # for p in range(1, len(session['pages'])):
    #     if p == 1:
    #         session['pages_history'] = session['pages'][p-1]
    #     else:
    #         session['pages_history'] = session['pages_history'] + ">"+ session['pages'][p-1]

    session.modified = True

    print(session['clientIPA'], 'route', session['routeID'], request.method, request.url, '<--'+session.get('active_module'))
    #log_page_visit('route', pageID, request.url, pageFunction, pageTemplate, pageTemplate_page, page_template_form)
    #app.logger.info('--%s route:%s %s %s %s', session['clientIPA'], session['routeID'], request.method, request.url, '### '+__name__+' ###')

def log_splash_page(pageName, pageFunction, pageTemplate='', pageTemplate_page='', page_template_form=''):
    pageID = pageName.upper().replace('_', '-').replace(' ', '-')
    # if 'pages' not in session:
    #     session['pages'] = []
    # session['pages'].append(pageName)
    # if len(session['pages']) > 9:
    #     session['pages'].pop(0)

    # for p in range(1, len(session['pages'])):
    #     if p == 1:
    #         session['pages_history'] = session['pages'][p-1]
    #     else:
    #         session['pages_history'] = session['pages_history'] + ">"+ session['pages'][p-1]

    # session.modified = True

    print(session['clientIPA'], 'splash-page', pageID, request.method, request.url, '<--'+session.get('active_module'))
    #log_page_visit('splash_page', pageID, request.url, pageFunction, pageTemplate, pageTemplate_page, page_template_form)

def log_page_visit(pageType, pageID, pageURL, pageFunction='', pageTemplate='', pageTemplate_page='', pageTemplate_form=''):
    #print('xx log_page_visit xx')
    if 'language' in session:
        lang = session['language']
    else:
        lang = session.get('language', request.accept_languages.best_match(app.config['LANGUAGES'].keys()))
    page_visit = Page_Visit(
        pageID=pageID
        , request_method=request.method
        , pageURL=pageURL
        , pageType=pageType
        , pageLanguage=lang
        , pageFunction=pageFunction
        , pageTemplate=pageTemplate
        , pageTemplate_page=pageTemplate_page
        , pageTemplate_form=pageTemplate_form
        #, clientIPA=session['clientIPA']
        )
    #if 'VisitorID' not in session:
    #    visitpoint = log_visitpoint()
    #page_visit.visitpoint_ID = session['VisitorID']
    if 'VisitID' not in session:
        visit = log_visit()
    page_visit.visit_ID = session['VisitID']

    db.session.add(page_visit)
    db.session.commit()
    session['page_visit_id'] = page_visit.id

def log_info(msg):
    print('   ', msg)

def log_variable(name='', value=''):
    msg = '{0}={1}'.format(name, value)
    print('   ', 'var', msg)

def log_url_param(name='', value=''):
    msg = '{0}={1}'.format(name, value)
    print('   ', 'url-param', msg)

def log_module_start(module_name):
    print(app.modules_stack, 'start', module_name)
    app.modules_stack.append(module_name)
def log_module_finish(module_name):
    print(app.modules_stack, 'finish', module_name)
    app.modules_stack.pop(len(app.modules_stack))

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

def log_visitpoint():
    print('###'+__name__+'###', 'log_visitpoint', 'session clientIPA=',session.get('clientIPA'))
    if not session.get('clientIPA'):
        clientip=client_IP()
        print('###'+__name__+'###', 'log_visitpoint', 'session clientIPA(recalc)=',session.get('clientIPA'))

    visitpoint = VisitPoint.query.filter_by(ip=session['clientIPA']).first()
    if not visitpoint:
        nextvisitpointNum = get_next_visitpointNumber()
        visitpoint = VisitPoint(
            ip=session['clientIPA']
            , visitDT=datetime.now()
            , visitpointNumber=nextvisitpointNum
            , visitsCount=1
            )

        res = get_client_info(session['clientIPA'])
        print('###'+__name__+'###', '***client info***', res)
        if res:
            visitpoint.iptype = res['type']
            visitpoint.continent_code = res['continent_code']
            visitpoint.continent_name = res['continent_name']
            visitpoint.country_code = res['country_code']
            visitpoint.country_name = res['country_name']
            visitpoint.region_code = res['region_code']
            visitpoint.region_name = res['region_name']
            visitpoint.city = res['city']
            visitpoint.zip = res['zip']
            visitpoint.latitude = res['latitude']
            visitpoint.longitude = res['longitude']
            visitpoint.location = res['location'] # this is a dictinary in json format
            # visitpoint.timezone = res['timezone']
            # visitpoint.currency = res['currency']
            # visitpoint.connection = res['connection']
            # visitpoint.security = res['security']
        db.session.add(visitpoint)
        db.session.commit()
        visitpoint = VisitPoint.query.filter_by(ip=session['clientIPA']).first()
        session['VisitorID'] = visitpoint.id
        session['VisitorNumber'] = visitpoint.visitpointNumber
        session['continent_name'] = visitpoint.continent_name
        session['country_name'] = visitpoint.country_name
        session['region_name'] = visitpoint.region_name
        session['city'] = visitpoint.city
        session['latitude'] = str(visitpoint.latitude)
        session['longitude'] = str(visitpoint.longitude)
        session.modified = True
        print('###'+__name__+'###', '***new visitpoint', visitpoint)
    else:
        if 'VisitorID' not in session or 'VisitorNumber' not in session:
            session['VisitorID'] = visitpoint.id
            session['VisitorNumber'] = visitpoint.visitpointNumber
            session['VisitorID'] = visitpoint.id
            session['VisitorNumber'] = visitpoint.visitpointNumber
            session['continent_name'] = visitpoint.continent_name
            session['country_name'] = visitpoint.country_name
            session['region_name'] = visitpoint.region_name
            session['city'] = visitpoint.city
            session['latitude'] = str(visitpoint.latitude)
            session['longitude'] = str(visitpoint.longitude)
            session.modified = True
            get_client_info(session['clihttp://ifestionas.pythonanywhere.com/entIPA'])

    return visitpoint

def log_visit(visitpoint=None):
    print('###'+__name__+'###', 'log_visit','session visitorid= [',session.get('VisitorID'),']')
    if not visitpoint
    or ('VisitorID' not in session)
    or not session.get('VisitorID'):
        visitpoint = log_visitpoint()

    if 'VisitID' not in session or not session.get('VisitID'):
        nextvisitNum = get_next_visitNumber()
        visit = Visit(
            ip=session['clientIPA']
            , visitDT=datetime.now()
            , visitNumber=nextvisitNum
            , visitpoint_ID=visitpoint.id
            )
        visitpoint.visitsCount = visitpoint.visitsCount + 1
        db.session.add(visit)
        db.session.commit()
        visitid = db.session.query(func.max(Visit.id)).filter_by(ip=session['clientIPA'])
        visit = Visit.query.filter_by(id=visitid).first()
        session['VisitNumber'] = nextvisitNum
        session['VisitID'] = visit.id
        session.modified = True
        flash('You are VisitPoint # {0}/{1}. Thanks for visiting us!'.format(visitpoint.visitpointNumber, visit.visitNumber,), 'success')
        print('###'+__name__+'###', '***new visit', visit)
    else:
        visit = Visit.query.filter_by(id=session['VisitID']).first()
        if 'VisitNumber' not in session:
            session['VisitNumber'] = visit.visitNumber
    return visit

if __name__ == '__main__':
    log_info('test.....')
    log_variable('test', 'test')
