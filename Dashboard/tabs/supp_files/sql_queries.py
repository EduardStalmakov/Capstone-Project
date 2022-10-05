# References external libraies
import pymssql
import pandas as pd
import warnings
# References files in this repository
from tabs.supp_files import config

# Ignore the warning message when using pd.read_sql
warnings.simplefilter(action='ignore', category=UserWarning) 


database = config.database
user = config.user
password  = config.password
server = config.server

conn = pymssql.connect(server,user,password,database)
cursor = conn.cursor()

# Select all from Census table
Census = pd.read_sql('SELECT * FROM Census', conn)

# Select all from Track table
Track = pd.read_sql('SELECT * FROM Track', conn)

#Select columns from Track table and join with Artist table
Tracks = pd.read_sql(
    'SELECT T.TrackID, TrackName, A.ArtistName, Popularity, DurationMS, ReleaseYear,    \
        Danceability, Energy, MusicalKey, Loudness, Mode, Speechiness, Acousticness,    \
        Instrumentalness, Liveness, Valence, Tempo, TimeSignature, Genres               \
        FROM Track T                                                                    \
        JOIN Artist A ON A.ArtistID = T.ArtistID',
    conn
)

# Select all from Artist table
Artists = pd.read_sql('SELECT * FROM Artist', conn)

# Select all from PlaylistTrack table
Playlist_Tracks = pd.read_sql('SELECT * FROM PlaylistTrack', conn)

# Select all from Playlist table
Playlist = pd.read_sql('SELECT * FROM Playlist', conn)

# Select all from LastFmUsers table
Users = pd.read_sql('SELECT * FROM LastFmUsers', conn)

# Select all from LastFmUsers table and join to Playlist table
User_Playlist   = pd.read_sql('SELECT * FROM LastFmUsers U JOIN Playlist P ON U.UserID = P.UserID', conn)

# Select all from Track table and join to Artist table
Track_Artist    = pd.read_sql('SELECT * FROM Track T JOIN Artist A ON T.ArtistID = A.ArtistID', conn)

# Select columns from Playlist table and join to PlaylistTrack table
Playlist_PT = pd.read_sql(
    'SELECT UserName, P.UserID, PlaylistTitle, P.PlaylistID, TrackID FROM Playlist P    \
        JOIN PlaylistTrack PT ON P.PlaylistID = PT.PlaylistID                           \
        JOIN LastFmUsers U ON P.UserID = U.UserID', 
    conn
)