# token_services/token_services.py
#import sys
import random
from itsdangerous import URLSafeTimedSerializer
#from myApp import app


def generate_confirmation_token(parWhat):
    #MAIL_userName = os.environ['APP_MAIL_userName']
    #MAIL_PASSWORD = os.environ['APP_MAIL_PASSWORD']
    #secret_key=app.config['SECRET_KEY']
    #salt_password=app.config['SECURITY_PASSWORD_SALT']
    secret_key='spithas'
    salt_password='chaos490px!'
    serializer = URLSafeTimedSerializer(secret_key)
    token=serializer.dumps(parWhat, salt_password)
    return token

def confirm_token(parToken, parExpiration=3600):
    #MAIL_userName = os.environ['APP_MAIL_userName']
    #MAIL_PASSWORD = os.environ['APP_MAIL_PASSWORD']
    #secret_key=app.config['SECRET_KEY']
    #salt_password=app.config['SECURITY_PASSWORD_SALT']
    secret_key='spithas'
    salt_password='chaos490px!'
    serializer = URLSafeTimedSerializer(secret_key)
    try:
        what = serializer.loads(
            parToken,
            salt=salt_password,
            max_age=parExpiration
        )
    except:
        return None
    return what

def generate_mobileconfirmation_code(parWhat):
    codeInt=random.randint(100000,999999)
    codeStr=str(codeInt)
    return codeStr

