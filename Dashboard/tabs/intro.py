from dash.dependencies import Input, Output
from dash import html, dcc 

from app import app

layout = [dcc.Markdown("""
### Intro
'Dev10's Cohort 31 Team 4 "Land'o'Datalake" is Vanessa Gleason, Alistair Marsden, Olivier Rochaix, Eduard Stalmakov. Together we 
have investgated the inner workings of music streaming services. A critical component to retaining user engagement is
to expose users to more material, new songs, that they will find appealing. Therefore, we created two types of recommenders
to increase the user experience, a content recommender and a collaborative recommender. 

#### User Interface

Land'o'Datalake is introducing two recommenders to increase the music streaming user's experience. Both of these models
capitalize on cosine similarities, but in different attributes of our data.


**Content Recommender**

The content recommender is based on our "songs" data set which provided attributes of each song, such as popularity, 
liveness, and instrumentalness. Assuming a user enjoys the songs on their playlist, our unsupervised content recommender model
 looks at the attributes of that collection of song and returns the most similar new songs to possibly extend their 
 playlist. 


**Collaborative Recommender**

Our collaborative recommender extends the user's listening session in a different way based on our playlist data set.
This data set has playlist and songs within that playlist. The collaborative model uses the premise of 'if playlist A
has songs X, Y, and Z, and playlist B has songs X and Y, the person listening to playlist B will probably like song Z.

Both the content recommender and collaborative recommender are available on the 'User Interface' tab. 


#### Target Market

Additionally, we researched the demographics of people who stream music. While we could not get proprietary information
from Spotify about demographics of their users and musical preferences, the US Census Bureau provided demographic data
about people and households that stream music. Visualization about this data, including age, race, household income is available on the
'Target Market' tab. 

Information on the current market size of music streaming services and trends in that market are also available on the 
'Target Market' tab.


#### Behind the Scenes

Information about how our recommender models work and our data sets are available in the 'Behind the Scenes'
tab.


""")]
