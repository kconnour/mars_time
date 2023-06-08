"""The orbit module contains functions for finding the MarsTime at various special points in the Martian orbit.
"""
import datetime

import scipy

from mars_time.constants import mars_year_start_days_since_j2000, j2000
from mars_time.retimers import datetime_to_marstime, MarsTime


def find_aphelion(mars_year: int) -> MarsTime:
    """Find the MarsTime of aphelion for a given Mars year.

    Parameters
    ----------
    mars_year: int
        The Mars year. Must be between -99 and 99.

    Returns
    -------
    MarsTime
        The time of aphelion for the given Mars year.

    See Also
    --------
    find_perihelion: Find perihelion for a given Mars year.

    Notes
    -----
    This algorithm works by numerically finding where the solar longitude is changing least rapidly with time.

    Examples
    --------
    Find aphelion for Mars year 33

    >>> import mars_time
    >>> mars_time.find_aphelion(33)
    MarsTime(year=33, sol=151.21)

    """
    def find_days_since_j2000_of_aphelion(day: float) -> float:
        day = float(day)
        pre_aphleion = datetime_to_marstime(j2000 + datetime.timedelta(days=day - 0.001))
        post_aphelion = datetime_to_marstime(j2000 + datetime.timedelta(days=day + 0.001))
        return abs(pre_aphleion.solar_longitude - post_aphelion.solar_longitude)

    bounds = (mars_year_start_days_since_j2000[mars_year], mars_year_start_days_since_j2000[mars_year + 1])
    days = scipy.optimize.minimize_scalar(find_days_since_j2000_of_aphelion, method='bounded', bounds=bounds).x
    return datetime_to_marstime(j2000 + datetime.timedelta(days=days))


def find_perihelion(mars_year: int) -> MarsTime:
    """Find the time of perihelion for a given Mars year.

    Parameters
    ----------
    mars_year: int
        The Mars year. Must be between -99 and 99.

    Returns
    -------
    MarsTime
        The time of perihelion for the given Mars year.

    See Also
    --------
    find_aphelion: Find aphelion for a given Mars year.

    Notes
    -----
    This algorithm works by numerically finding where the solar longitude is changing most rapidly with time.

    Examples
    --------
    Find perihelion for Mars year 33

    >>> import mars_time
    >>> mars_time.find_perihelion(33)
    MarsTime(year=33, sol=485.70)

    """
    def find_days_since_j2000_of_perihelion(day: float) -> float:
        day = float(day)
        pre_perihelion = datetime_to_marstime(j2000 + datetime.timedelta(days=day - 0.001))
        post_perihelion = datetime_to_marstime(j2000 + datetime.timedelta(days=day + 0.001))
        return abs(pre_perihelion.solar_longitude - post_perihelion.solar_longitude) * -1

    bounds = (mars_year_start_days_since_j2000[mars_year], mars_year_start_days_since_j2000[mars_year + 1])
    days = scipy.optimize.minimize_scalar(find_days_since_j2000_of_perihelion, method='bounded', bounds=bounds).x
    return datetime_to_marstime(j2000 + datetime.timedelta(days=days))
