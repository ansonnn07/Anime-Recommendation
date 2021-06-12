# Anime Recommendation

## Built with
<code><img height="40" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/python/python.png"></code>
<code><img height="40" src="https://raw.githubusercontent.com/numpy/numpy/7e7f4adab814b223f7f917369a72757cd28b10cb/branding/icons/numpylogo.svg"></code>
<code><img height="40" src="https://raw.githubusercontent.com/pandas-dev/pandas/761bceb77d44aa63b71dda43ca46e8fd4b9d7422/web/pandas/static/img/pandas.svg"></code>
<code><img height="40" src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Scikit_learn_logo_small.svg/1280px-Scikit_learn_logo_small.svg.png"></code>

## Summary
- The data is obtained from [Kaggle](https://www.kaggle.com/austinreese/craigslist-carstrucks-data),
and they were scraped from the Craigslist platform, which has a very large collection of listings of 
used vehicles that are being sold by people in United States.
- In this project, machine learning is used to predict used car prices based on various attributes such as the year of the vehicle, the location (latitude and longitude) of the listing and so on.
- The model used in the end is worse than the original Random Forest model built in the notebook (R-squared = 86.0% instead of 90.5%). This is due to the extremely large size of the Random Forest model, therefore some parameters were changed to reduce the size of the model, you can refer to the `modelling.ipynb` notebook to see the methods used to reduce and compress the model size under the **Save the model** section.

## Website
The Web App is accessible [here](https://share.streamlit.io/ansonnn07/used-car-price-prediction/main/app.py) which you can directly see all the visualizations made.

## Docker Installation

## Acknowledgement
Link to the Kaggle dataset: https://www.kaggle.com/hernan4444/anime-recommendation-database-2020
