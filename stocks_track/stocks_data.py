from nsepy import get_history
from datetime import date
from datetime import date
from nsepy import get_history


# get data of sbin stock


sbin = get_history(symbol='SBIN',
                   start=date(2020,8,10),
                   end=date(2020,8,16))
                   
                   
