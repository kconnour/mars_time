"""The constants module is a collection of Martian orbital and temporal constants."""
import datetime


mars_year_0_start: datetime.datetime = datetime.datetime(1953, 5, 24, 11, 57, 7, 200011, tzinfo=datetime.timezone.utc)
"""Time of the start of Mars year 0. This value comes from `Piqueux *et al* 2015 
<https://doi.org/10.1016/j.icarus.2014.12.014>`_."""

hours_per_sol: float = 24.6597
"""Length of a Martian sol [hours]. This value comes from `NASA's Mars fact sheet
<https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html>`_."""

seconds_per_sol: float = hours_per_sol / 24 * 86400
"""Number of seconds per Martian sol."""

sols_per_martian_year: float = 686.973 * 24 / hours_per_sol
"""Number of sols per Martian year. This value is derived from `NASA's Mars fact sheet
<https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html>`_."""

northern_spring_equinox_sol: float = 0
"""The sol of the northern spring equinox (solar longitude = 0 degrees). This values comes from the LMD calendar."""

northern_summer_solstice_sol: float = 193.47
"""The sol of the northern summer solstice (solar longitude = 90 degrees). This values comes from the LMD calendar."""

northern_autumn_equinox_sol: float = 371.99
"""The sol of the northern autumn equinox (solar longitude = 180 degrees). This values comes from the LMD calendar."""

northern_winter_solstice_sol: float = 514.76
"""The sol of the northern winter solstice (solar longitude = 270 degrees). This values comes from the LMD calendar."""

# TODO: add aphelion_sol. LMD didn't give me this number.

perihelion_sol: float = 485.35
"""Sol of perihelion. This values comes from LMD."""

orbital_eccentricity: float = 0.0935
"""Mars' orbital eccentricity. This value comes from `NASA's Mars fact sheet
<https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html>`_."""
