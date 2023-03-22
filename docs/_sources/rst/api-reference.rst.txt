API Reference
=============
.. currentmodule:: mars_time

This page describes the `mars_time` API, where the API is grouped by
functionality. Most docstrings contain practical example code.

Data types
----------
:code:`MarsTime` is the primary data type of this package and represents a
year and sol on Mars. :code:`MarsTimeDelta` can be used in conjunction with
:code:`MarsTime` to create new instances of :code:`MarsTime`. These may be
useful on their own, but as with the datetime module these are probably most
beneficial for attribute extraction.

.. autosummary::
   :toctree: generated/

   MarsTime
   MarsTimeDelta

Conversion functions
--------------------
These function help converting between :code:`MarsTime` and
:code:`datetime.datetime` objects. There are also functions for converting
between sols and solar longitudes.

.. autosummary::
   :toctree: generated/

   datetime_to_mars_time
   mars_time_to_datetime
   get_current_mars_time
   solar_longitude_to_sol
   sol_to_solar_longitude

Constants
---------
These constants are related to the orbit and/or timekeeping on Mars.

.. currentmodule:: mars_time.constants

.. autosummary::
   :toctree: generated/

   mars_year_starting_datetimes
   hours_per_sol
   seconds_per_sol
   sols_per_martian_year
   northern_spring_equinox_sol
   northern_summer_solstice_sol
   northern_autumn_equinox_sol
   northern_winter_solstice_sol
   perihelion_sol
   orbital_eccentricity
