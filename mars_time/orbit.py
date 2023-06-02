import datetime

import scipy

from mars_time.constants import mars_year_start_days_since_j2000, j2000
from mars_time.retimers import datetime_to_mars_time


def find_aphelion(mars_year):
    start = mars_year_start_days_since_j2000[mars_year]
    end = mars_year_start_days_since_j2000[mars_year + 1]

    def foo(day):
        day = float(day)
        bar = datetime_to_mars_time(j2000 + datetime.timedelta(days=day - 0.001))
        baz = datetime_to_mars_time(j2000 + datetime.timedelta(days=day + 0.001))
        return abs(bar.solar_longitude - baz.solar_longitude)

    answer = scipy.optimize.minimize_scalar(foo, bounds=(start, end), method='bounded').x
    return datetime_to_mars_time(j2000 + datetime.timedelta(days=answer))


def find_perihelion(mars_year):
    start = mars_year_start_days_since_j2000[mars_year]
    end = mars_year_start_days_since_j2000[mars_year + 1]

    def foo(day):
        day = float(day)
        bar = datetime_to_mars_time(j2000 + datetime.timedelta(days=day - 0.001))
        baz = datetime_to_mars_time(j2000 + datetime.timedelta(days=day + 0.001))
        return abs(bar.solar_longitude - baz.solar_longitude) * -1

    answer = scipy.optimize.minimize_scalar(foo, bounds=(start, end), method='bounded').x
    return datetime_to_mars_time(j2000 + datetime.timedelta(days=answer))


if __name__ == '__main__':
    import numpy as np

    sol = []
    ls = []
    for i in range(-99, 100):
        asdf = find_aphelion(i)
        dt = datetime_to_mars_time(j2000 + datetime.timedelta(days=asdf))
        sol.append(dt.sol)
        ls.append(dt.solar_longitude)

    print(np.mean(sol))
    print(np.mean(ls))
