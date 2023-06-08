API Reference
=============
.. currentmodule:: mars_time

This page describes the mars_time API, where the API is grouped by functionality. Many docstrings contain practical
example code.

Data types
----------
:code:`MarsTime` is the primary data type of this package and represents a year and sol on Mars.
:code:`MarsTimeDelta` can be used in conjunction with :code:`MarsTime` to create new instances of :code:`MarsTime`.
These may be useful on their own, but are probably most beneficial for attribute extraction and computation.

.. autosummary::
   :toctree: generated/

   MarsTime
   MarsTimeDelta

Conversion functions
--------------------
These function help converting between :code:`MarsTime` and
`datetime <https://docs.python.org/3/library/datetime.html>`_ objects.

.. autosummary::
   :toctree: generated/

   datetime_to_marstime
   marstime_to_datetime
   get_current_marstime

Orbital positions
-----------------
These function help for finding special points in an orbit

.. autosummary::
   :toctree: generated/

   find_aphelion
   find_perihelion

Constants
---------
These constants are related to the orbit of Mars and/or timekeeping on Mars.

True constants
**************
These are true constants.

.. currentmodule:: mars_time.constants

.. autosummary::
   :toctree: generated/

   mars_year_start_days_since_j2000
   j2000
   seconds_per_day
   seconds_per_sol
   hours_per_sol


Orbital constants
*****************
These are computed constants about the Martian orbit.

.. autosummary::
   :toctree: generated/

   aphelion_sol
   aphelion_solar_longitude
   perihelion_sol
   perihelion_solar_longitude
   northern_spring_equinox_sol
   northern_summer_solstice_sol
   northern_autumn_equinox_sol
   northern_winter_solstice_sol
   sols_per_year

Functional constants
********************
These are functions that apply mathematical operations to constants to express them in a different representation.

.. autosummary::
   :toctree: generated/

   mars_year_starting_datetimes
   sols_per_mars_year