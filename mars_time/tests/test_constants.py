import datetime

import numpy as np

from mars_time.constants import mars_year_start_days_since_j2000, j2000, seconds_per_day, hours_per_sol, \
    seconds_per_sol, aphelion_sol, aphelion_solar_longitude, perihelion_sol, perihelion_solar_longitude, \
    northern_spring_equinox_sol, northern_summer_solstice_sol, northern_autumn_equinox_sol, \
    northern_winter_solstice_sol, mars_year_starting_datetimes, sols_per_mars_year
from mars_time.orbit import find_aphelion, find_perihelion
from mars_time.retimers import MarsTime

# I believe test for constants or functions should look like:
# def test_aphelion_sol():
#     def test_value_is_expected():
#          # the tests
#
# However, it appears pytest cannot do this and all tests have to be in a class

class Test_mars_year_start_days_since_j2000:
    def test_value_matches_expected_value(self):
        assert mars_year_start_days_since_j2000 == {
            -99: -85033.149,
            -98: -84346.147,
            -97: -83659.157,
            -96: -82972.202,
            -95: -82285.232,
            -94: -81598.256,
            -93: -80911.313,
            -92: -80224.337,
            -91: -79537.345,
            -90: -78850.365,

            -89: -78163.396,
            -88: -77476.419,
            -87: -76789.479,
            -86: -76102.520,
            -85: -75415.524,
            -84: -74728.550,
            -83: -74041.600,
            -82: -73354.610,
            -81: -72667.640,
            -80: -71980.690,

            -79: -71293.710,
            -78: -70606.720,
            -77: -69919.760,
            -76: -69232.790,
            -75: -68545.820,
            -74: -67858.880,
            -73: -67171.880,
            -72: -66484.880,
            -71: -65797.930,
            -70: -65110.960,

            -69: -64423.980,
            -68: -63737.040,
            -67: -63050.080,
            -66: -62363.090,
            -65: -61676.100,
            -64: -60989.140,
            -63: -60302.160,
            -62: -59615.210,
            -61: -58928.250,
            -60: -58241.260,

            -59: -57554.280,
            -58: -56867.320,
            -57: -56180.340,
            -56: -55493.360,
            -55: -54806.420,
            -54: -54119.440,
            -53: -53432.450,
            -52: -52745.490,
            -51: -52058.520,
            -50: -51371.550,

            -49: -50684.610,
            -48: -49997.630,
            -47: -49310.620,
            -46: -48623.660,
            -45: -47936.700,
            -44: -47249.720,
            -43: -46562.760,
            -42: -45875.810,
            -41: -45188.820,
            -40: -44501.830,

            -39: -43814.860,
            -38: -43127.880,
            -37: -42440.920,
            -36: -41753.980,
            -35: -41066.997,
            -34: -40380.010,
            -33: -39693.050,
            -32: -39006.090,
            -31: -38319.090,
            -30: -37632.150,

            -29: -36945.180,
            -28: -36258.190,
            -27: -35571.220,
            -26: -34884.260,
            -25: -34197.270,
            -24: -33510.330,
            -23: -32823.360,
            -22: -32136.350,
            -21: -31449.370,
            -20: -30762.420,

            -19: -30075.450,
            -18: -29388.490,
            -17: -28701.540,
            -16: -28014.560,
            -15: -27327.570,
            -14: -26640.590,
            -13: -25953.620,
            -12: -25266.650,
            -11: -24579.710,
            -10: -23892.740,

            -9: -23205.740,
            -8: -22518.780,
            -7: -21831.820,
            -6: -21144.820,
            -5: -20457.870,
            -4: -19770.910,
            -3: -19083.920,
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


class Test_j2000:
    def test_value_matches_expected_value(self):
        assert j2000 == datetime.datetime(2000, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)


class Test_seconds_per_day:
    def test_value_matches_expected_value(self):
        assert seconds_per_day == 86400


class Test_hours_per_sol:
    def test_value_matches_expected_value(self):
        assert hours_per_sol == 24.6597


class Test_seconds_per_sol:
    def test_value_matches_expected_value(self):
        assert seconds_per_sol == 88774.92000000001


class Test_aphelion_sol:
    def test_value_matches_computed_value(self):
        sol = [find_aphelion(year).sol for year in range(-99, 100)]

        mean_sol = np.mean(sol)

        assert aphelion_sol == mean_sol


class Test_aphelion_solar_longitude:
    def test_value_matches_computed_value(self):
        solar_longitude = [find_aphelion(year).solar_longitude for year in range(-99, 100)]

        mean_solar_longitude = np.mean(solar_longitude)

        assert aphelion_solar_longitude == mean_solar_longitude


class Test_perihelion_sol:
    def test_value_matches_computed_value(self):
        sol = [find_perihelion(year).sol for year in range(-99, 100)]

        mean_sol = np.mean(sol)

        assert perihelion_sol == mean_sol


class Test_perihelion_solar_longitude:
    def test_value_matches_computed_value(self):
        solar_longitude = [find_perihelion(year).solar_longitude for year in range(-99, 100)]

        mean_solar_longitude = np.mean(solar_longitude)

        assert perihelion_solar_longitude == mean_solar_longitude


class Test_northern_spring_equinox_sol:
    def test_value_matches_computed_value(self):
        assert northern_spring_equinox_sol == 0


class Test_northern_summer_solstice_sol:
    def test_value_matches_computed_value(self):
        sol = [MarsTime.from_solar_longitude(year, 90).sol for year in range(-99, 100)]

        mean_sol = np.mean(sol)

        assert northern_summer_solstice_sol == mean_sol


class Test_northern_autumn_equinox_sol:
    def test_value_matches_computed_value(self):
        sol = [MarsTime.from_solar_longitude(year, 180).sol for year in range(-99, 100)]

        mean_sol = np.mean(sol)

        assert northern_autumn_equinox_sol == mean_sol


class Test_northern_winter_solstice_sol:
    def test_value_matches_computed_value(self):
        sol = [MarsTime.from_solar_longitude(year, 270).sol for year in range(-99, 100)]

        mean_sol = np.mean(sol)

        assert northern_winter_solstice_sol == mean_sol


class Test_mars_year_starting_datetimes:
    def test_select_values_match_tabuled_values(self):
        expected_dates = {-99: datetime.date(1767, 3, 10),
                          0: datetime.date(1953, 5, 24),
                          100: datetime.date(2141, 6, 24)}

        computed_datetimes = mars_year_starting_datetimes()

        for year in expected_dates.keys():
            assert expected_dates[year] == computed_datetimes[year].date()


class Test_sols_per_mars_year:
    def test_values_are_plausible(self):
        sols_per_year = sols_per_mars_year()

        for year in sols_per_year.keys():
            assert 668 <= sols_per_year[year] <= 669
