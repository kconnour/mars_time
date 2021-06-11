API reference
=============
You can find all classes and functions present in the package at this page.
In general, all classes have methods to convert to all other time
representations.

EarthDatetime
-------------
.. autoclass:: mer.EarthDatetime
   :members:
   :member-order: bysource

Sol
---
.. autoclass:: mer.Sol
   :members:
   :member-order: bysource

SolarLongitude
--------------
.. autoclass:: mer.SolarLongitude
   :members:
   :member-order: bysource

sol differences
---------------
A collection of functions for converting sol differences.

sols_after_mars_year_0
**********************
.. autofunction:: mer.sols_after_mars_year_0

sols_between_datetimes
**********************
.. autofunction:: mer.sols_between_datetimes

sols_since_datetime
*******************
.. autofunction:: mer.sols_since_datetime

Constants
---------
.. automodule:: mer.constants

Note that these can be accessed via the :code:`constants` module (as shown)
or used directly from mer's namespace.

.. autodata:: mer.constants.mars_year_0_start
.. autodata:: mer.constants.martian_sol_length
.. autodata:: mer.constants.seconds_per_sol
.. autodata:: mer.constants.sols_per_martian_year
