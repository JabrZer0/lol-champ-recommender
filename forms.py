from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class RecommendForm(FlaskForm):
	sum_name = StringField('Summoner Name', validators=[DataRequired()], description="test")
	region_id = SelectField('Region', choices=[('NA','NA'), ('EUW','EUW'), ('EUNE','EUNE'),
						('OCE','OCE'), ('RU','RU'), ('TR','TR'), ('TR','TR'),
						('LAN','LAN'), ('LAS','LAS'), ('JP','JP')], validators=[DataRequired()])
	submit = SubmitField('Recommend')
# need to replace the Region StringField with a multiple choice dropdown