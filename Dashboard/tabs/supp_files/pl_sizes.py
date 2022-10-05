# References external libraries
import plotly.express as px
import pymssql
import pandas as pd
# References files in the repository
from tabs.supp_files import sql_queries

#Ignores pandas warning for chained assignments.
pd.options.mode.chained_assignment = None


# Get a DataFrame that uses SQL to merge the Playlist and PlaylistTrack tables
Playlist_PT = sql_queries.Playlist_PT

# Group by UserName and PlaylistTitle in order to account for Playlists with the same titles
num_trk_pl  = Playlist_PT.groupby(['UserName', 'PlaylistTitle']).agg({'TrackID':'count'})
num_trk_pl.sort_values(by='TrackID', ascending=False, inplace=True)
num_trk_pl.reset_index(inplace=True)
num_trk_pl['Playlist [User]'] = num_trk_pl['PlaylistTitle'].str[0:12] + '...<br>[' + num_trk_pl['UserName'] + ']'
num_trk_pl  = num_trk_pl[['Playlist [User]', 'TrackID']]

# Grab both the top 5 and bottom 5 rows of the DataFrame to get an idea of the DataFrame's max and min values
top5_pl         =   num_trk_pl.head()
top5_pl['Rank'] = 'Largest 5'
bot5_pl         =   num_trk_pl.tail()
bot5_pl['Rank'] = 'Smallest 5'
top5_bot5       =   pd.concat([top5_pl, bot5_pl])

# Use the concatenated top and bottom 5 rows to make two side-by-side graphs in plotly express
pl_sizes = px.bar(
    x = top5_bot5['Playlist [User]'], y = top5_bot5['TrackID'],
    facet_col = top5_bot5['Rank'], 
    title = 'Playlist Sizes By Number of Tracks'.upper(), 
    labels = {'x' : 'Playlist [User]', 'y' : 'Number of Tracks'},
    text = top5_bot5['TrackID'], width = 1300, height = 800
)
pl_sizes.update_xaxes(matches = None)
pl_sizes.for_each_annotation(lambda a: a.update(text=a.text.split('=')[1]))
pl_sizes.add_annotation(x = 4.5, y = 11, text = 'AVG (10 Tracks)', font = {'color' : 'black'})
pl_sizes.add_hline(y = 10, line_dash = 'dash', line_color = 'grey')
pl_sizes.update_layout(
    title_font_size = 30, title_font_color = '#BDBDBD', title_x = 0.5,
    font_color = '#6699CC', paper_bgcolor = '#2A3439'
)