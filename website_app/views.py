"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import logging
from . import app
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

#@app.after_request
#def store_visited_urls(self):
    #self.session['urls'].append(request.url)
    #if len(session['urls']) > 5:
    #    session['urls'].pop(0)
    #session.modified = True
#    print('@@@@app.after_request',self.session['urls'])

@app.route('/')
def homepage():
    app.pages='home'
    print('HOME',request.method,request.url)
    #logging.critical('a request!')
    app.logger.info('%s logged in successfully', 'user.username')
    #session['username'] = "someuser"
    #session['urls'] = []
    return render_template(
        'page_templates/landing_page.html'
        ,title='home'
        ,pages=app.pages
    )

@app.route('/landingpage')
def landingpage():
    app.pages='landing page'
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
    print('CONTACT',request.method,request.url)
    #data = []
    #if 'urls' in session:
    #    data = session['urls']

    return render_template(
        'page_templates/contact.html'
        ,title='Ganimides Contact Info'
        ,pages=app.pages
    )

@app.route('/about')
def about():
    app.pages='about'
    print('ABOUT',request.method,request.url)
    return render_template(
        'page_templates/about.html'
        ,title='about Ganimides'
        ,pages=app.pages
    )


@app.route('/company')
def company():
    app.pages='company'
    print('COMPANY',request.method,request.url)
    return render_template(
        'page_templates/company.html'
        ,title='the company'
        ,pages=app.pages
    )

@app.route('/services')
def services():
    app.pages='services'
    print('SERVICES',request.method,request.url)
    return render_template(
        'page_templates/services.html'
        ,title='services'
        ,pages=app.pages
    )

@app.route('/why')
def why():
    app.pages='why'
    print('WHY',request.method,request.url)
    return render_template(
        'page_templates/why.html'
        ,title='why ganimides'
        ,pages=app.pages
    )

@app.route('/research')
def research():
    app.pages='research'
    print('RESEARCH',request.method,request.url)
    return render_template(
        'page_templates/research.html'
        ,title='research'
        ,pages=app.pages
    )

@app.route('/academy')
def academy():
    app.pages='academy'
    print('ACADEMY',request.method,request.url)
    return render_template(
        'page_templates/academy.html'
        ,title='BUSTEC ACADEMY'
        ,pages=app.pages
    )

@app.route('/knowledge')
def knowledge():
    app.pages='knowledge'
    print('KNOWLEDGE',request.method,request.url)
    return render_template(
        'page_templates/knowledge.html'
        ,title='KNOWLEDGE CENTER'
        ,pages=app.pages
    )

@app.route('/prototypes')
def prototypes():
    app.pages='prototypes'
    print('PROTOTYPES',request.method,request.url)
    return render_template(
        'page_templates/prototypes.html'
        ,title='PROTOTYPES'
        ,pages=app.pages
    )

@app.route('/cookies_policy')
def cookies_policy():
    app.pages='cookies policy'
    print('COOKIES',request.method,request.url)
    return render_template(
        'page_templates/cookies_policy.html'
        ,title='cookies policy'
        ,pages=app.pages
    )

@app.route('/privacy_policy')
def privacy_policy():
    app.pages='privacy policy'
    print('PRIVACY_POLICY',request.method,request.url)
    return render_template(
        'page_templates/privacy_policy.html'
        ,title='privacy policy'
        ,pages=app.pages
    )

@app.route('/terms_and_conditions')
def terms_and_conditions():
    app.pages='terms and conditions'
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
    print('MYGAME',request.method,request.url)
    """Renders the app(myBank) home page."""
    return render_template(
        'myGame/myGame.html'
        ,title='myGame'
        ,pages=app.pages
        ,message='gaming prototype........'
    )