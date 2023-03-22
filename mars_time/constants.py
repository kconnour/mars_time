"""The constants module is a collection of Martian orbital and temporal constants."""
import datetime


def mars_year_starting_datetimes() -> dict:
    """Get the catalog of datetimes denoting the start of Martian years. This is computed from the table from
    `Piqueux et al (2015) <https://doi.org/10.1016/j.icarus.2014.12.014>`_.

    Returns
    -------
    The datetimes of the start of each Martian year.

    Examples
    --------
    Get the start of Mars year 33.

    >>> import mars_time
    >>> mars_time.mars_year_starting_datetimes()[33]
    datetime.datetime(2015, 6, 18, 12, 17, 16, 800000, tzinfo=datetime.timezone.utc)

    """
    mars_year_start = {
        # TODO: the table starts at MY -184 so I could conceivably add those

        -9: -23205.740,
        -8: -22518.780,
        -7: -21831.820,
        -6: -21144.820,
        -5: -20457.870,
        -4: -19770.910,
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

        50: 17325.539,
        51: 18012.511,
        52: 18699.451,
        53: 19386.438,
        54: 20073.435,
        55: 20760.397,
        56: 21447.355,
        57: 22134.338,
        58: 22821.286,
        59: 23508.242,

        60: 24195.234,
        61: 24882.228,
        62: 25569.193,
        63: 26256.173,
        64: 26943.131,
        65: 27630.078,
        66: 28317.068,
        67: 29004.055,
        68: 29691.009,
        69: 30377.985,

        70: 31064.971,
        71: 31751.911,
        72: 32438.882,
        73: 33125.875,
        74: 33812.839,
        75: 34499.801,
        76: 35186.780,
        77: 35873.724,
        78: 36560.703,
        79: 37247.706,

        80: 37934.680,
        81: 38621.635,
        82: 39308.617,
        83: 39995.576,
        84: 40682.523,
        85: 41369.510,
        86: 42056.507,
        87: 42743.474,
        88: 43430.445,
        89: 44117.411,

        90: 44804.349,
        91: 45491.328,
        92: 46178.320,
        93: 46865.281,
        94: 47552.248,
        95: 48239.246,
        96: 48926.192,
        97: 49613.155,
        98: 50300.150,
        99: 50987.124,

        100: 51674.083
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
r"""The sol of the northern spring equinox (solar longitude = 0\ :math:`^\circ`). 
This values comes from the LMD calendar."""

northern_summer_solstice_sol: float = 193.47
r"""The sol of the northern summer solstice (solar longitude = 90\ :math:`^\circ`). 
This values comes from the LMD calendar."""

northern_autumn_equinox_sol: float = 371.99
r"""The sol of the northern autumn equinox (solar longitude = 180\ :math:`^\circ`). 
This values comes from the LMD calendar."""

northern_winter_solstice_sol: float = 514.76
r"""The sol of the northern winter solstice (solar longitude = 270\ :math:`^\circ`). 
This values comes from the LMD calendar."""

# TODO: add aphelion_sol. LMD didn't give me this number.

perihelion_sol: float = 485.35
"""Sol of perihelion. This values comes from LMD."""

orbital_eccentricity: float = 0.0935
"""Mars' orbital eccentricity. This value comes from `NASA's Mars fact sheet
<https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html>`_."""
