import datetime
import pytz
import pytest
from mer.constants import date_of_start_of_mars_year_0, sols_per_martian_year
from mer.retimers import sols_after_mars_year_0, sols_between_datetimes,\
    sols_since_datetime, EarthDatetime


class TestEarthDatetime:
    @pytest.fixture
    def utc_dt(self):
        yield datetime.datetime(2020, 1, 1, 0, 0, 0, 0, tzinfo=pytz.UTC)

    @pytest.fixture
    def unaware_dt(self):
        yield datetime.datetime(2020, 1, 1, 0, 0, 0, 0)

    @pytest.fixture
    def eastern_dt(self):
        eastern = pytz.timezone('US/Eastern')
        yield datetime.datetime(2020, 1, 1, 0, 0, 0, 0, tzinfo=eastern)

    def test_utc_datetime_equals_unaware_datetime(self, utc_dt, unaware_dt):
        assert EarthDatetime(utc_dt) == EarthDatetime(unaware_dt)

    def test_utc_datetime_is_not_eastern_datetime(self, utc_dt, eastern_dt):
        assert EarthDatetime(utc_dt) != EarthDatetime(eastern_dt)


class TestEarthDatetimeToFractionalMarsYear:
    @pytest.fixture
    def date_of_start_of_mars_year_10(self):
        yield datetime.datetime(1972, 3, 15, 0, 0, 0)

    def test_start_of_mars_year_0_returns_0(self):
        edt = EarthDatetime(date_of_start_of_mars_year_0)
        assert edt.to_fractional_mars_year() == 0

    def test_date_of_mars_year_10_returns_10(self, date_of_start_of_mars_year_10):
        edt = EarthDatetime(date_of_start_of_mars_year_10)
        assert edt.to_fractional_mars_year() == pytest.approx(10, abs=0.01)


class TestEarthDatetimeToWholeMarsYear:
    @pytest.fixture
    def positive_random_date(self):
        yield datetime.datetime(2000, 1, 1, 0, 0, 0, 0, pytz.UTC)

    @pytest.fixture
    def negative_random_date(self):
        yield datetime.datetime(1900, 1, 1, 0, 0, 0, 0, pytz.UTC)

    def test_positive_mars_year_returns_expected_value(self, positive_random_date):
        edt = EarthDatetime(positive_random_date)
        assert edt.to_whole_mars_year() == 24

    def test_negative_mars_year_returns_expected_value(self, negative_random_date):
        edt = EarthDatetime(negative_random_date)
        assert edt.to_whole_mars_year() == -29


class TestEarthDatetimeToSol:
    def test_first_moment_of_year_equals_0(self):
        edt = EarthDatetime(date_of_start_of_mars_year_0)
        assert edt.to_sol() == 0

    def test_last_moment_of_mars_year_equals_yearly_sols(self):
        last_moment = date_of_start_of_mars_year_0 - datetime.timedelta(seconds=1)
        edt = EarthDatetime(last_moment)
        assert edt.to_sol() == pytest.approx(sols_per_martian_year, abs=0.001)


class TestEarthDatetimeToSolarLongitude:
    def test_start_of_mars_year_0_is_0(self):
        edt = EarthDatetime(date_of_start_of_mars_year_0)
        assert edt.to_solar_longitude() == pytest.approx(0, abs=0.05)

    def test_last_moment_of_mars_year_is_almost_0(self):
        last_moment = date_of_start_of_mars_year_0 - datetime.timedelta(seconds=1)
        edt = EarthDatetime(last_moment)
        assert edt.to_solar_longitude() == pytest.approx(0, abs=0.05)


class TestSolsAfterMarsYear0:
    @pytest.fixture
    def maven_arrival_datetime(self):
        yield datetime.datetime(2014, 9, 2, 2, 24, 0, 0, pytz.UTC)

    def test_start_of_mars_year_0_returns_0(self):
        assert sols_after_mars_year_0(date_of_start_of_mars_year_0) == 0

    def test_maven_arrival_matches_known_value(self, maven_arrival_datetime):
        assert sols_after_mars_year_0(maven_arrival_datetime) == \
            21781.872772174716

    def test_int_input_raises_type_error(self):
        with pytest.raises(TypeError):
            sols_after_mars_year_0(2000)

    def test_date_input_raises_type_error(self, maven_arrival_datetime):
        with pytest.raises(TypeError):
            sols_after_mars_year_0(maven_arrival_datetime.date())


class TestSolsBetweenDatetimes:
    @pytest.fixture
    def generic_datetime(self):
        yield datetime.datetime(2000, 1, 1, 0, 0, 0)

    @pytest.fixture
    def opportunity_start(self):
        yield datetime.datetime(2004, 1, 25, 0, 0, 0)

    @pytest.fixture
    def opportunity_end(self):
        yield datetime.datetime(2018, 6, 10, 0, 0, 0)

    def test_identical_datetime_inputs_returns_0(self, generic_datetime):
        assert sols_between_datetimes(generic_datetime, generic_datetime) == 0

    def test_opportunity_length_matches_known_values(
            self, opportunity_start, opportunity_end) -> None:
        assert sols_between_datetimes(opportunity_start, opportunity_end) == \
            5109.551211085292

    def test_int_first_input_raises_type_error(self, generic_datetime):
        with pytest.raises(TypeError):
            sols_between_datetimes(2000, generic_datetime)

    def test_int_second_input_raises_type_error(self, generic_datetime):
        with pytest.raises(TypeError):
            sols_between_datetimes(generic_datetime, 2000)

    def test_int_both_inputs_raises_type_error(self):
        with pytest.raises(TypeError):
            sols_between_datetimes(2000, 2001)


class TestSolsSinceDatetime:
    pass
