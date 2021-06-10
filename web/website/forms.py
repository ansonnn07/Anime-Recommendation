from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from .models import User


class RegisterForm(FlaskForm):
    username = StringField(label='Username', validators=[
                           Length(min=5, max=25), DataRequired()])
    password = PasswordField(label='Password', validators=[
                             Length(min=5, max=30), DataRequired()])
    confirm_password = PasswordField(label='Confirm Password', validators=[
                                     Length(min=5, max=30), DataRequired(), EqualTo('password')])
    submit = SubmitField(label='Register')

    def validate_username(self, input_username):
        user = User.query.filter_by(username=input_username.data).first()
        if user:
            raise ValidationError(
                'Username is taken. Please use a different username.')


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[
                           Length(min=2, max=25), DataRequired()])
    password = PasswordField(label='Password', validators=[
                             Length(min=5, max=30), DataRequired()])
    submit = SubmitField(label='Login')


class RemoveBookmarkForm(FlaskForm):
    submit = SubmitField(label='Remove')
