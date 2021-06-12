# Anime Recommendation

Visit the website [here](http://34.87.106.210/)!

## Built with
<img height="50" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/python/python.png" alt="python"> <img height="50" src="https://raw.githubusercontent.com/numpy/numpy/7e7f4adab814b223f7f917369a72757cd28b10cb/branding/icons/numpylogo.svg" alt="numpy"> <img height="50" src="https://raw.githubusercontent.com/pandas-dev/pandas/761bceb77d44aa63b71dda43ca46e8fd4b9d7422/web/pandas/static/img/pandas.svg" alt="pandas"> <img height="50" src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Scikit_learn_logo_small.svg/1280px-Scikit_learn_logo_small.svg.png" alt="scikit-learn"> <img height="50" src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Flask_logo.svg/1280px-Flask_logo.svg.png" alt="flask"> <img height="50" src="https://idroot.us/wp-content/uploads/2019/03/TensorFlow-logo.png" alt="tensorflow">

<img height="60" src="https://i.pinimg.com/originals/42/3b/97/423b97b41c8b420d28e84f9b07a530ec.png" alt="html-css-javascript">  <img height="60" src="https://i.pinimg.com/originals/c1/78/5d/c1785d50a929254419fa4aad0560b058.png" alt="bootstrap">  <img height="60" src="https://i.pinimg.com/originals/40/58/3b/40583b9485486616cc310cf5c5282b85.png" alt="google-cloud-platform">

## Summary
- The Anime recommendation model used in the Website was built with a collaborative filtering model using the Anime dataset scraped from [MyAnimeList](https://myanimelist.net/) and shared in [Kaggle](https://www.kaggle.com/hernan4444/anime-recommendation-database-2020).
- The model was trained in Kaggle kernel using TPUs and the entire process can be referred in the notebook here: [cf_embedding.ipynb](https://github.com/ansonnn07/Anime-Recommendation/blob/main/web/cf_embedding.ipynb).
- The website is then deployed using Docker in a Virtual Machine (VM) instance created in the Google Compute Engine, which is an Infrastructure as a Service (IaaS) component offered by Google Cloud Platform.

**NOTE**: The website will be taken down by September 2021 because the free trial has ended by then and I would like to avoid unnecessary charges.

## Website and Demo
The website is accessible [here](http://34.87.106.210/) until September 2021.


[![website demo](website_demo.png)](https://youtu.be/SgnyXSIhGR8)


## Main Notebooks for References
- [All Scrapping process.ipynb](https://github.com/ansonnn07/Anime-Recommendation/blob/main/web/All%20Scrapping%20process.ipynb) - This notebook came from the GitHub repo [here](https://github.com/Hernan4444/MyAnimeList-Database) which keep everything related to the data for the Kaggle dataset.
- [cf_embedding.ipynb](https://github.com/ansonnn07/Anime-Recommendation/blob/main/web/cf_embedding.ipynb) - notebook used for preparing the data and training the **collaborative filtering (CF) embedding model with neural networks**. This notebook is highly inspired by the amazing [Kaggle notebook](https://www.kaggle.com/chaitanya99/recommendation-system-cf-anime/) by [Chaitanya](https://www.kaggle.com/chaitanya99).
- [collab_filter_rec.ipynb](https://github.com/ansonnn07/Anime-Recommendation/blob/main/web/collab_filter_rec.ipynb) - This notebook shows the training of another **collaborative filtering model** which is not based on embeddings, but based on cosine similarity instead, and trained using an unsupervised K-Nearest Neighbor model instead of neural networks.
- [content_based_rec.ipynb](https://github.com/ansonnn07/Anime-Recommendation/blob/main/web/content_based_rec.ipynb) - This notebook shows the training of **content-based recommendation model** based on cosine similarity and word-transformed vectors.
- [scrape_img_synopsis.ipynb](https://github.com/ansonnn07/Anime-Recommendation/blob/main/web/scrape_img_synopsis.ipynb) - This notebook shows the scraping process of the Anime image thumbnail URLs and more complete synopsis as the image URLs were not provided in the original dataset, and there were some words missing in the synopsis scraped in the original dataset.

### Notebooks used for Checking:
- [check_sql_db.ipynb](https://github.com/ansonnn07/Anime-Recommendation/blob/main/web/check_sql_db.ipynb) - Checking the database contents directly using Python.
- [test_cf_embedding_model.ipynb](https://github.com/ansonnn07/Anime-Recommendation/blob/main/web/test_cf_embedding_model.ipynb) - Testing the trained CF embedding model for **inference**.
- [web_functions.ipynb](https://github.com/ansonnn07/Anime-Recommendation/blob/main/web/web_functions.ipynb) - Testing some functions used in building the Flask routes.

## Instructions for Deploying with Docker

## Acknowledgement

Kaggle dataset: https://www.kaggle.com/hernan4444/anime-recommendation-database-2020 <br>

Amazing Kaggle notebook: https://www.kaggle.com/chaitanya99/recommendation-system-cf-anime/ <br> The final model used in the website deployed here was highly inspired by his notebook. Please consider upvoting him!

### YouTube Flask Tutorials that Saved Me
Corey Schafer (Best tutorials by far): [Flask Tutorials](https://youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH)

Krish Naik: [Deployment of ML Models](https://www.youtube.com/playlist?list=PLZoTAELRMXVOAvUbePX1lTdxQR8EY35Z1)

JimShapedCoding: [Web Application Deployment with Docker & Docker Compose](https://www.youtube.com/playlist?list=PLOkVupluCIjtjNDlZOb2ebib1aIvAivhx)

Tech with Time: [Flask Tutorial](https://youtu.be/dam0GPOAvVI)