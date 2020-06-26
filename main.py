from datetime import datetime, timedelta

import functions as fn

test_date = datetime(year=2020, month=6, day=26)
df = fn.import_data(test_date, test_date)
print(df)
