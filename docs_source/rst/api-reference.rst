API Reference
=============

.. currentmodule:: mars_time

Data types
----------
:code:`MarsTime` is the primary data type of this library and represents a
year and sol on Mars. :code:`MarsTimeDelta` can be used in conjunction with
:code:`MarsTime` to create new instances of :code:`MarsTime`.

.. autosummary::
   :toctree: generated/

   MarsTime
   MarsTimeDelta

Convenience functions
---------------------
These function help converting between :code:`MarsTime` and
:code:`datetime.datetime`. There are also functions for converting between
sols and solar longitudes.

.. autosummary::
   :toctree: generated/

   datetime_to_mars_time
   mars_time_to_datetime
   get_current_mars_time
   solar_longitude_to_sol
   sol_to_solar_longitude

Orbital constants
-----------------
These constants are related to the orbit and/or timekeeping on Mars.

.. autosummary::
   :toctree: generated/

   constants.mars_year_0_start
   constants.martian_sol_length
   constants.orbital_eccentricity
   constants.perihelion_sol
   constants.seconds_per_sol
   constants.sols_per_martian_year

Rover constants
---------------
These constants are related to Martian rovers.

.. autosummary::
   :toctree: generated/

   rovers.opportunity_landing_date
   rovers.opportunity_last_contact_date
   rovers.perseverance_landing_date
