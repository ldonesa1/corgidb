import os
import json
import copy
import astropy.units as u
import astropy.time as t
import pandas as pd
import sqlalchemy as sql
import corgietc as ct
import EXOSIMS.Prototypes.TargetList
import EXOSIMS.Prototypes.TimeKeeping
import roman_pointing as rp
import corgisim as csm
import corgidb as cdb


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
    # Connect to the DB and get tables
    metadata = sql.MetaData()
    stars_table = sql.Table('Stars', metadata, autoload_with=engine)
    conn = engine.connect()
    # query for a Star with the correct st_name entry
    stmt = sql.select(stars_table).where(stars_table.c.st_name == st_name)
    sci_target = conn.execute(stmt)
    # refStarCoverage in roman_pointing seems very similar? Are we allow to leverage or adapt that code? yes
    
    # how tightly bound is the obvs time? If something starts ~5 days out of bounds but then comes into bounds do we care? treat the inputs as exact. Need down stream determination of observation window validity.  

    # Is this method responsible for checking the validity of the observation window supplied? Checking only availibility of target and reference given all constraints. 

    # Blocking out code and pasting in relvent examples. 

    # search the HIP star catalog? (I think the database is named something else) by the name column looking for a match on the supplied name, currently st_name should be considered an exact match to a column
        # error handling for no name supplied, wrong data type supplied, no star found

    # Set Target coordinates:
    # This code is straight out of roman pointing and looks to do what we want. It is out of the demo ipynb, can be reused for setting targets coords and Area Bounds
#    target = SkyCoord(
#    res["ra"].value.data[0],
#    res["dec"].value.data[0],
#    unit=(res["ra"].unit, res["dec"].unit),
#    frame="icrs",
#    distance=Distance(parallax=res["plx_value"].value.data[0] * res["plx_value"].unit),
#    pm_ra_cosdec=res["pmra"].value.data[0] * res["pmra"].unit,
#    pm_dec=res["pmdec"].value.data[0] * res["pmdec"].unit,
#    radial_velocity=res["rvz_radvel"].value.data[0] * res["rvz_radvel"].unit,
#    equinox="J2000",
#    obstime="J2000",
#    ).transform_to(BarycentricMeanEcliptic)



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