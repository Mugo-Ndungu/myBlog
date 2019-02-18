from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,BooleanField,SubmitField,TextAreaField,RadioField, SelectField
from wtforms.validators import Required,Email,EqualTo
from wtforms import ValidationError

class PostForm(FlaskForm):
    category = SelectField('Select category', choices=[('pickupPost', 'Pick Up Lines'), ('techPost', 'Technology'), ('businessPost', 'Business'),('interviewPost','Interview')])
    title = StringField('Title of your Post')
    description = TextAreaField('Type in your Post')
    submit = SubmitField('Add Post')

class CommentForm(FlaskForm):
    description = TextAreaField('Add comment',validators=[Required()])
    submit = SubmitField()

class UpvoteForm(FlaskForm):
    submit = SubmitField()


class Downvote(FlaskForm):
    submit = SubmitField()

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.', validators=[Required()])
    submit = SubmitField('Submit')