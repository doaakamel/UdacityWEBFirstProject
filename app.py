import babel
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_migrate import Migrate
from flask_moment import Moment

import sys
from models import Venue, Artist, Show, app, db
import dateutil.parser
from forms import VenueForm, ArtistForm , ShowForm
# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#
moment = Moment(app)
app.config.from_object('config')


# TODO: connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:doaa2971995*@localhost:5432/music'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(str(value))
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    data = Venue.query.all()
    return render_template('pages/venues.html', venues=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    counter=0
    dataList=[]

    search_term = request.form.get('search_term', '')
    for ven in Venue.query.all():
        if str(search_term).lower() in ven.name.lower():
            counter = counter+1
            dataList.append(ven.__dict__)

    response = {"count": counter,"data": dataList}

    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    data = Venue.query.filter_by(id=venue_id).one()
    shows= db.session.query(Show.id,Show.venue_id ,Show.Upcomming,Show.start_time,Show.artist_id,Artist.name).filter(Show.artist_id == Artist.id).all()
    print(shows[0].name)
    return render_template('pages/show_venue.html', venue=data,shows=shows)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    error = False
    try:
        venName = request.form.get('name')
        venAddress= request.form.get('address')
        venCity=request.form.get('city')
        venPhone=request.form.get('phone')
        venState=request.form.get('state')
        venFacebookLink=request.form.get('facebook_link')
        ven=Venue(name=venName,address=venAddress,city=venCity,phone=venPhone,state=venState,facebook_link=venFacebookLink)
        db.session.add(ven)
        db.session.commit()
    # TODO: modify data to be the data object returned from db insertion
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    # on successful db insert, flash success
    # db.flash('Venue ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return render_template('pages/home.html')
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/



@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using

    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()

    except:
        db.session.rollback()

    finally:
        db.session.close()
    return jsonify({'success': True})
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage



#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    counter = 0
    dataList = []

    search_term = request.form.get('search_term', '')
    for Art in Artist.query.all():
        if str(search_term).lower() in Art.name.lower():
            counter = counter + 1
            dataList.append(Art.__dict__)

    response = {"count": counter, "data": dataList}

    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id

    data = Artist.query.filter_by(id=artist_id).one()
    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    # TODO: populate form with fields from artist with ID <artist_id>
    artist = Artist.query.filter_by(id=artist_id).one()
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    error = False
    try:
        Artist.query.filter_by(id=artist_id).delete()
        venId = artist_id
        venName = request.form.get('name')
        venCity = request.form.get('city')
        venPhone = request.form.get('phone')
        venState = request.form.get('state')
        venFacebookLink = request.form.get('facebook_link')
        ven = Artist(id=venId, name=venName, city=venCity, phone=venPhone, state=venState, facebook_link=venFacebookLink)
        db.session.add(ven)
        db.session.commit()
    # TODO: modify data to be the data object returned from db insertion
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    # TODO: populate form with values from venue with ID <venue_id>
    venue = Venue.query.filter_by(id=venue_id).one()
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    error = False
    try:
        Venue.query.filter_by(id=venue_id).delete()
        venId=venue_id
        venName = request.form.get('name')
        venAddress = request.form.get('address')
        venCity = request.form.get('city')
        venPhone = request.form.get('phone')
        venState = request.form.get('state')
        venFacebookLink = request.form.get('facebook_link')
        ven = Venue(id=venId,name=venName, address=venAddress, city=venCity, phone=venPhone, state=venState,
                    facebook_link=venFacebookLink)
        db.session.add(ven)
        db.session.commit()
    # TODO: modify data to be the data object returned from db insertion
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    error = False
    try:
        venName = request.form.get('name')
        venCity=request.form.get('city')
        venPhone=request.form.get('phone')
        venState=request.form.get('state')
        venFacebookLink=request.form.get('facebook_link')
        ven=Artist(name=venName,city=venCity,phone=venPhone,state=venState,facebook_link=venFacebookLink)
        db.session.add(ven)
        db.session.commit()
    # TODO: modify data to be the data object returned from db insertion
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    # on successful db insert, flash success
    # db.flash('Venue ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return render_template('pages/home.html')
    # on successful db insert, flash success
    #db.flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')



#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    data = Show.query.all()
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    error = False
    try:
        artId= request.form.get('artist_id')
        venID= request.form.get('venue_id')
        start=request.form.get('start_time')
        up=bool(request.form.get('Upcomming'))
        ven = Show( artist_id=artId,venue_id= venID,start_time=start,Upcomming=up)
        db.session.add(ven)
        db.session.commit()
    # TODO: modify data to be the data object returned from db insertion
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    # on successful db insert, flash success
    # db.flash('Venue ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return render_template('pages/home.html')
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead



@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
