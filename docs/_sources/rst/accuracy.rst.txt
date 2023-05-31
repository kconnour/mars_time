Accuracy
========
Mars' orbit varies significantly with time and thus any attempt to accurately
convert between Earth and Mars times can only really be accurate within a narrow
time window. Most of the conversions found in this package are based on
`dynamical calculations <https://doi.org/10.1016/j.icarus.2014.12.014>`_ and are
accurate between the years of 1607 (the first Mars year observed by Galilleo)
and 2141 (the start of Mars year 100---an arbitrary cutoff date).

This package makes a few assumptions, for better or worse:

* The length of a sol is constant, but the length of a Mars year is not
  constant. Other planets perturb Mars' orbit such that the length of the year
  can vary by several hours from year to year. Assuming a constant length of a
  year can lead to significant errors over time.
* There is a way to generically convert Ls to sol. This is not really possible,
  as there are a different number of sols per Martian year. Nevertheless, I
  use an equation that can approximate this value. I hope to make a more
  accurate function in a future update that includes the Mars year and thus can
  potentially be more accurate.

Therefore I recommend you use this package as a *generally* accurate
time converter---not a *supremely* accurate time converter. If you know of a way
to perform more accurate calculations, please
`raise an issue <https://github.com/kconnour/mars_time/issues>`_ to help improve
this package.

SPICE
-----
I have no idea how accurate this package is compared to SPICE computations of
solar longitude. If you have some knowledge on this topic, feel free to contact
me!
