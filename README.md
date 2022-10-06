# Music Streaming Song Recommender 

## Introduction
Introduction
Upon beginning our Capstone Project, team Land’o’datalakes was first interested in exploring recommender models. We found it interesting that when you make, or even think about making an online purchase, stores like Amazon already know items to cross-sell with your potential purchase. If you put a lawn chair in your cart, how does Amazon decide to tell you “here are some other lawn chairs you might like more” or “don't you need these cool sunglasses, too?”. We also considered creating a recommender model to be an interesting and feasible challenge. While we hadn’t ever created machine learning models geared to recommendations before, we knew that with some smart application of previously learned subjects and research we could make a successful attempt at them. Below are some of the specifics of our projects.


## Questions
1. Who are the people who use audio streaming services?

2. How might we build a database that allows us to make recommendations based on music?

3. How would songs trend over time in this database?

4. What trends or patterns are there in the user metrics of our application?

5. How does our database compare to actual music streaming services?

6. Are recommendation models important to user retention on a music platform?


## Table of Contents
1. **[Setting up the Environemnt](#env)**
2. **[Datasets](#datasets)**
3. **[Project Structure](#structure)**
4. **[SQL Database](#sql)**
5. **[Machine Learning](#learning)**
6. **[Dash Dashboard](#dash)**
7. **[References](#references)**


<a name="env"></a>
## Setting up the Environment

To set up the environment for this project, after downloading the repo, enter the following code in the terminal; "conda env create -f"Code\environment.yml"
Select landodatalake as your desired environment.
When running your first cell after the environment is installed and activated, you may be prompted with a message like:
“Running cells with 'Python 3.9.13 ('landodatalake')' requires ipykernel package.
Run the following command to install 'ipykernel' into the Python environment. 
Command: 'conda install -n landodatalake ipykernel --update-deps --force-reinstall'”
In which case, you should run "conda install -n landodatalake ipykernel --update-deps --force-reinstall" in your terminal
When it prompts you to proceed, enter ‘y’
Your environment is now ready to go.

<a name="datasets"></a>
## Datasets

Three datasets pertaining to music streaming and United States demographics are used to create a narrative of music streaming in the United States.

<ins>Current Population Survey: Computer and Internet Use Supplement 2019</ins>

Current Population Survey: Computer and Internet Use Supplement 2019 (United States Census Bureau, 2020) from the United States Census Bureau illustrated the demographic characteristics of households in the United States that, among other things, stream music. 

<ins>Spotify Dataset 1921-2020, 600k+ Tracks</ins>

The first large dataset we used for the data streaming and machine learning of this project was “Spotify Dataset 1921-2020, 600k+ Tracks” (Eren Ay, 2021) which was used for the attributes it presents on individual songs. This data set was used to make a content recommender based on an individual song’s attributes, like popularity or danceability. 

<ins>Streamable Playlists with User Data</ins>

The second large data set we used was the Streamable Playlists with User Data (Boland, n.d.)  dataset. From it we were able to collect music streaming users’ playlists. This revealed how users like to group songs, which we used to create a collaborative recommender model. 


<a name="structure"></a>
## Project Structure
### Data Platform
![Owner](https://github.com/EduardStalmakov/Capstone-Project/blob/main/ProjectSpecifications/DataPlaformDiagram.png)
### ETL Pipeline
![Owner](https://github.com/EduardStalmakov/Capstone-Project/blob/main/ProjectSpecifications/ETL-Pipeline.PNG)
### Kafka Producer and Consumer
![Owner](https://github.com/EduardStalmakov/Capstone-Project/blob/main/ProjectSpecifications/Kafka-Producer-Consumer.PNG)

<a name="sql"></a>
## SQL Database
![SQL-Data](https://github.com/EduardStalmakov/Capstone-Project/blob/main/ERD.png)
<a name="learning"></a>
## Machine Learning
Their were two types of machine learning used in this project, a content and a collaborative based song recommender. 

<ins>Content based recommender</ins>

The content recommender model uses cosine similarity to recommend songs that are most similar to a user’s selected playlist. This machine learning algorithm works by first converting each song into a vector with 823 dimensions/features. The features include the song’s genre, attributes, popularity, and Release Year. When a user selects a playlist, a vector is built based on the sum of the song features to create an eigenvector for the playlist. This eigenvector and all of the song vectors are normalized by dividing by their Euclidean magnitudes. Afterwards, a dot product between the normalized playlist and each song’s unit vector is performed to calculate the cosine similarity. These values range from 0 (no similarity) to 1 (perfectly similar) and are sorted in descending order. The top 10 songs are selected as the recommendations. 


<ins>Collaborative Recommender</ins>

The collaborative recommender model uses cosine distances of a searched song to recommend songs that appear most often on other users playlists that also include the searched song. For readability to the end user, the cosine of 1 to -1  is converted to pairwise distance of 0 to 1. 0 being the song most similar to the searched song, and 1 being the most dissimilar. 
This machine learning algorithm works by first joining datasets to have each row represent a song and a playlist on which it is included. Therefore, a song can be listed more than once if it is on more than one playlist. However, we want to know on which playlist a song is listed, so we create a pivot table with the index being the song, and the columns being playlists. This creates a huge dataframe where if a specific song is on a specific playlist, it will return a 1. Everything else is 0.  To make the data more manageable, the pivot table is converted into a sparse matrix. Sparse matrices only show values that exist, so the 1s. From here, we can calculate the cosine distance. This returns a distance matrix, comparing every song with every other song in the dataset.
The distance matrix is an array that starts with a 0, meaning that a specific song is similar to itself. There is a diagonal line of the songs being similar to themselves across the array. From there, we convert the array into a dataframe. A user enters a search for a song, that search term is used to find a matching song/artist.  The returned songs are sorted in ascending order, so closest to 0, which is most similar, first. 
 This model only works if users have a song saved to their playlist. if new songs get added to a music streaming platform, it will not be on any playlists, thus will not get recommended. As users add it to their playlists, a correlation will develop and we will be able to see what other songs people like that song listen to. 


<a name="dash"></a>
## Dash Dashboard


<a name="references"></a>
## References
[1] Boland, D. (n.d.). Streamable Playlists with User Data. Streamable playlists with User Data.
        Retrieved September 19, 2022, from http://www.dcs.gla.ac.uk/~daniel/spud/
        
[2] Ay, Y. E. (2021, April). Spotify dataset 1921-2020, 600K+ tracks. Kaggle. Retrieved September 26,
        2022, from https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-19212020-600k-tracks 
        
[3] Bureau, U. S. C. (2019, November). Current Population Survey: Computer and Internet Use Supplement. Retrieved September 23, 2022, from  
        https://api.census.gov/data/2019/cps/internet/nov
