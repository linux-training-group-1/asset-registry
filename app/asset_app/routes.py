import bcrypt
from flask.helpers import flash
from flask_wtf.form import FlaskForm
from asset_app import app
from flask import render_template, redirect, url_for, flash, request
from asset_app.models import Asset, load_user
from asset_app.models import User
from flask_login import login_user, logout_user, login_required, current_user

from asset_app.forms import AddAssetForm, EditAssetForm, LoginForm, SearchAssetForm
from asset_app import db


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def home_page():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    else:
        form = LoginForm()

        if form.validate_on_submit():

            attempted_user = User.query.filter_by(
                username=form.username.data).first()

            if attempted_user and attempted_user.check_password(attempted_password=form.password.data):

                login_user(attempted_user)
                flash(f'you logged in successfully!', category='success')
                return redirect(url_for('dashboard'))
            else:
                flash(f'Incorrect username or password ', category='error')

        return render_template('login.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    total_assets = Asset.query.count()

    return render_template('dashboard.html', total_assets=total_assets)


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchAssetForm()

    if form.validate_on_submit():
        search_query = form.search_query.data
        if form.search_type.data == 'id':
            search_result = Asset.query.filter(
                Asset.asset_id == search_query).all()

        if form.search_type.data == 'name':
            search = "%{}%".format(search_query)
            search_result = Asset.query.filter(Asset.name.like(search)).all()

        if search_result:
            print('in search_results loop')
            return render_template('search.html', form=form, search_result=search_result)

        else:
            return render_template('search.html', form=form, nohit='empty')

    return render_template('search.html', form=form)


@app.route('/add-asset', methods=['GET', 'POST'])
@login_required
def add_asset():

    form = AddAssetForm()

    if form.validate_on_submit():

        assetToAdd = Asset(
            name=form.assetName.data,
            owner=form.assetOwner.data,
            description=form.assetDescription.data,
            location=form.assetLocation.data,
            criticality=form.assetCriticality.data
        )
        db.session.add(assetToAdd)
        db.session.commit()
        flash(f'Asset added successfully', category='success')
        return redirect(url_for('list_assets'))

    elif form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'{err_msg}', category='error')

    return render_template('add-asset.html', form=form)


@app.route('/list-assets', methods=['GET', 'POST'])
@login_required
def list_assets():
    all_assets = Asset.query.all()
    return render_template('list-assets.html', all_assets=all_assets)


@app.route('/edit-asset', methods=['GET', 'POST'])
@login_required
def edit_asset():

    form = EditAssetForm()

    asset_id = request.args.get("asset_id")
    asset = Asset.query.filter(Asset.asset_id == asset_id).first()

    if form.validate_on_submit():

        update = form.submit_update.data
        delete = form.submit_delete.data

        if update:
            asset.name = form.assetName.data
            asset.owner = form.assetOwner.data
            asset.description = form.assetDescription.data
            asset.location = form.assetLocation.data
            asset.criticality = form.assetCriticality.data
            db.session.commit()
            flash(f'Asset added successfully', category='success')
            return redirect(url_for('list_assets'))

        if delete:

            db.session.delete(asset)
            db.session.commit()
            flash(f'Asset deleted successfully', category='success')
            return redirect(url_for('list_assets'))

    elif form.errors != {}:
        for err_msg in form.errors.values():
            print('validation errors')
            flash(f'{err_msg}', category='error')

    # if ((request.referrer == request.url_root+url_for("list_assets")[1:]) or (request.referrer == request.url_root+url_for("edit_asset")[1:])):

    if asset:
        form.assetID.data = asset.asset_id
        form.assetName.data = asset.name
        form.assetOwner.data = asset.owner
        form.assetLocation.data = asset.location
        form.assetDescription.data = asset.description
        form.assetCriticality.data = asset.criticality

    else:
        return redirect(url_for('list_assets'))

    # if request.headers.get("Referer")==url_for('list_assets'):
    #     return render_template('edit-asset.html',asset=asset,form=form)
    # else:
    #     return redirect(url_for('list_assets'))
    return render_template('edit-asset.html', form=form)


@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash("You have been logged out", category='info')
    return redirect(url_for('home_page'))
