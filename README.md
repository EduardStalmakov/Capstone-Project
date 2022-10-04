# Capstone-Project

## Questions

## Table of Contents
1. **[Datasets](#datasets)**
2. **[Project Structure](#structure)**
3. **[SQL Database](#sql)**
4. **[Machine Learning](#learning)**
5. **[Visualizations](#Visuals)**
6. **[References](#references)**


<a name="datasets"></a>
## Datasets
To set up the environment for this project, after downloading the repo, enter the following code in the terminal; "conda env create -f"Code\environment.yml"
Select landodatalake as your desired environment.
When running your first cell after the environment is installed and activated, you may be prompted with a message like:
“Running cells with 'Python 3.9.13 ('landodatalake')' requires ipykernel package.
Run the following command to install 'ipykernel' into the Python environment. 
Command: 'conda install -n landodatalake ipykernel --update-deps --force-reinstall'”
In which case, you should run "conda install -n landodatalake ipykernel --update-deps --force-reinstall" in your terminal
When it prompts you to proceed, enter ‘y’
Your environment is now ready to go.


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
        2022, from https://www.kaggle.com/datasets/yamaerenay/spotify-dataset- 19212020-600k-tracks 
        
[3] Bureau, U. S. C. (2019, November). Current Population Survey: Computer and Internet Use Supplement. Retrieved September 23, 2022, from  
        https://api.census.gov/data/2019/cps/internet/nov
