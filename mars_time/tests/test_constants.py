import datetime

import numpy as np

from mars_time.constants import mars_year_start_days_since_j2000, j2000, seconds_per_day, hours_per_sol, \
    seconds_per_sol, aphelion_sol, aphelion_solar_longitude, perihelion_sol, perihelion_solar_longitude, \
    northern_spring_equinox_sol, northern_summer_solstice_sol, northern_autumn_equinox_sol, \
    northern_winter_solstice_sol, mars_year_starting_datetimes, sols_per_mars_year
from mars_time.orbit import find_aphelion, find_perihelion
from mars_time.retimers import MarsTime


# TODO: Is it worthwhile to test a constant? I test the computations that go into constants below but not the copied
#  constants.

def test_aphelion_sol():
    def test_value_of_constant_matches_precomputed_value():
        sol = [find_aphelion(year).sol for year in range(-99, 100)]

        mean_sol = np.mean(sol)

        assert aphelion_sol == mean_sol

    test_value_of_constant_matches_precomputed_value()


def test_aphelion_solar_longitude():
    def test_value_of_constant_matches_precomputed_value():
        solar_longitude = [find_aphelion(year).solar_longitude for year in range(-99, 100)]

        mean_solar_longitude = np.mean(solar_longitude)

        assert aphelion_solar_longitude == mean_solar_longitude

    test_value_of_constant_matches_precomputed_value()


def test_perihelion_sol():
    def test_value_of_constant_matches_precomputed_value():
        sol = [find_perihelion(year).sol for year in range(-99, 100)]

        mean_sol = np.mean(sol)

        assert perihelion_sol == mean_sol

    test_value_of_constant_matches_precomputed_value()


def test_perihelion_solar_longitude():
    def test_value_of_constant_matches_precomputed_value():
        solar_longitude = [find_perihelion(year).solar_longitude for year in range(-99, 100)]

        mean_solar_longitude = np.mean(solar_longitude)

        assert perihelion_solar_longitude == mean_solar_longitude

    test_value_of_constant_matches_precomputed_value()


def test_northern_spring_equinox_sol():
    def test_value_of_constant_matches_precomputed_value():
        assert northern_spring_equinox_sol == 0

    test_value_of_constant_matches_precomputed_value()


def test_northern_summer_solstice_sol():
    def test_value_of_constant_matches_precomputed_value():
        sol = [MarsTime.from_solar_longitude(year, 90).sol for year in range(-99, 100)]

        mean_sol = np.mean(sol)

        assert northern_summer_solstice_sol == mean_sol

    test_value_of_constant_matches_precomputed_value()


def test_northern_autumn_equinox_sol():
    def test_value_of_constant_matches_precomputed_value():
        sol = [MarsTime.from_solar_longitude(year, 180).sol for year in range(-99, 100)]

        mean_sol = np.mean(sol)

        assert northern_autumn_equinox_sol == mean_sol

    test_value_of_constant_matches_precomputed_value()


def test_northern_winter_solstice_sol():
    def test_value_of_constant_matches_precomputed_value():
        sol = [MarsTime.from_solar_longitude(year, 270).sol for year in range(-99, 100)]

        mean_sol = np.mean(sol)

        assert northern_winter_solstice_sol == mean_sol

    test_value_of_constant_matches_precomputed_value()


def test_mars_year_starting_datetimes():
    def test_mars_year_negative_99_matches_tabulated_value():
        my_negative_99_date = datetime.date(1767, 3, 10)

        computed_datetimes = mars_year_starting_datetimes()

        assert computed_datetimes[-99].date() == my_negative_99_date

    def test_mars_year_0_matches_tabulated_value():
        my_0_date = datetime.date(1953, 5, 24)

        computed_datetimes = mars_year_starting_datetimes()

        assert computed_datetimes[0].date() == my_0_date

    def test_mars_year_100_matches_tabulated_value():
        my_100_date = datetime.date(2141, 6, 24)

        computed_datetimes = mars_year_starting_datetimes()

        assert computed_datetimes[100].date() == my_100_date

    test_mars_year_negative_99_matches_tabulated_value()
    test_mars_year_0_matches_tabulated_value()
    test_mars_year_100_matches_tabulated_value()


def test_sols_per_mars_year():
    def test_all_values_are_within_1_sol():
        sols_per_year = sols_per_mars_year()

        for year in sols_per_year.keys():
            assert 668 <= sols_per_year[year] <= 669

    test_all_values_are_within_1_sol()
