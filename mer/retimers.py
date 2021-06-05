"""The retimers module contains classes to convert between different time
representations."""
import datetime
import math
import pytz
from mer.constants import mars_year_0_start, sols_per_martian_year, \
    seconds_per_sol


# TODO: remove the print statements in the examples
class EarthDatetime:
    """Convert Earth datetimes into Martian times.

    """
    def __init__(self, dt: datetime.datetime):
        """
        Parameters
        ----------
        dt
            Any datetime.

        Raises
        ------
        TypeError
            Raised if :code:`dt` is not a datetime.datetime.

        Notes
        -----
        :code:`dt` can be "aware" (have time zone information included with it)
        or "unaware" (have no associated time zone information). If it is
        unaware, it is assumed to be a UTC time and will have that info added to
        it.

        Examples
        --------
        This object simply accepts datetimes. You can include time zone
        information as shown below.

        >>> import datetime, pytz, mer
        >>> dt = datetime.datetime(2020, 1, 1, 0, 0, 0, 0, tzinfo=pytz.UTC)
        >>> aware_dt = EarthDatetime(dt)
        >>> print(aware_dt)
        2020-01-01 00:00:00+00:00

        If no time zone information is included, the datetime is assumed to be
        in UTC.

        >>> dt = datetime.datetime(2020, 1, 1, 0, 0, 0, 0)
        >>> unaware_dt = EarthDatetime(dt)
        >>> print(unaware_dt)
        2020-01-01 00:00:00+00:00
        >>> aware_dt == unaware_dt
        True

        You can also include non-UTC timezones.

        >>> eastern = pytz.timezone('US/Eastern')
        >>> dt = datetime.datetime(2020, 1, 1, 0, 0, 0, 0, tzinfo=eastern)
        >>> print(EarthDatetime(dt))
        2020-01-01 00:00:00-04:56

        """
        self.__raise_type_error_if_not_datetime(dt)
        self.__dt = self.__make_aware_timezone(dt)

    @staticmethod
    def __raise_type_error_if_not_datetime(dt) -> None:
        if not isinstance(dt, datetime.datetime):
            message = 'dt must be a datetime.datetime.'
            raise TypeError(message)

    @staticmethod
    def __make_aware_timezone(dt):
        return dt.replace(tzinfo=pytz.UTC) if dt.tzinfo is None else dt

    def __str__(self):
        return f'{self.__dt}'

    def __eq__(self, other):
        return self.__dt == other.__dt if isinstance(other, EarthDatetime) \
            else False

    def to_fractional_mars_year(self) -> float:
        """Compute the fractional Mars year corresponding to the input datetime.

        Examples
        --------
        Convert a datetime into its corresponding fractional Mars year.

        >>> import datetime, pytz, mer
        >>> dt = datetime.datetime(2020, 1, 1, 0, 0, 0, 0, tzinfo=pytz.UTC)
        >>> EarthDatetime(dt).to_fractional_mars_year()
        35.41260282427384

        """
        return sols_after_mars_year_0(self.__dt) / sols_per_martian_year

    def to_whole_mars_year(self) -> int:
        """Compute the integer Mars year corresponding to the input datetime.

        Examples
        --------
        Convert a datetime into its corresponding "whole" Mars year.

        >>> import datetime, pytz, mer
        >>> date = datetime.datetime(2020, 1, 1, 0, 0, 0, 0, tzinfo=pytz.UTC)
        >>> EarthDatetime(date).to_whole_mars_year()
        35

        """
        return math.floor(self.to_fractional_mars_year())

    def to_sol(self) -> float:
        """Compute the sol (day of the Martian year) corresponding to an input
        datetime.

        Notes
        -----
        This function begins counting from 0. Beware that some places like LMD
        use the convention that the new year starts on sol 1.

        Examples
        --------
        Convert a datetime into its corresponding sol.

        >>> import datetime, pytz, mer
        >>> date = datetime.datetime(2020, 1, 1, 0, 0, 0, 0, tzinfo=pytz.UTC)
        >>> EarthDatetime(date).to_sol()
        275.86418326244836

        """
        return sols_after_mars_year_0(self.__dt) % sols_per_martian_year

    def to_solar_longitude(self) -> float:
        r"""Compute the Martian solar longitude corresponding to the input
        datetime.

        Examples
        --------
        Convert a datetime into its corresponding solar longitude.

        >>> import datetime, pytz, mer
        >>> date = datetime.datetime(2020, 1, 1, 0, 0, 0, 0, tzinfo=pytz.UTC)
        >>> EarthDatetime(date).to_solar_longitude()
        128.8354595387973

        References
        ----------
        The equation used to convert to L\ :sub:`s` can be found in `this paper
        <https://agupubs.onlinelibrary.wiley.com/doi/pdf/10.1029/97GL01950>`_.
        """
        j2000 = datetime.datetime(2000, 1, 1, 12, 0, 0, 0, pytz.UTC)
        elapsed_days = (self.__dt - j2000).total_seconds() / 86400
        m = math.radians(19.41 + 0.5240212 * elapsed_days)
        a = 270.39 + 0.5240384 * elapsed_days
        ls = a + (10.691 + 3.7 * 10 ** -7 * elapsed_days) * math.sin(m) + \
            0.623 * math.sin(2 * m) + 0.05 * math.sin(3 * m) + \
            0.005 * math.sin(4 * m)
        return ls % 360


class Sol:
    """Convert sols into different temporal representations.

    """
    def __init__(self, mars_year: int, sol: float):
        """
        Parameters
        ----------
        mars_year
            The Mars year.
        sol
            The sol number, assuming the Mars year starts at sol 0.

        Raises
        ------
        TypeError
            Raised if :code:`mars_year` is not an int, or if :code:`sol` is not
            an int or float.
        ValueError
            Raised if :code:`sol` is an unphysical value.

        """
        self.__my = mars_year
        self.__sol = sol

        self.__raise_type_error_if_mars_year_is_not_int()
        self.__raise_type_error_if_sol_is_not_int_or_float()
        self.__raise_value_error_if_sol_is_unphysical()

    def __raise_type_error_if_mars_year_is_not_int(self):
        if not isinstance(self.__my, int):
            message = 'mars_year must be an int.'
            raise TypeError(message)

    def __raise_type_error_if_sol_is_not_int_or_float(self):
        if not isinstance(self.__sol, (int, float)):
            message = 'sol must be an int or a float.'
            raise TypeError(message)

    def __raise_value_error_if_sol_is_unphysical(self):
        if not (0 <= self.__sol <= sols_per_martian_year):
            message = f'sol must be between 0 and {sols_per_martian_year}.'
            raise ValueError(message)

    def __str__(self):
        return f'Mars year: {self.__my}, sol: {self.__sol}'

    def to_fractional_mars_year(self) -> float:
        """Compute the fractional Mars year of the input Mars year and sol.

        Examples
        --------
        Convert a sol to a fractional Mars year.

        >>> Sol(30, 254).to_fractional_mars_year()
        30.379901138763824

        """
        return self.__my + self.__sol / sols_per_martian_year

    def to_datetime(self) -> datetime.datetime:
        """Convert the sol of the Mars year to a datetime.

        Raises
        ------
        OverflowError
            Raised if the input Mars year is too far from the present. This
            happens around Mars years of -1039 and 4279.

        Examples
        --------
        Convert a sol to its corresponding datetime.

        >>> Sol(30, 254).to_datetime()
        datetime.datetime(2010, 7, 14, 16, 4, 32, 880011, tzinfo=<UTC>)

        """
        try:
            frac_my = self.to_fractional_mars_year()
            elapsed_seconds = frac_my * sols_per_martian_year * \
                seconds_per_sol
            return mars_year_0_start + \
                datetime.timedelta(seconds=elapsed_seconds)
        except OverflowError as overflow_error:
            message = 'The input Mars year is too far from the present for ' \
                      'datetime to compute dates.'
            raise OverflowError(message) from overflow_error

    def to_solar_longitude(self) -> float:
        """Convert the input to a solar longitude.

        Raises
        ------
        OverflowError
            Raised if the input Mars year is too far from the present. This
            happens around Mars years of -1039 and 4279.

        Examples
        --------
        Convert a sol to its corresponding solar longitude.

        >>> Sol(30, 254).to_solar_longitude()
        118.21959480190617

        """
        dt = self.to_datetime()
        return EarthDatetime(dt).to_solar_longitude()


def sols_after_mars_year_0(dt: datetime.datetime) -> float:
    """Compute the number of sols between a datetime and the start of Mars year
    0.

    Parameters
    ----------
    dt
        Any datetime.

    Raises
    ------
    TypeError
        Raised if :code:`dt` is not a datetime.datetime.

    Examples
    --------
    Find the number of sols after Mars year 0 that MAVEN arrived at Mars.

    >>> import datetime, mer
    >>> maven_arrival_datetime = datetime.datetime(2014, 9, 2, 2, 24, 0, 0, tzinfo=pytz.UTC)
    >>> mer.sols_after_mars_year_0(maven_arrival_datetime)
    21781.872772174716

    """
    try:
        return sols_between_datetimes(mars_year_0_start, dt)
    except TypeError as type_error:
        message = 'dt must be a datetime.datetime.'
        raise TypeError(message) from type_error


def sols_between_datetimes(early_dt: datetime.datetime,
                           later_dt: datetime.datetime) -> float:
    """Compute the number of sols between two datetimes.

    Parameters
    ----------
    early_dt
        The earlier of the two datetimes.
    later_dt
        The latter of the two datetimes.

    Raises
    ------
    TypeError
        Raised if either :code:`early_dt` or :code:`later_dt` are not a
        datetime.datetime.

    Examples
    --------
    Compute the number of sols Opportunity was active. I don't know the hour,
    minute, or second of the start or end of the mission so I set them to 0.

    >>> import datetime, mer
    >>> opportunity_start = datetime.datetime(2004, 1, 25, 0, 0, 0, 0, tzinfo=pytz.UTC)
    >>> opportunity_end = datetime.datetime(2018, 6, 10, 0, 0, 0, 0, tzinfo=pytz.UTC)
    >>> mer.sols_between_datetimes(opportunity_start, opportunity_end)
    5109.551211085292

    """
    try:
        elapsed_seconds = (later_dt - early_dt).total_seconds()
        return elapsed_seconds / seconds_per_sol
    except TypeError as type_error:
        message = 'Both inputs must be a datetime.datetime.'
        raise TypeError(message) from type_error
    except AttributeError as attr_error:
        message = 'Both inputs must be a datetime.datetime.'
        raise TypeError(message) from attr_error


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
