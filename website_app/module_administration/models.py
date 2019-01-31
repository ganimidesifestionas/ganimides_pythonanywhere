# myApp/module_administration/models.py
#from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
# Import the database object (db) from the main application module. We define the db inside /myApp/__init__.py
from .. import db
from .. import login_manager

# Define a reusable base model for other database tables to inherit (will be part of all defined tables)
class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

# Define a User model
class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    userName = db.Column(db.String(60), index=True, unique=False, default='')
    firstName = db.Column(db.String(60), index=True, default='')
    lastName = db.Column(db.String(60), index=True, default='')
    roleX = db.Column(db.String(60), index=True, default='')
    mobile = db.Column(db.String(20), index=True, default='')
    company = db.Column(db.String(60), index=True, default='')
    jobTitle = db.Column(db.String(60), index=True, default='')
    # agreeTerms = db.Column(db.Boolean, nullable=False, default=False)
    # agreeTermsDT = db.Column(db.DateTime, nullable=True)
    # mailingListSignUp = db.Column(db.Boolean, nullable=False, default=False)
    # mailingListSignUpDT = db.Column(db.DateTime, nullable=True)
    rememberMe = db.Column(db.Boolean, nullable=False, default=False)
    passwordHash = db.Column(db.String(128) , default='')
    passwordReset = db.Column(db.Boolean, nullable=False, default=False)
    isAdmin = db.Column(db.Boolean, default=False)
    registeredDT = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    #confirmedDT = db.Column(db.DateTime, nullable=True)
    lastLoginDT = db.Column(db.DateTime, nullable=True)
    mobileConfirmed = db.Column(db.Boolean, nullable=False, default=False)
    mobileConfirmedDT = db.Column(db.DateTime, nullable=True)
    emailConfirmed = db.Column(db.Boolean, nullable=False, default=False)
    emailConfirmedDT = db.Column(db.DateTime, nullable=True)
    mobileConfirmationCodeHash = db.Column(db.String(128), nullable=True, default='')
    mobileConfirmationCodeDT = db.Column(db.DateTime, nullable=True)
    avatarImageFile = db.Column(db.String(255), nullable=True)

    department_ID = db.Column(db.Integer, db.ForeignKey('departments.id'))
    #one-to-one relationship
    #user_department = db.relationship("Department", back_populates="department_users", uselist=False) 

    role_ID = db.Column(db.Integer, db.ForeignKey('roles.id'))
    #many-to-one relationship
    user_roles = db.relationship("Role", back_populates="role_users")

    # addresses = db.relationship('Address', lazy='select',
    #         backref=db.backref('person', lazy='joined'))

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

    def json_view(self):
        if self.emailConfirmed:
            emailconfirmatonString = str(self.emailConfirmedDT)
        else:
            emailconfirmatonString = ''

        if self.rememberMe:
            rememberMeString = str(self.rememberMe)
        else:
            rememberMeString = ''

        if self.mobileConfirmed:
            mobileconfirmatonString = str(self.mobileConfirmedDT)
        else:
            mobileconfirmatonString = ''

        if self.lastLoginDT:
            lastloginString = str(self.lastLoginDT)
        else:
            lastloginString = ''

        registrationString = str(self.registeredDT)

        rec={
            'id':self.id
            ,'userName':self.userName
            ,'first name':self.firstName
            ,'last name':self.lastName
            ,'email':self.email
            ,'roleX':self.roleX
            ,'mobile':self.mobile
            ,'job title':self.jobTitle
            ,'company':self.company
            ,'registered':registrationString
            #,'confirmed':confirmatonString
            ,'email confirmed':emailconfirmatonString
            ,'mobile confirmed':mobileconfirmatonString
            ,'last login':lastloginString
            #,'terms agreement':termsAgreeString
            ,'remember me':rememberMeString
            #,'mailing list signup':mailingListSignUpString
        }
        return rec
    def __repr__(self):
        return '<User: {}>'.format(self.email)

class Department(Base):
    """
    Create a Department table
    """
    # Ensures table will be named in plural and not in singular, as is the name of the model
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    #department_users = db.relationship("User", back_populates='user_department', cascade="all, delete, delete-orphan")
    
    #department_users = db.relationship('User', backref='user_department',lazy='dynamic')
    #subscribers = db.relationship('Subscriber', backref='department',lazy='dynamic')
    
    # 1-to-1 relationship with users
    staff1 = db.relationship('User', backref='department', uselist=False)
    staff = db.relationship("User", back_populates='department', cascade="all, delete, delete-orphan")
    
    def __repr__(self):
        return '{}'.format(self.name)

class Role(Base):
    """
    Create a Role table
    """
    # Ensures table will be named in plural and not in singular, as is the name of the model
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    #subscribers = db.relationship('Subscriber', backref='role',lazy='dynamic')
    #one-to-many relationship
    role_users = db.relationship("User", back_populates='user_roles', cascade="all, delete, delete-orphan")
    role_users2 = db.relationship('User', backref='user_roles2', uselist=True)
    #one-to-many relationship
    #role_subscribers = db.relationship("Subscriber", back_populates='subscriber_role', cascade="all, delete, delete-orphan")

    def __repr__(self):
        return '{}'.format(self.name)

# # Set up user_loader
# @login_manager.user_loader
# def load_user(user_id):
#     return Subscriber.query.get(int(user_id))