import corgietc as ct  # noqa
import os
import json
import EXOSIMS.Prototypes.TargetList
import EXOSIMS.Prototypes.TimeKeeping
import copy
import astropy.units as u
import astropy.time as t
import pandas as pd
import roman_pointing as rp
import corgisim as cs
import corgidb as cd 

def select_ref_star(st_name: str, obs_start: t.Time, obs_duration: t.Time) -> str:
    """Select refrence star given target and observation parameters

    Args: 
        st_name (str): Target star name in db
        obs_start (astropy.time.Time): Start time of observation window
        obs_duration (astropy.time.Time): Duration of the observation window

    Returns:
        ref_star (str): Reference star name in db
    """
    return ref_star