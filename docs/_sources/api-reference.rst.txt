API reference
=============
The mer package supplies classes and functions for converting between different
time representations.

Constants
---------
.. automodule:: mer.constants

Note that these can be accessed via the :code:`constants` module (as shown)
or used directly from mer's namespace.

.. autodata:: mer.constants.mars_year_0_start
.. autodata:: mer.constants.martian_sol_length
.. autodata:: mer.constants.orbital_eccentricity
.. autodata:: mer.constants.perihelion_sol
.. autodata:: mer.constants.seconds_per_sol
.. autodata:: mer.constants.sols_per_martian_year

Available types
---------------

EarthDatetime
*************
.. autoclass:: mer.EarthDateTime
   :members:
   :member-order: bysource

MarsYearSol
***********
.. autoclass:: mer.MarsYearSol
   :members:
   :member-order: bysource

MarsYearSolarLongitude
**********************
.. autoclass:: mer.MarsYearSolarLongitude
   :members:
   :member-order: bysource

Miscellaneous functions
-----------------------
A collection of functions for helping during time conversions.

datetime_to_earthdatetime
*************************
.. autofunction:: mer.datetime_to_earthdatetime

sols_after_mars_year_0
**********************
.. autofunction:: mer.sols_after_mars_year_0

sols_between_datetimes
**********************
.. autofunction:: mer.sols_between_datetimes

sols_since_datetime
*******************
.. autofunction:: mer.sols_since_datetime
