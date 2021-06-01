import datetime
from mer.constants import seconds_per_sol, sols_per_martian_year, \
    date_of_start_of_mars_year_0


def mars_year_to_datetime(mars_year: float) -> datetime.datetime:
    """Compute the datetime of an input Mars year.

    Parameters
    ----------
    mars_year
        Any Mars year.

    Examples
    --------
    Convert a Mars year to a datetime.

    >>> import datetime, mer
    >>> mars_year = 35.41260282427384
    >>> mer.mars_year_to_datetime(mars_year)
    datetime.datetime(2020, 1, 1, 0, 0)

    """
    seconds_since_my0 = mars_year * sols_per_martian_year * seconds_per_sol
    return date_of_start_of_mars_year_0 + \
        datetime.timedelta(seconds=seconds_since_my0)
