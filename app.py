# dependencies
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# access database
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
measurement=Base.classes.measurement
station=Base.classes.station
session=Session(engine)

# set up flask
app=Flask(__name__)
@app.route("/")
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    '''

    )
@app.route("/api/v1.0/precipitation")
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(measurement.tobs).\
      filter(measurement.station == 'USC00519281').\
      filter(measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")