import datetime
import math
import pytz
import pytest
from mer.constants import mars_year_0_start, sols_per_martian_year
from mer.retimers import sols_after_mars_year_0, sols_between_datetimes,\
    EarthDatetime, Sol


class TestEarthDatetime:
    class TestInit:
        @pytest.fixture
        def utc_dt(self) -> datetime.datetime:
            yield datetime.datetime(2020, 1, 1, 0, 0, 0, 0, tzinfo=pytz.UTC)

        @pytest.fixture
        def eastern_dt(self) -> datetime.datetime:
            eastern = pytz.timezone('US/Eastern')
            yield datetime.datetime(2020, 1, 1, 0, 0, 0, 0, tzinfo=eastern)

        @pytest.fixture
        def unaware_dt(self) -> datetime.datetime:
            yield datetime.datetime(2020, 1, 1, 0, 0, 0, 0)

        def test_aware_datetime_raises_no_errors(self, utc_dt):
            EarthDatetime(utc_dt)

        def test_unaware_datetime_raises_no_errors(self, unaware_dt):
            EarthDatetime(unaware_dt)

        def test_int_input_raises_type_error(self):
            with pytest.raises(TypeError):
                EarthDatetime(2837476)

        def test_date_input_raises_type_error(self):
            date = datetime.date(2020, 1, 1)
            with pytest.raises(TypeError):
                EarthDatetime(date)

        def test_utc_datetime_equals_unaware_datetime(self, utc_dt, unaware_dt):
            assert EarthDatetime(utc_dt) == EarthDatetime(unaware_dt)

        def test_utc_datetime_is_not_eastern_datetime(self, utc_dt, eastern_dt):
            assert EarthDatetime(utc_dt) != EarthDatetime(eastern_dt)

        def test_datetime_is_not_earth_datetime(self, utc_dt):
            assert EarthDatetime(utc_dt) != utc_dt

        def test_str_equals_aware_datetime(self, utc_dt):
            assert str(EarthDatetime(utc_dt)) == str(utc_dt)

        def test_str_does_not_equal_unaware_datetime(self, unaware_dt):
            assert str(EarthDatetime(unaware_dt)) != str(unaware_dt)

    class TestToFractionalMarsYear:
        @pytest.fixture
        def mars_year_10_start(self) -> datetime.datetime:
            yield datetime.datetime(1972, 3, 15, 0, 0, 0)

        def test_start_of_mars_year_0_returns_0(self):
            edt = EarthDatetime(mars_year_0_start)
            assert edt.to_fractional_mars_year() == 0

        def test_date_of_mars_year_10_returns_10(self, mars_year_10_start):
            edt = EarthDatetime(mars_year_10_start)
            assert edt.to_fractional_mars_year() == pytest.approx(10, abs=0.01)

    class TestToWholeMarsYear:
        @pytest.fixture
        def positive_date(self) -> datetime.datetime:
            yield datetime.datetime(2000, 1, 1, 0, 0, 0, 0, pytz.UTC)

        @pytest.fixture
        def negative_date(self) -> datetime.datetime:
            yield datetime.datetime(1900, 1, 1, 0, 0, 0, 0, pytz.UTC)

        def test_positive_mars_year_returns_expected_value(self, positive_date):
            edt = EarthDatetime(positive_date)
            assert edt.to_whole_mars_year() == 24

        def test_negative_mars_year_returns_expected_value(self, negative_date):
            edt = EarthDatetime(negative_date)
            assert edt.to_whole_mars_year() == -29

    class TestToSol:
        def test_first_moment_of_year_equals_0(self):
            edt = EarthDatetime(mars_year_0_start)
            assert edt.to_sol() == 0

        def test_last_moment_of_mars_year_equals_yearly_sols(self):
            last_moment = mars_year_0_start - datetime.timedelta(seconds=1)
            sol = EarthDatetime(last_moment).to_sol()
            assert sol == pytest.approx(sols_per_martian_year, abs=0.001)

    class TestToSolarLongitude:
        def test_start_of_mars_year_0_is_0(self):
            edt = EarthDatetime(mars_year_0_start)
            sin_ls = math.sin(math.radians(edt.to_solar_longitude()))
            assert sin_ls == pytest.approx(0, abs=0.05)

        def test_last_moment_of_mars_year_is_almost_0(self):
            last_moment = mars_year_0_start - datetime.timedelta(seconds=1)
            edt = EarthDatetime(last_moment)
            sin_ls = math.sin(math.radians(edt.to_solar_longitude()))
            assert sin_ls == pytest.approx(0, abs=0.05)


class TestSol:
    class TestInit:
        def test_int_mars_year_float_sol_raises_no_error(self):
            Sol(0, 234.567)

        def test_float_mars_year_raises_type_error(self):
            with pytest.raises(TypeError):
                Sol(14.0, 54)

        def test_first_moment_of_year_raises_no_error(self):
            Sol(14, 0)

        def test_last_moment_of_year_raises_no_error(self):
            Sol(14, sols_per_martian_year)

        def test_negative_sol_raises_value_error(self):
            with pytest.raises(ValueError):
                Sol(14, -0.5)

        def test_large_sol_raises_value_error(self):
            sol = sols_per_martian_year + 0.0001
            with pytest.raises(ValueError):
                Sol(14, sol)

    class TestToDatetime:
        def test_sol_0_of_my_0_matches_known_datetime(self):
            assert Sol(0, 0).to_datetime() == mars_year_0_start

        def test_far_future_date_raises_overflow_error(self) -> None:
            with pytest.raises(OverflowError):
                Sol(4279, 0).to_datetime()

        def test_not_far_future_date_raises_no_error(self) -> None:
            Sol(4278, 0).to_datetime()

        def test_far_past_date_raises_overflow_error(self) -> None:
            with pytest.raises(OverflowError):
                Sol(-1039, 0).to_datetime()

        def test_not_far_past_date_raises_no_error(self) -> None:
            Sol(-1038, 0).to_datetime()

    class TestToFractionalMarsYear:
        def test_sol_0_returns_0(self):
            assert Sol(14, 0).to_fractional_mars_year() - 14 == 0

        def test_last_sol_is_1(self):
            mars_year = Sol(14, sols_per_martian_year).to_fractional_mars_year()
            assert mars_year - 14 == pytest.approx(1, abs=0.01)

        def test_midpoint_sol_is_half(self):
            mars_year = Sol(14, sols_per_martian_year / 2).to_fractional_mars_year()
            assert mars_year - 14 == pytest.approx(0.5, abs=0.01)

    class TestToSolarLongitude:
        def test_start_of_year_returns_0(self):
            sin_ls = math.sin(math.radians(Sol(30, 0).to_solar_longitude()))
            assert sin_ls == pytest.approx(0, abs=0.05)

        def test_end_of_year_returns_0(self):
            sin_ls = math.sin(math.radians(
                Sol(30, sols_per_martian_year).to_solar_longitude()))
            assert sin_ls == pytest.approx(0, abs=0.05)

        def test_northern_summer_solstice_matches_lmd_value(self):
            assert Sol(0, 193.47).to_solar_longitude() == \
                   pytest.approx(90, abs=0.1)

        def test_northern_autumn_equinox_matches_lmd_value(self):
            assert Sol(0, 371.99).to_solar_longitude() == \
                   pytest.approx(180, abs=0.2)

        def test_northern_winter_solstice_matches_lmd_value(self):
            assert Sol(0, 514.76).to_solar_longitude() == \
                   pytest.approx(270, abs=0.2)


class TestSolsAfterMarsYear0:
    @pytest.fixture
    def maven_arrival_datetime(self) -> datetime.datetime:
        yield datetime.datetime(2014, 9, 2, 2, 24, 0, 0, pytz.UTC)

    def test_int_input_raises_type_error(self):
        with pytest.raises(TypeError):
            sols_after_mars_year_0(2000)

    def test_date_input_raises_type_error(self, maven_arrival_datetime):
        with pytest.raises(TypeError):
            sols_after_mars_year_0(maven_arrival_datetime.date())

    def test_start_of_mars_year_0_returns_0(self):
        assert sols_after_mars_year_0(mars_year_0_start) == 0

    def test_maven_arrival_matches_known_value(self, maven_arrival_datetime):
        assert sols_after_mars_year_0(maven_arrival_datetime) == \
            21781.872772174716


class TestSolsBetweenDatetimes:
    @pytest.fixture
    def generic_datetime(self) -> datetime.datetime:
        yield datetime.datetime(2000, 1, 1, 0, 0, 0)

    @pytest.fixture
    def opportunity_start(self) -> datetime.datetime:
        yield datetime.datetime(2004, 1, 25, 0, 0, 0)

    @pytest.fixture
    def opportunity_end(self) -> datetime.datetime:
        yield datetime.datetime(2018, 6, 10, 0, 0, 0)

    def test_int_first_input_raises_type_error(self, generic_datetime):
        with pytest.raises(TypeError):
            sols_between_datetimes(2000, generic_datetime)

    def test_int_second_input_raises_type_error(self, generic_datetime):
        with pytest.raises(TypeError):
            sols_between_datetimes(generic_datetime, 2000)

    def test_int_both_inputs_raises_type_error(self):
        with pytest.raises(TypeError):
            sols_between_datetimes(2000, 2001)

    def test_identical_datetime_inputs_returns_0(self, generic_datetime):
        assert sols_between_datetimes(generic_datetime, generic_datetime) == 0

    def test_opportunity_length_matches_known_value(
            self, opportunity_start, opportunity_end):
        assert sols_between_datetimes(opportunity_start, opportunity_end) == \
            5109.551211085292


class TestSolsSinceDatetime:
    pass
