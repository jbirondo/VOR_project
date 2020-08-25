#hotfix for disabling ssl checking 
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/fantasydatapros/data/master/fantasypros/fp_projections.csv')

print(df.head(5))