Examples
========

These are examples of questions that can be answered by this package and
practical uses of this package.

Opportunity length
------------------
How long was the Opportunity rover in operation?

.. code-block:: python

   import datetime
   import mars_time

   start = datetime_to_mars_time(datetime.datetime(2004, 1, 25, 5, 5, 0))
   end = datetime_to_mars_time(datetime.datetime(2018, 6, 12, 0, 0, 0))
   print(f'{(end-start).sols:.1f}')

This gives 5111.3, consistent with the Wikipedia page.

Perseverance ice halo
---------------------
At what solar longitude did Lemmon *et al* (2022) find water-ice halos, given
that they mention "A water-ice halo was unambiguously visible on sol 292
(of Perseverance's life)..."

.. code-block:: python

   import datetime
   import mars_time

   landing_date = datetime.datetime(2021, 2, 18, 20, 55, 0)
   landing_time = datetime_to_mars_time(landing_date)
   detection_time = landing_time + MarsTimeDelta(sol=292)
   print(f'{sol_to_solar_longitude(detection_time.sol):.2f}')

This gives 142.49, consistent with the values in the paper.
