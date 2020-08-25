#hotfix for disabling ssl checking 
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/fantasydatapros/data/master/fantasypros/fp_projections.csv')

#.iloc[] is primarily integer position based (from 0 to length-1 of the axis), but may also be used with a boolean array.
#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iloc.html
df = df.iloc[:, 1:]

scoring_weights = {
    'receptions': 1, # PPR
    'receiving_yds': 0.1,
    'receiving_td': 6,
    'FL': -2, #fumbles lost
    'rushing_yds': 0.1,
    'rushing_td': 6,
    'passing_yds': 0.04,
    'passing_td': 4,
    'int': -2
}

print(' '.join((df.columns)))