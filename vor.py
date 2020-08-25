#hotfix for disabling ssl checking 
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import pandas as pd

# import seaborn as sns # in case you did not import it above

df = pd.read_csv('https://raw.githubusercontent.com/fantasydatapros/data/master/fantasypros/fp_projections.csv')
adp_df = pd.read_csv('https://raw.githubusercontent.com/fantasydatapros/data/master/fantasypros/adp/PPR_ADP.csv', index_col=0) # set index col = 0 to set the range index as our dataframes index

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

# rb_df = df.loc[df['Pos'] == 'RB']
# rb_df = rb_df.loc[rb_df['RushingAtt'] > 250]

# print(rb_df.head())


# base_columns = ['Player', 'Team', 'Pos']
# rushing_columns = ['FantasyPoints', 'Receptions', 'ReceivingYds', 'ReceivingTD', 'RushingAtt', 'RushingYds', 'RushingTD', 'FL']

# """
# Here, we can mask (what we are doing in the row indexer) and filter (what we are doing in the column indexer)
# all in one line. Pass in (the boolean indexer, columns you'd like to keep) as a tuple.
# Also recall that lists can be concatenated together.
# """
# rb_df = df.loc[(df['Pos'] == 'RB', base_columns + rushing_columns)]

# rb_df.head()

# print(df[:5])

# """
# The sort_values method of a DataFrame allows us sort our table by a given column.
# The 'by' parameter of the function here is a required argument, and it should be the name of 
# one of the columns in your table.
# The 'ascending' argument is optional. If you want to sort your table from largest to smallest, set
# ascending = False to sort in descending order. The object we get back from the sort_values function
# is also a pandas DataFrame, and so we can chain methods as we do below with sort_values and head.
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html
# """

# # sort RBs by RushingYds in descending order and get us back the top 15 rows.
# rb_df.sort_values(by='RushingYds', ascending=False).head(15)


adp_df['ADP RANK'] = adp_df['AVG'].rank()

adp_df_cutoff = adp_df[:100]

replacement_players = {
    'RB': '',
    'QB': '',
    'WR': '',
    'TE': ''
}

for _, row in adp_df_cutoff.iterrows():
    
    position = row['POS'] # extract out the position and player value from each row as we loop through it
    player = row['PLAYER']
    
    if position in replacement_players: # if the position is in the dict's keys
        replacement_players[position] = player # set that player as the replacement player

# print(adp_df[:10])
# print(replacement_players)

df = df[['Player', 'Pos', 'Team', 'FantasyPoints']] # filtering out the columns we need.


replacement_values = {} # initialize an empty dictionary

for position, player_name in replacement_players.items():
    
    player = df.loc[df['Player'] == player_name]
    
    # because this is a series object we get back, we need to use the tolist method
    # to get back the series as a list. The list object is of length 1, and the 1 item has the value we need.
    # we tack on a [0] to get the value we need.
    
    replacement_values[position] = player['FantasyPoints'].tolist()[0]

print(replacement_values)

# """
# the isin method lets us check if a value is in a list
# and can be passed as a boolean indexer / row filter / mask
# here, we want to filter out all those rows who's position column is not in
# ['QB', 'RB', 'WR', 'TE']
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.isin.html
# """ 

# this will be explained in the next chapter
pd.set_option('chained_assignment', None)

df = df.loc[df['Pos'].isin(['QB', 'RB', 'WR', 'TE'])]

# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.apply.html
df['VOR'] = df.apply(
    lambda row: row['FantasyPoints'] - replacement_values.get(row['Pos']), axis=1
)


# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.set_option.html
pd.set_option('display.max_rows', None) # turn off truncation of rows setting inherent to pandas

df['VOR Rank'] = df['VOR'].rank(ascending=False)
# print(df.sort_values(by='VOR', ascending=False).head(100))


# """
# the pandas groupby method allows us to groupby a specific column, called "splitting",
# then apply a summary function over to each group. We can split this up by column as well, by tacking
# on ['ColumName'] after grouping and before applying the summary function.
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.groupby.html
# """

# print(df.groupby('Pos')['VOR'].describe())

# standard score example. Notice axis is not set to 1 as we are applying a function across a column here.
# df['VOR'] = df['VOR'].apply(lambda x: (x - df['VOR'].mean()) / df['VOR'].std())

df['VOR'] = df['VOR'].apply(lambda x: (x - df['VOR'].min()) / (df['VOR'].max() - df['VOR'].min()))

df = df.sort_values(by='VOR Rank')
# print(df[:100])

# num_teams = 12
# num_spots = 16 # 1 QB, 2RB, 2WR, 1TE, 1FLEX, 1K, 1DST, 7 BENCH
# draft_pool = num_teams * num_spots

# df_copy = df[:draft_pool]

# print(sns.boxplot(x=df_copy['Pos'], y=df_copy['VOR']))

# let's rename our VOR column to just Value.
# remember, to make a change to our DataFrame, you set it equal to itself + some modifcation
# we can use the rename method here to help us do that
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rename.html

df = df.rename({
    'VOR': 'Value',
    'VOR Rank': 'Value Rank'
}, axis=1) # axis = 1 means make the change along the column axis.

# print(df[:5])

adp_df = adp_df.rename({
    'PLAYER': 'Player',
    'POS': 'Pos',
    'AVG': 'Average ADP',
    'ADP RANK': 'ADP Rank'
}, axis=1) # let's rename some columns first.