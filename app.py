from flask import Flask, g, jsonify, abort, make_response, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS

from database import db, Pick, Pickset, User, Team, Matchup

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./tmp/test.db'
db.init_app(app)
app.app_context().push()

auth = HTTPBasicAuth()
@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/')
def index():
    return "howdy"

# Users
@app.route('/api/users/', methods=['POST'])
def new_user():
    username = request.json['username']
    password = request.json['password']
    print(f"New user {username}")
    if username is None or password is None:
        print("missing username or password")
        abort(400)
    if User.query.filter_by(username=username).first() is not None:
        abort(400)
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'username': user.username}), 201, {'Location': url_for('get_user', id=user.id, _external=True)}

@app.route('/api/user/<int:id>', methods=['GET'])
@auth.login_required
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    if id != g.user.id:
        abort(400, f"Active user {g.user.id} cannot view data for user {id}")
    return jsonify({'username': user.username})

# Picks
@app.route('/api/picks/', methods=['GET'])
def get_picks():
    picks = Pick.query.all()
    return jsonify(picks)


# Picksets
@app.route('/api/picksets/', methods=['GET'])
def get_picksets():
    picksets = Pickset.query.all()
    return jsonify(picksets)

# create only the pickset name here?
# POSTs to /api/pickset/<int:pickset_id>/<int:week> to create/update a week's picks
@app.route('/api/picksets/', methods=['POST'])
# @auth.login_required
def create_pickset():
    if not request.json or not 'name' in request.json or not 'picks' in request.json \
        or not 'pool_id' in request.json:
        abort(400)
    ps = Pickset(user_id=g.user.id, pool_id=request.json['pool_id'],  name=request.json['name'])
    db.session.add(ps)
    db.session.flush() # ensure Pickset has an id
    for pick_json in request.json['picks']:
        assert False, "Pick.create_from_json() unimplemented"
        # pick = Pick.create_from_json(ps.id, pick_json)
        db.session.add(pick)
    db.session.commit()
    return jsonify(ps)

# @app.route('/api/pickset/<int:pickset_id>', methods=['GET'])
@app.route('/api/pickset/<int:pickset_id>/<int:week>', methods=['GET'])
def get_pickset(pickset_id, week):
    ps = Pickset.query.filter_by(id=pickset_id).first()
    if not ps:
        abort(404)
    picks = Pick.query.filter_by(pickset_id=pickset_id).all()
    week_picks = []
    for p in picks:
        mu = Matchup.query.filter_by(id=p.matchup_id).first()
        if mu.week != week:
            continue
        week_picks.append({'home_team':mu.home, 'away_team':mu.away, 'home_win':p.home_win})
    if len(week_picks) > 0:
        return jsonify({'name':ps.name, 'picks':week_picks})
    else: # return faked-out picks with matchup info if no picks for this week
        return jsonify({'name':ps.name, 'picks':f"NO PICKS FOUND FOR WEEK {week}"})

# # Add mock picks to pickset
# @app.route('/api/mockpicks/<int:pickset_id>', methods=['GET'])
# def get_mock_picks(pickset_id):
#     ps = Pickset.query.filter_by(id=pickset_id).first()
#     if not ps:
#         abort(404)
#     picks = mock.create_mock_picks(pickset_id, week=1)
#     for pick in picks:
#         db.session.add(pick)
#     db.session.commit()
#     return jsonify(picks)

# @app.route('/api/pickset/<int:pickset_id>', methods=['DELETE'])
# def delete_pickset(pickset_id):
#     ps = Pickset.query.filter_by(id=pickset_id).first()
#     if not ps:
#         abort(404)
#     db.session.delete(ps)
#     db.session.commit()
#     return jsonify({'result': True})


if __name__ == "__main__":
    app.run(debug=True)