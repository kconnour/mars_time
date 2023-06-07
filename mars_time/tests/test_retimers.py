import datetime
import math
from unittest import mock

import numpy as np
import pytest

from mars_time import MarsTime, MarsTimeDelta, datetime_to_mars_time, mars_time_to_datetime, get_current_mars_time, \
    mars_year_starting_datetimes, sols_per_mars_year


class TestMarsTime:
    def test_sol_0_raises_no_errors(self):
        MarsTime(0, 0)

    def test_sol_equal_sols_per_year_raises_no_error(self):
        mars_year_0_sols = sols_per_mars_year()[0]
        MarsTime(0, mars_year_0_sols)

    def test_two_identical_objects_are_equal(self):
        mt0 = MarsTime(0, 0)
        mt1 = MarsTime(0, 0)
        assert mt0 == mt1

    def test_adding_1_year_gives_expected_result(self):
        mt = MarsTime(0, 0)
        mtd = MarsTimeDelta(year=1)
        assert mt + mtd == MarsTime(1, 0)

    def test_subtracting_1_year_gives_expected_result(self):
        mt = MarsTime(0, 0)
        mtd = MarsTimeDelta(year=1)
        assert mt - mtd == MarsTime(-1, 0)

    def test_negative_mars_years_give_expected_result(self):
        mars_year_negative_11_sols = sols_per_mars_year()[-11]
        mars_time = MarsTime(-10, 0) - MarsTimeDelta(sol=200)
        assert mars_time.year == -11 and pytest.approx(mars_time.sol) == mars_year_negative_11_sols - 200

    def test_subtracting_mars_times_gives_expected_mars_time_delta(self):
        assert MarsTime(32, 0) - MarsTime(31, 0) == MarsTimeDelta(year=1)

    def test_list_year_raises_type_error(self):
        with pytest.raises(TypeError):
            MarsTime([0, 1], 0)

    def test_list_sol_raises_type_error(self):
        with pytest.raises(TypeError):
            MarsTime(0, [0, 1])

    def test_non_numeric_string_year_raises_value_error(self):
        with pytest.raises(ValueError):
            MarsTime('foo', 0)

    def test_non_numeric_string_sol_raises_value_error(self):
        with pytest.raises(ValueError):
            MarsTime(0, 'foo')

    def test_negative_sol_raises_value_error(self):
        with pytest.raises(ValueError):
            MarsTime(0, np.nextafter(0, -1))

    def test_sol_greater_than_sols_per_martian_year_raises_value_error(self):
        mars_year_0_sols = sols_per_mars_year()[0]
        with pytest.raises(ValueError):
            MarsTime(0, math.nextafter(mars_year_0_sols, 1000))

    def test_setting_year_raises_attribute_error(self):
        mt = MarsTime(0, 0)
        with pytest.raises(AttributeError):
            mt.year = 0

    def test_setting_sol_raises_attribute_error(self):
        mt = MarsTime(0, 0)
        with pytest.raises(AttributeError):
            mt.sol = 0

    def test_adding_two_mars_times_raises_type_error(self):
        with pytest.raises(TypeError):
            MarsTime(0, 0) + MarsTime(1, 0)

    def test_from_solar_longitude_returns_expected_result(self):
        mt = MarsTime.from_solar_longitude(32, 180)

        assert mt.year == 32
        assert pytest.approx(mt.sol, 0.01) == 371.88


class TestMarsTimeDelta:
    def test_year_only_input_raises_no_error(self):
        MarsTimeDelta(year=1)

    def test_sol_only_input_raises_no_error(self):
        MarsTimeDelta(sol=10)

    def test_non_numeric_string_year_raises_value_error(self):
        with pytest.raises(ValueError):
            MarsTimeDelta(year='foo', sol=0)

    def test_non_numeric_string_sol_raises_value_error(self):
        with pytest.raises(ValueError):
            MarsTimeDelta(year=0, sol='foo')

    def test_adding_mars_time_delta_returns_mars_time_delta(self):
        mtd = MarsTimeDelta(sol=5)
        assert isinstance(mtd + mtd, MarsTimeDelta)

    def test_two_identical_mars_time_deltas_are_equal(self):
        mtd0 = MarsTimeDelta(sol=5)
        mtd1 = MarsTimeDelta(sol=5)
        assert mtd0 == mtd1

    def test_setting_year_raises_attribute_error(self):
        mtd = MarsTimeDelta(0, 0)
        with pytest.raises(AttributeError):
            mtd.year = 0

    def test_setting_sol_raises_attribute_error(self):
        mtd = MarsTimeDelta(0, 0)
        with pytest.raises(AttributeError):
            mtd.sol = 0


def test_datetime_to_mars_time():
    def native_datetime() -> datetime.datetime:
        return datetime.datetime(2020, 1, 1, 0, 0, 0)

    def aware_datetime() -> datetime.datetime:
        return datetime.datetime(2020, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)

    def test_function_matches_tabulated_results():
        for year in mars_year_starting_datetimes().keys():
            if year == 100:
                continue
            computed_mars_year = datetime_to_mars_time(mars_year_starting_datetimes()[year])
            fractional_mars_year = computed_mars_year.year + computed_mars_year.sol / 668
            assert pytest.approx(fractional_mars_year, abs=1e-2) == year

    def test_native_and_utc_aware_datetimes_give_same_answer(native_datetime, aware_datetime):
        assert datetime_to_mars_time(native_datetime) == datetime_to_mars_time(aware_datetime)

    test_function_matches_tabulated_results()
    test_native_and_utc_aware_datetimes_give_same_answer(native_datetime(), aware_datetime())


def test_mars_time_to_datetime():
    def test_function_matches_tabulated_results():
        for year in mars_year_starting_datetimes().keys():
            if year == 100:
                continue
            tabulated_datetime = mars_year_starting_datetimes()[year]
            computed_datetime = mars_time_to_datetime(MarsTime(year, 0))
            assert computed_datetime.year == tabulated_datetime.year and \
                   computed_datetime.month == tabulated_datetime.month and \
                   computed_datetime.day == tabulated_datetime.day

    def test_this_function_is_inverse_of_datetime_to_mars_time():
        starting_mars_time = MarsTime(30, 0)
        dt = mars_time_to_datetime(starting_mars_time)
        new_mars_time = datetime_to_mars_time(dt)
        assert pytest.approx(new_mars_time.year) == 30 and pytest.approx(new_mars_time.sol, abs=1e-10) == 0

    test_function_matches_tabulated_results()
    test_this_function_is_inverse_of_datetime_to_mars_time()


def test_get_current_mars_time():
    def test_function_gives_expected_answer():
        with mock.patch('datetime.datetime', wraps=datetime.datetime) as dt:
            test_dt = datetime.datetime(2022, 1, 1)
            dt.now.return_value = test_dt
            assert get_current_mars_time() == datetime_to_mars_time(test_dt)

    test_function_gives_expected_answer()
