# -*- encoding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
# for editing their profile
from wtforms import TextAreaField
from wtforms.validators import Length
from app.models import User
# for I18n and L10n
from flask_babel import _
# for dynamic  component translation
from flask_babel import lazy_gettext as _l


# Profile 编辑功能
class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'), validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))


# Blog submission form
class PostForm(FlaskForm):
    post = TextAreaField(_l('Say morning'), validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField(_l('Submit'))



