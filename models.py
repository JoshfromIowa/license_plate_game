from flask import session, flash
from config import db, bcrypt
from sqlalchemy.sql import func, or_

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45))
    password = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    def initialize_plates(self):
        plates_list = {
            'United States':[
                'Alabama',
                'Alaska',
                'Arizona',
                'Arkansas',
                'California',
                'Colorado',
                'Connecticut',
                'Delaware',
                'Florida',
                'Georgia',
                'Hawaii',
                'Idaho',
                'Illinois',
                'Indiana',
                'Iowa',
                'Kansas',
                'Kentucky',
                'Louisiana',
                'Maine',
                'Maryland',
                'Massachusetts',
                'Michigan',
                'Minnesota',
                'Mississippi',
                'Missouri',
                'Montana',
                'Nebraska',
                'Nevada',
                'New Hampshire',
                'New Jersey',
                'New Mexico',
                'New York',
                'North Carolina',
                'North Dakota',
                'Ohio',
                'Oklahoma',
                'Oregon',
                'Pennsylvania',
                'Rhode Island',
                'South Carolina',
                'South Dakota',
                'Tennessee',
                'Texas',
                'Utah',
                'Vermont',
                'Virginia',
                'Washington',
                'West Virginia',
                'Wisconsin',
                'Wyoming',
                'Washington, D.C.'
            ],
            'Canada':[
                'Alberta',
                'British Columbia',
                'Manitoba',
                'Newfoundland & Labrador',
                'New Brunswick',
                'Nova Scotia',
                'Northwest Territories',
                'Nunavut',
                'Ontario',
                'Prince Edward Island',
                'Quebec',
                'Saskatchewan',
                'Yukon'
            ]
        }
        for country in plates_list:
            for place in plates_list[country]:
                Plate.create_plate({
                    'place':place,
                    'country':country
                })
    def ongoing_trip(self):
        trip = Trip.query.filter_by(user_id=self.id, end_time=None).all()
        if trip:
            return trip[0]
        return False

    @classmethod
    def reg_validate(cls, form):
        print('Validating new user')
        if len(form['un']) < 1:
            flash('Please enter a username', 'un')
        else:
            users = cls.query.filter_by(username=form['un']).all()
            if users:
                flash('That username is already taken','reg_em')
        if len(form['pw']) < 8:
            flash('Password must be at least eight characters', 'reg_pw')
        if form['cp'] != form['pw']:
            flash('Passwords must match', 'cp')
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
    name = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='cascade'), nullable=False)
    user = db.relationship('User', foreign_keys=[user_id], backref='trips')
    start_time = db.Column(db.DateTime, server_default=func.now())
    end_time = db.Column(db.DateTime)

    def ordered_finds(self):
        ordered = Find.query.filter_by(trip_id=self.id).order_by(Find.found_at.asc()).all()
        return ordered
    def end_trip(self):
        self.end_time = func.now()
        db.session.commit()

    @classmethod
    def validate_trip(cls, form):
        if len(form['tn']) < 1:
            flash('Please enter a name for your trip', 'tn')
        else:
            trips = cls.query.filter_by(name=form['tn']).all()
            if trips:
                flash('You already have a trip by that name!','tn')
        if '_flashes' in session.keys():
            return False
        return True
    @classmethod
    def start_trip(cls, form):
        new_trip = cls(
            name = form['tn'],
            user_id = session['uid']
        )
        db.session.add(new_trip)
        db.session.commit()
    @classmethod
    def current_trip(cls, id):
        trip = cls.query.get(id)
        return trip

class Plate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    place = db.Column(db.String(255))
    country = db.Column(db.String(45))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='cascade'), nullable=False)
    user = db.relationship('User', foreign_keys=[user_id], backref='plates')
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    @classmethod
    def validate_plate(cls, form):
        if len(form['place']) < 1:
            flash('Place name cannot be blank', 'place')
        else:
            trips = cls.query.filter_by(user_id=session['uid'], place=form['place']).all()
            if trips:
                flash('That place is already on your list!','place')
        if '_flashes' in session.keys():
            return False
        return True
    @classmethod
    def create_plate(cls, form):
        new_plate = cls(
            place = form['place'],
            country = form['country'],
            user_id = session['uid']
        )
        db.session.add(new_plate)
        db.session.commit()
        print(new_plate.id)
        return new_plate.id

class Find(db.Model):
    found_at = db.Column(db.DateTime, server_default=func.now())
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id', ondelete='cascade'), primary_key=True)
    trip = db.relationship('Trip', foreign_keys=[trip_id], backref='finds')
    plate_id = db.Column(db.Integer, db.ForeignKey('plate.id', ondelete='cascade'), primary_key=True)
    plate = db.relationship('Plate', foreign_keys=[plate_id], backref='finds')

    def unfind(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_plate(cls, pid, tid):
        new_find = cls(
            trip_id = tid,
            plate_id = pid
        )
        db.session.add(new_find)
        db.session.commit()
    @classmethod
    def get_find(cls, pid, tid):
        find = cls.query.filter_by(plate_id=pid, trip_id = tid).all()
        return find[0]