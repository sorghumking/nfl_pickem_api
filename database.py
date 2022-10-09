from dataclasses import dataclass

from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    pw_hash = db.Column(db.String(64)) # sha256
    is_admin = db.Column(db.Boolean, nullable=False)

    def hash_password(self, password):
        self.pw_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.pw_hash)

    def __repr__(self):
        return f"<User {self.id} {self.username}>"

# dataclass enables jsonify without further effort
@dataclass
class Pickset(db.Model):
    id: int
    user_id: int
    name: str

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)

    picks = db.relationship('Pick', back_populates="pickset", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Pickset {self.id} {self.name}>"

@dataclass
class Pick(db.Model):
    id: int
    pickset_id: int
    matchup_id: int
    home_win: bool
    correct: bool
    superpick: bool
    points: int

    id = db.Column(db.Integer, primary_key=True)
    pickset_id = db.Column(db.Integer, db.ForeignKey('pickset.id'), nullable=False)
    matchup_id = db.Column(db.Integer, db.ForeignKey('matchup.id'), nullable=False)
    home_win = db.Column(db.Boolean, nullable=False)
    correct = db.Column(db.Boolean)
    superpick = db.Column(db.Boolean)
    points = db.Column(db.Integer)

    pickset = db.relationship('Pickset', back_populates="picks")
    matchup = db.relationship('Matchup')

    def __repr__(self):
        return f"<Pick {self.id}>"

    # @classmethod
    # def create_from_json(cls, ps_id, pick_json):
        # return Pick(pickset_id=ps_id, home_team=pick_json['home_team'], away_team=pick_json['away_team'], week=pick_json['week'], home_win=pick_json['home_win'])
        # print(pick_json)

@dataclass
class Team(db.Model):
    id: int
    name: str
    abbv: str
    image_uri: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    abbv = db.Column(db.String, nullable=False)
    image_uri = db.Column(db.String)


@dataclass
class Matchup(db.Model):
    id: int
    away_team: int
    home_team: int
    week: int
    away_score: int
    home_score: int
    home_win: bool

    id = db.Column(db.Integer, primary_key=True)
    away_team = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    home_team = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    week = db.Column(db.Integer, nullable=False)
    away_score = db.Column(db.Integer)
    home_score = db.Column(db.Integer)
    home_win = db.Column(db.Boolean)

    home = db.relationship('Team', foreign_keys=[home_team])
    away = db.relationship('Team', foreign_keys=[away_team])
