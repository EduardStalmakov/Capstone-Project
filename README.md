# Music Streaming Song Recommender 

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
6. **[Visualizations](#Visuals)**
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


<a name="Visuals"></a>
## Visualizations

<a name="results"></a>
## Results

<a name="references"></a>
## References
[1] Boland, D. (n.d.). Streamable Playlists with User Data. Streamable playlists with User Data.
        Retrieved September 19, 2022, from http://www.dcs.gla.ac.uk/~daniel/spud/
        
[2] Ay, Y. E. (2021, April). Spotify dataset 1921-2020, 600K+ tracks. Kaggle. Retrieved September 26,
        2022, from https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-19212020-600k-tracks 
        
[3] Bureau, U. S. C. (2019, November). Current Population Survey: Computer and Internet Use Supplement. Retrieved September 23, 2022, from  
        https://api.census.gov/data/2019/cps/internet/nov
