# import dependencies
import numpy as np

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

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Set up Flask
#create app
app=Flask(__name__)

#Create Routes
@app.route("/")
def home():
    return (
        f"Welcome to the Jenna Nytes' SQLAlchemy Homework Home Page!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/temp/<start><br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return dates and prcp"""
    # Query all dates and prcp measurements
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    prcp_measurements = []
    for date, prcp in results:
        date_prcp_dict = {}
        date_prcp_dict["date"] = date
        date_prcp_dict["prcp"] = prcp
        prcp_measurements.append(date_prcp_dict)

    return jsonify(prcp_measurements)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""
    # Query dates and prcps
    results = session.query(Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return a list of temperatures for the last year"""
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # Query all dates and prcp measurements
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date > query_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    tobs_measurements = []
    for date, tobs in results:
        date_tobs_dict = {}
        date_tobs_dict["date"] = date
        date_tobs_dict["tobs"] = tobs
        tobs_measurements.append(date_tobs_dict)

    return jsonify(tobs_measurements)
    
    
@app.route("/api/v1.0/temp/<start_date>")
@app.route("/api/v1.0/temp/<start_date>/<end_date>")
def calc_temps(start_date = None, end_date = None):
    session = Session(engine)
    
    query = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    if not end_date:
        
        results = session.query(*query).filter(Measurement.date >= start_date).all()
        
        temps=list(np.ravel(results))
        
        return jsonify(temps)

    results = session.query(*query).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    
    temps=list(np.ravel(results))
    
    return jsonify(temps)

    return jsonify({"error: date not found."}), 404
    
if __name__ == "__main__":
    app.run(debug=True)