Examples
========

Perseverance detection
----------------------
From Lemmon et al (2022): "A water-ice halo was unambiguously visible on sol
292 (of Perseverance's life)...". What solar longitude was this?

.. code-block:: python

   import mars_time

   landing_date = mars_time.rovers.perseverance_landing_date
   landing_time = mars_time.datetime_to_mars_time(landing_date)
   detection_time = mars_time.MarsTimeDelta(sol=292)
   print(mars_time.sol_to_solar_longitude(detection_time.sol))

This gives about 142.49, consistent with the values in the paper.