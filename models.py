from flask import session, flash
from config import db, bcrypt
from sqlalchemy.sql import func, or_

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45))
    password = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    def ongoing_trip():
        # Method to check for ongoing trips
        pass

    @classmethod
    def reg_validate(cls, form):
        if len(form['un']) < 1:
            flash('Please enter a username.', 'un')
        else:
            users = cls.query.filter_by(username=form['un']).all()
            if users:
                flash('Username already in use','reg_em')
        if len(form['pw']) < 8:
            flash('Password must be at least eight characters', 'reg_pw')
        if form['con'] != form['pw']:
            flash('Passwords must match', 'con')
        if '_flashes' in session.keys():
            return False
        return True
    @classmethod
    def add_new_user(cls, form):
        pw_hash = bcrypt.generate_password_hash(form['pw'])
        new_user = cls(
            username = form['un'],
            password = pw_hash
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user
    @classmethod
    def log_validate(cls, form):
        user = cls.query.filter_by(username=form['un']).all()
        if not user:
            flash('Username not found', 'log_un')
        elif not bcrypt.check_password_hash(user[0].password, form['pw']):
            flash('Password is incorrect', 'log_pw')
        if '_flashes' in session.keys():
            return False
        return user[0]
    @classmethod
    def current_user(cls, id):
        user = cls.query.get(id)
        return user
    @classmethod
    def username_check(cls, form):
        names = cls.query.filter_by(username=form['un']).all()
        if names:
            return True
        return False

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='cascade'), nullable=False)
    user = db.relationship('User', foreign_keys=[user_id], backref='trips')
    start_time = db.Column(db.DateTime, server_default=func.now())
    end_time = db.Column(db.DateTime)

    def end_trip():
        pass

    @classmethod
    def validate_trip(cls, form):
        pass
    @classmethod
    def start_trip(cls, form):
        pass

class Plate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    place = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='cascade'), nullable=False)
    user = db.relationship('User', foreign_keys=[user_id], backref='plates')
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    @classmethod
    def create_plate(cls):
        pass

class Find(db.Model):
    found_at = db.Column(db.DateTime, server_default=func.now())
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id', ondelete='cascade'), primary_key=True)
    trip = db.relationship('Trip', foreign_keys=[trip_id], backref='finds')
    plate_id = db.Column(db.Integer, db.ForeignKey('plate.id', ondelete='cascade'), primary_key=True)
    plate = db.relationship('Plate', foreign_keys=[plate_id], backref='finds')

    def delete_find(self):
        pass

    @classmethod
    def find_plate(cls, form):
        pass