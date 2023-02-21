Release Notes
=============

v0.4.0
------
This is a significant overhaul to try to create a more Pythonic API while
keeping the same functionality.

* Renamed the package from mer to mars_time to avoid confusion with the Mars
  Exploration Rovers
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
