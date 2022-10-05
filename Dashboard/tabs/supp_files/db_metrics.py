# References external libraries
import plotly.express as px
import pymssql
import pandas as pd

database    =   'landodatalakes-group4'
user        =   'spotify'
password    =   'T35TPA55W0RD!'
server      =   'gen10-data-fundamentals-22-07-sql-server.database.windows.net'

conn    = pymssql.connect(server, user, password, database)
cursor  = conn.cursor()

# Get a DataFrame that uses SQL to read the Track table
Track = pd.read_sql('SELECT * FROM Track', conn)

# Get a DataFrame that uses SQL to merge the LastFmUsers and Playlist tables
User_Playlist   = pd.read_sql('SELECT * FROM LastFmUsers U JOIN Playlist P ON U.UserID = P.UserID', conn)

# Get a DataFrame that uses SQL to merge the Track and Artist tables
Track_Artist    = pd.read_sql('SELECT * FROM Track T JOIN Artist A ON T.ArtistID = A.ArtistID', conn)

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

