import datetime
import pytest
from mer import mars_year_to_datetime


class TestMarsYearToDatetime:
    @staticmethod
    def my10():
        return datetime.date(1972, 3, 15)

    @staticmethod
    def my20():
        return datetime.date(1991, 1, 4)

    def test_my10_matches_known_value(self):
        assert mars_year_to_datetime(10).date() == self.my10()

    def test_my20_matches_known_value(self):
        assert mars_year_to_datetime(20).date() == self.my20()

    def test_int_and_float_inputs_are_equal(self):
        assert mars_year_to_datetime(10) == mars_year_to_datetime(10.0)

    def test_str_raises_type_error(self):
        with pytest.raises(TypeError):
            mars_year_to_datetime('10')
