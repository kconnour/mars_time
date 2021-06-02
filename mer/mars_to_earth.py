"""Convert Martian times to Earth datetimes. """
import datetime
from mer.constants import seconds_per_sol, sols_per_martian_year, \
    date_of_start_of_mars_year_0


# TODO: in python3.10, using int | float
def mars_year_to_datetime(mars_year: float) -> datetime.datetime:
    """Compute the datetime corresponding to an input Mars year.

    Parameters
    ----------
    mars_year
        Any Mars year.

    Raises
    ------
    TypeError
        Raised if :code:`mars_year` is not an int or a float.
    OverflowError
        Raised if :code:`mars_year` is too far in the past or future. This
        occurs around -1038 and 4278.

    Examples
    --------
    Convert a Mars year into its corresponding datetime.

    >>> import datetime, mer
    >>> mars_year = 35.41260282427384
    >>> mer.mars_year_to_datetime(mars_year)
    datetime.datetime(2020, 1, 1, 0, 0)

    Convert sol 300 of Mars year 28 into a datetime.

    >>> import datetime, mer
    >>> my28_start_date = mer.mars_year_to_datetime(28)
    >>> my28_start_date
    datetime.datetime(2006, 1, 21, 17, 48, 28, 800011)
    >>> seconds_since_year_start = 300 * mer.seconds_per_sol
    >>> my28_start_date + datetime.timedelta(seconds=seconds_since_year_start)
    datetime.datetime(2006, 11, 25, 23, 43, 4, 800011)

    """
    try:
        seconds_since_my0 = mars_year * sols_per_martian_year * seconds_per_sol
        return date_of_start_of_mars_year_0 + \
            datetime.timedelta(milliseconds=seconds_since_my0*1000)
    except TypeError as type_error:
        message = 'year must be an int or a float.'
        raise TypeError(message) from type_error
    except OverflowError as overflow_error:
        message = 'The input year is too large for datetime to handle.'
        raise OverflowError(message) from overflow_error
