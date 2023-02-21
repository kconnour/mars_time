import datetime
import math

import pytest

from mars_time import MarsTime, MarsTimeDelta, datetime_to_mars_time, mars_time_to_datetime, get_current_mars_time, \
    solar_longitude_to_sol, sol_to_solar_longitude, mars_year_0_start, sols_per_martian_year, \
    northern_spring_equinox_sol, northern_summer_solstice_sol, northern_autumn_equinox_sol, \
    northern_winter_solstice_sol, mars_year_starting_datetime


class TestMarsTime:
    def test_sol_0_raises_no_errors(self):
        MarsTime(0, 0)

    def test_sol_equal_sols_per_year_raises_no_error(self):
        MarsTime(0, sols_per_martian_year)

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
        mars_time = MarsTime(-10, 0) - MarsTimeDelta(sol=200)
        assert mars_time.year == -11 and pytest.approx(mars_time.sol) == sols_per_martian_year - 200

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
            MarsTime(0, math.nextafter(0, -1))

    def test_sol_greater_than_sols_per_martian_year_raises_value_error(self):
        with pytest.raises(ValueError):
            MarsTime(0, math.nextafter(sols_per_martian_year, 1000))

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


class TestMarsTimeDelta:
    def test_year_only_raises_no_error(self):
        MarsTimeDelta(year=1)

    def test_sol_only_raises_no_error(self):
        MarsTimeDelta(sol=10)

    def test_2_years_split_into_year_and_sol_gives_expected_properties(self):
        mtd = MarsTimeDelta(year=1, sol=sols_per_martian_year)
        assert mtd.year == 1 and mtd.years == 2 and mtd.sol == sols_per_martian_year and mtd.sols == 2 * sols_per_martian_year

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

    def test_setting_years_raises_attribute_error(self):
        mtd = MarsTimeDelta(0, 0)
        with pytest.raises(AttributeError):
            mtd.years = 0

    def test_setting_sol_raises_attribute_error(self):
        mtd = MarsTimeDelta(0, 0)
        with pytest.raises(AttributeError):
            mtd.sol = 0

    def test_setting_sols_raises_attribute_error(self):
        mtd = MarsTimeDelta(0, 0)
        with pytest.raises(AttributeError):
            mtd.sols = 0


class Test_datetime_to_mars_time:
    @pytest.fixture
    def native_datetime(self) -> datetime.datetime:
        yield datetime.datetime(2020, 1, 1, 0, 0, 0)

    @pytest.fixture
    def aware_datetime(self) -> datetime.datetime:
        yield datetime.datetime(2020, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)

    def test_function_matches_tabulated_results(self):
        for year in mars_year_starting_datetime:
            computed_mars_year = datetime_to_mars_time(mars_year_starting_datetime[year])
            fractional_mars_year = computed_mars_year.year + computed_mars_year.sol / sols_per_martian_year
            assert pytest.approx(fractional_mars_year, abs=1e-2) == year

    def test_native_and_utc_aware_datetimes_give_same_answer(self, native_datetime, aware_datetime):
        assert datetime_to_mars_time(native_datetime) == datetime_to_mars_time(aware_datetime)

    def test_string_raises_type_error(self):
        with pytest.raises(TypeError):
            datetime_to_mars_time('foo')


class Test_mars_time_to_datetime:
    def test_function_matches_tabulated_results(self):
        for year in mars_year_starting_datetime:
            tabulated_datetime = mars_year_starting_datetime[year]
            computed_datetime = mars_time_to_datetime(MarsTime(year, 0))
            assert computed_datetime.year == tabulated_datetime.year and \
                   computed_datetime.month == tabulated_datetime.month and \
                   computed_datetime.day == tabulated_datetime.day

    def test_this_function_is_inverse_of_datetime_to_mars_time(self):
        starting_mars_time = MarsTime(30, 0)
        dt = mars_time_to_datetime(starting_mars_time)
        new_mars_time = datetime_to_mars_time(dt)
        assert pytest.approx(new_mars_time.year) == 30 and pytest.approx(new_mars_time.sol, abs=1e-10) == 0

    def test_string_raises_type_error(self):
        with pytest.raises(TypeError):
            mars_time_to_datetime('foo')

    def test_mars_time_delta_raises_type_error(self):
        with pytest.raises(TypeError):
            mars_time_to_datetime(MarsTimeDelta(year=0, sol=0))


class Test_get_current_mars_time:
    # TODO: I don't know how to easily mock time.now() and it's not currently worth the effort
    pass


class Test_solar_longitude_to_sol:
    def test_northern_spring_quinox_sol_matches_lmd_result(self):
        assert solar_longitude_to_sol(0) == pytest.approx(northern_spring_equinox_sol + sols_per_martian_year, abs=0.5)

    def test_northern_summer_solstice_sol_matches_lmd_result(self):
        assert solar_longitude_to_sol(90) == pytest.approx(northern_summer_solstice_sol, abs=0.5)

    def test_northern_autumn_equinox_sol_matches_lmd_result(self):
        assert solar_longitude_to_sol(180) == pytest.approx(northern_autumn_equinox_sol, abs=0.5)

    def test_northern_winter_solstice_sol_matches_lmd_result(self):
        assert solar_longitude_to_sol(270) == pytest.approx(northern_winter_solstice_sol, abs=0.5)

    def test_unphysical_solar_longitude_is_cyclic(self):
        assert solar_longitude_to_sol(360+180) == solar_longitude_to_sol(180)

    def test_non_numeric_string_raises_value_error(self):
        with pytest.raises(ValueError):
            solar_longitude_to_sol('foo')

    def test_numeric_string_raises_no_errors(self):
        solar_longitude_to_sol('180')


class Test_sol_to_solar_longitude:
    def test_northern_spring_quinox_sol_matches_lmd_result(self):
        assert sol_to_solar_longitude(northern_spring_equinox_sol) == pytest.approx(360, abs=0.5)

    def test_northern_summer_solstice_sol_matches_lmd_result(self):
        assert sol_to_solar_longitude(northern_summer_solstice_sol) == pytest.approx(90, abs=0.5)

    def test_northern_autumn_equinox_sol_matches_lmd_result(self):
        assert sol_to_solar_longitude(northern_autumn_equinox_sol) == pytest.approx(180, abs=0.5)

    def test_northern_winter_solstice_sol_matches_lmd_result(self):
        assert sol_to_solar_longitude(northern_winter_solstice_sol) == pytest.approx(270, abs=0.5)

    def test_non_numeric_string_raises_value_error(self):
        with pytest.raises(ValueError):
            solar_longitude_to_sol('foo')

    def test_numeric_string_raises_no_errors(self):
        solar_longitude_to_sol('180')
