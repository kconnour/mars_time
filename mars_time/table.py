import datetime

mars_year_starting_datetime: dict = {
    0: datetime.datetime(1953, 5, 24),
    1: datetime.datetime(1955, 4, 11),
    2: datetime.datetime(1957, 2, 26),
    3: datetime.datetime(1959, 1, 14),
    4: datetime.datetime(1960, 12, 1),
    5: datetime.datetime(1962, 10, 19),
    6: datetime.datetime(1964, 9, 5),
    7: datetime.datetime(1966, 7, 24),
    8: datetime.datetime(1968, 6, 10),
    9: datetime.datetime(1970, 4, 28),

    10: datetime.datetime(1972, 3, 15),
    11: datetime.datetime(1974, 1, 31),
    12: datetime.datetime(1975, 12, 19),
    13: datetime.datetime(1977, 11, 5),
    14: datetime.datetime(1979, 9, 23),
    15: datetime.datetime(1981, 8, 10),
    16: datetime.datetime(1983, 6, 28),
    17: datetime.datetime(1985, 5, 15),
    18: datetime.datetime(1987, 4, 1),
    19: datetime.datetime(1989, 2, 16),

    20: datetime.datetime(1991, 1, 4),
    21: datetime.datetime(1992, 11, 21),
    22: datetime.datetime(1994, 10, 9),
    23: datetime.datetime(1996, 8, 26),
    24: datetime.datetime(1998, 7, 14),
    25: datetime.datetime(2000, 5, 31),
    26: datetime.datetime(2002, 4, 18),
    27: datetime.datetime(2004, 3, 5),
    28: datetime.datetime(2006, 1, 21),
    29: datetime.datetime(2007, 12, 9),

    30: datetime.datetime(2009, 10, 26),
    31: datetime.datetime(2011, 9, 13),
    32: datetime.datetime(2013, 7, 31),
    33: datetime.datetime(2015, 6, 18),
    34: datetime.datetime(2017, 5, 5),
    35: datetime.datetime(2019, 3, 23),
    36: datetime.datetime(2021, 2, 7),
    37: datetime.datetime(2022, 12, 26),
    38: datetime.datetime(2024, 11, 12),
    39: datetime.datetime(2026, 9, 30),

    40: datetime.datetime(2028, 8, 17),
    41: datetime.datetime(2030, 7, 5),
    42: datetime.datetime(2032, 5, 22),
    43: datetime.datetime(2034, 4, 9),
    44: datetime.datetime(2036, 2, 25),
    45: datetime.datetime(2038, 1, 12),
    46: datetime.datetime(2039, 11, 30),
    47: datetime.datetime(2041, 10, 17),
    48: datetime.datetime(2043, 9, 4),
    49: datetime.datetime(2045, 7, 22),
}
"""Catalog of values denoting the start datetimes of Martian years. This table is from `Piqueux et al (2015) 
<https://doi.org/10.1016/j.icarus.2014.12.014>`_."""

mars_year_starting_j2000: dict = {
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
"""Catalog of values denoting the start of Martian years in days since J2000. This table is from `Piqueux et al (2015) 
<https://doi.org/10.1016/j.icarus.2014.12.014>`_."""


if __name__ == '__main__':
    for i in range(50):
        print(mars_year_starting_datetime[i], datetime.datetime(2000, 1, 1, 12) + datetime.timedelta(days=mars_year_starting_j2000[i]))
