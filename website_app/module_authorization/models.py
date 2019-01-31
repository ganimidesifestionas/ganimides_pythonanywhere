# myApp/module_authorization/models.py
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
# Import the database object (db) from the main application module. We define the db inside /myApp/__init__.py
from .. import db
from .. import login_manager


# Define a reusable base model for other database tables to inherit (will be part of all defined tables)
class Base(db.Model):
    __abstract__  = True
    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),onupdate=db.func.current_timestamp())

###########################################################################
class Subscriber(UserMixin, db.Model):
    """
    Create a Subscriber table in mySQL
    """
    # Ensures table will be named in plural and not in singular, as is the name of the model
    __tablename__ = 'subscribers'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    userName = db.Column(db.String(60), index=True, unique=True , default='')
    firstName = db.Column(db.String(60), index=True , default='')
    lastName = db.Column(db.String(60), index=True , default='')
    roleX = db.Column(db.String(60), index=True , default='')
    mobile = db.Column(db.String(20), index=True , default='')
    company = db.Column(db.String(60), index=True , default='')
    jobTitle = db.Column(db.String(60), index=True , default='')
    agreeTerms = db.Column(db.Boolean, nullable=False, default=False)
    agreeTermsDT = db.Column(db.DateTime, nullable=True)
    mailingListSignUp = db.Column(db.Boolean, nullable=False, default=False)
    mailingListSignUpDT = db.Column(db.DateTime, nullable=True)
    rememberMe = db.Column(db.Boolean, nullable=False, default=False)
    passwordHash = db.Column(db.String(128) , default='')
    passwordReset = db.Column(db.Boolean, nullable=False, default=False)
    registeredDT = db.Column(db.DateTime, nullable=False)
    #confirmedDT = db.Column(db.DateTime, nullable=True)
    lastLoginDT = db.Column(db.DateTime, nullable=True)
    mobileConfirmed = db.Column(db.Boolean, nullable=False, default=False)
    mobileConfirmedDT = db.Column(db.DateTime, nullable=True)
    emailConfirmed = db.Column(db.Boolean, nullable=False, default=False)
    emailConfirmedDT = db.Column(db.DateTime, nullable=True)
    mobileConfirmationCodeHash = db.Column(db.String(128), nullable=True,default='')
    mobileConfirmationCodeDT = db.Column(db.DateTime, nullable=True)
    avatarImageFile = db.Column(db.String(255), nullable=True)
    accessModules = db.Column(db.String(255), nullable=True)
    #departmentID = db.Column(db.Integer, db.ForeignKey('departments.id'))
    #roleID = db.Column(db.Integer, db.ForeignKey('roles.id'))
    isAdmin = db.Column(db.Boolean, default=False)
    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.passwordHash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.passwordHash, password)

    @property
    def mobileConfirmationCode(self):
        """
        Prevent mobileConfirmationCode from being accessed
        """
        raise AttributeError('mobileConfirmationCode is not a readable attribute.')

    @mobileConfirmationCode.setter
    def mobileConfirmationCode(self, mobileConfirmationCode):
        """
        Set mobileConfirmationCode to a hashed mobileConfirmationCode
        """
        self.mobileConfirmationCodeHash = generate_password_hash(mobileConfirmationCode)

    def verify_mobileConfirmationCode(self, mobileConfirmationCode):
        """
        Check if hashed mobileConfirmationCode matches actual mobileConfirmationCode
        """
        return check_password_hash(self.mobileConfirmationCodeHash, mobileConfirmationCode)


    def __repr__(self):
        return '<Subscriber: {}>'.format(self.email)

    def json_view(self):

        if self.emailConfirmed:
            emailconfirmatonString = str(self.emailConfirmedDT)
        else:
            emailconfirmatonString = ''

        if self.agreeTerms:
            termsAgreeString = str(self.agreeTerms)
        else:
            termsAgreeString = ''

        if self.rememberMe:
            rememberMeString = str(self.rememberMe)
        else:
            rememberMeString = ''

        if self.mailingListSignUp:
            mailingListSignUpString = str(self.mailingListSignUpDT)
        else:
            mailingListSignUpString = ''

        if self.mobileConfirmed:
            mobileconfirmatonString = str(self.mobileConfirmedDT)
        else:
            mobileconfirmatonString = ''

        if self.lastLoginDT:
            lastloginString = str(self.lastLoginDT)
        else:
            lastloginString = ''

        registrationString = str(self.registeredDT)

        rec = {
            'id':self.id
            ,'userName':self.userName
            ,'first name':self.firstName
            ,'last name':self.lastName
            ,'email':self.email
            ,'mobile':self.mobile
            ,'job title':self.jobTitle
            ,'company':self.company
            ,'registered':registrationString
            #,'confirmed':confirmatonString
            ,'email confirmed':emailconfirmatonString
            ,'mobile confirmed':mobileconfirmatonString
            ,'last login':lastloginString
            ,'terms agreement':termsAgreeString
            ,'remember me':rememberMeString
            ,'mailing list signup':mailingListSignUpString
        }

        return rec

# class Department(db.Model):
#     """
#     Create a Department table
#     """
#     # Ensures table will be named in plural and not in singular, as is the name of the model
#     __tablename__ = 'departments'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(60), unique=True)
#     description = db.Column(db.String(200))
#     subscribers = db.relationship('Subscriber', backref='department',lazy='dynamic')
#     employees = db.relationship('User', backref='department',lazy='dynamic')

#     def __repr__(self):
#         return '<Department: {}>'.format(self.name)

# class Role(db.Model):
#     """
#     Create a Role table
#     """
#     # Ensures table will be named in plural and not in singular, as is the name of the model
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(60), unique=True)
#     description = db.Column(db.String(200))
#     subscribers = db.relationship('Subscriber', backref='role',lazy='dynamic')
#     employees = db.relationship('User', backref='role',lazy='dynamic')

#     def __repr__(self):
#         return '<Role: {}>'.format(self.name)

class ContactMessage(db.Model):
    """
    Create a ContactMessage table
    """

    # Ensures table will be named in plural and not in singular, as is the name of the model
    __tablename__ = 'contactmessages'

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
@login_manager.user_loader
def load_user(user_id):
    return Subscriber.query.get(int(user_id))