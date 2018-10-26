from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,\
        TextAreaField, RadioField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError,\
        Length, Regexp, Optional
from flask_babel import _, lazy_gettext as _l
from app.models import User


class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditProfileForm(FlaskForm):
    title = "Edit Profile"
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class PostForm(FlaskForm):
    post_body = TextAreaField('Post', validators=[
                              DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Post')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset Email')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')


class DenialForm(FlaskForm):
    electionId = SelectField(
            'Election selection*',
            choices=[],
            description="""These options come from the Voter Information Project.  
                        NOTE: The "VIP Test Election" option is used for testing, 
                        but sometimes has data that the actual election 
                        doesn\'t offer
                        """)
    pollZip = StringField('Polling Place Zip*', validators=[DataRequired()])
    pollStreet = StringField('Polling Place Street*', validators=[DataRequired()])
    pollCity = StringField('Polling Place City*', validators=[DataRequired()])
    pollState = StringField('Polling Place State*', validators=[DataRequired()])
    pollName = StringField('Polling Place Name')
    poc = BooleanField('You identify as a person of color')
    registration_type = SelectField(
            'What party are you registered for?',
            choices=[
                ('N', 'None'),
                ('D', 'Democrat'),
                ('R', 'Republican'),
                ('I', 'Independent'),
                ('G', 'Green'),
                ('K', 'Don\'t know'),
                ('O', 'Other')])
    submit = SubmitField('Submit your log')


class PollingPlaceFinder(FlaskForm):
    optPersonName = StringField('Name (optional)',
                                validators=[Optional(strip_whitespace=True)])
    optEmail = StringField('Email (optional)',
                           validators=[
                                Optional(strip_whitespace=True),
                                Email("Please use a valid email address")
                            ])
    optPersonStreet = StringField(
            'Street (optional, but required for poll finder to work)',
            validators=[Optional(strip_whitespace=True)])
    optPersonCity = StringField(
            'City (optional)', validators=[Optional(strip_whitespace=True)])
    optPersonState = StringField(
            'State (optional)', validators=[Optional(strip_whitespace=True)])
    optPersonZip = StringField(
            'Zip (optional, but required for poll finder to work)',
            validators=[
                    Optional(strip_whitespace=True),
                    Regexp("^\d{5}(?:[-\s]\d{4})?$",
                           message="Must be a U.S. zip code")
            ])
