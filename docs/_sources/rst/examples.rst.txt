Examples
========

These are examples of practical uses of this package.

Start of a global dust storm
----------------------------
When was the start of the 2018 global dust storm?
`Sanchez-Lavega et al (2019)
<https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2019GL083207>`_
simply mention they first saw it expanding on 2018-05-30.

.. code-block:: python

   import datetime
   import mars_time

   start = mars_time.datetime_to_mars_time(datetime.datetime(2018, 5, 30))
   print(start.year, f'{start.sol:.0f}', f'{start.solar_longitude:.0f}')

This gives Mars year 34, sol 379, and a solar longitude 184 degrees.

Opportunity length
------------------
How long was the Opportunity rover in operation? `Wikipedia's Opportunity page
<https://en.wikipedia.org/wiki/Opportunity_(rover)>`_ says it landed on
2004-01-25 at 05:05 UTC and entered hibernation on 2018-06-12.

.. code-block:: python

   import datetime
   import mars_time

   start = mars_time.datetime_to_mars_time(datetime.datetime(2004, 1, 25, 5, 5, 0))
   end = mars_time.datetime_to_mars_time(datetime.datetime(2018, 6, 12, 0, 0, 0))
   print(f'{(end-start).sols:.1f}')

This gives 5111.3, consistent with the Wikipedia page.

Season of the halo
------------------
At what solar longitude did `Lemmon et al (2022)
<https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2022GL099776>`_
find water-ice halos?
They mention "A water-ice halo was unambiguously visible on sol 292
(of Perseverance's life)..." and `Wikipedia's Perseverance page
<https://en.wikipedia.org/wiki/Perseverance_(rover)>`_ mentions the Perseverance
rover successfully landed on 2021-02-18 at 20:55 UTC.

.. code-block:: python

   import datetime
   import mars_time

   landing_time = mars_time.datetime_to_mars_time(datetime.datetime(2021, 2, 18, 20, 55, 0))
   detection_time = landing_time + mars_time.MarsTimeDelta(sol=292)
   print(f'{sol_to_solar_longitude(detection_time.sol):.1f}')

This gives 142.5, consistent with the values in the paper.
