from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import Required
class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class BlogForm(FlaskForm):

    title = StringField('Review title',validators=[Required()])
    description = TextAreaField('Description', validators=[Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    comment=TextAreaField('Comment', validators=[Required()])
    submit = SubmitField('Submit')