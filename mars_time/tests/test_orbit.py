from mars_time.orbit import find_aphelion, find_perihelion
from mars_time.retimers import MarsTime


def test_find_aphelion():
    def test_aphelion_of_mars_year_0_is_computed_value():
        year = 0

        mt = find_aphelion(year)

        assert mt == MarsTime(0, 150.4234195434476)

    test_aphelion_of_mars_year_0_is_computed_value()


def test_find_perihelion():
    def test_perihelion_of_mars_year_0_is_computed_value():
        year = 0

        mt = find_perihelion(year)

        assert mt == MarsTime(0, 484.58831793369114)

    test_perihelion_of_mars_year_0_is_computed_value()
