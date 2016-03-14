from base64 import decodestring, encodestring
from json import dumps
from math import cos, sin, acos, radians
from uuid import uuid4
from cStringIO import StringIO
from os.path import dirname, realpath
from hashlib import md5
from datetime import datetime
import time

from PIL import Image
from flask import Flask, request, session, redirect, render_template

import model
from model import create_place, validate_user, make_place_good, make_place_bad, create_hoot


app = Flask(__name__)

############################# UTILITIES #############################

def timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp)


def datetime_to_timestamp(date_time):
    return time.mktime(date_time.timetuple())


def write_temp_image(pic, temp_path):
    f = open(temp_path, "w+")
    f.write(decodestring(pic))
    f.flush()


def __temp_path__(path):
    temp_path = dirname(realpath(__file__)) + path
    return temp_path


def reshape_image(pic, size):
    temp_path = __temp_path__(path="/temp.png")
    print temp_path
    buffer = StringIO()
    write_temp_image(pic, temp_path)
    image = Image.open(temp_path)
    image.thumbnail(size)
    image.save(buffer, format="JPEG")
    reshaped = encodestring(buffer.getvalue())
    return reshaped


def get_formatted_place(place_id):
    place = model.get_place(place_id)
    return {'name': place[1], 'description': place[2], 'pic': encodestring(place[3]), 'category': place[4],
            'latitude': place[5], 'longitude': place[6], 'from': place[7], 'to': place[8], 'place_id': place[9]}


def get_formatted_places():
    places = model.get_places()
    places = [
        {
            'name': place[1], 'category': place[4], 'latitude': place[5], 'longitude': place[6], 'from': place[7],
            'to': place[8], 'place_id': place[9]
        } for place in places
    ]
    return places


def get_formatted_places_with_thumbnail():
    places = model.get_places()
    places = [
        {
            'name': place[1], 'description': place[2], 'pic': reshape_image(place[3], (90, 90)), 'category': place[4],
            'latitude': place[5],
            'longitude': place[6], 'from': place[7], 'to': place[8], 'place_id': place[9]
        } for place in places
    ]

    [write_temp_image(place['pic'], __temp_path__('/static/pics/' + place['place_id'] + ".png")) for place in places]
    return places


def hoots_to_places(hoots):
    places = []
    for hoot in hoots:
        place = model.get_place2(hoot[1])
        places.append({'name': place[1], 'description': place[2], 'category': place[4], 'latitude': place[5],
                       'longitude': place[6], 'from': place[7], 'to': place[8], 'place_id': place[9],
                       'last_seen': hoot[2]})
    return places


def get_vetted_places():
    places = model.get_places()
    places = [{'name': place[1], 'category': place[4], 'latitude': place[5], 'longitude': place[6], 'from': place[7],
               'to': place[8], 'place_id': place[9], 'verified': place[10]} for place in places]
    return places


def distance(latitude, longitude, place):
    distance = 6371 * acos(cos(radians(latitude)) * cos(radians(place['latitude'])) * cos(
        radians(place['longitude']) - radians(longitude)) + sin(radians(latitude)) * sin(
        radians(place['latitude'])))
    return distance


############################# REST APIs #############################

@app.route('/furlencode/add/place', methods=['POST'])
def add_place():
    incoming_place = request.get_json(force=True)
    user = incoming_place['user']
    place = incoming_place['place']
    name, description, pic, category, latitude, longitude, _from_, _to_ = place['name'], place['description'], place[
        'pic'], place['category'], place['latitude'], place['longitude'], place['from'], place['to']
    reshaped_pic = reshape_image(pic, (600, 400))
    create_place(name, description, reshaped_pic, category, latitude, longitude, _from_, _to_,
                 uuid4())
    return 'Added place: {}'.format(name)


@app.route('/furlencode/get/places')
def get_places():
    places = get_vetted_places()
    return dumps(places)


@app.route('/furlencode/get/nearbyplaces')
def get_nearby_places():
    latitude, longitude = request.args['latitude'], request.args['longitude']
    places = get_vetted_places()
    places = [place for place in places if distance(float(latitude), float(longitude), place) < 3]
    return dumps(places)


@app.route('/furlencode/get/place')
def get_place_details():
    place_id = request.args['place_id']
    place = get_formatted_place(place_id)
    return dumps(place)


@app.route('/furlencode/hoot', methods=['POST'])
def hoot():
    payload = request.get_json(force=True)
    place_id, timestamp = payload['place_id'], long(payload['timestamp'])
    place = model.get_place(place_id)
    if place is not None:
        create_hoot(place[0], timestamp)
        return 'Created hoot for place: {} at time: {}'.format(place[1], timestamp)
    else:
        return 'Place doesn\'t exist yet. Please create it before hooting it'


@app.route('/furlencode/get/hoots')
def get_hoots():
    timestamp = request.args['timestamp']
    return dumps(hoots_to_places(model.get_hoots(timestamp)))


############################# ADMIN APIs #############################

@app.route('/home')
def user_home():
    if session.get('user'):
        return render_template('home.html', places=get_formatted_places_with_thumbnail())
    else:
        return render_template('error.html', error='Unauthorized Access')


@app.route('/login')
def show_sign_in():
    if session.get('user'):
        return redirect('/home')
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


@app.route('/validateLogin', methods=['POST'])
def validate_login():
    try:
        username = request.form['inputEmail']
        password = request.form['inputPassword']

        _md5_ = md5()
        _md5_.update(password)
        password_hash = _md5_.hexdigest()
        if validate_user(username, password_hash):
            session['user'] = username
            return redirect('/home')
        else:
            return render_template('error.html', error='Wrong Email address or Password.')

    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/showPlaces')
def show_places():
    return None


@app.route('/goodPlace')
def good_place():
    place_id = request.args['place_id']
    make_place_good(place_id)
    return redirect('/home')


@app.route('/badPlace')
def bad_place():
    place_id = request.args['place_id']
    make_place_bad(place_id)
    return redirect('/home')


#######################################################################################

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.secret_key = 'notasecret'
    app.run(host='0.0.0.0', debug=True)
