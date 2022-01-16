import logging
import logging.config
import os
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics

from asset_app import app
from flask import render_template, redirect, url_for, flash, request, jsonify
from asset_app.models import Asset
from asset_app.models import User
from flask_login import login_user, logout_user, login_required, current_user

from asset_app.forms import AddAssetForm, EditAssetForm, LoginForm, SearchAssetForm
from asset_app import db
from asset_app import redis_client
import json
from datetime import timedelta
from dotenv import load_dotenv

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('app')

load_dotenv()


def when_ready(server):
    GunicornPrometheusMetrics.start_http_server_when_ready(int(os.getenv('METRICS_PORT')))


def child_exit(server, worker):
    GunicornPrometheusMetrics.mark_process_dead_on_child_exit(worker.pid)


metrics = GunicornPrometheusMetrics(app, group_by='endpoint')


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
                logger.debug("username " + str(form.username.data) + " Logged in successfully")
                return redirect(url_for('dashboard'))
            else:
                logger.debug("username " + str(form.username.data) + " Logging unsuccessful")
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

    # set the expiration time on redis cache for entry
    cache_expire_in_seconds = 3600

    if form.validate_on_submit():
        search_query = form.search_query.data

        if form.search_type.data == 'id':

            redis_result = redis_client.get(f':{search_query}')

            if redis_result:
                logger.debug(f'search result from redis:{redis_result}')
                search_result = json.loads(redis_result)

            else:
                search_result = Asset.query.filter(Asset.asset_id == search_query).all()

                mysql_result_to_json = []
                for asset in search_result:
                    item = {
                        'asset_id': asset.asset_id,
                        'name': asset.name,
                        'owner': asset.owner,
                        'description': asset.description,
                        'location': asset.location,
                        'criticality': asset.criticality
                    }

                    mysql_result_to_json.append(item)

                redis_client.set(f':{search_query}', json.dumps(mysql_result_to_json))
                redis_client.expire(f':{search_query}', timedelta(seconds=cache_expire_in_seconds))

        if form.search_type.data == 'name':

            redis_result = redis_client.get(f'{search_query}:')

            if redis_result:
                search_result = json.loads(redis_result)
                logging.debug(f'search result from redis:{redis_result}')

            else:
                search = "%{}%".format(search_query)
                search_result = Asset.query.filter(Asset.name.like(search)).all()

                mysql_result_to_json = []
                for asset in search_result:
                    item = {
                        'asset_id': asset.asset_id,
                        'name': asset.name,
                        'owner': asset.owner,
                        'description': asset.description,
                        'location': asset.location,
                        'criticality': asset.criticality
                    }

                    mysql_result_to_json.append(item)

                redis_client.set(f'{search_query}:', json.dumps(mysql_result_to_json))
                redis_client.expire(f'{search_query}:', timedelta(seconds=cache_expire_in_seconds))

        if search_result:

            return render_template('search.html', form=form, search_result=search_result)

        else:
            logger.debug("No result found for " + str(search_query))
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
        logger.debug("Asset added successfully: " + str(form.assetName.data))
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
            logger.debug("Asset updated successful: " + str(form.assetName.data))
            flash(f'Asset added successfully', category='success')
            return redirect(url_for('list_assets'))

        if delete:
            db.session.delete(asset)
            db.session.commit()
            logger.debug("Asset deleted successful: " + str(form.assetName.data))
            flash(f'Asset deleted successfully', category='success')
            return redirect(url_for('list_assets'))

    elif form.errors != {}:
        for err_msg in form.errors.values():
            logger.debug('validation errors ')
            flash(f'{err_msg}', category='error')

    # if ((request.referrer == request.url_root+url_for("list_assets")[1:]) or (request.referrer ==
    # request.url_root+url_for("edit_asset")[1:])):

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
    logger.debug("User logged out")
    flash("You have been logged out", category='info')
    return redirect(url_for('home_page'))


@app.route('/health', methods=['GET'])
def health():
    # Health probe for k8s
    return ''


@app.route('/ready', methods=['GET'])
def ready():
    # Readiness probe for k8s
    try:
        db.session.execute('SELECT 1')
        return '', 200
    except Exception as e:
        output = str(e)
        logger.warning("MySQL connection failed, Application not ready")
        return jsonify({"message": output}), 502


metrics.register_endpoint('/metrics')
