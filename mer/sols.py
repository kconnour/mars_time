import datetime
from mer import date_of_start_of_mars_year_0, seconds_per_sol


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

    Examples
    --------
    Find the number of sols after Mars year 0 that MAVEN arrived at Mars.

    >>> import datetime, mer
    >>> date = datetime.datetime(2014, 9, 2, 2, 24, 0)
    >>> sols = mer.sols_after_mars_year_0(date)
    >>> sols
    21781.872772174716

    Get the Mars year at the arrival date. Note that it's more efficient to use
    the built-in function.

    >>> sols / mer.sols_per_martian_year
    32.57857586833816
    >>> mer.datetime_to_fractional_mars_year(date)
    32.57857586833816

    """
    return sols_between_datetimes(date_of_start_of_mars_year_0, date)


def sols_between_datetimes(early_date: datetime.datetime,
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

    >>> import datetime, mer
    >>> opportunity_start = datetime.datetime(2004, 1, 25, 0, 0, 0)
    >>> opportunity_end = datetime.datetime(2018, 6, 10, 0, 0, 0)
    >>> mer.sols_between_datetimes(opportunity_start, opportunity_end)
    5109.551211085292

    """
    _DateValidator(early_date)
    _DateValidator(later_date)
    elapsed_seconds = (later_date - early_date).total_seconds()
    return elapsed_seconds / seconds_per_sol


def sols_since_datetime(date: datetime.datetime) -> float:
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
    return sols_between_datetimes(date, datetime.datetime.utcnow())


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
