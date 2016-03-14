from sqlalchemy import create_engine


def execute_query(query):
    engine = create_engine('mysql+pymysql://bhat:bhat@localhost:3306/furlencode', echo=True)
    connection = engine.connect()
    results = connection.execute(query)
    connection._commit_impl(autocommit=True)
    return results


def get_last_id(table):
    query = 'SELECT id FROM {} order by id desc limit 1'.format(table)
    results = execute_query(query)
    id = 1 if results.rowcount is 0 else results._fetchone_impl()[0]
    return id


def create_place(name, description, pic, category, latitude, longitude, _from_, _to_, uuid):
    id = get_last_id('places')
    query = "INSERT into places values ({},'{}','{}','{}','{}',{},{},'{}','{}','{}',FALSE)".format(id + 1, name,
                                                                                                   description,
                                                                                                   pic, category,
                                                                                                   latitude, longitude,
                                                                                                   _from_,
                                                                                                   _to_, uuid)
    results = execute_query(query)
    results.close()


def get_place(place_id):
    results = execute_query("SELECT * FROM places where place_uuid='{}'".format(place_id))
    places = results._fetchone_impl()
    results.close()
    return places


def get_place2(id):
    results = execute_query("SELECT * FROM places where id={}".format(id))
    places = results._fetchone_impl()
    results.close()
    return places


def get_places():
    results = execute_query("SELECT * FROM places")
    places = results._fetchall_impl()
    results.close()
    return places


def make_place_good(place_id):
    results = execute_query("UPDATE places set place_is_good=TRUE where place_uuid='{}'".format(place_id))
    results.close()


def make_place_bad(place_id):
    results = execute_query("UPDATE places set place_is_good=FALSE where place_uuid='{}'".format(place_id))
    results.close()


def validate_user(username, password_hash):
    results = execute_query("SELECT * FROM admin WHERE user='{}'".format(username))
    if results.rowcount is 0:
        return False
    else:
        user = results._fetchone_impl()
        hash = user[1]
        return hash == password_hash


def create_hoot(place_id, timestamp):
    id = get_last_id('visited_places')
    results = execute_query("INSERT INTO visited_places VALUES ({},{},{})".format(id + 1, place_id, timestamp))
    results.close()


def get_hoots(timestamp):
    results = execute_query(
        "SELECT * FROM visited_places WHERE ({} - last_seen)/3600000 between 0 and 3".format(timestamp))
    hoots = results._fetchall_impl()
    return hoots
