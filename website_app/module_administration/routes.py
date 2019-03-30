"""
Controllers (Routes) and views for the flask application.(administration)
"""
import os
import requests
import json
import time
import inspect
from datetime import datetime
from math import ceil

# Import the database object from the main app module
from .. import db
#from app import db

# Import flask dependencies
from flask import Flask
from flask import flash
from flask import render_template
from flask import request, make_response, jsonify, redirect, url_for
from flask import g, session, abort, Response
from flask import Blueprint
from flask import current_app as app
from flask_login import current_user, login_required, login_user, logout_user
from flask_paginate import Pagination, get_page_parameter, get_page_args
from sqlalchemy import func

# Import password / encryption helper tools
#from werkzeug import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from .. external_services.email_services import send_email
#from .. external_services.token_services import generate_confirmation_token, confirm_token, generate_mobileconfirmation_code
#from .. external_services.log_services import *
from .. external_services.token_services import generate_unique_sessionID, generate_confirmation_token, confirm_token, generate_mobileconfirmation_code
from .. external_services.log_services import set_geolocation, client_IP, log_visit, log_page, log_route, log_splash_page, log_self_page, RealClientIPA
from .. external_services.graphs import build_graph

from .. debug_services.debug_log_services import *

# Import module forms
from . forms import UserAdminForm, RoleForm, DepartmentForm, SetPasswordForm, LoginForm, RegistrationForm, PasswordChangeForm, mobileConfirmationForm, UserProfileDisplayForm, UserProfileChangeForm, emailConfirmationForm, PasswordReSetForm, forgetPasswordForm, ContactUsForm, AvatarUploadForm

# Import module models (i.e. User)
from . models import User, Role, Department #,ContactMessage
from ..module_authorization.models import Subscriber
from ..models import VisitPoint, Visit

# Define the blueprint: 'administration', set its url prefix: app.url/administration
administration = Blueprint('administration', __name__, url_prefix='/administration')
#from . import module_administration as administration

#PER_PAGE = 20

def check_admin():
	"""
	Prevent a non admin access
	"""
	if not current_user.is_admin:
		abort(403)
###########################################################################
###########################################################################
###########################################################################
### standard decorators functions
###########################################################################
###########################################################################
###########################################################################
@administration.before_request
def set_cookies():
    #print('###'+__name__+'###', 'before_request')
    session['active_module'] = __name__

    if not session.get('sessionID'):
        token = generate_unique_sessionID()
        session['sessionID'] = token
        print('@@@@@@ NEW SESSION @@@@@@ session_id =', session.get('sessionID'))

    if 'urls' not in session:
        session['urls'] = []
    if 'pages' not in session:
        session['pages'] = []
    if not 'clientIPA' in session:
        clientIPA = client_IP()
        session['clientIPA'] = clientIPA

    if current_user.is_authenticated:
        session['firstName'] = current_user.firstName
        session['lastName'] = current_user.lastName
        session['company'] = current_user.company
        session['jobTitle'] = current_user.jobTitle
        session['email'] = current_user.email
        #contactusform.firstName.data = current_user.firstName
        #contactusform.lastName.data = current_user.lastName
        #contactusform.company.data = current_user.company
        #contactusform.jobTitle.data = current_user.jobTitle
        #contactusform.email.data = current_user.email
        #forgetpasswordform.email.data = current_user.email

    #app.contactusform = contactusform
    #app.forgetpasswordform = forgetpasswordform
    session.modified = True

@administration.after_request
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
def auto_assigned_userName(userid, username):
    if not username:
        username = 'User'

    trialusername = username
    exists = 1
    while exists > 0 and exists < 100:
        u = User.query.filter(User.userName == trialusername, User.id != userid).first()
        if u:
            suffix = '000' + str(exists)
            suffix = suffix[-2:] #right(suffix,2)
            trialusername = username+suffix
            exists = exists + 1
        else:
            exists = 0
    return trialusername

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

def send_emailconfirmation_email(email):
    """ Send an email confirmation email to the user
    """
    log_info('###send_emailconfirmation_email###')
    u = Subscriber.query.filter_by(email=email).first()
    if not u :
        return 'email not found'
    token = generate_confirmation_token(u.email)
    confirm_url = url_for('administration.emailconfirm', token=token, _external=True)
    log_variable('url', confirm_url)
    html = render_template('administration/email_templates/email_confirmation_email.html', confirm_url=confirm_url)
    log_variable('message', html)
    subject = "Please confirm your email"
    result = send_email(u.email, subject, html)
    log_variable('result', result)
    return result

def send_mobileconfirmation_sms(code):
    """ Send a mobile confirmation Code via SMS
    """
    log_info('###send_mobileconfirmation_sms###')
    user = User.query.filter_by(id=current_user.id).first()
    user.mobileConfirmationCode = code
    user.mobileConfirmationCodeDT = datetime.now()
    user.mobileConfirmed = False
    user.mobileConfirmedDT = None
    db.session.commit()
    sms_message = render_template('administration/sms_templates/sms_mobile_confirmation.html', verification_code=code)
    smsfrom = 'Ganimides'
    log_variable('message', sms_message)
    #result = send_sms(user.mobile,smsfrom,sms_message)
    subject = "please confirm your mobile"
    result = send_email(user.email, subject, sms_message)
    log_variable('result',result)
    return(result)

def copy_user_to_subscriber(user,action):
    subscriber = Subscriber.query.filter_by(email=user.email).first()
    if subscriber:
        print('   change subscriber:',subscriber, ' from user',user)
        if action.lower()=='delete':
            #subscriber.role = ''
            #subscriber.status = 'Deleted'
            print('   delete subscriber')
            subscriber.company = ''
            subscriber.jobTitle = ''
            subscriber.accessModules = ''
            print('   user deleted from subscribers')
        else:
            print('   change subscriber')
            subscriber.firstName = user.firstName
            subscriber.lastName = user.lastName
            subscriber.userName = user.userName
            subscriber.mobile = user.mobile
            subscriber.company = user.company
            subscriber.jobTitle = user.jobTitle
            subscriber.accessModules = 'Administration'
            print('   subscriber changed')
    else:
        print('   add user:',user,' to subscribers')
        subscriber = Subscriber(
            email = user.email
            ,firstName = user.firstName
            ,lastName = user.lastName
            ,registeredDT = datetime.now()
            ,userName = user.userName
            ,mobile = user.mobile
            ,company = user.company
            ,jobTitle = user.jobTitle
            ,accessModules = 'Administration'
            ,passwordReset = True
            #,passwordHash = ''
            #,roleX = user.role
            #,isAdmin = user.jobTitle
            #,isUser = True
            )

        # add subscriber to the database
        db.session.add(subscriber)
        print('   subscriber added')
    if not subscriber.emailConfirmed:
        # genereate an email activation code
        result = send_emailconfirmation_email(user.email)
        if result != 'OK':
            error_text = result.dumps()
            ErrorMsg = 'Failed to send confirmation email. Request a New Confirmation Email'
            flash(ErrorMsg, 'error')
            print('   FAILED to send activation email')
        else:
            flash('an activation email has been sent to {}.'.format(subscriber.email),'warning')
            print('   activation email sent.')
class xPagination(object):

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num
###########################################################################
###########################################################################
###########################################################################

##########################################
#put this after @ decorator
##########################################
#how to get a config variable app.config.get('RECAPTCHA_PUBLIC_KEY'))
#how to get a config variable app.config.get('RECAPTCHA_PRIVATE_KEY'))

#request.method:              GET
#request.url:                 http://127.0.0.1:5000/alert/dingding/test?x = y
#request.base_url:            http://127.0.0.1:5000/alert/dingding/test
#request.url_charset:         utf-8
#request.url_root:            http://127.0.0.1:5000/
#str(request.url_rule):       /alert/dingding/test
#request.host_url:            http://127.0.0.1:5000/
#request.host:                127.0.0.1:5000
#request.script_root:
#request.path:                /alert/dingding/test
#request.full_path:           /alert/dingding/test?x = y

#request.args:                ImmutableMultiDict([('x', 'y')])
#request.args.get('x'):       y
###########################################################################
###########################################################################
###########################################################################
### define the routes, accepted methods (GET/POST) and the service function
###########################################################################
###########################################################################
###########################################################################
#@administration.route('/pictures/<path:imagefile>')
#def pathtoimage(imagefile):
    #print('request-/:',request.url)
#    return request.url+'/'+imagefile
#############################################################
#############################################################
#############################################################
### routes and pages
#############################################################
#############################################################
#############################################################
@administration.route('/', methods = ['GET', 'POST'])
def homepage():
    page_name = 'administration-home'
    page_function = 'homepage'
    log_route(page_name, page_function)
    return redirect(url_for('administration.usersadmin',action_tab = ''))


# @administration.route('/users/', defaults={'page': 1})
# @administration.route('/users/page/<int:page>')
# def show_users(page):
#     count = count_all_users()
#     users = get_users_for_page(page, PER_PAGE, count)
#     if not users and page != 1:
#         abort(404)
#     pagination = Pagination(page, PER_PAGE, count)
#     return render_template('users.html',
#         pagination=pagination,
#         users=users
#     )

@administration.route('/usersadmin/', defaults={'action_tab':''} , methods = ['GET', 'POST'])
@administration.route('/usersadmin/<action_tab>', methods = ['GET', 'POST'])
def usersadmin(action_tab='users', userspageNum=0, visitspageNum=0, visitpointspageNum=0):
    print('###1-action_tab', action_tab)
    print('###1-userspageNum', userspageNum)
    print('###1-visitspageNum', visitspageNum)
    print('###1-visitpointspageNum', visitpointspageNum)
    print('')
    page_name = 'useradmin'
    page_function = 'useradmin'
    page_template = 'administration/page_templates/administration_pages_template.html'
    page_template_page = 'usersadmin_page_content.html'
    page_form = ''
    log_page(page_name, page_function, page_template, page_template_page, page_form)
    log_url_param('action_tab',action_tab)
    # if not action_tab or action_tab == '*':
    #     action_tab = 'users'
    #print('###2-action_tab', action_tab)
    #log_url_param('action_tab',action_tab)
    #log_url_param('page',page)
    # page = request.args.get(get_page_parameter(), type=int, default=1)
    # print('###---param page', page)
    userspageNum = request.args.get('userspageNum', type=int, default=1)
    visitspageNum = request.args.get('visitspageNum', type=int, default=1)
    visitpointspageNum = request.args.get('visitpointspageNum', type=int, default=1)
    print('###2-action_tab', action_tab)
    print('###2-userspageNum', userspageNum)
    print('###2-visitspageNum', visitspageNum)
    print('###2-visitpointspageNum', visitpointspageNum)
    print('')
    if not action_tab:
        if userspageNum > 0:
            action_tab = 'users'
        else:
            if visitspageNum > 0:
                action_tab = 'visits'
            else:
                if visitpointspageNum > 0:
                    action_tab = 'visitpoints'
                else:
                    action_tab = 'users'
    print('###3-action_tab', action_tab)
    print('###3-userspageNum', userspageNum)
    print('###3-visitspageNum', visitspageNum)
    print('###3-visitpointspageNum', visitpointspageNum)
    print('')

    # if action_tab.lower == 'visits':
    #     visitspageNum = page
    # else:
    #     if action_tab.lower == 'visitpoints':
    #         visitpointspageNum = page
    #     else:
    #         userspageNum = page

    log_url_param('action_tab',action_tab)
    log_url_param('userspageNum',userspageNum)
    log_url_param('visitspageNum',visitspageNum)
    log_url_param('visitpontspageNum',visitpointspageNum)

    #users = get_users_for_page(userspage, PER_PAGE, userscount)
    #userspagination1 = User.query.order_by(User.id).paginate(userspageNum, app.config.get('PER_PAGE',2), False)

    search = False
    q = request.args.get('q')
    if q:
        search = True

    #print('###1.userspageNum', userspageNum)
    #page = request.args.get('userspageNum', type=int, default=page)
    #print('###3.userspageNum', userspageNum)

    #users = User.query.all()
    # #print('############users1:', users.count(User.id))
    # c = 0
    # for user in users:
    #     c = c + 1
    #     print(c,user)
    # print('############users1a:', c)
    # count User records, without
    # using a subquery.
    #session.query(func.count(User.id))
    #db.session.commit()
    #userscount = User.query.all(func.count(User.id))
    #User.query.filter(UserImage.user_id == 1).count()
    # userscount = User.query.all().count()
    # print('############users2:', userscount)
    # userscount = db.session.query(User).all().count(User.id)
    # print('############users3:', userscount)
    total_users = db.session.query(func.count(User.id)).scalar() 
    #print('############total_users:', total_users)
    #Pagination.__init__()
    #pagination = Pagination(page_parameter='page')
    #pagination = Pagination(per_page_parameter='pp')
    #total = g.cur.fetchone()[0]
    #page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    #print('############1params:', page, per_page, offset)
    page, per_page, offset = get_page_args(page_parameter='userspageNum', per_page_parameter='per_page')
    #print('############2params:', page, per_page, offset)
    sql = 'select name from users order by name limit {}, {}'\
        .format(offset, per_page)
    #print('############sql:', sql)
    #users = User.query.all()
    #users = User.query.order_by(User.userName).limit(offset,per_page).all()
    users = User.query.order_by(User.userName).paginate(page=userspageNum, per_page=per_page).items
    #g.cur.execute(sql)
    #users = g.cur.fetchall()
    # pagination = get_pagination(page=page,
    #                             per_page=per_page,
    #                             total=userscount,
    #                             record_name='users',
    #                             format_total=True,
    #                             format_number=True,
    #                             )
# def get_pagination(**kwargs):
#     kwargs.setdefault('record_name', 'records')
#     return Pagination(
#         css_framework=get_css_framework(),
#                       link_size=get_link_size(),
#                       alignment=get_alignment(),
#                       show_single_page=show_single_page_or_not(),
#                       **kwargs
#                       )
    page, per_page, offset = get_page_args(page_parameter='userspageNum', per_page_parameter='per_page')
    #print('users_page',page)
    href = url_for('administration.usersadmin', action_tab='users', userspageNum='0').replace('=0','={0}')
    #print('href_users',href)
    #print('users_page',userspageNum)
    userspagination = Pagination(
        page=page,
        total=total_users,
        search=search,
        record_name='users',
        css_framework=app.config.get('CSS_FRAMEWORK', 'bootstrap4'),
        link_size=app.config.get('LINK_SIZE', 'sm'),
        alignment=app.config.get('LINK_ALIGNMENT', ''),
        show_single_page=app.config.get('SHOW_SINGLE_PAGE', False),
        per_page=app.config.get('PER_PAGE', 10),
        page_parameter='page',
        href=href,
        )
    print('users_page',userspagination.page)
    #userspagination = Pagination(page=userspageNum, total=userscount, search=search, record_name='users')
    #print('#####per_page', userspagination.per_page)
    # 'page' is the default name of the page parameter, it can be customized
    # e.g. Pagination(page_parameter='p', ...)
    # or set PAGE_PARAMETER in config file
    # also likes page_parameter, you can customize for per_page_parameter
    # you can set PER_PAGE_PARAMETER in config file
    # e.g. Pagination(per_page_parameter='pp')
    #log_variable('userspagination.info', userspagination.info)
    #log_variable('userspagination.links', userspagination.links)

    # existingISG = ISG.query \
    # .filter(or_(ISG.coouserspaginationrdinator_status == 'IAT Verified', ISG.coordinator_status == 'New')) \
    # .order_by("isg.id desc") \
    # .paginate(page,per_page,error_out=False)
    #users = User.query.all()
    #if not users and page != 1:
    #    abort(404)
    # = Pagination(userspageNum, PER_PAGE, userscount)
    #users = userspagination.items

    # users_nexturl = None
    # users_prevurl = None
    # if userspagination.has_next:
    #     #users_nexturl = url_for('administration.usersadmin', action_tab='users', userspageNum=userspagination.next_num, visitspageNum=1, visitpointspageNum=1)
    #     users_nexturl = url_for('administration.usersadmin', action_tab='users', pages='{1,1,1,1}')
    # if userspagination.has_prev:
    #     #users_prevurl = url_for('administration.usersadmin', action_tab='users', userspageNum=userspagination.prev_num, visitspageNum=1, visitpointspageNum=1)
    #     users_nexturl = url_for('administration.usersadmin', action_tab='users', pages='{1,1,1,1}')

    roles = Role.query.all()
    departments = Department.query.all()
    
    #visitpoints
    total_visitpoints = db.session.query(func.count(VisitPoint.id)).scalar() 
    log_variable('total_visitpoints:', total_visitpoints)
    visitpoints = VisitPoint.query.order_by(VisitPoint.lastvisitDT.desc()).paginate(page=visitpointspageNum, per_page=per_page).items
    #visitpointspagination = Pagination(page=visitpointspageNum, total=total_visitpoints, search=search, record_name='visitpoints')
    page, per_page, offset = get_page_args(page_parameter='visitpointspageNum', per_page_parameter='per_page')
    #print('visitpoints_page',page)
    href=url_for('administration.usersadmin',action_tab='visitpoints',visitpointspageNum='0').replace('=0','={0}')
    #print('href_visitpoints',href)
    #print('visitpoints_page',visitpointspageNum)
    visitpointspagination = Pagination(
        page=page,
        total=total_visitpoints,
        search=search,
        record_name='visit points',
        css_framework=app.config.get('CSS_FRAMEWORK', 'bootstrap4'),
        link_size=app.config.get('LINK_SIZE', 'sm'),
        alignment=app.config.get('LINK_ALIGNMENT', ''),
        show_single_page=app.config.get('SHOW_SINGLE_PAGE', False),
        per_page=app.config.get('PER_PAGE', 10),
        page_parameter='page',
        href=href
        )
    print('visitpoints_page',visitpointspagination.page)

    #visitpoints = VisitPoint.query.all()
    #visitpoints = VisitPoint.query.order_by(VisitPoint.lastvisitDT.desc()).limit(100).all()



    #visits = Visit.query.all()
    # visits = Visit.query
    #                 # .filter_by(party_id=form.party.data)
    #                 # .filter_by(topic_id=form.topic.data)
    #                 .join('VisitPoint')
    #                 .all()


    #visits
    total_visits = db.session.query(func.count(Visit.id)).scalar() 
    log_variable('total_visits:', total_visits)
    visits = Visit.query.join('visitpoint').order_by(Visit.visitDT.desc()).paginate(page=visitspageNum, per_page=per_page).items
    page, per_page, offset = get_page_args(page_parameter='visitspageNum', per_page_parameter='per_page')
    #print('visits_page1',page)
    href=url_for('administration.usersadmin',action_tab='visits',visitspageNum='0').replace('=0','={0}')
    #href: Add custom href for links - this supports forms with post method. MUST contain {0} to format page number        
    #print('visits_page2',visitspageNum)
    #print('href_visits',href)
    #visitspagination = Pagination(page=visitspageNum, total=total_visits, search=search, record_name='visits')
    visitspagination = Pagination(
        page=page,
        total=total_visits,
        search=search,
        record_name='visits',
        css_framework=app.config.get('CSS_FRAMEWORK', 'bootstrap4'),
        link_size=app.config.get('LINK_SIZE', 'sm'),
        alignment=app.config.get('LINK_ALIGNMENT', ''),
        show_single_page=app.config.get('SHOW_SINGLE_PAGE', False),
        per_page=app.config.get('PER_PAGE', 10),
        page_parameter='page',
        href=href,
        )
    print('visits_page',visitspagination.page)

    #print(users)
    #print(roles)
    #print(departments)
    #print(visitpoints)
    #print(visits)
    #print('###action_tab',action_tab)
    return render_template(
        'administration/page_templates/administration_pages_template.html',
        displayPage='usersadmin_page_content.html',
        activeTAB=action_tab,
        users=users,
        roles=roles,
        departments=departments,
        visitpoints=visitpoints,
        visits=visits,
        usersPagination=userspagination,
        visitsPagination=visitspagination,
        visitpointsPagination=visitpointspagination,
    )

@administration.route('/visits', methods=['GET'])
def visitspage():
    page_name = 'visitspage'
    page_function = 'visitspage'
    page_template = 'administration/page_templates/administration_pages_template.html'
    page_template_page = 'visits_page_content.html'
    page_form = ''
    log_page(page_name, page_function, page_template, page_template_page, page_form)
    visitspageNum = request.args.get('page', type=int, default=1)
    log_url_param('page',visitspageNum)
    search = False
    q = request.args.get('q')
    if q:
        search = True
    total_visits = db.session.query(func.count(Visit.id)).scalar() 
    log_variable('total_visits:', total_visits)
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    visits = Visit.query.join('visitpoint').order_by(Visit.visitDT.desc()).paginate(page=visitspageNum, per_page=per_page).items
    visitspagination = Pagination(
        page=page,
        total=total_visits,
        search=search,
        record_name='visits',
        page_parameter='page',
        css_framework=app.config.get('CSS_FRAMEWORK', 'bootstrap4'),
        link_size=app.config.get('LINK_SIZE', 'sm'),
        alignment=app.config.get('LINK_ALIGNMENT', ''),
        show_single_page=app.config.get('SHOW_SINGLE_PAGE', False),
        per_page=app.config.get('PER_PAGE', 10),
        )
    print('visits_page', visitspagination.page)
    
    xvisits = db.session.query(func.date(Visit.date_created),func.count(Visit.id)).group_by(func.date(Visit.date_created)).all()
    #visitsX = db.session.query(func.date(Visit.date_created)).group_by(func.date(Visit.date_created)).all()
    #visitsY = db.session.query(func.count(Visit.id)).group_by(func.date(Visit.date_created)).all()
    #print ('################',xvisits)
    #print ('################',visitsX)
    #print('################', visitsY)
    X = []
    Y = []
    for x in xvisits:
        X.append(x[0]) 
        Y.append(x[1])
    print('#####',X)
    print('#####',Y)
    # #These coordinates could be stored in DB
    x1 = [0, 1, 2, 3, 4]
    y1 = [10, 30, 40, 5, 50]
    x2 = [0, 1, 2, 3, 4]
    y2 = [50, 30, 20, 10, 50]
    x3 = [0, 1, 2, 3, 4]
    y3 = [0, 30, 10, 5, 30]

    graph1_url = build_graph(x1,y1)
    graph2_url = build_graph(x2,y2)
    #graph3_url = build_graph(x3,y3)
    graph3_url = build_graph(X,Y)

    # return render_template('graphs.html',
    # graph1=graph1_url,
    # graph2=graph2_url,
    # graph3=graph3_url)

    return render_template(
        'administration/page_templates/administration_pages_template.html',
        displayPage="visits_page_content.html",
        visits=visits,
        visitsPagination=visitspagination,
        graph1=graph1_url,
        graph2=graph2_url,
        graph3=graph3_url
    )

@administration.route('/visitpoints', methods=['GET'])
def visitpointspage():
    page_name = 'visitpointspage'
    page_function = 'visitpointspage'
    page_template = 'administration/page_templates/administration_pages_template.html'
    page_template_page = 'visitpoints_page_content.html'
    page_form = ''
    log_page(page_name, page_function, page_template, page_template_page, page_form)
    visitpointspageNum = request.args.get('page', type=int, default=1)
    log_url_param('page',visitpointspageNum)
    search = False
    q = request.args.get('q')
    if q:
        search = True
    total_visitpoints = db.session.query(func.count(VisitPoint.id)).scalar() 
    log_variable('total_visitpoints:', total_visitpoints)
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    visitpoints = VisitPoint.query.order_by(VisitPoint.lastvisitDT.desc()).paginate(page=visitpointspageNum, per_page=per_page).items
    visitpointspagination = Pagination(
        page=page,
        total=total_visitpoints,
        search=search,
        record_name='visit points',
        page_parameter='page',
        css_framework=app.config.get('CSS_FRAMEWORK', 'bootstrap4'),
        link_size=app.config.get('LINK_SIZE', 'sm'),
        alignment=app.config.get('LINK_ALIGNMENT', ''),
        show_single_page=app.config.get('SHOW_SINGLE_PAGE', False),
        per_page=app.config.get('PER_PAGE', 10),
        )
    print('visitpoints_page',visitpointspagination.page)
    return render_template(
        'administration/page_templates/administration_pages_template.html',
        displayPage="visitpoints_page_content.html",
        visitpoints=visitpoints,
        visitpointsPagination=visitpointspagination,
    )

@administration.route('/useredit/<action>/<int:id>', methods = ['GET', 'POST'])
def useredit(action, id):
    page_name = 'UserEdit'
    page_function = 'useredit'
    page_template = 'administration/page_templates/administration_forms_template.html'
    page_template_page = ''
    page_form = 'form_user_edit.html'
    log_page(page_name, page_function, page_template, page_template_page, page_form)
    log_url_param('id',id)
    log_url_param('action',action)
    if request.method=='GET':
        #fill-in the form from database
        form = UserAdminForm()
        user = User.query.filter_by(id = id).first()
        if not(user):
            user = User(
                id=0
                ,firstName="first name"
                ,lastName="last name"
                )
        # handle nulls
        if not(user.id):
            user.id = 0
        #print('   ','form init',form.__class__.__name__)
        form.action.data = action
        form.id.data = user.id
        form.email.data = user.email
        form.firstName.data = user.firstName
        form.lastName.data = user.lastName
        form.company.data = user.company
        form.jobTitle.data = user.jobTitle
        form.mobile.data = user.mobile
        form.userName.data = user.userName
        form.department.data = user.department
        form.roles.data = user.user_roles

    if request.method=='POST':
        form = UserAdminForm()
        try:
            post_action = request.form['submit']
        except:
            post_action = ''
        if not post_action:
            try:
                post_action = request.form['action']
            except:
                post_action = ''
        log_variable('post_action',post_action)

        if post_action.lower() in ['cancel','close'] :
            return redirect(url_for('administration.usersadmin',action_tab = 'users'))

        if not(form.validate_on_submit()):
            #form input has errors
            log_info('form input has errors')
            dummy = 1
        else:
            #copy url_parameters to form (not passed from post)
            form.action.data = action
            form.id.data = id

            #delete record
            if action.lower()=='delete':
                user = User.query.filter_by(id = id).first()
                userName = user.email
                if user is None:
                    flash("user record {id} not found".format(id = id),'warning')
                    return redirect(url_for('administration.usersadmin',action_tab = 'users'))
                # delete subscriber record
                copy_user_to_subscriber(user,'delete')
                # delete from db
                db.session.delete(user)
                db.session.commit()
                flash("user [{u}] deleted".format(u = userName),'success')
                return redirect(url_for('administration.usersadmin',action_tab = 'users'))

            #add record
            if action.lower()=='add':
                r = User.query.filter_by(email = form.email.data).first()
                if r :
                    form.email.errors.append("user already exists")
                else:
                    r = User.query.filter_by(email = form.email.data).first()
                    if r :
                        form.email.errors.append("user already exists")
                    else:
                        form.userName.data = auto_assigned_userName(id,form.userName.data)
                        user = User(
                        email = form.email.data
                        ,firstName = form.firstName.data
                        ,lastName = form.lastName.data
                        ,company = form.company.data
                        ,jobTitle = form.jobTitle.data
                        ,mobile = form.mobile.data
                        ,userName = form.userName.data
                        ,department = form.department.data
                        ,user_roles = form.roles.data
                            )
                        #changed_by
                        #user = User.query.filter_by(id = current_user.id).first()
                        # add to the database
                        db.session.add(user)
                        # add user to subscribers
                        copy_user_to_subscriber(user,'add')
                        db.session.commit()
                        flash("user [{u}] added".format(u = user.email),'success')
                        return redirect(url_for('administration.usersadmin',action_tab = 'users'))

            #change record
            #if action.lower() not in ['add','delete','']:
            action = 'Update'
            user = User.query.filter_by(id = id).first()
            if user is None:
                flash("user record {id} not found".format(id = id),'warning')
                return redirect(url_for('administration.usersadmin',action_tab = 'users'))

            if (user.email == form.email.data
                and user.firstName == form.firstName.data
                and user.lastName == form.lastName.data
                and user.company == form.company.data
                and user.jobTitle == form.jobTitle.data
                and user.mobile == form.mobile.data
                and user.userName == form.userName.data
                and user.department == form.department.data
                and user.user_roles == form.roles.data
            ):
                copy_user_to_subscriber(user,'change')
                flash('Nothing changed!','info')
                return redirect(url_for('administration.usersadmin',action_tab = 'users'))

            ok = True
            if user.email  != form.email.data:
                r = User.query.filter_by(email = form.email.data).first()
                if r :
                    form.email.errors.append("user [{u}] already exists".format(u = r.email))
                    ok = False

            #all ok:
            if ok:
                user = User.query.filter_by(id = id).first()
                userName = user.email
                form.userName.data = auto_assigned_userName(id,form.userName.data)
                # get field values from form
                user.email = form.email.data
                user.firstName = form.firstName.data
                user.lastName = form.lastName.data
                user.company = form.company.data
                user.jobTitle = form.jobTitle.data
                user.mobile = form.mobile.data
                user.userName = form.userName.data
                user.department = form.department.data
                user.user_roles = form.roles.data
                #changed_by
                #user = User.query.filter_by(id = current_user.id).first()
                copy_user_to_subscriber(user,'change')
                # update user in database
                db.session.commit()
                flash("user {r} updated".format(r = userName),'success')

                return redirect(url_for('administration.usersadmin',action_tab = 'users'))

    #load user edit page
    return render_template(
        'administration/page_templates/administration_forms_template.html',
        formPage='form_user_edit.html',
        useredit_form=form,
        )

#tispaolas
@administration.route('/roleedit/<action>/<int:id>', methods = ['GET', 'POST'])
def roleedit(action,id):
    page_name = 'RoleEdit'
    page_function = 'roleedit'
    page_template = 'administration/page_templates/administration_forms_template.html'
    page_template_page = ''
    page_form = 'form_role_edit.html'
    log_page(page_name, page_function, page_template, page_template_page, page_form)
    log_url_param('id',id)
    log_url_param('action',action)
    if request.method=='GET':
        #fill-in the form from database
        form = RoleForm()
        role = Role.query.filter_by(id = id).first()
        if not(role):
            role = Role(
                id = 0
                ,name = "role name"
                ,description = "description"
                )
        # handle nulls
        if not(role.name):
            role.name = ''
        if not(role.description):
            role.description = ''
        # from the url params
        form.action.data = action
        form.id.data = role.id
        form.submit.data = action
        # from the database
        form.name.data = role.name
        form.description.data = role.description

    if request.method=='POST':
        form = RoleForm()
        try:
            post_action = request.form['submit']
        except:
            post_action = ''
        if not post_action:
            try:
                post_action = request.form['action']
            except:
                post_action = ''
        log_variable('***post_action',post_action)
        if post_action.lower() in ['cancel','close'] :
            return redirect(url_for('administration.usersadmin',action_tab = 'roles'))

        if not(form.validate_on_submit()):
            #form input has errors
            log_info('form input has errors')
            dummy = 1
        else:
            #copy url_parameters to form (not passed from post)
            form.action.data = action
            form.id.data = id

            #delete record
            if action.lower()=='delete':
                role = Role.query.filter_by(id = id).first()
                roleName = role.name
                if role is None:
                    flash("role record {id} not found".format(id = id),'warning')
                    return redirect(url_for('administration.usersadmin',action_tab = 'roles'))
                db.session.delete(role)
                db.session.commit()
                flash("role [{r}] deleted".format(r = roleName),'success')
                return redirect(url_for('administration.usersadmin',action_tab = 'roles'))

            #add record
            if action.lower()=='add':
                r = Role.query.filter_by(name = form.name.data).first()
                if r :
                    form.name.errors.append("role already exists")
                else:
                    r = Role.query.filter_by(description = form.description.data).first()
                    if r :
                        form.description.errors.append("role [{role}] already exists with this description".format(role = r.name))
                    else:
                        role = Role(
                            name = form.name.data
                            ,description = form.description.data
                            )
                        db.session.add(role)
                        db.session.commit()
                        flash("role [{name}] added".format(name = role.name),'success')
                        return redirect(url_for('administration.usersadmin',action_tab = 'roles'))

            #update record
            #if action.lower() not in ['add','delete','']:
            action = 'Update'
            role = Role.query.filter_by(id = id).first()
            if role is None:
                flash("role record {id} not found".format(id = id),'warning')
                return redirect(url_for('administration.usersadmin',action_tab = 'roles'))

            if (role.name == form.name.data
                and role.description == form.description.data
                ):
                flash('Nothing changed!','info')
                return redirect(url_for('administration.usersadmin',action_tab = 'roles'))

            ok = True
            if role.name  != form.name.data:
                r = Role.query.filter_by(name = form.name.data).first()
                if r :
                    form.name.errors.append("role [{role}] already exists".format(role = r.name))
                    ok = False
            if role.description  != form.description.data:
                r = Role.query.filter_by(description = form.description.data).first()
                if r :
                    form.description.errors.append("role [{0}] already exists".format(r.description))
                    ok = False
            #all ok:
            if ok:
                role = Role.query.filter_by(id = id).first()
                VarRoleName = role.name
                role.name = form.name.data
                role.description = form.description.data
                # update role in database
                db.session.commit()
                flash("role {r} updated".format(r = VarRoleName),'success')
                return redirect(url_for('administration.usersadmin',action_tab = 'roles'))

    #load role edit page
    return render_template('administration/page_templates/administration_forms_template.html'
        , title='Role'
        , formPage='form_role_edit.html'
        , roleedit_form=form
        )

@administration.route('/departmentedit/<action>/<int:id>', methods = ['GET', 'POST'])
def departmentedit(action,id):
    page_name = 'DepartmentEdit'
    page_function = 'departmentedit'
    page_template = 'administration/page_templates/administration_forms_template.html'
    page_template_page = ''
    page_form = 'form_department_edit.html'
    log_page(page_name, page_function, page_template, page_template_page, page_form)
    log_url_param('id',id)
    log_url_param('action',action)

    if request.method=='GET':
        #fill-in the form from database
        form = DepartmentForm()
        department = Department.query.filter_by(id = id).first()
        if not(department):
            department = Department(
                id = 0
                ,name = "department name"
                ,description = "description"
                )
        # handle nulls
        if not(department.name):
            department.name = ''
        if not(department.description):
            department.description = ''
        # from the url params
        form.action.data = action
        form.id.data = department.id
        form.submit.data = action
        # from the database
        form.name.data = department.name
        form.description.data = department.description

    if request.method=='POST':
        form = DepartmentForm()
        try:
            post_action = request.form['submit']
        except:
            post_action = ''
        if not post_action:
            try:
                post_action = request.form['action']
            except:
                post_action = ''
        log_variable('***post_action',post_action)
        if post_action.lower() in ['cancel','close'] :
            return redirect(url_for('administration.usersadmin',action_tab = 'departments'))

        if not(form.validate_on_submit()):
            #form input has errors
            log_info('form input has errors')
            dummy = 1
        else:
            #copy url_parameters to form (not passed from post)
            form.action.data = action
            form.id.data = id
            #delete record
            if action.lower()=='delete':
                department = Department.query.filter_by(id = id).first()
                VarDepartmentName = department.name
                if department is None:
                    flash("department record {id} not found (internal error)".format(id = id),'warning')
                    return redirect(url_for('administration.usersadmin',action_tab = 'departments'))
                db.session.delete(department)
                db.session.commit()
                flash("department [{0}] deleted".format(VarDepartmentName),'success')
                return redirect(url_for('administration.usersadmin',action_tab = 'departments'))

            #add record
            if action.lower()=='add':
                r = Department.query.filter_by(name = form.name.data).first()
                if r :
                    form.name.errors.append("department already exists")
                else:
                    r = Department.query.filter_by(description = form.description.data).first()
                    if r :
                        form.description.errors.append("department [{0}] already exists with this description".format(r.name))
                    else:
                        department = Department(
                            name = form.name.data
                            ,description = form.description.data
                            )
                        # add to the database
                        db.session.add(department)
                        db.session.commit()
                        flash("department [{0}] added".format(department.name),'success')
                        return redirect(url_for('administration.usersadmin',action_tab = 'departments'))

            #change record
            action = 'Update'
            department = Department.query.filter_by(id = id).first()
            if department is None:
                flash("department record {id} not found".format(id = id),'warning')
                return redirect(url_for('administration.usersadmin',action_tab = 'departments'))

            if (department.name == form.name.data
                and department.description == form.name.description
                ):
                flash('Nothing changed!','info')
                return redirect(url_for('administration.usersadmin',action_tab = 'departments'))

            ok = True
            if department.name  != form.name.data:
                r = department.query.filter_by(name = form.name.data).first()
                if r :
                    form.name.errors.append("department [{0}] already exists".format(r.name))
                    ok = False
            if department.description  != form.description.data:
                r = department.query.filter_by(description = form.description.data).first()
                if r :
                    form.description.errors.append("department [{0}] already exists".format(r.description))
                    ok = False
            #all ok:
            if ok:
                department = Department.query.filter_by(id = id).first()
                VarDepartmentName = department.name #before change
                department.name = form.name.data
                department.description = form.description.data
                # update department in database
                db.session.commit()
                flash("department {0} updated".format(VarDepartmentName),'success')
                return redirect(url_for('administration.usersadmin',action_tab = 'departments'))

    #load department edit page
    return render_template('administration/page_templates/administration_forms_template.html'
        , title='Department'
        , formPage='form_department_edit.html'
        , departmentedit_form=form
        )

@administration.route('/setpassword/<email>', methods = ['GET', 'POST'])
def setpassword(email = ''):
    page_name = 'user-password-set'
    page_function = 'setpassword'
    page_template = 'administration/page_templates/administration_forms_template.html'
    page_template_page = ''
    page_form = 'form_password_set.html'
    log_page(page_name, page_function, page_template, page_template_page, page_form)

    form = SetPasswordForm()
    varTitle = 'Password Set'
    form.email.data = email
    # special case retrieve the email from the currently login user
    if email=='*':
        user = User.query.filter_by(id = current_user.id).first()
        email = user.email

    subscriber = Subscriber.query.filter_by(email = form.email.data).first_or_404()
    if not(subscriber):
        flash('invalid email. Retry','error')
    if form.validate_on_submit():
        subscriber.password = form.new_password.data
        subscriber.passwordReset = False
        db.session.commit()
        flash('You have successfully set your password.','success')
        flash('login with your password.','info')
        # redirect to the login page
        return redirect(url_for('authorization.login'))

    # load passsword set template
    return render_template('administration/page_templates/administration_forms_template.html'
        , form=form
        , title=varTitle
        , formPage='form_password_set.html'
        )
#############################################################
#############################################################
#############################################################
### routes: confirmation pages with email link, after send emal or sms etc.
#############################################################
#############################################################
#############################################################
@administration.route('/confirm/<token>')
def emailconfirm(token):
    page_name = 'user-email-confirmation'
    page_function = 'emailconfirm'
    log_route(page_name, page_function)
    try:
        email = confirm_token(token,3600)
    except:
        flash('The confirmation link is invalid or has expired.Retry', 'warning')
        return redirect(url_for('authorization.userprofile'))

    if not(email):
        flash('The confirmation link is invalid or has expired.Retry', 'warning')
        return redirect(url_for('authorization.userprofile'))

    subscriber = Subscriber.query.filter_by(email = email).first_or_404()
    if subscriber.emailConfirmed:
        flash('Email already confirmed. Please login.', 'info')
    else:
        subscriber.emailConfirmed = True
        subscriber.emailConfirmedDT = datetime.now()
        db.session.add(subscriber)
    user = User.query.filter_by(email = email).first_or_404()
    if not user.emailConfirmed:
        user.emailConfirmed = True
        user.emailConfirmedDT = datetime.now()
        db.session.add(user)

    db.session.commit()
    flash('You have confirmed your Email. Thanks!', 'success')

    return redirect(url_for('administration.setpassword',email=email))
