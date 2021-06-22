"""The retimers module contains tools to convert between different time
representations."""
import datetime
import math
from mer.constants import mars_year_0_start, sols_per_martian_year, \
    seconds_per_sol, orbital_eccentricity, perihelion_sol


class EarthDateTime(datetime.datetime):
    """An EarthDateTime object represents an Earth datetime.

    This extends datetime.datetime and adds methods to convert Earth times into
    common Martian times.

    """
    def __new__(cls, year: int, month: int, day: int, hour: int = 0,
                minute: int = 0, second: int = 0, microsecond: int = 0,
                tzinfo=datetime.timezone.utc):
        """
        Parameters
        ----------
        year
            The year. Must be between the minyear and maxyear supported by
            datetime.
        month
            The month. Must be between 1 and 12.
        day
            The day. Must be between 1 and the number of days in the given month
            and year.
        hour
            The hour. Must be between 0 and 24.
        minute
            The minute. Must be between 0 and 60.
        second
            The second. Must be between 0 and 60.
        microsecond
            The microsecond. Must be between 0 and 1000000.
        tzinfo
            The timezone. Can be any compatible timezone.

        Raises
        ------
        TypeError
            Raised if any of the inputs except :code:`tzinfo` are not ints.

        ValueError
            Raised if

        Notes
        -----
        If you do not include time zone information when constructing this
        class, I assume it is a UTC time and add that information automatically.

        Examples
        --------
        Create an instance of this class the same way you'd make a datetime.

        >>> import mer
        >>> print(mer.EarthDateTime(2020, 1, 1, 0, 0, 0, 0))
        2020-01-01 00:00:00+00:00

        You can also add timezones the same way you'd add them to a datetime. I
        recommend using the :code:`pytz` module if you want to use them.

        >>> import pytz
        >>> eastern = pytz.timezone('US/Eastern')
        >>> print(mer.EarthDateTime(2020, 1, 1, 0, 0, 0, 0, tzinfo=eastern))
        2020-01-01 00:00:00-04:56

        This class is compatible with time deltas, just like datetimes.

        >>> mer.EarthDateTime(2020, 1, 1, 0, 0, 0) + datetime.timedelta(hours=7)
        EarthDateTime(2020, 1, 1, 7, 0, tzinfo=datetime.timezone.utc)

        """
        return datetime.datetime.__new__(
            cls, year, month=month, day=day, hour=hour, minute=minute,
            second=second, microsecond=microsecond, tzinfo=tzinfo)

    def to_fractional_mars_year(self) -> float:
        """Compute the corresponding fractional Mars year.

        Examples
        --------
        Convert a date and time into its corresponding fractional Mars year.

        >>> import mer
        >>> mer.EarthDateTime(2020, 1, 1, 0, 0, 0, 0).to_fractional_mars_year()
        35.41260282427384

        """
        return sols_after_mars_year_0(self) / sols_per_martian_year

    def to_whole_mars_year(self) -> int:
        """Compute the corresponding integer Mars year.

        Examples
        --------
        Convert a date and time into its corresponding integer Mars year.

        >>> import mer
        >>> mer.EarthDateTime(2020, 1, 1, 0, 0, 0, 0).to_whole_mars_year()
        35

        """
        return math.floor(self.to_fractional_mars_year())

    def to_sol(self) -> float:
        """Compute the corresponding sol (day of the Martian year).

        Notes
        -----
        This function begins counting from 0 such that the first moment of the
        Mars year is sol 0. Beware that some places/people use the convention
        that the new year starts on sol 1.

        Examples
        --------
        Convert a date and time into its corresponding sol.

        >>> import mer
        >>> mer.EarthDateTime(2020, 1, 1, 0, 0, 0, 0).to_sol()
        275.86418326244836

        """
        return sols_after_mars_year_0(self) % sols_per_martian_year

    def to_solar_longitude(self) -> float:
        r"""Compute the corresponding Martian solar longitude.

        Examples
        --------
        Convert a date and time into its corresponding solar longitude.

        >>> import mer
        >>> mer.EarthDateTime(2020, 1, 1, 0, 0, 0, 0).to_solar_longitude()
        128.855367761636

        References
        ----------
        The equation used in this method can be found in `this paper
        <https://doi.org/10.1016/j.icarus.2014.12.014>`_. While this paper
        claims the equation is accurate to within 0.05 degrees, I have found
        errors up to 0.2 $^\circ$.
        """
        utc = datetime.timezone.utc
        j2000 = datetime.datetime(2000, 1, 1, 12, 0, 0, 0, tzinfo=utc)
        elapsed_days = (self - j2000).total_seconds() / 86400
        m = math.radians(19.38095 + 0.524020769 * elapsed_days)
        ls = 270.38859 + \
            0.524038542 * elapsed_days + \
            10.67848 * math.sin(m) + \
            0.62077 * math.sin(2*m) + \
            0.05031 * math.sin(3*m)
        return ls % 360


class MarsYearSol:
    """A MarsYearSol represents time in Mars year and sol.

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

        Examples
        --------
        Create an instance of this class. Printing it shows its input values.

        >>> import mer
        >>> print(mer.MarsYearSol(34, 200.5))
        Mars year 34, sol 200.5

        """
        self.__my = mars_year
        self.__sol = sol

        self.__raise_type_error_if_mars_year_is_not_int()
        self.__raise_type_error_if_sol_is_not_int_or_float()
        self.__raise_value_error_if_sol_is_unphysical()

    def __raise_type_error_if_mars_year_is_not_int(self) -> None:
        if not isinstance(self.__my, int):
            message = 'mars_year must be an int.'
            raise TypeError(message)

    def __raise_type_error_if_sol_is_not_int_or_float(self) -> None:
        if not isinstance(self.__sol, (int, float)):
            message = 'sol must be an int or a float.'
            raise TypeError(message)

    def __raise_value_error_if_sol_is_unphysical(self) -> None:
        if not 0 <= self.__sol <= sols_per_martian_year:
            message = f'sol must be between 0 and {sols_per_martian_year}.'
            raise ValueError(message)

    def __str__(self):
        return f'Mars year {self.__my}, sol {self.__sol}'

    def __repr__(self):
        return f'MarsYearSol({self.__my}, {self.__sol})'

    def to_datetime(self) -> datetime.datetime:
        """Compute the corresponding datetime.

        Raises
        ------
        OverflowError
            Raised if the Mars year is too far from the present. This happens
            around Mars years of -1039 and 4279.

        Examples
        --------
        Convert a Mars year and sol into its corresponding datetime.

        >>> import mer
        >>> print(mer.MarsYearSol(30, 254).to_datetime())
        2010-07-14 16:04:32.880011+00:00

        """
        try:
            frac_my = self.to_fractional_mars_year()
            elapsed_seconds = frac_my * sols_per_martian_year * seconds_per_sol
            return mars_year_0_start + datetime.timedelta(
                seconds=elapsed_seconds)
        except OverflowError as overflow_error:
            message = 'The input Mars year is too far from the present for ' \
                      'datetime to compute dates.'
            raise OverflowError(message) from overflow_error

    def to_fractional_mars_year(self) -> float:
        """Compute the corresponding fractional Mars year.

        Examples
        --------
        Convert a sol to a fractional Mars year.

        >>> import mer
        >>> mer.MarsYearSol(30, 254).to_fractional_mars_year()
        30.379901138763824

        """
        return self.__my + self.__sol / sols_per_martian_year

    def to_solar_longitude(self) -> float:
        """Compute the corresponding solar longitude [degrees].

        Raises
        ------
        OverflowError
            Raised if the input Mars year is too far from the present. This
            happens around Mars years of -1039 and 4279.

        Examples
        --------
        Convert a sol to its corresponding solar longitude.

        >>> import mer
        >>> mer.MarsYearSol(30, 254).to_solar_longitude()
        118.23478131776619

        """
        edt = datetime_to_earthdatetime(self.to_datetime())
        return edt.to_solar_longitude()


class MarsYearSolarLongitude:
    """A MarsYearSolarLongitude represents time in Mars year and solar longitude.

    """
    def __init__(self, mars_year: int, ls: float):
        """

        Parameters
        ----------
        mars_year
            The Mars year.
        ls
            The solar longitude [degrees].

        Raises
        ------
        TypeError
            Raised if :code:`mars_year` is not an int, or if :code:`ls` is not
            an int or float.
        ValueError
            Raised if :code:`ls` is not between 0 and 360.

        Examples
        --------
        Create an instance of this class. Printing it shows its input values.

        >>> import mer
        >>> print(mer.MarsYearSolarLongitude(34, 200.5))
        Mars year 34, Ls 200.5

        """
        self.__my = mars_year
        self.__ls = ls

        self.__raise_type_error_if_mars_year_is_not_int()
        self.__raise_type_error_if_ls_is_not_int_or_float()
        self.__raise_value_error_if_ls_is_unphysical()

    def __raise_type_error_if_mars_year_is_not_int(self) -> None:
        if not isinstance(self.__my, int):
            message = 'mars_year must be an int.'
            raise TypeError(message)

    def __raise_type_error_if_ls_is_not_int_or_float(self) -> None:
        if not isinstance(self.__ls, (int, float)):
            message = 'ls must be an int or a float.'
            raise TypeError(message)

    def __raise_value_error_if_ls_is_unphysical(self) -> None:
        if not 0 <= self.__ls <= 360:
            message = 'ls must be between 0 and 360.'
            raise ValueError(message)

    def __str__(self):
        return f'Mars year {self.__my}, Ls {self.__ls}'

    def __repr__(self):
        return f'MarsYearSolarLongitude({self.__my}, {self.__ls})'

    def to_datetime(self) -> datetime.datetime:
        """Compute the corresponding datetime.

        Examples
        --------
        Convert a solar longitude into its corresponding datetime.

        >>> import mer
        >>> print(mer.MarsYearSolarLongitude(34, 200.5).to_datetime())
        2018-06-26 23:50:49.579031+00:00

        Find the start of Mars year 1.

        >>> print(mer.MarsYearSolarLongitude(1, 0).to_datetime())
        1955-04-11 11:19:36.327061+00:00

        """
        sol = self.to_sol()
        return MarsYearSol(self.__my, sol).to_datetime()

    def to_fractional_mars_year(self) -> float:
        """Compute the corresponding fractional Mars year.

        Examples
        --------
        Convert a solar longitude into its corresponding Mars year.

        >>> import mer
        >>> mer.MarsYearSolarLongitude(34, 200.5).to_fractional_mars_year()
        34.607612860165986

        """
        sol = self.to_sol()
        return self.__my + sol / sols_per_martian_year

    def to_sol(self) -> float:
        """Compute the corresponding sol.

        Examples
        --------
        Convert a solar longitude into its corresponding sol.

        >>> import mer
        >>> print(mer.MarsYearSolarLongitude(34, 200.5).to_sol())
        406.2469172489268

        """
        # 1.90... is: 2*Pi*(1-Ls(perihelion)/360); Ls(perihelion)=250.99
        # according to the LMD converter code
        true_anomaly = self.__ls * math.pi / 180 + 1.90258341759902
        eccentric_anomaly = 2*math.atan(math.tan(0.5*true_anomaly) /
                                        math.sqrt((1 + orbital_eccentricity) /
                                                  (1 - orbital_eccentricity)))
        mean_anomaly = eccentric_anomaly - orbital_eccentricity * \
            math.sin(eccentric_anomaly)
        return ((mean_anomaly / (2 * math.pi)) *
                sols_per_martian_year + perihelion_sol) % sols_per_martian_year


def datetime_to_earthdatetime(dt: datetime.datetime) -> EarthDateTime:
    """Convert a datetime to an EarthDateTime.

    Parameters
    ----------
    dt
        Any datetime.

    Raises
    ------
    TypeError
        Raised if the input is not a datetime.datetime.

    Examples
    --------
    Make an EarthDateTime from a known date.

    >>> import datetime, mer
    >>> print(datetime_to_earthdatetime(datetime.datetime(2020, 1, 1, 0, 0, 0)))
    2020-01-01 00:00:00+00:00

    Make an EarthDateTime from the start of Mars year 0.

    >>> print(datetime_to_earthdatetime(mer.mars_year_0_start))
    1953-05-24 11:57:07.200011+00:00

    """
    try:
        return EarthDateTime(dt.year, dt.month, dt.day, dt.hour, dt.minute,
                             dt.second, dt.microsecond,
                             tzinfo=dt.tzinfo) if dt.tzinfo is not None else \
            EarthDateTime(dt.year, dt.month, dt.day, dt.hour, dt.minute,
                          dt.second, dt.microsecond)
    except AttributeError as attribute_error:
        message = 'dt must be a datetime.datetime'
        raise TypeError(message) from attribute_error


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
    >>> maven_arrival_datetime = datetime.datetime(2014, 9, 2, 2, 24, 0, 0)
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
    >>> opportunity_start = datetime.datetime(2004, 1, 25, 0, 0, 0, 0)
    >>> opportunity_end = datetime.datetime(2018, 6, 10, 0, 0, 0, 0)
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
