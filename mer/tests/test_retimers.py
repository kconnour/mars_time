import datetime
import math
import pytz
import pytest
from mer.constants import mars_year_0_start, sols_per_martian_year
from mer.retimers import EarthDateTime, MarsYearSol, MarsYearSolarLongitude, \
    datetime_to_earthdatetime, sols_after_mars_year_0, sols_between_datetimes, \
    sols_since_datetime


class TestEarthDateTime:
    class TestNew:
        @pytest.fixture
        def utc_edt(self) -> datetime.datetime:
            yield EarthDateTime(2020, 1, 1, 0, 0, 0, 0, tzinfo=pytz.UTC)

        @pytest.fixture
        def eastern_edt(self) -> datetime.datetime:
            eastern = pytz.timezone('US/Eastern')
            yield EarthDateTime(2020, 1, 1, 0, 0, 0, 0, tzinfo=eastern)

        @pytest.fixture
        def native_edt(self) -> datetime.datetime:
            yield EarthDateTime(2020, 1, 1, 0, 0, 0, 0)

        def test_int_input_raises_type_error(self):
            with pytest.raises(TypeError):
                EarthDateTime(2837476)

        def test_datetime_input_raises_type_error(self):
            dt = datetime.datetime(2020, 1, 1, 0, 0, 0)
            with pytest.raises(TypeError):
                EarthDateTime(dt)

        def test_utc_input_equals_unaware_input(self, utc_edt, native_edt):
            assert utc_edt == native_edt

        def test_utc_input_is_not_eastern_input(self, utc_edt, eastern_edt):
            assert utc_edt != eastern_edt

    class TestToFractionalMarsYear:
        @pytest.fixture
        def mars_year_10_start(self) -> EarthDateTime:
            yield EarthDateTime(1972, 3, 15, 4, 48, 0)

        @pytest.fixture
        def mars_year_20_start(self) -> EarthDateTime:
            yield EarthDateTime(1991, 1, 4, 21, 50, 24)

        def test_mars_year_10_start_returns_10(self, mars_year_10_start):
            assert mars_year_10_start.to_fractional_mars_year() == \
                   pytest.approx(10, abs=0.0001)

        def test_mars_year_20_start_returns_20(self, mars_year_20_start):
            assert mars_year_20_start.to_fractional_mars_year() == \
                   pytest.approx(20, abs=0.0001)

    class TestToWholeMarsYear:
        @pytest.fixture
        def positive_date(self) -> EarthDateTime:
            yield EarthDateTime(2000, 1, 1, 0, 0, 0, 0)

        @pytest.fixture
        def negative_date(self) -> EarthDateTime:
            yield EarthDateTime(1900, 1, 1, 0, 0, 0, 0)

        def test_positive_mars_year_returns_expected_value(self, positive_date):
            assert positive_date.to_whole_mars_year() == 24

        def test_negative_mars_year_returns_expected_value(self, negative_date):
            assert negative_date.to_whole_mars_year() == -29

    class TestToSol:
        @pytest.fixture
        def mars_year_0_start_edt(self) -> EarthDateTime:
            yield datetime_to_earthdatetime(mars_year_0_start)

        @pytest.fixture
        def moment_before_mars_year_0_start(self) -> EarthDateTime:
            yield datetime_to_earthdatetime(mars_year_0_start) - \
                  datetime.timedelta(milliseconds=1)

        def test_first_moment_of_year_equals_0(self, mars_year_0_start_edt):
            assert mars_year_0_start_edt.to_sol() == 0

        def test_last_moment_of_mars_year_equals_yearly_sols(
                self, moment_before_mars_year_0_start):
            sol = moment_before_mars_year_0_start.to_sol()
            assert sol == pytest.approx(sols_per_martian_year, abs=0.001)

    class TestToSolarLongitude:
        @pytest.fixture
        def mars_year_0_start_edt(self) -> EarthDateTime:
            yield datetime_to_earthdatetime(mars_year_0_start)

        def test_start_of_mars_year_0_returns_0(self, mars_year_0_start_edt):
            ls = mars_year_0_start_edt.to_solar_longitude()
            assert math.sin(math.radians(ls)) == pytest.approx(0, abs=0.001)


class TestMarsYearSol:
    class TestInit:
        def test_int_mars_year_float_sol_raises_no_error(self):
            MarsYearSol(0, 234.567)

        def test_float_mars_year_raises_type_error(self):
            with pytest.raises(TypeError):
                MarsYearSol(14.0, 54)

        def test_first_moment_of_year_raises_no_error(self):
            MarsYearSol(14, 0)

        def test_last_moment_of_year_raises_no_error(self):
            MarsYearSol(14, sols_per_martian_year)

        def test_negative_sol_raises_value_error(self):
            with pytest.raises(ValueError):
                MarsYearSol(14, -0.0001)

        def test_large_sol_raises_value_error(self):
            sol = sols_per_martian_year + 0.0001
            with pytest.raises(ValueError):
                MarsYearSol(14, sol)

    class TestToDatetime:
        def test_sol_0_of_my_0_matches_known_datetime(self):
            assert MarsYearSol(0, 0).to_datetime() == mars_year_0_start

        def test_far_future_date_raises_overflow_error(self) -> None:
            with pytest.raises(OverflowError):
                MarsYearSol(4279, 0).to_datetime()

        def test_not_far_future_date_raises_no_error(self) -> None:
            MarsYearSol(4278, 0).to_datetime()

        def test_far_past_date_raises_overflow_error(self) -> None:
            with pytest.raises(OverflowError):
                MarsYearSol(-1039, 0).to_datetime()

        def test_not_far_past_date_raises_no_error(self) -> None:
            MarsYearSol(-1038, 0).to_datetime()

    class TestToFractionalMarsYear:
        def test_sol_0_returns_mars_year_number(self):
            assert MarsYearSol(14, 0).to_fractional_mars_year() == 14

        def test_last_sol_of_year_returns_1_more_than_year(self):
            mars_year = MarsYearSol(14, sols_per_martian_year).to_fractional_mars_year()
            assert mars_year == pytest.approx(15, abs=0.01)

        def test_midpoint_sol_returns_half_greater_mars_year(self):
            mars_year = MarsYearSol(14, sols_per_martian_year / 2).to_fractional_mars_year()
            assert mars_year == pytest.approx(14.5, abs=0.01)

    class TestToSolarLongitude:
        def test_start_of_year_returns_0(self):
            sin_ls = math.sin(math.radians(MarsYearSol(30, 0).to_solar_longitude()))
            assert sin_ls == pytest.approx(0, abs=0.05)

        def test_end_of_year_returns_0(self):
            sin_ls = math.sin(math.radians(
                MarsYearSol(30, sols_per_martian_year).to_solar_longitude()))
            assert sin_ls == pytest.approx(0, abs=0.05)

        def test_northern_summer_solstice_matches_lmd_value(self):
            assert MarsYearSol(0, 193.47).to_solar_longitude() == \
                   pytest.approx(90, abs=0.1)

        def test_northern_autumn_equinox_matches_lmd_value(self):
            assert MarsYearSol(0, 371.99).to_solar_longitude() == \
                   pytest.approx(180, abs=0.2)

        def test_northern_winter_solstice_matches_lmd_value(self):
            assert MarsYearSol(0, 514.76).to_solar_longitude() == \
                   pytest.approx(270, abs=0.2)


class TestMarsYearSolarLongitude:
    class TestInit:
        def test_int_mars_year_float_ls_raises_no_error(self):
            MarsYearSolarLongitude(0, 234.567)

        def test_float_mars_year_raises_type_error(self):
            with pytest.raises(TypeError):
                MarsYearSolarLongitude(14.0, 54)

        def test_first_moment_of_year_raises_no_error(self):
            MarsYearSolarLongitude(14, 0)

        def test_last_moment_of_year_raises_no_error(self):
            MarsYearSolarLongitude(14, 360)

        def test_negative_ls_raises_value_error(self):
            with pytest.raises(ValueError):
                MarsYearSolarLongitude(14, -0.0001)

        def test_large_ls_raises_value_error(self):
            with pytest.raises(ValueError):
                MarsYearSolarLongitude(14, 360.0001)

    class TestToDatetime:
        def test_sol_0_of_my_0_matches_known_datetime(self):
            assert MarsYearSol(0, 0).to_datetime() == mars_year_0_start

        def test_far_future_date_raises_overflow_error(self) -> None:
            with pytest.raises(OverflowError):
                MarsYearSol(4279, 0).to_datetime()

        def test_not_far_future_date_raises_no_error(self) -> None:
            MarsYearSol(4278, 0).to_datetime()

        def test_far_past_date_raises_overflow_error(self) -> None:
            with pytest.raises(OverflowError):
                MarsYearSol(-1039, 0).to_datetime()

        def test_not_far_past_date_raises_no_error(self) -> None:
            MarsYearSol(-1038, 0).to_datetime()

    class TestToFractionalMarsYear:
        def test_ls_0_returns_mars_year_number(self):
            assert MarsYearSolarLongitude(14, 0).to_fractional_mars_year() == pytest.approx(14, abs=0.001)

        def test_ls_360_of_year_returns_1_more_than_year(self):
            mars_year = MarsYearSolarLongitude(14, 359.99).to_fractional_mars_year()
            assert mars_year == pytest.approx(15, abs=0.01)

    class TestToSol:
        def test_start_of_year_returns_0(self):
            sol = MarsYearSolarLongitude(30, 0).to_sol()
            assert sol == pytest.approx(0, abs=0.05)

        def test_end_of_year_returns_0(self):
            sol = MarsYearSolarLongitude(30, 359.99).to_sol()
            assert sol == pytest.approx(sols_per_martian_year, abs=0.05)

        def test_northern_summer_solstice_matches_lmd_value(self):
            sol = MarsYearSolarLongitude(0, 90).to_sol()
            assert sol == pytest.approx(193.47, abs=0.2)

        def test_northern_autumn_equinox_matches_lmd_value(self):
            sol = MarsYearSolarLongitude(0, 180).to_sol()
            assert sol == pytest.approx(371.99, abs=0.2)

        def test_northern_winter_solstice_matches_lmd_value(self):
            sol = MarsYearSolarLongitude(0, 270).to_sol()
            assert sol == pytest.approx(514.76, abs=0.2)


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


class TestDatetimeToEarthdatetime:
    def test_datetime_raises_no_error(self):
        datetime_to_earthdatetime(mars_year_0_start)

    def test_date_raises_type_error(self):
        date = datetime.date(2020, 1, 1)
        with pytest.raises(TypeError):
            datetime_to_earthdatetime(date)


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
