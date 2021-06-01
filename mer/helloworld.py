import datetime
import julian

d = datetime.datetime(2000, 1, 1, 12, 0, 0)
j2000 = julian.to_jd(d, 'jd')
print(j2000)
my0 = -17023.002
print(my0 + j2000)
foo = julian.from_jd(my0 + j2000, 'jd')
print(type(foo))
print(foo)
