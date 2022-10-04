from dash.dependencies import Input, Output
from dash import html, dcc 
from app import app

layout = [dcc.Markdown("""
### Final Results

The predictions were equal to or greater than the actual winning offer 53.48% of the time.
Several metrics were calculated in order to evaluate the predictions versus the actuals:

|  Metric      |  Result   |
|--------------|-----------|
| Median Error |  0.49%    |
| Within 1%    | 14.69%    |
| Within 5 %   | 69.72%    |
| Within 10%   | 91.49%    |

### Resources

1. Boland, D. (n.d.). Streamable Playlists with User Data. Retrieved October 4, 2022, from http://www.dcs.gla.ac.uk/~daniel/spud/

2. Eren Ay, Y. (2021, April). Spotify Dataset 1921-2020, 600k+ Tracks. Kaggle. Retrieved September 28, 2022, from https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-19212020-600k-tracks

3. United States Census Bureau. (2020, June 22). Current Population Survey: Computer and Internet Use Supplement 2019. Retrieved September 22, 2022, from http://api.census.gov/data/2019/cps/internet/nov
"""),
#this was an image provided in the example 
html.Img(src='https://raw.githubusercontent.com/JimKing100/Multiple_Offers/master/data/prediction_errors.png')] 
