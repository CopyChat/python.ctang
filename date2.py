pd.date_range(start=pd.datetime(2000, 1, 1), periods=4, freq='A')

returns

DatetimeIndex(['2000-12-31', '2001-12-31', '2002-12-31', '2003-12-31'], dtype='datetime64[ns]', freq='A-DEC', tz=None)

Annual indexing to the beginning of an arbitrary month

If you need it to be annual from a particular time use an anchored offset, eg. pd.date_range(start=pd.datetime(2000, 1, 1), periods=10, freq='AS-AUG')

returns

DatetimeIndex(['2000-08-01', '2001-08-01', '2002-08-01', '2003-08-01'], dtype='datetime64[ns]', freq='AS-AUG', tz=None)

Annual indexing from an arbitrary date

To index from an arbitrary date, begin the series on that date and use a custom DateOffset object.

eg. pd.date_range(start=pd.datetime(2000, 9, 10), periods=4, freq=pd.DateOffset(years=1))

returns

DatetimeIndex(['2000-09-10', '2001-09-10', '2002-09-10', '2003-09-10'], dtype='datetime64[ns]', freq='<DateOffset: kwds={'years': 1}>', tz=None)
