from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from werkzeug.security import generate_password_hash


class LoginForm(FlaskForm):
    username = StringField('Никнейм', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])


class RegistrationForm(FlaskForm):
    username = StringField('Никнейм', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])

    def validate(self):
        if not super().validate():
            return False

        if self.password.data != self.confirm_password.data:
            self.password.errors.append('Passwords must match.')
            return False

        self.password.data = generate_password_hash(self.password.data)
        return True
