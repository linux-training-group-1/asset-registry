from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, RadioField, PasswordField
from wtforms.validators import DataRequired, ValidationError

from asset_app.models import Asset


class AddAssetForm(FlaskForm):

    def validate_assetID(self, assetID_to_check):
        assetID = Asset.query.filter_by(asset_id=assetID_to_check.data).first()
        if assetID:
            raise ValidationError(
                'Asset ID already exists! Try a different asset name')

    assetName = StringField(label='Asset Name', validators=[DataRequired()])
    assetID = IntegerField(
        render_kw={'readonly': True}, label='Asset ID')
    assetOwner = StringField(
        label="Asset Owner", validators=[DataRequired(), ])
    assetDescription = StringField(
        label='Asset Description', validators=[DataRequired()])
    assetLocation = StringField(
        label='Asset Location', validators=[DataRequired()])
    assetCriticality = SelectField(label='Asset Criticality', choices=[(
        '', 'Select'), ('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default=1, validators=[DataRequired()])
    submit = SubmitField(label='Add Asset')


class SearchAssetForm(FlaskForm):
    search_query = StringField(validators=[DataRequired()])
    search_type = RadioField(validators=[DataRequired()], choices=[
        ('id', 'ID'), ('name', 'Name')], default='name')
    submit = SubmitField(label='Search')


class EditAssetForm(FlaskForm):

    def validate_assetID(self, assetID_to_check):
        assetID = Asset.query.filter_by(asset_id=assetID_to_check.data).first()
        if assetID is None:
            raise ValidationError('Asset ID doesn\'t exist!')

    # def validate_assetName(self,assetName_to_check):
    #     id=Asset.query.filter_by(name=assetName_to_check.data).first()
    #     if id is None:
    #         raise ValidationError('Asset name already exists! Try a different asset name')

    assetName = StringField(label='Asset Name', validators=[DataRequired()])
    assetID = IntegerField(
        render_kw={'readonly': True}, label='Asset ID', validators=[DataRequired()])
    assetOwner = StringField(
        label="Asset Owner", validators=[DataRequired(), ])
    assetDescription = StringField(
        label='Asset Description', validators=[DataRequired()])
    assetLocation = StringField(
        label='Asset Location', validators=[DataRequired()])
    assetCriticality = SelectField(label='Asset Criticality', choices=[(
        '', 'Select'), ('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default=1, validators=[DataRequired()])
    submit_update = SubmitField(label='Update Asset')
    submit_delete = SubmitField(label='Delete Asset')


class LoginForm(FlaskForm):
    username = StringField(label="username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Sign In")
