import os
import json
import copy
import numpy as np
import astropy.units as u
import astropy.time as t
import astropy.coordinates as c
import pandas as pd
import sqlalchemy as sql
import corgietc as ct
import EXOSIMS.Prototypes.TargetList
import EXOSIMS.Prototypes.TimeKeeping
from roman_pointing import roman_pointing as rp
import corgisim as csm
import corgidb as cdb

#Wrapper function to return a dataframe rather than an sql object and clean up the sqlalchemy objects inside
def select_query_db(conn: sql.engine.base.Connection, stmt: sql.Select) -> pd.DataFrame:
    """Take db connection and select statment to return data from the db

    Args:
        conn (sqlalchemy.engine.base.Connection): sqlalchemy connection object
        stmt (sqlalchemy.Select): sqlalchemy select statement for desired data

    Returns:
        data (pandas.DataFrame): dataframe containing the desired data
    """
    #connect to db and run statement
    db_res = conn.execute(stmt)
    #change return into a dataframe
    raw_data = pd.DataFrame([obj.__dict__ for obj in db_res])
    #select only data thats not sqlalchemy objects and return them
    good_data = ~raw_data.columns.str.startswith('_sa_')
    data = raw_data.loc[:, good_data]
    return data

def check_pointing(tar: pd.DataFrame, obs_start: t.Time, obs_duration: t.TimeDelta) -> tuple[bool, list, list]:
    """Check that the observation window defined for a stars data does not violate any constraints
    
    Args:
        tar (pandas.DataFrame): Target star data defined as a DataFrame
        obs_start (astropy.time.Time): Start time of the observation
        obs_duration (astropy.time.Time): Duration of the observation
    
    Returns:
        result (tuple[bool, list]): returns a boolean true/false if the observation is valid, and a list of pointings over the window
    """
    #New to data frames and not sure quite how the accessing is going to work. Guess we just gotta test it. Seems like you can call columns by name like a dict, could also just convert with the line below. 
    #d_tar = tar.to_dict(orient='records')
    
    #need to check that all the required data came in with the dataframe, if there isn't a value for the data return error
    # define descrete times to calculate angles over
    times = obs_start + obs_duration * np.linspace(0, 100, 100)
    # Build sky coord object for the target
    tar_cords = c.SkyCoord(
    tar["ra"].value.data[0],
    tar["dec"].value.data[0],
    unit=(tar["ra"].unit, tar["dec"].unit),
    frame="icrs",
    distance=c.Distance(parallax=tar["plx_value"].value.data[0] * tar["plx_value"].unit),
    pm_ra_cosdec=tar["pmra"].value.data[0] * tar["pmra"].unit,
    pm_dec=tar["pmdec"].value.data[0] * tar["pmdec"].unit,
    radial_velocity=tar["rvz_radvel"].value.data[0] * tar["rvz_radvel"].unit,
    equinox="J2000",
    obstime="J2000",
    ).transform_to(c.BarycentricMeanEcliptic)
    #calculate angles of interest over the observation window 
    sun_ang_targ, yaw_targ, pitch_targ, B_C_I_targ = rp.calcRomanAngles(
    tar_cords, times, rp.getL2Positions(times)
    )
    #Convert angles to degrees
    sun_ang_d_targ = sun_ang_targ.to(u.degree)
    #Check the five degree sun angle constraint and set validity
    if any((item > 54 ) & (item < 126) for item in sun_ang_d_targ):
        valid = False
    else:
        valid = True
    result = valid, sun_ang_targ, pitch_targ
    return result

def select_ref_star(st_name: str, obs_start: t.Time, obs_duration: t.TimeDelta, engine: sql.engine.base.Engine) -> str:
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
    sci_target = select_query_db(conn, stmt)
    tar_val, tar_sun_angs, tar_pitch_angs = check_pointing(sci_target, obs_start, obs_duration)
    if tar_val is False:
        pass
        # logic to handle a observation that is not valid
    else:
        pass
        # Logic to start selecting reference stars
    ref_star = sci_target["st_name"]


    return ref_star







    # how tightly bound is the obvs time? If something starts ~5 days out of bounds but then comes into bounds do we care? treat the inputs as exact. Need down stream determination of observation window validity.  

    # Is this method responsible for checking the validity of the observation window supplied? Checking only availibility of target and reference given all constraints. 

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
