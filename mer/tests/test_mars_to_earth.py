import datetime
import pytest
from mer import mars_year_to_datetime


class TestMarsYearToDatetime:
    @staticmethod
    def my10() -> datetime.date:
        return datetime.date(1972, 3, 15)

    @staticmethod
    def my20() -> datetime.date:
        return datetime.date(1991, 1, 4)

    def test_my10_matches_known_date(self) -> None:
        assert mars_year_to_datetime(10).date() == self.my10()

    def test_my20_matches_known_date(self) -> None:
        assert mars_year_to_datetime(20).date() == self.my20()

    def test_int_and_float_inputs_are_equal(self) -> None:
        assert mars_year_to_datetime(10.0) == mars_year_to_datetime(10)

    def test_str_input_raises_type_error(self) -> None:
        with pytest.raises(TypeError):
            mars_year_to_datetime('10')

    def test_datetime_input_raises_type_error(self) -> None:
        with pytest.raises(TypeError):
            mars_year_to_datetime(datetime.datetime(2020, 1, 1, 0, 0))

    def test_far_future_date_raises_overflow_error(self) -> None:
        with pytest.raises(OverflowError):
            mars_year_to_datetime(4279)

    def test_not_far_future_date_raises_no_error(self) -> None:
        mars_year_to_datetime(4278)

    def test_far_past_date_raises_overflow_error(self) -> None:
        with pytest.raises(OverflowError):
            mars_year_to_datetime(-1039)

    def test_not_far_past_date_raises_no_error(self) -> None:
        mars_year_to_datetime(-1038)
