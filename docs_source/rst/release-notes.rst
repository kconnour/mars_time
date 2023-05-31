Release Notes
=============
These describe the "beta" state of the project. Since any API changes will break
links, these may be removed with v1.0.0. My idea is that they will look more
like numpy's after that point.

v0.5.0
------
This update expands upon the constants in the previous version and adds an
additional attribute to ``MarsTime``.

* Added attribute :attr:`mars_time.MarsTime.solar_longitude`
* Removed :data:`mars_time.mars_year_starting_datetime`. This is replaced with
  :func:`mars_time.mars_year_starting_datetimes` which goes from year -99 to 100.
  This improved the accuracy of the computations
* Added tests to :func:`mars_time.get_current_mars_time`
* Modified the __str__ of :class:`mars_time.MarsTime` and
  :class:`mars_time.MarsTimeDelta` to truncate at 2 decimals
* Added classmethod to :class:`mars_time.MarsTime` to create that class from Ls
* Added improved Ls computation function to :class:`mars_time.MarsTime`

With the addition of more accurate Mars year starting datetimes, the computation
of the solar longitude is now more accurate.

v0.4.0
------
This update overhauls the previous API in favor of a more Pythonic API that's
similar to the datetime API, while largely keeping the same functionality.

* Renamed the package from ``mer`` to ``mars_time`` in order to avoid confusion
  with the Mars Exploration Rovers
* Removed entire previous API, with the exception of some constants
* Added :class:`mars_time.MarsTime`
* Added :class:`mars_time.MarsTimeDelta`
* Added :func:`mars_time.datetime_to_mars_time`
* Added :func:`mars_time.mars_time_to_datetime`
* Added :func:`mars_time.get_current_mars_time`
* Added :func:`mars_time.solar_longitude_to_sol`
* Added :func:`mars_time.sol_to_solar_longitude`
* Added several constants from LMD.
* Added incomplete table of Mars year starting times
* Improved documentation for these classes and function

v0.3.0
------
This update adds additional objects that can convert between each other.

* Added classes: ``MarsYearSol``, ``MarsYearSolarLongitude``
* Added functions: ``datetime_to_earthdatetime``
* Added constants: ``orbital_eccentricity``, ``perihelion_sol``

v0.2.0
------
This update adds an object for converting from an Earth datetime.

* Added classes: ``EarthDateTime``
* Added functions: ``mars_year_to_datetime``, ``sols_between_datetimes``,
  ``sols_since_datetime``

These functions are more appropriately named functions and contain the same
functionality as before. Other functions are wrapped into ``EarthDateTime``.

v0.1.0
------
This update adds constants along with functions for converting between different
times.

* Added functions: ``convert_to_solar_longitude``,
  ``convert_to_fractional_mars_year``, ``convert_to_whole_mars_year``,
  ``convert_to_sol_number``, ``sols_between_dates``, ``sols_since_date``,
  ``sols_after_mars_year_0``
* Added constants: ``martian_sol_length``, ``seconds_per_sol``,
  ``sols_per_martian_year``, ``date_of_start_of_mars_year_0``
