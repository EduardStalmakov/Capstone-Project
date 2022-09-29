# Multiple_Offers
The final live version of the Multiple Offer Calculator

The contents include the following:

data - a data directory

- Marin-MultiOffers-2015-2019-Final.csv - The raw data downloaded from the Marin MLS for muliple offer sales in 2015-2019.
- 
- prediction_errors.png - The prediction errors histogram used in the Evaluate tab. #image used to show results of the ML model

model - the model directory
##=====this is going to have to change====
- XGBoost.ipynb - The colab code for running the XGBoost model and downloading the pipeline.
- pipeline.joblib - The downloaded XGBoost pipeline used for predictions in the Predict tab.

tabs - the tabs directory

- demographics.py - The code for the demographics tab.
- interface.py - The code for the interface tab.
- intro.py - The code for the intro tab.
- investors.py - The code for the investors tab.

The main app

- app.py - Initiates the Dash app
- index.py - The main Dash code with the layout and callback
- Procfile - The Procfile for Heroku
- requirements.txt - The requirements.txt file for Heroku

