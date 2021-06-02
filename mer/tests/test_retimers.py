import datetime
import pytest
from mer.constants import date_of_start_of_mars_year_0
from mer.retimers import sols_after_mars_year_0, sols_between_datetimes,\
    sols_since_datetime


class TestSolsAfterMarsYear0:
    @pytest.fixture
    def maven_arrival_datetime(self):
        yield datetime.datetime(2014, 9, 2, 2, 24, 0)

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
