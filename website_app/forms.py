from flask_wtf import FlaskForm
from flask_wtf.recaptcha import RecaptchaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import PasswordField, StringField, TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, BooleanField,FileField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired
#DB
from .models import Visit

###########################################################################
###########################################################################
###########################################################################
### customized classes (functions)
###########################################################################
###########################################################################
###########################################################################
class ReadonlyStringField(StringField):
  def __call__(self, *args, **kwargs):
    kwargs.setdefault('readonly', True)
    return super(ReadonlyStringField, self).__call__(*args, **kwargs)
class ReadonlyCheckboxField(BooleanField):
  def __call__(self, *args, **kwargs):
    kwargs.setdefault('readonly', True)
    kwargs.setdefault('disabled', 'disabled')
    return super(ReadonlyCheckboxField, self).__call__(*args, **kwargs)
###########################################################################

###########################################################################
###########################################################################
###########################################################################
### Define the forms (WTForms)
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
class CookiesConsentForm(FlaskForm):
    """
    Form for user to consent on our cookies policy
    """
    submit = SubmitField('Accept')
###########################################################################
###########################################################################
###########################################################################
