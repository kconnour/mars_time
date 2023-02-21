"""The retimers module contains tools to convert between different time representations."""
import datetime
import math

from mars_time.constants import mars_year_0_start, orbital_eccentricity, perihelion_sol, seconds_per_sol, \
    sols_per_martian_year


class MarsTime:
    """A MarsTime represents the year and sol on Mars.

    In many ways, a MarsTime is analogous to a datetime.datetime. Objects of this type are immutable.

    Parameters
    ----------
    year
        The Martian year. Can be any value that can be cast to an int.
    sol
        The sol (day of the Martian year). Must be between 0 and ~668.

    Raises
    ------
    TypeError
        Raised if either of the inputs are a type that cannot be cast to a numeric data type.
    ValueError
        Raised if either of the inputs are a value that cannot be cast to a numeric data type or if :code:`sol` is
        outside its valid range.

    Examples
    --------
    Create an instance of this class.

    >>> import mars_time
    >>> mt = mars_time.MarsTime(30, 0)
    >>> mt
    MarsTime(year=30, sol=0.0)

    You can add a MarsTimeDelta to this object. Note that the resultant sol is "ugly" because I assume there aren't an
    integer number of sols/year.

    >>> dt = mars_time.MarsTimeDelta(sol=700)
    >>> mt + dt
    MarsTime(year=31, sol=31.405004927067417)

    You can also subtract MarsTimeDeltas from this object.

    >>> dt = mars_time.MarsTimeDelta(sol=700)
    >>> mt - dt
    MarsTime(year=28, sol=637.1899901458652)

    The difference between two MarsTime objects is a MarsTimeDelta:

    >>> MarsTime(33, 0) - MarsTime(32, 400)
    MarsTimeDelta(year=1.0, sol=-400.0)

    """
    def __init__(self, year: int, sol: float):
        self._year = self._validate_year(year)
        self._sol = self._validate_sol(sol)

    @staticmethod
    def _validate_year(year) -> int:
        try:
            return int(year)
        except TypeError as te:
            message = f'The year argument (type={type(year)}) cannot be converted to an int.'
            raise TypeError(message) from te
        except ValueError as ve:
            message = f'The year argument (value={year}) cannot be converted to an int.'
            raise ValueError(message) from ve

    @staticmethod
    def _validate_sol(sol) -> float:
        try:
            sol = float(sol)
        except TypeError as te:
            message = f'The sol argument (type={type(sol)}) cannot be converted to a float.'
            raise TypeError(message) from te
        except ValueError as ve:
            message = f'The sol argument (value={sol}) cannot be converted to a float.'
            raise ValueError(message) from ve
        if 0 <= sol <= sols_per_martian_year:
            return sol
        else:
            message = f'The sol must be between 0 and {sols_per_martian_year:.2f}.'
            raise ValueError(message)

    @property
    def year(self) -> int:
        """Get the input year.

        Returns
        -------
        The Martian year.

        """
        return self._year

    @property
    def sol(self) -> float:
        """Get the input sol.

        Returns
        -------
        The sol.

        """
        return self._sol

    def __str__(self):
        return f'MarsTime(year={self.year}, sol={self.sol})'

    def __repr__(self):
        return f'{self}'

    def __add__(self, other):
        if isinstance(other, MarsTimeDelta):
            new_fractional_year = self.year + self.sol / sols_per_martian_year + other.years
            year = int(new_fractional_year // 1)
            sol = (new_fractional_year % 1) * sols_per_martian_year
            return MarsTime(year, sol)
        else:
            raise TypeError(f'Cannot add f{type(other)} to MarsTime.')

    def __sub__(self, other):
        if isinstance(other, MarsTimeDelta):
            new_fractional_year = self.year + self.sol / sols_per_martian_year - other.years
            year = int(new_fractional_year // 1)
            sol = (new_fractional_year % 1) * sols_per_martian_year
            return MarsTime(year, sol)
        elif isinstance(other, MarsTime):
            return MarsTimeDelta(year=self.year-other.year, sol=self.sol-other.sol)
        else:
            raise TypeError(f'Cannot subtract f{type(other)} from MarsTime.')

    def __eq__(self, other):
        if not isinstance(other, MarsTime):
            return False
        else:
            return self.year == other.year and self.sol == other.sol


class MarsTimeDelta:
    """A MarsTimeDelta represents the difference in years and sols on Mars.

    In many ways, a MarsTimeDelta is analogous to a datetime.timedelta. Objects of this type are immutable.

    Parameters
    ----------
    year
        The difference in Mars years.
    sol
        The difference in sols.

    Raises
    ------
    TypeError
        Raised if either of the inputs are a type that cannot be cast to a numeric data type.
    ValueError
        Raised if either input cannot be converted to a float.

    Examples
    --------
    Create an instance of this class.

    >>> import mars_time
    >>> mars_time.MarsTimeDelta(year=1, sol=50)
    MarsTimeDelta(year=1.0, sol=50.0)

    Adding or subtracting a MarsTimeDelta to or from this object results in another MarsTimeDelta.

    >>> mtd = mars_time.MarsTimeDelta(year=1, sol=50) + mars_time.MarsTimeDelta(sol=700)
    >>> mtd
    MarsTimeDelta(year=1.0, sol=750.0)

    The native year and aggregate year difference are found in its attributes. The same is true for sols.

    >>> mtd.year, mtd.sol
    (1.0, 750.0)
    >>> mtd.years, mtd.sols
    (2.1217553309955415, 1418.5949950729328)

    """
    def __init__(self, year: float = 0, sol: float = 0):
        self._year = self._validate_year(year)
        self._sol = self._validate_sol(sol)

    @staticmethod
    def _validate_year(year):
        try:
            return float(year)
        except TypeError as te:
            message = f'The year argument (type={type(year)}) cannot be converted to a float.'
            raise TypeError(message) from te
        except ValueError as ve:
            message = f'The year argument (value={year}) cannot be converted to a float.'
            raise ValueError(message) from ve

    @staticmethod
    def _validate_sol(sol):
        try:
            return float(sol)
        except TypeError as te:
            message = f'The sol argument (type={type(sol)}) cannot be converted to a float.'
            raise TypeError(message) from te
        except ValueError as ve:
            message = f'The sol argument (value={sol}) cannot be converted to a float.'
            raise ValueError(message) from ve

    @property
    def year(self) -> float:
        """Get the input year.

        Returns
        -------
        The year.

        """
        return self._year

    @property
    def years(self) -> float:
        """Get the fractional number of Mars years this object represents.

        Returns
        -------
        The fractional Mars years.

        """
        return self._year + self._sol / sols_per_martian_year

    @property
    def sol(self) -> float:
        """Get the input sol.

        Returns
        -------
        The sol.

        """
        return self._sol

    @property
    def sols(self) -> float:
        """Get the total number of sols that this object represents.

        Returns
        -------
        The total number of sols.

        """
        return self._sol + self._year * sols_per_martian_year

    def __str__(self):
        return f'MarsTimeDelta(year={self.year}, sol={self.sol})'

    def __repr__(self):
        return f'{self}'

    def __add__(self, other):
        if isinstance(other, MarsTimeDelta):
            year = self.year + other.year
            sol = self.sol + other.sol
            return MarsTimeDelta(year=year, sol=sol)
        else:
            message = f'Cannot add f{type(other)} to MarsTimeDelta.'
            raise TypeError(message)

    def __sub__(self, other):
        if isinstance(other, MarsTimeDelta):
            year = self.year - other.year
            sol = self.sol - other.sol
            return MarsTimeDelta(year=year, sol=sol)
        else:
            message = f'Cannot subtract f{type(other)} from MarsTimeDelta.'
            raise TypeError(message)

    def __eq__(self, other):
        if not isinstance(other, MarsTimeDelta):
            return False
        else:
            return self.year == other.year and self.sol == other.sol


def datetime_to_mars_time(dt: datetime.datetime) -> MarsTime:
    """Convert a datetime.datetime to a MarsTime.

    Parameters
    ----------
    dt: datetime.datetime
        Any datetime.datetime. If it has no timezone info, this will assume the timezone is UTC.

    Returns
    -------
    MarsTime
        The MarsTime associated with the input datetime.datetime.

    Raises
    ------
    TypeError
        Raised if the input is not a datetime.datetime.

    Examples
    --------
    Get the Mars time when MAVEN arrived at Mars (date taken from Wikipedia).

    >>> import mars_time, datetime
    >>> orbit_insertion = datetime.datetime(2014, 9, 22, 2, 24, 0)
    >>> datetime_to_mars_time(orbit_insertion)
    MarsTime(year=32, sol=406.2978778240522)

    Get the Mars time when the Perseverance rover landed (date taken from Wikipedia).

    >>> landing_date = datetime.datetime(2021, 2, 18, 20, 55, 0)
    >>> datetime_to_mars_time(landing_date)
    MarsTime(year=36, sol=11.0420015022269)

    """
    try:
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.timezone.utc)
        time_delta = dt - mars_year_0_start
        elapsed_seconds = time_delta.days * 60*60*24 + time_delta.seconds
        elapsed_sols = elapsed_seconds / seconds_per_sol
        return MarsTime(0, 0) + MarsTimeDelta(sol=elapsed_sols)
    except AttributeError as ae:
        message = 'The input must be a datetime.datetime() object.'
        raise TypeError(message) from ae


def mars_time_to_datetime(mt: MarsTime) -> datetime.datetime:
    """Convert a MarsTime to a datetime.datetime.

    Parameters
    ----------
    mt: MarsTime
        Any MarsTime.

    Returns
    -------
    datetime.datetime
        The datetime associated with the input MarsTime.

    Raises
    ------
    TypeError
        Raised if the input is not a MarsTime.

    Examples
    --------
    Find the UTC time that corresponds to the start of Mars year 30.

    >>> import mars_time
    >>> mars_time.mars_time_to_datetime(mars_time.MarsTime(30, 0))
    datetime.datetime(2009, 10, 26, 16, 30, 43, 200011, tzinfo=datetime.timezone.utc)

    """
    if isinstance(mt, MarsTimeDelta):
        raise TypeError('The input must be a MarsTime.')
    try:
        elapsed_sols = mt.year * sols_per_martian_year + mt.sol
        elapsed_seconds = elapsed_sols * seconds_per_sol
        return mars_year_0_start + datetime.timedelta(seconds=elapsed_seconds)
    except AttributeError as te:
        raise TypeError('The input must be a MarsTime.') from te


def get_current_mars_time() -> MarsTime:
    """Get the current MarsTime.

    Returns
    -------
    MarsTime
        The current MarsTime.

    """
    return datetime_to_mars_time(datetime.datetime.now(tz=datetime.timezone.utc))


def solar_longitude_to_sol(solar_longitude: float) -> float:
    """Convert solar longitude to sol.

    Parameters
    ----------
    solar_longitude: float
        The solar longitude.

    Returns
    -------
    float
        The sol corresponding to the input solar longitude.

    Raises
    ------
    TypeError
        Raised if the input cannot be cast to a float.
    ValueError
        Raised if the input is not numeric.

    Notes
    -----
    This equation comes from LMD.

    Examples
    --------
    Determine the sol corresponding to solar longitude 180. The "official" LMD calendar gives 371.99.

    >>> import mars_time
    >>> mars_time.solar_longitude_to_sol(180)
    371.8584911665763

    """
    try:
        solar_longitude = float(solar_longitude)
    except TypeError as te:
        raise TypeError('solar_longitude must be a type that can be cast to a float.') from te
    except ValueError as ve:
        raise ValueError('solar_longitude must be numeric') from ve

    # 1.90... is: 2*Pi*(1-Ls(perihelion)/360); Ls(perihelion)=250.99 according to the LMD converter code
    true_anomaly = solar_longitude * math.pi / 180 + 1.90258341759902
    eccentric_anomaly = 2 * math.atan(math.tan(0.5 * true_anomaly) /
                                      math.sqrt((1 + orbital_eccentricity) /
                                                (1 - orbital_eccentricity)))
    mean_anomaly = eccentric_anomaly - orbital_eccentricity * math.sin(eccentric_anomaly)
    return (mean_anomaly / (2 * math.pi) * sols_per_martian_year + perihelion_sol) % sols_per_martian_year


def sol_to_solar_longitude(sol: float) -> float:
    """Convert sol to solar longitude.

    Parameters
    ----------
    sol: float
        The sol number.

    Returns
    -------
    float
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
    try:
        sol = float(sol)
    except TypeError as te:
        raise TypeError('sol must be a type that can be cast to a float.') from te
    except ValueError as ve:
        raise ValueError('sol must be numeric') from ve

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


if __name__ == '__main__':
    s = solar_longitude_to_sol(182)
    m = MarsTime(34, s)
    print(mars_time_to_datetime(m))