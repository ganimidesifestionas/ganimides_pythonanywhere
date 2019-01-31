"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import Flask
from flask import flash
from flask import render_template
from flask import request
from flask import session
from flask import logging
from flask import jsonify

from .. import app
# Import the database object from the main app module
from .. import db

# Import module forms
#from .module_authorization.forms import LoginForm, RegistrationForm, ContactUsForm, forgetPasswordForm
#from .forms import CookiesConsentForm
from .. models import Visit, Visitor, Page_Visit
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import func


def client_IP():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        clientipa = request.environ['REMOTE_ADDR']
    else:
        clientipa = request.environ['HTTP_X_FORWARDED_FOR']
    
    session['clientIPA'] = clientipa
    return clientipa
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
    if not 'pages' in session:
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

    print(session['clientIPA'], 'page', session['pageID'], request.method, request.url, '### '+__name__+' ###')
    log_page_visit('page', pageID, request.url, pageFunction, pageTemplate, pageTemplate_page, page_template_form)

def log_route(pageName, pageFunction='', pageTemplate='', pageTemplate_page='', page_template_form=''):
    pageID = pageName.upper().replace('_','-').replace(' ','-')
    session['routeID'] = pageID
    if not 'pages' in session:
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

    print(session['clientIPA'], 'route', session['routeID'], request.method, request.url, '### '+__name__+' ###')
    log_page_visit('route', pageID, request.url, pageFunction, pageTemplate, pageTemplate_page, page_template_form)

def log_splash_page(pageName, pageFunction, pageTemplate='', pageTemplate_page='', page_template_form=''):
    pageID = pageName.upper().replace('_','-').replace(' ','-')
    if not 'pages' in session:
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

    print(session['clientIPA'], 'splash-page, pageID', request.method, request.url, '#'+__name__+'#')
    log_page_visit('splash_page', pageID, request.url, pageFunction, pageTemplate, pageTemplate_page, page_template_form)

def log_page_visit(pageType, pageID, pageURL, pageFunction='', pageTemplate='', pageTemplate_page='', pageTemplate_form=''):
    if 'language' in session:
        lang = session['language']
    else:
        lang = session.get('language',request.accept_languages.best_match(app.config['LANGUAGES'].keys()))

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
        , clientIPA=session['clientIPA']
        )

    if not 'VisitorID' in session:
        visitor = log_visitor()
    page_visit.visitor_ID = session['VisitorID']
    
    if not 'VisitID' in session:
        visit = log_visit(visitor)
    page_visit.visit_ID = session['VisitID']

    db.session.add(page_visit)
    db.session.commit()

def log_info(msg):
    print('   ', msg)

def log_variable(name='', value=''):
    msg = '{0}={1}'.format(name, value)
    print('   ', 'var',msg)

def log_url_param(name='', value=''):
    msg = '{0}={1}'.format(name, value)
    print('   ', 'url-param',msg)

def get_next_visitorNumber():
    max_id = db.session.query(func.max(Visitor.id)).scalar()
    #log_variable('last visitor id', max_id)
    nextvisitorNum = 1
    if max_id:
        last_visitor = Visitor.query.filter_by(id=max_id).first()
        #log_variable('last visitor', last_visitor)
        if last_visitor:
            #log_variable('last visitor visitorNumber', last_visitor.visitorNumber)
            if last_visitor.visitorNumber:
                nextvisitorNum = last_visitor.visitorNumber + 1
    log_variable('next visitor Number', nextvisitorNum)
    return(nextvisitorNum)

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

    log_variable('next visit Number', nextvisitNum)
    return(nextvisitNum)

def log_visitor():
    visitor = Visitor.query.filter_by(ipa=session['clientIPA']).first()
    if not visitor:
        nextvisitorNum = get_next_visitorNumber()
        visitor = Visitor(
            ipa=session['clientIPA']
            , visitDT=datetime.now()
            , visitorNumber=nextvisitorNum
            , visitsCount=1
            )
        db.session.add(visitor)
        db.session.commit()
        visitor = Visitor.query.filter_by(ipa=session['clientIPA']).first()
        session['VisitorID'] = visitor.id
        session.modified = True
        log_variable('***new visitor', visitor)
    else:
        log_variable('visitor', visitor)
        if not 'VisitorID' in session:
            session['VisitorID'] = visitor.id
            session.modified = True
    
    #log_variable('VisitorID', session['VisitorID'])
    return(visitor)

def log_visit(visitor=None):
    if not visitor:
        visitor = log_visitor()
    if not 'VisitID' in session:
        nextvisitNum = get_next_visitNumber()
        visit = Visit(
            ipa=session['clientIPA']
            , visitDT=datetime.now()
            , visitNumber=nextvisitNum
            , visitor_ID=visitor.id
            )
        visitor.visitsCount = visitor.visitsCount + 1
        db.session.add(visit)
        db.session.commit()
        visitid = db.session.query(func.max(Visit.id)).filter_by(ipa=session['clientIPA'])
        visit = Visit.query.filter_by(id=visitid).first()
        session['VisitNumber'] = nextvisitNum
        session['VisitID'] = visit.id
        session.modified = True

        flash('You are Visitor # {0}. Thanks for visiting us!'.format(nextvisitNum,),'success')
        log_variable('***new visit', visit)
    else:
        visit = Visit.query.filter_by(id=session['VisitID']).first()
        if not 'VisitNumber' in session:
            session['VisitNumber'] = visit.visitNumber
    
    return(visit)

if __name__ == '__main__':
    log_info('test.....')
    log_variable('test','test')
    