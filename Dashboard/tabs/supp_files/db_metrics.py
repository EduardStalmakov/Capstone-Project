# References external libraries
import plotly.express as px
# References files in the repository
from tabs.supp_files import sql_queries


# Select data from SQL database
User_Playlist   = sql_queries.User_Playlist
Track_Artist    = sql_queries.Track_Artist
# Get a DataFrame that uses SQL to merge the Track and Artist tables, and then merge it with the PlaylistTrack table
Playlist_Tracks_merged = sql_queries.Playlist_Tracks.merge(sql_queries.Tracks, how = 'inner', on = 'TrackID')


# Get a value for the count of unique users / playlists and the max amount of playlists to a user
usr_count   = User_Playlist['UserName'].drop_duplicates().count()
pl_count    = User_Playlist['PlaylistID'].drop_duplicates().count()
max_pl      = User_Playlist.groupby('UserName')['PlaylistID'].count().sort_values(ascending=False).values[0]
min_pl      = User_Playlist.groupby('UserName')['PlaylistID'].count().values[0]

# Get a value for the count of unique tracks / artists and the max amount of tracks to an artist
trk_count   = Track_Artist['TrackID'].drop_duplicates().count()
art_count   = Track_Artist['ArtistName'].drop_duplicates().count()
gre_count   = Track_Artist['Genres'].drop_duplicates().count()
max_trk     = Track_Artist.groupby('ArtistName')['TrackID'].count().sort_values(ascending=False).values[0]
min_trk     = Track_Artist.groupby('ArtistName')['TrackID'].count().values[0]

# Get top 5s for tracks, genres, and artists
top_5_track  = Playlist_Tracks_merged['TrackName'].value_counts().sort_values(ascending = False)[0:5]
top_5_genre  = Playlist_Tracks_merged['Genres'].value_counts().sort_values(ascending = False)[0:5]
top_5_artist = Playlist_Tracks_merged['ArtistName'].value_counts().sort_values(ascending = False)[0:5]

# Create a bar graph for the top 5 tracks
top_5_track = px.bar(
    x       = top_5_track.index, 
    y       = top_5_track.values, 
    title   = 'Top Trending Songs'.upper(), 
    labels  = {'x' : 'Song', 'y' : 'Count on Playlists'}
)
top_5_track.update_layout(
    title_font_size     = 20, 
    title_font_color    = '#BDBDBD', 
    title_x             = 0.5,
    font_color          = '#6699CC', 
    paper_bgcolor       = '#2A3439'
)

# Create a bar graph for the top 5 genres
top_5_genre = px.bar(
    x       = top_5_genre.index, 
    y       = top_5_genre.values, 
    title   = 'Top Trending Genres'.upper(), 
    labels  = {'x' : 'Genre', 'y' : 'Count on Playlists'}
)
top_5_genre.update_layout(
    title_font_size     = 20, 
    title_font_color    = '#BDBDBD', 
    title_x             = 0.5,
    font_color          = '#6699CC', 
    paper_bgcolor       = '#2A3439'
)

# Create a bar graph for the top 5 artists
top_5_artist = px.bar(
    x = top_5_artist.index, 
    y = top_5_artist.values, 
    title = 'Top Trending Artists'.upper(), 
    labels = {'x' : 'Artist', 'y' : 'Count on Playlists'}
)
top_5_artist.update_layout(
    title_font_size     = 20, 
    title_font_color    = '#BDBDBD', 
    title_x             = 0.5,
    font_color          = '#6699CC', 
    paper_bgcolor       = '#2A3439'
)