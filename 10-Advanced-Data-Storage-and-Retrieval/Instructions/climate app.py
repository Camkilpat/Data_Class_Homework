import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Create our session (link) from Python to the DB
session = Session(engine)

#Create an app, being sure to pass __name__
app = Flask(__name__)

@app.route ("/")
def index():
    return(
        f"Routes:<br />"
        f"<br />"
        f"/api/v1.0/precipitation<br />"
        f"/api/v1.0/stations<br />"
        f"/api/v1.0/tobs<br />"
        f"/api/v1.0/temp/start/end<br />"
    )

@app.route ("/api/v1.0/precipitation")
def precipitation():
    precip_calc = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").\
        filter (Measurement.date <= "2017-08-23").\
        group_by(Measurement.date).all()
    return jsonify(precip_calc)

@app.route ("/api/v1.0/stations")
def stations():
    s_results = session.query(Station.station, Station.name).all()
    return jsonify(s_results)

@app.route ("/api/v1.0/tobs")
def tobs():
    t_results = session.query (Measurement.station, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.station == most_active_station [0]).all()
    return jsonify(t_results)

@app.route ("/api/v1.0/temp/start/end")
def startDateEndDate (start,end):
    multiple_day = session.query (func.min(Mesurement.tobs), func.avg(Mesurement.tobs), func.max(Mesurement.tobs)).filter(Mesurement.date >= start).filter(Mesurement.date <= end).all()
    return jsonify(multiple_day)

if _name_ = "_main_":
    app.run(debug = True)