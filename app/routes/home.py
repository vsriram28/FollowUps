from flask import render_template, Blueprint
from app import app, db
from sqlalchemy import distinct
from app.models.meetings import Meeting
from app.models.notes import Note

main = Blueprint('main', __name__)


@app.route('/')
def home():
    # unique_dates = db.session.query(distinct(Meeting.start_time.cast(db.Date))).all()
    unique_dates = db.session.query(distinct(Meeting.start_time.cast(db.Date))).order_by(Meeting.start_time.cast(db.Date).desc()).all()
    # print(unique_dates)
    return render_template('landed.html', title='MyNotes', unique_dates=unique_dates)
    # return render_template('landed.html', title='My Notes')
