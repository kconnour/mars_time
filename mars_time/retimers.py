"""The retimers module contains tools to convert between different time representations."""
from __future__ import annotations
import datetime
import math
import click

import scipy

from mars_time.constants import j2000, seconds_per_day, seconds_per_sol, mars_year_start_days_since_j2000, \
    mars_year_starting_datetimes, sols_per_mars_year, sols_per_year


class MarsTime:
    """A ``MarsTime`` represents the year and sol on Mars.

    In many ways, a ``MarsTime`` is analogous to a ``datetime.datetime``. As with ``datetime.datetime``, instances of
    this class may be most useful for attribute extraction.

    Parameters
    ----------
    year
        The Martian year. Must be between -99 and 99.
    sol
        The sol (day of the Martian year). Must be between 0 and ~668 (it varies by Martian year).

    Raises
    ------
    TypeError
        Raised if either of the inputs are a type that cannot be cast to a numeric data type.
    ValueError
        Raised if either of the inputs are a value that cannot be cast to a numeric data type or if :code:`sol` is
        outside its valid range for the input year.

    See Also
    --------
    MarsTimeDelta: For adding time differences to this class.

    Notes
    -----
    Objects of this type are immutable.

    Examples
    --------
    Create an instance of this class from a given Mars year and sol.

    >>> import mars_time
    >>> mt = mars_time.MarsTime(30, 0)
    >>> mt
    MarsTime(year=30, sol=0.00)

    Alternatively, you can create an instance of this class from a Mars year and solar longitude.

    >>> mars_time.MarsTime.from_solar_longitude(year=33, solar_longitude=180)
    MarsTime(year=33, sol=371.92)

    You can add a :class:`~mars_time.MarsTimeDelta` to this object. Note that the resultant sol is "ugly" because I
    assume there aren't an integer number of sols per year.

    >>> dt = mars_time.MarsTimeDelta(sol=700)
    >>> mt + dt
    MarsTime(year=31, sol=31.41)

    You can also subtract a :class:`~mars_time.MarsTimeDelta` from this object.

    >>> mt - dt
    MarsTime(year=28, sol=637.19)

    The difference between two ``MarsTime`` objects is a :class:`~mars_time.MarsTimeDelta`.

    >>> MarsTime(33, 0) - MarsTime(32, 400)
    MarsTimeDelta(year=1, sol=-400.00)

    You can extract the input year and sol from this object via its properties. You can also extract the solar longitude
    corresponding to the input sol.

    >>> mt = MarsTime(33, 200)
    >>> mt.year, mt.sol, f'{mt.solar_longitude:.1f}'
    (33, 200.0, '93.1')

    """
    def __init__(self, year: int, sol: float):
        self._year = self._validate_year(year)
        self._sol = self._validate_sol(sol)

    @staticmethod
    def _validate_year(year) -> int:
        try:
            year = int(year)
        except TypeError as te:
            message = f'The year argument (type={type(year)}) cannot be converted to an int.'
            raise TypeError(message) from te
        except ValueError as ve:
            message = f'The year argument (value={year}) cannot be converted to an int.'
            raise ValueError(message) from ve
        if -99 <= year <= 99:
            return year
        else:
            message = 'The year must be between -99 and 99.'
            raise ValueError(message)

    def _validate_sol(self, sol) -> float:
        try:
            sol = float(sol)
        except TypeError as te:
            message = f'The sol argument (type={type(sol)}) cannot be converted to a float.'
            raise TypeError(message) from te
        except ValueError as ve:
            message = f'The sol argument (value={sol}) cannot be converted to a float.'
            raise ValueError(message) from ve
        sols_per_current_mars_year = sols_per_mars_year()[self.year]
        if 0 <= sol <= sols_per_current_mars_year:
            return sol
        else:
            message = f'The sol must be between 0 and ~{sols_per_current_mars_year:.2f}.'
            raise ValueError(message)

    @classmethod
    def from_solar_longitude(cls, year: int, solar_longitude: float) -> MarsTime:
        """Create an instance of this class from a solar longitude instead of a sol.

        Parameters
        ----------
        year
            The Martian year. Must be between -99 and 99.
        solar_longitude
            The solar longitude. Can be any value between 0 and 360.

        Returns
        -------
        An instance of this class.

        Examples
        --------
        Create an instance of this class from a solar longitude.

        >>> import mars_time
        >>> mt = MarsTime.from_solar_longitude(33, 10)
        >>> mt
        MarsTime(year=33, sol=19.80)

        """
        def find_ls(day):
            day = float(day)
            pre_target_ls = datetime_to_marstime(j2000 + datetime.timedelta(days=day - 0.001))
            post_target_ls = datetime_to_marstime(j2000 + datetime.timedelta(days=day + 0.001))
            return abs(2 * solar_longitude - pre_target_ls.solar_longitude - post_target_ls.solar_longitude)

        bounds = (mars_year_start_days_since_j2000[year], mars_year_start_days_since_j2000[year + 1])
        days = scipy.optimize.minimize_scalar(find_ls, method='bounded', bounds=bounds).x
        return datetime_to_marstime(j2000 + datetime.timedelta(days=days))

    @property
    def year(self) -> int:
        """Get the input Mars year.

        Returns
        -------
        The Mars year.

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

    @property
    def solar_longitude(self) -> float:
        r"""Get the solar longitude corresponding to the input Mars time.

        Returns
        -------
        The solar longitude.

        Notes
        -----
        The equation used to compute this value comes from `Piqueux et al (2015)
        <https://doi.org/10.1016/j.icarus.2014.12.014>`_. According to the paper, it has a maximum error of 0.0045
        :math:`^\circ` with RMS residual of 0.00105 :math:`^\circ`.
        """
        # The paper took a few liberties that they failed to mention... I only figured them out by going to the IDL
        # source code.
        # 1. the mean anomaly has to be in the range [-180, 180) after the equation given in the paper
        # 2. Then the mean anomaly has to be converted to radians
        # 3. The output has to be %360'd

        # It might be beastly, but I suspect I could invert this equation to turn a Mars year + Ls into a datetime.
        # If so, I could make certain aspects more accurate. But that's a project for a later time.

        dt = marstime_to_datetime(self)
        days_since_j2000 = (dt - j2000).total_seconds() / seconds_per_day

        julian_centuries = days_since_j2000 / 36525
        linear_rate_angle = 270.389001822 + 0.52403850205 * days_since_j2000 - 0.000565452 * julian_centuries ** 2
        mean_anomaly = (19.38028331517 + 0.52402076345 * days_since_j2000) % 360
        if mean_anomaly > 180:
            mean_anomaly -= 360
        mean_anomaly = mean_anomaly * math.pi / 180
        eccentricity = 0.093402202 + 0.000091406 * julian_centuries
        delta = (2 * eccentricity - eccentricity ** 3 / 4 + 5 * eccentricity ** 5 / 96) * math.sin(mean_anomaly) + \
                (5 * eccentricity ** 2 / 4 - 11 * eccentricity ** 4 / 24 + 17 * eccentricity ** 6 / 192) * math.sin(2 * mean_anomaly) + \
                (13 * eccentricity ** 3 / 12 - 43 * eccentricity ** 5 / 64) * math.sin(3 * mean_anomaly) + \
                (103 * eccentricity ** 4 / 96 - 451 * eccentricity ** 6 / 480) * math.sin(4 * mean_anomaly) + \
                (1097 * eccentricity ** 5 / 960) * math.sin(5 * mean_anomaly) + \
                (1223 * eccentricity ** 5 / 960) * math.sin(6 * mean_anomaly)

        def compute_planetary_perturbation(amplitude, period, phase):
            return amplitude / 1000 * math.cos(2 * math.pi * days_since_j2000 / period + math.pi / 180 * phase)

        planetary_perturbation = compute_planetary_perturbation(7.0591, 816.3755210, 48.48944) + \
            compute_planetary_perturbation(6.0890, 1005.8002614, 167.55418) + \
            compute_planetary_perturbation(4.4462, 408.1877605, 188.35480) + \
            compute_planetary_perturbation(3.8947, 5765.3098103, 19.97295) + \
            compute_planetary_perturbation(2.4328, 779.9286472, 12.03224) + \
            compute_planetary_perturbation(2.0400, 901.9431281, 95.98253) + \
            compute_planetary_perturbation(1.7746, 11980.9332471, 49.00256) + \
            compute_planetary_perturbation(1.34607, 2882.1147, 288.7737) + \
            compute_planetary_perturbation(1.03438, 4332.2204, 37.9378) + \
            compute_planetary_perturbation(0.88180, 373.07883, 65.3160) + \
            compute_planetary_perturbation(0.72350, 1069.3231, 175.4911) + \
            compute_planetary_perturbation(0.65555, 343.49194, 98.8644) + \
            compute_planetary_perturbation(0.81460, 1309.9410, 186.2253) + \
            compute_planetary_perturbation(0.74578, 450.69255, 202.9323) + \
            compute_planetary_perturbation(0.58359, 256.06036, 212.1853) + \
            compute_planetary_perturbation(0.42864, 228.99145, 32.1227)

        return (linear_rate_angle + 180 / math.pi * delta + planetary_perturbation) % 360

    def __str__(self):
        return f'MarsTime(year={self.year}, sol={self.sol:.2f})'

    def __repr__(self):
        return f'{self}'

    def __add__(self, other):
        if isinstance(other, MarsTimeDelta):
            sols_per_martian_year = sols_per_mars_year()
            new_year = self.year + other.year
            total_sol = self.sol + other.sol
            if total_sol >= 0:
                while total_sol >= sols_per_martian_year[new_year]:
                    total_sol -= sols_per_martian_year[new_year]
                    new_year += 1
            else:
                while total_sol < 0:
                    new_year -= 1
                    total_sol += sols_per_martian_year[new_year]

            return MarsTime(new_year, total_sol)
        else:
            raise TypeError(f'Cannot add f{type(other)} to MarsTime.')

    def __sub__(self, other):
        if isinstance(other, MarsTimeDelta):
            reversed_time = MarsTimeDelta(other.year * -1, other.sol * -1)
            return self + reversed_time

        elif isinstance(other, MarsTime):
            return MarsTimeDelta(year=self.year-other.year, sol=self.sol-other.sol)
        else:
            raise TypeError(f'Cannot subtract f{type(other)} from MarsTime.')

    def __eq__(self, other):
        if not isinstance(other, MarsTime):
            return False
        else:
            return self.year == other.year and self.sol == other.sol
        
    def __gt__(self, other):
        if not isinstance(other, MarsTime):
            return False
        else:
            if self.year == other.year:
                return self.sol > other.sol
            else:
                return self.year > other.year

    def __ge__(self, other):
        if not isinstance(other, MarsTime):
            return False
        else:
            if self.year == other.year:
                return self.sol >= other.sol
            else:
                return self.year > other.year
    


class MarsTimeDelta:
    """A ``MarsTimeDelta`` represents a generic change in time on Mars.

    Parameters
    ----------
    year
        Some amount of Mars years.
    sol
        Some amount of sols.

    Raises
    ------
    TypeError
        Raised if either of the inputs are a type that cannot be cast to a numeric data type.
    ValueError
        Raised if either input cannot be converted to its prefered type.

    See Also
    --------
    MarsTime: Create new Mars times from these time deltas.

    Notes
    -----
    Objects of this type are immutable.

    Examples
    --------
    Create an instance of this class.

    >>> import mars_time
    >>> mars_time.MarsTimeDelta(year=1, sol=50)
    MarsTimeDelta(year=1, sol=50.00)

    Adding or subtracting a ``MarsTimeDelta`` to or from this object results in another ``MarsTimeDelta``.

    >>> mtd = mars_time.MarsTimeDelta(year=1, sol=50) + mars_time.MarsTimeDelta(sol=700)
    >>> mtd
    MarsTimeDelta(year=1, sol=750.00)

    """
    def __init__(self, year: int = 0, sol: float = 0):
        self._year = self._validate_year(year)
        self._sol = self._validate_sol(sol)

    @staticmethod
    def _validate_year(year):
        try:
            return int(year)
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
    def year(self) -> int:
        """Get the input number of Mars years.

        Returns
        -------
        The number of Mars years.

        """
        return self._year

    @property
    def sol(self) -> float:
        """Get the input number of sol.

        Returns
        -------
        The number of sols.

        """
        return self._sol

    @property
    def sols(self) -> float:
        """Get the approximate number of sols that this object represents.

        Returns
        -------
        The total number of sols.

        Notes
        -----
        This can only be an approximation, as the number of sols per Mars year varies from year to year.

        """
        return self.year * sols_per_year + self.sol

    def __str__(self):
        return f'MarsTimeDelta(year={self.year}, sol={self.sol:.2f})'

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


class ClickMarsTime(click.ParamType):
    """
    Converts string of type MY{XX}Ls{YYY} or MY{XX}Sol{YYY} to
    MarsTime type
    """

    name = "marstime"

    def convert(self, value, param, ctx):
        if isinstance(value, MarsTime):
            return value
        if "Sol" in value:
            my = int(value.split("Sol")[0].split("MY")[1])
            sol = float(value.split("Sol")[1])
            return MarsTime(my, sol)
        elif "Ls" in value:
            my = int(value.split("Ls")[0].split("MY")[1])
            ls = float(value.split("Ls")[1])
            return MarsTime.from_solar_longitude(my, ls)
        else:
            self.fail(f"{value!r} is not a valid Mars Date string", param, ctx)



def datetime_to_marstime(dt: datetime.datetime) -> MarsTime:
    """Convert a ``datetime.datetime`` to a ``MarsTime``.

    Parameters
    ----------
    dt: datetime.datetime
        A datetime.datetime between Mars year -99 and 99. If it has no timezone info, this will assume the timezone is
        UTC.

    Returns
    -------
    MarsTime
        The MarsTime associated with the input datetime.datetime.

    Examples
    --------
    Get the Mars time when MAVEN arrived at Mars. `Wikipedia's MAVEN page
    <https://en.wikipedia.org/wiki/MAVEN>`_ mentions the spacecraft successfully entered orbit on 2014-09-22 at
    02:24 UTC.

    >>> import mars_time, datetime
    >>> orbit_insertion = datetime.datetime(2014, 9, 22, 2, 24, 0)
    >>> datetime_to_marstime(orbit_insertion)
    MarsTime(year=32, sol=406.36)

    Get the Mars time when the Perseverance rover landed. `Wikipedia's Perseverance page
    <https://en.wikipedia.org/wiki/Perseverance_(rover)>`_ mentions the rover successfully landed on 2021-02-18 at
    20:55 UTC.

    >>> landing_date = datetime.datetime(2021, 2, 18, 20, 55, 0)
    >>> datetime_to_marstime(landing_date)
    MarsTime(year=36, sol=11.11)

    """
    start = mars_year_starting_datetimes()
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    tabulated_mars_years = list(start.keys())
    seconds_between_datetime_and_mars_year_starts = [(dt - start[i]).total_seconds() for i in tabulated_mars_years]
    mars_year, elapsed_seconds = [[tabulated_mars_years[year_idx], elapsed_seconds] for year_idx, elapsed_seconds
                                  in enumerate(seconds_between_datetime_and_mars_year_starts) if elapsed_seconds >= 0][-1]
    return MarsTime(mars_year, 0) + MarsTimeDelta(sol=elapsed_seconds / seconds_per_sol)


def marstime_to_datetime(mt: MarsTime) -> datetime.datetime:
    """Convert a ``MarsTime`` to a ``datetime``.

    Parameters
    ----------
    mt: MarsTime
        Any MarsTime.

    Returns
    -------
    datetime.datetime
        The datetime associated with the input MarsTime.

    Examples
    --------
    Find the UTC time that corresponds to the start of Mars year 30.

    >>> import mars_time
    >>> mars_time.marstime_to_datetime(mars_time.MarsTime(30, 0))
    datetime.datetime(2009, 10, 26, 14, 58, 33, 600000, tzinfo=datetime.timezone.utc)

    """
    starting_datetime = mars_year_starting_datetimes()[mt.year]
    elapsed_seconds = mt.sol * seconds_per_sol
    return starting_datetime + datetime.timedelta(seconds=elapsed_seconds)


def get_current_marstime() -> MarsTime:
    """Get the current time on Mars.

    Returns
    -------
    MarsTime
        The current time on Mars.

    """
    return datetime_to_marstime(datetime.datetime.now(tz=datetime.timezone.utc))
