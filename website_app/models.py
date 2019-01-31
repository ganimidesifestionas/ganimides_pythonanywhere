# myApp/module_authorization/models.py
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
# Import the database object (db) from the main application module. We define the db inside /myApp/__init__.py
from .import db
from .import login_manager


# Define a reusable base model for other database tables to inherit (will be part of all defined tables)
class Base(db.Model):
    __abstract__  = True
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),onupdate=db.func.current_timestamp())
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    id            = db.Column(db.Integer, primary_key=True)

###########################################################################
class Visitor(Base):
    """
    Create a Visitors table in mySQL
    """
    # Ensures table will be named in plural and not in singular, as is the name of the model
    __tablename__ = 'visitors'

    id = db.Column(db.Integer, primary_key=True)
    ipa = db.Column(db.String(60), index=True, unique=True, nullable=True,default='')
    visitorNumber = db.Column(db.Integer, nullable=True, default=1)
    visitsCount = db.Column(db.Integer, nullable=True, default=1)
    visitDT = db.Column(db.DateTime, nullable=False)
    visits = db.relationship("Visit", backref='visitor')

    #email = db.Column(db.String(60), index=True, unique=True)
    #userName = db.Column(db.String(60), index=True, unique=True , default='')
    #firstName = db.Column(db.String(60), index=True , default='')
    #lastName = db.Column(db.String(60), index=True , default='')
    #roleX = db.Column(db.String(60), index=True , default='')
    #mobile = db.Column(db.String(20), index=True , default='')
    #company = db.Column(db.String(60), index=True , default='')
    #jobTitle = db.Column(db.String(60), index=True , default='')
    #agreeTerms = db.Column(db.Boolean, nullable=False, default=False)
    #agreeTermsDT = db.Column(db.DateTime, nullable=True)
    #mailingListSignUp = db.Column(db.Boolean, nullable=False, default=False)
    #mailingListSignUpDT = db.Column(db.DateTime, nullable=True)
    #rememberMe = db.Column(db.Boolean, nullable=False, default=False)
    #passwordHash = db.Column(db.String(128) , default='')
    #passwordReset = db.Column(db.Boolean, nullable=False, default=False)
    #confirmedDT = db.Column(db.DateTime, nullable=True)
    #lastLoginDT = db.Column(db.DateTime, nullable=True)
    #mobileConfirmed = db.Column(db.Boolean, nullable=False, default=False)
    #mobileConfirmedDT = db.Column(db.DateTime, nullable=True)
    #emailConfirmed = db.Column(db.Boolean, nullable=False, default=False)
    #emailConfirmedDT = db.Column(db.DateTime, nullable=True)
    #mobileConfirmationCodeHash = db.Column(db.String(128), nullable=True,default='')
    #mobileConfirmationCodeDT = db.Column(db.DateTime, nullable=True)
    #avatarImageFile = db.Column(db.String(255), nullable=True)
    #accessModules = db.Column(db.String(255), nullable=True)
    #departmentID = db.Column(db.Integer, db.ForeignKey('departments.id'))
    #roleID = db.Column(db.Integer, db.ForeignKey('roles.id'))
    #isAdmin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<visitor: {0} ipa:{1}>'.format(self.id,self.ipa)
###########################################################################
class Visit(Base):
    """
    Create a Visits table in mySQL
    """
    # Ensures table will be named in plural and not in singular, as is the name of the model
    __tablename__ = 'visits'

    id = db.Column(db.Integer, primary_key=True)
    visitNumber = db.Column(db.Integer, nullable=True, default=0)
    visitDT = db.Column(db.DateTime, nullable=False)
    ipa = db.Column(db.String(60), nullable=True, default='')
    visitor_ID = db.Column(db.Integer, db.ForeignKey('visitors.id'))

    def __repr__(self):
        return '<visit: {}>'.format(self.id)

class Page_Visit(Base):
    """
    Create a page Visits table in mySQL
    """
    __tablename__ = 'page_visits'

    id = db.Column(db.Integer, primary_key=True)
    clientIPA = db.Column(db.String(60), nullable=True, default='')
    pageID = db.Column(db.String(60), nullable=True, default='')
    pageType = db.Column(db.String(60), nullable=True, default='')
    pageLanguage = db.Column(db.String(60), nullable=True, default='')
    pageFunction = db.Column(db.String(60), nullable=True, default='')
    pageURL = db.Column(db.String(1024), nullable=True, default='')
    request_method = db.Column(db.String(60), nullable=True, default='')
    pageTemplate = db.Column(db.String(1024), nullable=True, default='')
    pageTemplate_page = db.Column(db.String(1024), nullable=True, default='')
    pageTemplate_form = db.Column(db.String(1024), nullable=True, default='')
    visitor_ID = db.Column(db.Integer, db.ForeignKey('visitors.id'))
    visit_ID = db.Column(db.Integer, db.ForeignKey('visits.id'))

    def __repr__(self):
        return '<page_visit:{0} page:{1}>'.format(self.id,self.pageID)

class xContactMessage(db.Model):
    """
    Create a ContactMessage table
    """

    # Ensures table will be named in plural and not in singular, as is the name of the model
    __tablename__ = 'xcontactmessages'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True)
    firstName = db.Column(db.String(60), index=True)
    lastName = db.Column(db.String(60), index=True)
    jobTitle = db.Column(db.String(60), index=True , default='')
    company = db.Column(db.String(60), index=True)
    message = db.Column(db.String(1024))
    mobile = db.Column(db.String(20), index=True)
    receivedDT = db.Column(db.DateTime, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmedDT = db.Column(db.DateTime, nullable=True)
    repliedDT = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<ContactMessage: {}>'.format(self.message)

    def json_view(self):

        if self.confirmed:
            confirmatonString=str(self.confirmedDT)
        else:
            confirmatonString=''

        if self.repliedDT:
            repliedString=str(self.repliedDT)
        else:
            repliedString=''

        receivedString=str(self.receivedDT)

        rec = {
            'id':self.id
            ,'firstName':self.firstName
            ,'lastName':self.lastName
            ,'email':self.email
            ,'company':self.company
            ,'title':self.jobTitle
            ,'mobile':self.mobile
            ,'receivedDT':receivedString
            ,'confirmed':confirmatonString
            ,'repliedDT':repliedString
        }

        return rec

# Set up user_loader
#@login_manager.user_loader
#def load_user(user_id):
#    return Subscriber.query.get(int(user_id))