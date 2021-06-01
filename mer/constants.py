import datetime


date_of_start_of_mars_year_0: datetime.datetime = \
    datetime.datetime(1953, 5, 24, 11, 57, 7, 200011)
"""Time of the start of Mars year 0. This value comes from `this article
<https://doi.org/10.1016/j.icarus.2014.12.014>`_."""

martian_sol_length: float = 24.6597
"""Length of a Martian sol [hours]. This value comes from the `Mars fact sheet
<https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html>`_."""

seconds_per_sol: float = martian_sol_length / 24 * 86400
"""Number of seconds per Martian sol."""

sols_per_martian_year: float = 686.973 * 24 / martian_sol_length
"""Number of sols per Martian year."""
