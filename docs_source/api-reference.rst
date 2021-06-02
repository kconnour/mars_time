API reference
=============
You can find all functions present in the package at this page.

Earth times to Mars times
*************************
These are a series of functions to convert Earth datetime objects into Martian
times.

datetime_to_fractional_mars_year
--------------------------------
.. autofunction:: mer.datetime_to_fractional_mars_year

datetime_to_whole_mars_year
---------------------------
.. autofunction:: mer.datetime_to_whole_mars_year

datetime_to_sol
---------------
.. autofunction:: mer.datetime_to_sol

datetime_to_solar_longitude
---------------------------
.. autofunction:: mer.datetime_to_solar_longitude

sols_between_datetimes
----------------------
.. autofunction:: mer.sols_between_datetimes

sols_since_datetime
-------------------
.. autofunction:: mer.sols_since_datetime

sols_after_mars_year_0
----------------------
.. autofunction:: mer.sols_after_mars_year_0

Mars times to Earth times
*************************
.. automodule:: mer.mars_to_earth

mars_year_to_datetime
---------------------
.. autofunction:: mer.mars_year_to_datetime

Constants
*********
.. automodule:: mer.constants

Note that these can be accessed via the :code:`constants` module (as shown)
or used directly from mer's namespace.

.. autodata:: mer.constants.date_of_start_of_mars_year_0
.. autodata:: mer.constants.martian_sol_length
.. autodata:: mer.constants.seconds_per_sol
.. autodata:: mer.constants.sols_per_martian_year
