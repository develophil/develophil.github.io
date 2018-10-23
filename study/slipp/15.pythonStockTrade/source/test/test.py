import pickle
import gzip
import pandas_datareader.data as web
import datetime

data = {
    'a': [1, 2.0, 3, 4+6j],
    'b': ("character string", b"byte string"),
    'c': {None, True, False},
    '00001': web.DataReader("078930.KS", "yahoo", datetime.datetime(2018, 10, 1), datetime.datetime(2018, 10, 10))
}

# save and compress.
# with gzip.open('testPickleFile.pickle', 'wb') as f:
#     pickle.dump(data, f)

# load and uncompress.
with gzip.open('testPickleFile.pickle','rb') as f:
    data = pickle.load(f)
    print(data)
