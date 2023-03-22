"""The constants module is a collection of Martian orbital and temporal constants."""
import datetime


def mars_year_starting_datetimes() -> dict:
    """Get the catalog of datetimes denoting the start of Martian years. This is computed from the table from
    `Piqueux et al (2015) <https://doi.org/10.1016/j.icarus.2014.12.014>`_.

    Returns
    -------
    The datetimes of the start of each Martian year.

    """
    mars_year_start = {
        -3: -19093.920,
        -2: -18396.940,
        -1: -17709.980,

        0: -17023.002,
        1: -16336.050,
        2: -15649.090,
        3: -14962.090,
        4: -14275.110,
        5: -13588.160,
        6: -12901.180,
        7: -12214.210,
        8: -11527.270,
        9: -10840.290,

        10: -10153.300,
        11: -9466.317,
        12: -8779.349,
        13: -8092.373,
        14: -7405.432,
        15: -6718.466,
        16: -6031.469,
        17: -5344.497,
        18: -4657.544,
        19: -3970.550,

        20: -3283.590,
        21: -2596.642,
        22: -1909.654,
        23: -1222.672,
        24: -535.714,
        25: 151.264,
        26: 838.229,
        27: 1525.176,
        28: 2212.173,
        29: 2899.166,

        30: 3586.124,
        31: 4273.090,
        32: 4960.070,
        33: 5647.012,
        34: 6333.979,
        35: 7020.971,
        36: 7707.956,
        37: 8394.918,
        38: 9081.896,
        39: 9768.843,

        40: 10455.797,
        41: 11142.793,
        42: 11829.774,
        43: 12516.727,
        44: 13203.716,
        45: 13890.691,
        46: 14577.634,
        47: 15264.618,
        48: 15951.609,
        49: 16638.569,
    }
    for year in mars_year_start.keys():
        mars_year_start[year] = datetime.datetime(2000, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc) + \
                                datetime.timedelta(days=mars_year_start[year])
    return mars_year_start


hours_per_sol: float = 24.6597
"""Length of a Martian sol [hours]. This value comes from `NASA's Mars fact sheet
<https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html>`_."""

seconds_per_sol: float = hours_per_sol / 24 * 86400
"""Number of seconds per Martian sol."""

sols_per_martian_year: float = 686.973 * 24 / hours_per_sol
"""Number of sols per Martian year. This value is derived from `NASA's Mars fact sheet
<https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html>`_."""

northern_spring_equinox_sol: float = 0
"""The sol of the northern spring equinox (solar longitude = 0\ :math:`^\circ`). 
This values comes from the LMD calendar."""

northern_summer_solstice_sol: float = 193.47
"""The sol of the northern summer solstice (solar longitude = 90\ :math:`^\circ`). 
This values comes from the LMD calendar."""

northern_autumn_equinox_sol: float = 371.99
"""The sol of the northern autumn equinox (solar longitude = 180\ :math:`^\circ`). 
This values comes from the LMD calendar."""

northern_winter_solstice_sol: float = 514.76
"""The sol of the northern winter solstice (solar longitude = 270\ :math:`^\circ`). 
This values comes from the LMD calendar."""

# TODO: add aphelion_sol. LMD didn't give me this number.

perihelion_sol: float = 485.35
"""Sol of perihelion. This values comes from LMD."""

orbital_eccentricity: float = 0.0935
"""Mars' orbital eccentricity. This value comes from `NASA's Mars fact sheet
<https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html>`_."""
