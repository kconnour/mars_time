"""The retimers module contains tools to convert between different time representations."""
import datetime
import math

from mars_time.constants import mars_year_0_start, orbital_eccentricity, perihelion_sol, seconds_per_sol, \
    sols_per_martian_year


class MarsTime:
    """A MarsTime object represents a Mars time and is in many ways analogous to a datetime.datetime() object. Objects
    of this type are immutable.

    Parameters
    ----------
    year
        The Martian year. Can be any value that can be cast to an int.
    sol
        The sol (day of the Martian year). Must be between 0 and ~668.

    Raises
    ------
    TypeError
        Raised if any of the inputs cannot be cast to their assumed type.

    ValueError
        Raised if :code:`sol` is not in its valid range.

    Examples
    --------
    Create an instance of this class.

    >>> import mars_time
    >>> mt = mars_time.MarsTime(30, 0)
    >>> mt
    MarsTime(year=30, sol=0.0)

    You can add time deltas to this object or subtract time deltas from this object.

    >>> dt = mars_time.MarsTimeDelta(sol=700)
    >>> mt + dt
    MarsTime(year=31, sol=31.405004927067353)

    Note that the resultant sol is "ugly" because I assume there aren't an integer number of sols/year.

    """
    def __init__(self, year: int, sol: float):
        self._year = self._validate_year(year)
        self._sol = self._validate_sol(sol)

    @property
    def year(self):
        """Get the year of this object.

        Returns
        -------
        The Martian year.

        """
        return self._year

    @property
    def sol(self):
        """Get the sol of this object.

        Returns
        -------
        The sol.

        """
        return self._sol

    @staticmethod
    def _validate_year(year):
        try:
            return int(year)
        except TypeError as te:
            message = 'The year cannot be converted to an int.'
            raise TypeError(message) from te
        except ValueError as ve:
            message = 'The year cannot be converted to an int.'
            raise ValueError(message) from ve

    @staticmethod
    def _validate_sol(sol):
        try:
            sol = float(sol)
        except TypeError as te:
            message = 'The sol cannot be converted to a float.'
            raise TypeError(message) from te
        except ValueError as ve:
            message = 'The sol cannot be converted to a float.'
            raise ValueError(message) from ve
        if 0 <= sol <= sols_per_martian_year:
            return sol
        else:
            message = f'The sol must be between 0 and {sols_per_martian_year:.2f}.'
            raise ValueError(message)

    def __str__(self):
        return f'MarsTime(year={self.year}, sol={self.sol})'

    def __repr__(self):
        return f'{self}'

    def __add__(self, other):
        if not isinstance(other, MarsTimeDelta):
            message = f'Cannot add f{type(other)} to MarsTime.'
            raise TypeError(message)
        year = self.year + other.year + int((self.sol + other.sol) // sols_per_martian_year)
        sol = (self.sol + other.sol) % sols_per_martian_year
        return MarsTime(year, sol)

    def __sub__(self, other):
        # TODO: add ability for mars_time - mars_time = mars_time_delta
        if not isinstance(other, MarsTimeDelta):
            message = f'Cannot add f{type(other)} to MarsTime.'
            raise TypeError(message)
        year = self.year - other.year + int((self.sol - other.sol) // sols_per_martian_year)
        sol = (self.sol - other.sol) % sols_per_martian_year
        return MarsTime(year, sol)

    def __eq__(self, other):
        if not isinstance(other, MarsTime):
            return False
        else:
            return self.year == other.year and self.sol == other.sol


class MarsTimeDelta:
    """A MarsTimeDelta object represents the difference between Mars times.

    Parameters
    ----------
    year
        The difference in Mars years. Must be non-negative.
    sol
        The difference in sols. Must be non-negative.

    Raises
    ------
    TypeError
        Raised if any of the inputs cannot be cast to their assumed type.

    ValueError
        Raised if either :code:`year` or :code:`sol` is negative.

    """
    def __init__(self, year: int = 0, sol: float = 0):
        self._year = self._validate_year(year)
        self._sol = self._validate_sol(sol)

    @property
    def year(self):
        return self._year

    @property
    def sol(self):
        return self._sol

    @staticmethod
    def _validate_year(year):
        try:
            year = int(year)
        except TypeError as te:
            message = 'The year cannot be converted to an int.'
            raise TypeError(message) from te
        except ValueError as ve:
            message = 'The year cannot be converted to an int.'
            raise ValueError(message) from ve
        if year >= 0:
            return year
        else:
            message = 'year must be non-negative.'
            raise ValueError(message)

    @staticmethod
    def _validate_sol(sol):
        try:
            sol = float(sol)
        except TypeError as te:
            message = 'The sol cannot be converted to a float.'
            raise TypeError(message) from te
        except ValueError as ve:
            message = 'The sol cannot be converted to a float.'
            raise ValueError(message) from ve
        if sol >= 0:
            return sol
        else:
            message = 'sol must be non-negative.'
            raise ValueError(message)

    def __str__(self):
        return f'MarsTimeDelta(year={self.year}, sol={self.sol})'


def datetime_to_mars_time(dt: datetime.datetime) -> MarsTime:
    """Convert a datetime to a MarsTime.

    Parameters
    ----------
    dt
        Any datetime. If it has no timezone info, this will assume the timezone is UTC.

    Returns
    -------
    The MarsTime associated with the input datetime.

    Examples
    --------
    Turn a generic datetime into a Mars time

    >>> import mars_time, datetime
    >>> random_time = datetime.datetime(2020, 1, 1, 0, 0, 0)
    >>> datetime_to_mars_time(random_time)
    MarsTime(year=35, sol=275.8641742510148)

    Get the Mars time when the Perseverance rover landed.

    >>> datetime_to_mars_time(mars_time.rovers.perseverance_landing_date)
    MarsTime(year=36, sol=11.042001502225048)

    """
    try:
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.timezone.utc)
        time_delta = dt - mars_year_0_start
        elapsed_seconds = time_delta.days * 60*60*24 + time_delta.seconds
        elapsed_sols = elapsed_seconds / seconds_per_sol
        return MarsTime(0, 0) + MarsTimeDelta(sol=elapsed_sols)
    except TypeError as te:
        message = 'The input must be a datetime.'
        raise TypeError(message) from te


def mars_time_to_datetime(mt: MarsTime) -> datetime.datetime:
    """Convert a MarsTime to a datetime.

    Parameters
    ----------
    mt
        Any mars_time.

    Returns
    -------
    The datetime associated with the input MarsTime.

    Examples
    --------
    Find the UTC time that corresponds to the start of Mars year 30.

    >>> import mars_time
    >>> mars_time.mars_time_to_datetime(mars_time.MarsTime(30, 0))
    datetime.datetime(2009, 10, 26, 16, 30, 43, 200011, tzinfo=datetime.timezone.utc)

    """
    try:
        elapsed_sols = mt.year * sols_per_martian_year + mt.sol
        elapsed_seconds = elapsed_sols * seconds_per_sol
        return mars_year_0_start + datetime.timedelta(seconds=elapsed_seconds)
    except TypeError as te:
        message = 'The input must be a mars_time.'
        raise TypeError(message) from te


def get_current_mars_time() -> MarsTime:
    """Get the current MarsTime.

    Returns
    -------
    The MarsTime.

    """
    return datetime_to_mars_time(datetime.datetime.now(tz=datetime.timezone.utc))


def solar_longitude_to_sol(solar_longitude: float) -> float:
    """Convert solar longitude to sol.

    Parameters
    ----------
    solar_longitude
        The solar longitude.

    Returns
    -------
    The sol corresponding to the input solar longitude.

    Notes
    -----
    This equation comes from LMD but should be more accurate.

    Examples
    --------
    Determine the sol corresponding to solar longitude 180. The "official" LMD calendar gives 371.99.

    >>> import mars_time
    >>> mars_time.solar_longitude_to_sol(180)
    371.8584911665763

    """
    # 1.90... is: 2*Pi*(1-Ls(perihelion)/360); Ls(perihelion)=250.99 according to the LMD converter code
    true_anomaly = solar_longitude * math.pi / 180 + 1.90258341759902
    eccentric_anomaly = 2 * math.atan(math.tan(0.5 * true_anomaly) /
                                      math.sqrt((1 + orbital_eccentricity) /
                                                (1 - orbital_eccentricity)))
    mean_anomaly = eccentric_anomaly - orbital_eccentricity * math.sin(eccentric_anomaly)
    return (mean_anomaly / (2 * math.pi) * sols_per_martian_year + perihelion_sol) % sols_per_martian_year


def sol_to_solar_longitude(sol: float):
    """Convert sol to solar longitude.

    Parameters
    ----------
    sol
        The sol number.

    Returns
    -------
    The solar longitude corresponding to the input sol.

    Notes
    -----
    The equation used in this method can be found in `this paper <https://doi.org/10.1016/j.icarus.2014.12.014>`_. While
    this paper claims the equation is accurate to within 0.05\ :math:`^\circ`, I have found errors up to
    0.2\ :math:`^\circ`.

    Examples
    --------
    Determine the solar longitude of sol 200. The "official" LMD document gives 92.965.

    >>> import mars_time
    >>> mars_time.sol_to_solar_longitude(200)
    93.0250805781161

    """
    dt = mars_time_to_datetime(MarsTime(0, sol))
    utc = datetime.timezone.utc
    j2000 = datetime.datetime(2000, 1, 1, 12, 0, 0, 0, tzinfo=utc)
    elapsed_days = (dt - j2000).total_seconds() / 86400
    m = math.radians(19.38095 + 0.524020769 * elapsed_days)
    ls = 270.38859 + \
        0.524038542 * elapsed_days + \
        10.67848 * math.sin(m) + \
        0.62077 * math.sin(2*m) + \
        0.05031 * math.sin(3*m)
    return ls % 360
