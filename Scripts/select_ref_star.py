import os
import json
import copy
import astropy.units as u
import astropy.time as t
import astropy.coordinates as c
import pandas as pd
import sqlalchemy as sql
import corgietc as ct
import EXOSIMS.Prototypes.TargetList
import EXOSIMS.Prototypes.TimeKeeping
import roman_pointing as rp
import corgisim as csm
import corgidb as cdb

#Simple wrapper function to return a dataframe rather than an sql object and clean up the sqlalchemy objects inside
def select_query_db(conn: sql.engine.base.Connection, stmt: sql.Select) -> pd.DataFrame:
    """Take db connection and select statment to return data from the db

    Args:
        conn (sql.engine.base.Connection): sqlalchemy connection object
        stmt (sql.Select): sqlalchemy select statement for desired data

    Returns:
        data (pd.DataFrame): dataframe containing the desired data
    """
    db_res = conn.execute(stmt)
    raw_data = pd.DataFrame([obj.__dict__ for obj in db_res])
    good_data = ~raw_data.columns.str.startswith('_sa_')
    data = raw_data.loc[:, good_data]
    return data

def select_ref_star(st_name: str, obs_start: t.Time, obs_duration: t.Time, engine: sql.engine.base.Engine) -> str:
    """Select refrence star given target and observation parameters

    Args: 
        st_name (str): Target star name in db
        obs_start (astropy.time.Time): Start time of observation window
        obs_duration (astropy.time.Time): Duration of the observation window
        engine (sql.engine.base.Engine): Sqlalchemy engine object that is connected to plandb

    Returns:
        str: Reference star name in db
    """
    # Type checking for inputs and other generic error handling

    # Connect to the DB and get tables
    metadata = sql.MetaData()
    stars_table = sql.Table('Stars', metadata, autoload_with=engine)
    # pass this connection to the query method to be used and then spun up and cleaned up in the calling method 
    conn = engine.connect()
    # query for a Star with the correct st_name entry
    stmt = sql.select(stars_table).where(stars_table.c.st_name == st_name)
    # Test values/statements for making sure that little bits of the code work
    obs_start = obs_start
    obs_duration = obs_duration
    sci_target = select_query_db(conn, stmt)
    target_cords = c.SkyCoord(
    sci_target["ra"].value.data[0],
    sci_target["dec"].value.data[0],
    unit=(sci_target["ra"].unit, sci_target["dec"].unit),
    frame="icrs",
    distance=c.Distance(parallax=sci_target["plx_value"].value.data[0] * sci_target["plx_value"].unit),
    pm_ra_cosdec=sci_target["pmra"].value.data[0] * sci_target["pmra"].unit,
    pm_dec=sci_target["pmdec"].value.data[0] * sci_target["pmdec"].unit,
    radial_velocity=sci_target["rvz_radvel"].value.data[0] * sci_target["rvz_radvel"].unit,
    equinox="J2000",
    obstime="J2000",
    ).transform_to(c.BarycentricMeanEcliptic)
    ref_star = sci_target
    # refStarCoverage in roman_pointing seems very similar? Are we allow to leverage or adapt that code? yes
    
    # how tightly bound is the obvs time? If something starts ~5 days out of bounds but then comes into bounds do we care? treat the inputs as exact. Need down stream determination of observation window validity.  

    # Is this method responsible for checking the validity of the observation window supplied? Checking only availibility of target and reference given all constraints. 

    # Blocking out code and pasting in relvent examples. 

    # search the HIP star catalog? (I think the database is named something else) by the name column looking for a match on the supplied name, currently st_name should be considered an exact match to a column
        # error handling for no name supplied, wrong data type supplied, no star found

    # Set Target coordinates:
    # This code is straight out of roman pointing and looks to do what we want. It is out of the demo ipynb, can be reused for setting targets coords and Area Bounds

        # Error handling here for dates where the target is not observable for bounding reasons at any point? (maybe just a warning about duration and time of issue) during the observation 
        # error handling for targets that are completely outside of the range of observability

    # Construct bounded set of reference stars
    #  
    # Area of observability (5 deg, Solar, and roll? constraints) Are these seperate columns?
    # create an sql query that searches first for class A then B then C stars bounded by the coordinates that define our AOO
    # Query DB for all refs and then compute location and 

    # Convert the DB return for the highest class of star found into a data frame

    # Calculate the Delta pitch and delta Yaw (total combined angular seperation)

    # Find minimum entry for total angular seperation

    return ref_star
