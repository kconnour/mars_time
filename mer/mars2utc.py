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

    Examples
    --------
    Convert a Mars year into its corresponding datetime.

    >>> import datetime, mer
    >>> mars_year = 35.41260282427384
    >>> mer.mars_year_to_datetime(mars_year)
    datetime.datetime(2020, 1, 1, 0, 0)

    """
    _MarsYear(mars_year)
    seconds_since_my0 = mars_year * sols_per_martian_year * seconds_per_sol
    return date_of_start_of_mars_year_0 + \
        datetime.timedelta(seconds=seconds_since_my0)


class _MarsYear:
    """Ensure an input value is a valid Mars year

    """
    def __init__(self, year: float):
        """
        Parameters
        ----------
        year
            Any Mars year.

        Raises
        ------
        TypeError
            Raised if year is not an int or a float.

        """
        self.year = year

        self.__raise_type_error_if_not_castable_to_float()

    def __raise_type_error_if_not_castable_to_float(self):
        if not isinstance(self.year, (float, int)):
            message = 'year must be an int or a float.'
            raise TypeError(message)

    #def __raise_value_error_if_
