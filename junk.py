

import datetime
import mars_time

landing_time = mars_time.datetime_to_mars_time(datetime.datetime(2021, 2, 18, 20, 55, 0))
detection_time = landing_time + mars_time.MarsTimeDelta(sol=292)
print(f'{sol_to_solar_longitude(detection_time.sol):.1f}')

