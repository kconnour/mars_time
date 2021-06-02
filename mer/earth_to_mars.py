"""Convert Earth datetimes into Martian times."""
import datetime
import math
from mer.constants import sols_per_martian_year
#sols_after_mars_year_0


def datetime_to_fractional_mars_year(date: datetime.datetime) -> float:
    """Compute the fractional Mars year corresponding to an input datetime.

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
    Convert a datetime into its corresponding fractional Mars year.

    >>> import datetime, mer
    >>> date = datetime.datetime(2020, 1, 1, 0, 0, 0)
    >>> mer.datetime_to_fractional_mars_year(date)
    35.41260282427384

    """
    return sols_after_mars_year_0(date) / sols_per_martian_year


def datetime_to_whole_mars_year(date: datetime.datetime) -> int:
    """Compute the integer Mars year corresponding to an input datetime.

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
    Convert a datetime into its corresponding "whole" Mars year.

    >>> import datetime, mer
    >>> date = datetime.datetime(2020, 1, 1, 0, 0, 0)
    >>> mer.datetime_to_whole_mars_year(date)
    35

    """
    return math.floor(datetime_to_fractional_mars_year(date))


def datetime_to_sol(date: datetime.datetime) -> float:
    """Compute the sol (day of the Martian year) corresponding to an input
    datetime.

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
    Convert a datetime into its corresponding sol.

    >>> import datetime, mer
    >>> date = datetime.datetime(2020, 1, 1, 0, 0, 0)
    >>> mer.datetime_to_sol(date)
    275.86418326244836

    """
    return sols_after_mars_year_0(date) % sols_per_martian_year


def datetime_to_solar_longitude(date: datetime.datetime) -> float:
    r"""Compute the Martian solar longitude corresponding to an input datetime.

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
    Convert a datetime into its corresponding solar longitude.

    >>> import datetime, mer
    >>> date = datetime.datetime(2020, 1, 1, 0, 0, 0)
    >>> mer.datetime_to_solar_longitude(date)
    128.8354595387973

    References
    ----------
    The equation used to convert to L\ :sub:`s` can be found in `this paper
    <https://agupubs.onlinelibrary.wiley.com/doi/pdf/10.1029/97GL01950>`_."""
    _DateValidator(date)
    j2000 = datetime.datetime(2000, 1, 1, 12, 0, 0)
    elapsed_days = (date - j2000).total_seconds() / 86400
    m = math.radians(19.41 + 0.5240212 * elapsed_days)
    a = 270.39 + 0.5240384 * elapsed_days
    ls = a + (10.691 + 3.7 * 10 ** -7 * elapsed_days) * math.sin(m) + \
        0.623 * math.sin(2 * m) + 0.05 * math.sin(3 * m) + \
        0.005 * math.sin(4 * m)
    return ls % 360


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
