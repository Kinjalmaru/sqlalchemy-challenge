import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB

session = Session(engine)
################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitaion<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/start<br>"
        f"/api/v1.0/start-end"
    )

@app.route("/api/v1.0/precipitaion")
def precipitaion():
    # Design a query to retrieve the last 12 months of precipitation data and plot the results

    # Calculate the date one year from the last date in data set.
    previous = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    results =  session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date >= previous).all()

    #dictionary with the date as the key and the precipitation as the value
    precip = {date: prcp for date, prcp in results}

    session.close()
    return  jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    # DEsign a query to show all the stationis available in the dataset
    results = session.query(Station.station).all()

    stations = list(np.ravel(results))

    session.close()
    return jsonify(stations)


    
if __name__ == '__main__':
    app.run(debug=True)
