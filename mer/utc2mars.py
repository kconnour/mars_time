"""Convert UTC times into Martian times.

This module provides functions to convert coordinated universal time (UTC) into
Martian sols, Martian years, and solar longitude.

"""
import datetime
import math
import numpy as np
from mer.constants import seconds_per_sol, sols_per_martian_year, \
    date_of_start_of_mars_year_0


def convert_to_solar_longitude(date: datetime.datetime) -> float:
    r"""Compute the Martian solar longitude of an input datetime.

    Parameters
    ----------
    date
        Any date.

    Raises
    ------
    TypeError
        Raised if :code:`date` is not a datetime.datetime.

    Examples
    --------
    Convert a date to solar longitude.

    >>> import datetime
    >>> import mer
    >>> date = datetime.datetime(2020, 1, 1, 0, 0, 0)
    >>> mer.convert_to_solar_longitude(date)
    128.8354595387973

    References
    ----------
    The equation used to convert to L\ :sub:`s` can be found in `this paper
    <https://agupubs.onlinelibrary.wiley.com/doi/pdf/10.1029/97GL01950>`_."""
    _DateValidator(date)
    j2000 = datetime.datetime(2000, 1, 1, 12, 0, 0)
    elapsed_days = (date - j2000).total_seconds() / 86400
    m = np.radians(19.41 + 0.5240212 * elapsed_days)
    a = 270.39 + 0.5240384 * elapsed_days
    ls = a + (10.691 + 3.7 * 10 ** -7 * elapsed_days) * np.sin(m) + \
        0.623 * np.sin(2 * m) + 0.05 * np.sin(3 * m) + 0.005 * np.sin(4 * m)
    return ls % 360


def convert_to_fractional_mars_year(date: datetime.datetime) -> float:
    """Compute the fractional Mars year of an input datetime.

    Parameters
    ----------
    date
        Any date.

    Raises
    ------
    TypeError
        Raised if :code:`date` is not a datetime.datetime.

    Examples
    --------
    Convert a date to a fractional Mars year.

    >>> import datetime
    >>> import mer
    >>> date = datetime.datetime(2020, 1, 1, 0, 0, 0)
    >>> mer.convert_to_fractional_mars_year(date)
    35.41260282764361

    """
    return sols_after_mars_year_0(date) / sols_per_martian_year


def convert_to_whole_mars_year(date: datetime.datetime) -> int:
    """Compute the integer Mars year of an input datetime.

    Parameters
    ----------
    date
        Any date.

    Raises
    ------
    TypeError
        Raised if :code:`date` is not a datetime.datetime.

    Examples
    --------
    Convert a date to a "whole" Mars year.

    >>> import datetime
    >>> import mer
    >>> date = datetime.datetime(2020, 1, 1, 0, 0, 0)
    >>> mer.convert_to_whole_mars_year(date)
    35

    """
    return math.floor(convert_to_fractional_mars_year(date))


def convert_to_sol_number(date: datetime.datetime) -> float:
    """Compute the sol number (day of the year) of an input datetime.

    Parameters
    ----------
    date
        Any date.

    Raises
    ------
    TypeError
        Raised if :code:`date` is not a datetime.datetime.

    Notes
    -----
    This function begins counting from 0. Beware that some places like LMD
    use the convention that the new year starts on sol 1.

    Examples
    --------
    Convert a date to a sol number from that Mars year.

    >>> import datetime
    >>> import mer
    >>> date = datetime.datetime(2020, 1, 1, 0, 0, 0)
    >>> mer.convert_to_sol_number(date)
    275.86418551545955

    """
    return sols_after_mars_year_0(date) % sols_per_martian_year


def sols_between_dates(early_date: datetime.datetime,
                       later_date: datetime.datetime) -> float:
    """Compute the number of sols between two datetimes.

    Parameters
    ----------
    early_date
        The earlier of the two dates.
    later_date
        The latter of the two dates.

    Raises
    ------
    TypeError
        Raised if either :code:`early_date` or :code:`later_date` are not a
        datetime.datetime.

    Examples
    --------
    Compute the number of sols Opportunity was active. I don't know the hour,
    minute, or second of the start or end of the mission so I set them to 0.

    >>> import datetime
    >>> import mer
    >>> opportunity_start = datetime.datetime(2004, 1, 25, 0, 0, 0)
    >>> opportunity_end = datetime.datetime(2018, 6, 10, 0, 0, 0)
    >>> mer.sols_between_dates(opportunity_start, opportunity_end)
    5109.551211085292

    """
    _DateValidator(early_date)
    _DateValidator(later_date)
    elapsed_seconds = (later_date - early_date).total_seconds()
    return elapsed_seconds / seconds_per_sol


def sols_since_date(date: datetime.datetime) -> float:
    """Compute the number of sols between an input datetime and today.

    Parameters
    ----------
    date
        Any date.

    Raises
    ------
    TypeError
        Raised if :code:`date` is not a datetime.datetime.

    """
    return sols_between_dates(date, datetime.datetime.utcnow())


def sols_after_mars_year_0(date: datetime.datetime) -> float:
    """Compute the number of sols between a datetime and the start of Mars year
    0.

    Parameters
    ----------
    date
        Any date.

    Raises
    ------
    TypeError
        Raised if :code:`date` is not a datetime.datetime.

    """
    return sols_between_dates(date_of_start_of_mars_year_0, date)


class _DateValidator:
    """Ensure an input date is a valid UTC datetime.

    """
    def __init__(self, date: datetime.datetime):
        """
        Parameters
        ----------
        date
            Any date.

        Raises
        ------
        TypeError
            Raised if date is not a datetime.date.

        """
        self.date = date

        self.__raise_type_error_if_not_datetime_date()

    def __raise_type_error_if_not_datetime_date(self):
        if not isinstance(self.date, datetime.datetime):
            message = 'date must be a datetime.datetime.'
            raise TypeError(message)
