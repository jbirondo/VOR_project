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
    'passing_td': 6,
    'int': -2
}

df['FantasyPoints'] = (
    df['Receptions']*scoring_weights['receptions'] + \
    df['ReceivingYds']*scoring_weights['receiving_yds'] + \
    df['ReceivingTD']*scoring_weights['receiving_td'] + \
    df['FL']*scoring_weights['FL'] + \
    df['RushingYds']*scoring_weights['rushing_yds'] + \
    df['RushingTD']*scoring_weights['rushing_td'] + \
    df['PassingYds']*scoring_weights['passing_yds'] + \
    df['PassingTD']*scoring_weights['passing_td'] + \
    df['Int']*scoring_weights['int'] 
    )


# # mask our dataframe based off a position
# """
# .loc is a way of getting back specified cross sections of your dataframe.
# The syntax is as follows:
# new_df = old_df.loc[row_indexer, column_indexer]
# Where row_indexer can take the form of a boolean indexer.
# For example, df['Pos'] == 'RB'
# or, df['RushingAtt'] > 20
# or, df['Pos'].isin(['QB', 'WR', 'RB', TE]) # check if a player's position is a skill position
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html # docs on loc
# https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html # docs on indexing
# """

rb_df = df.loc[df['Pos'] == 'RB']
# rb_df = rb_df['RushingAtt'] > 250

print(rb_df.head())

# print(df[:5])