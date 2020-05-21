
import requests

import time
from _datetime import datetime as dt, timedelta
#from datetime import datetime, timedelta
d = dt.now()
seven = d - timedelta(days=7)
unixto = str(int(time.mktime(d.timetuple())))
unixfrom = str(int(time.mktime(seven.timetuple())))
url= 'https://finnhub.io/api/v1/forex/candle?symbol=OANDA:EUR_USD&resolution=D&from='+unixfrom+'&to='+unixto+'&token=br0ht3frh5radq31f800'

print(url)

r = requests.get(url)

print(r.json())

status_code = r.status_code

if(status_code == 429):
    print("Too many requests !")
else:
    print(r.json())
