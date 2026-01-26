# Movie Recommendation System

## Overview

This repository contains a Movie Recommendation System built using the TMDB dataset. It includes data files, a Jupyter notebook for development and analysis, and an application entry point for running the recommender.

## Files Provided


# Movie Recommendation System — Step-by-step Guide

## Project Overview

This project implements a content-based Movie Recommendation System using the TMDB datasets included in this repo. The repository contains the full analysis pipeline in a notebook, a runnable app entrypoint, and dataset CSVs to reproduce the results.

## Key Files

- [tmdb_5000_movies.csv](tmdb_5000_movies.csv) — movie metadata
- [tmdb_5000_credits.csv](tmdb_5000_credits.csv) — credits (cast, crew)
- [movie_recommeder_system.ipynb](movie_recommeder_system.ipynb) — exploratory analysis & pipeline
- [app.py](app.py) — application entrypoint (API or UI)
- [Procfile](Procfile) — Heroku deployment config
- [requirements.txt](requirements.txt) — Python dependencies

## Step-by-step Workflow

1. Environment setup

	- Create and activate a virtual environment (Windows example):

	```bash
	python -m venv venv
	venv\Scripts\activate
	```

	- Install dependencies:

	```bash
	pip install -r requirements.txt
	```

2. Inspect the data

	- Load the CSVs with pandas and inspect columns:

	```python
	import pandas as pd
	movies = pd.read_csv('tmdb_5000_movies.csv')
	credits = pd.read_csv('tmdb_5000_credits.csv')
	movies.head()
	credits.head()
	```

3. Merge and clean

	- The notebook demonstrates merging on movie title or id. Typical merge:

	```python
	# If credits has movie_id column matching movies.id:
	data = movies.merge(credits, left_on='id', right_on='movie_id', how='left')
	```

	- Clean and normalize text fields (genres, cast, crew) by parsing JSON-like strings and extracting names.

4. Feature engineering

	- Create a combined text feature for each movie (e.g., genres + cast + crew + keywords).

	```python
	def collapse_features(row):
		 return ' '.join([row['genres'], row['cast'], row['crew'], row['keywords']])

	data['combined'] = data.apply(collapse_features, axis=1)
	```

5. Vectorize and compute similarity

	- Use `sklearn` TF-IDF (or CountVectorizer) and compute cosine similarity.

	```python
	from sklearn.feature_extraction.text import TfidfVectorizer
	from sklearn.metrics.pairwise import linear_kernel

	tfidf = TfidfVectorizer(stop_words='english')
	tfidf_matrix = tfidf.fit_transform(data['combined'])
	cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
	```

6. Build a recommendation function

	- Map titles to indices and return top-N similar movies:

	```python
	indices = pd.Series(data.index, index=data['title']).drop_duplicates()

	def recommend(title, topn=10):
		 idx = indices[title]
		 sims = list(enumerate(cosine_sim[idx]))
		 sims = sorted(sims, key=lambda x: x[1], reverse=True)
		 sims = sims[1:topn+1]
		 movie_indices = [i[0] for i in sims]
		 return data['title'].iloc[movie_indices].tolist()
	```

7. Evaluate

	- For content-based systems, manual/qualitative evaluation is common (inspect top recommendations). Optionally, use held-out user interactions for quantitative metrics if available.

8. Run the notebook

	- Open and run [movie_recommeder_system.ipynb](movie_recommeder_system.ipynb):

	```bash
	jupyter notebook movie_recommeder_system.ipynb
	```

9. Run the app

	- If `app.py` contains a Flask app or Streamlit UI, run it accordingly:

	Flask example:
	```bash
	python app.py
	```

	Streamlit example:
	```bash
	streamlit run app.py
	```

	- Open the indicated local URL in your browser.

10. Deployment (Heroku)

	 - Ensure `requirements.txt` and [Procfile](Procfile) are correct. Typical steps:

	 ```bash
	 heroku login
	 heroku create your-app-name
	 git add .
	 git commit -m "Deploy: add README and app"
	 git push heroku main
	 ```

	 - Set config vars (e.g., `PORT`, API keys) via Heroku dashboard or `heroku config:set`.

11. Testing and improvements

	 - Add unit tests for preprocessing and the `recommend()` function.
	 - Cache similarity matrix to speed up repeated lookups.
	 - Add a lightweight UI that shows posters and details for recommended movies.

## Tips & Notes

- If filenames differ or columns mismatch, inspect the notebook [movie_recommeder_system.ipynb](movie_recommeder_system.ipynb) for the exact merges and preprocessing routines.
- If `requirements.txt` has issues, check `requiremwnts.txt` as a fallback.
- Use the included `tmdb` virtual environment only as a reference; creating a fresh venv is recommended.

## Quick Links

- Notebook: [movie_recommeder_system.ipynb](movie_recommeder_system.ipynb)
- App entry: [app.py](app.py)
- Datasets: [tmdb_5000_movies.csv](tmdb_5000_movies.csv), [tmdb_5000_credits.csv](tmdb_5000_credits.csv)

---

I've expanded the README with a detailed, reproducible step-by-step walkthrough. Tell me if you want me to: add a LICENSE, create a `tests/` folder with a few unit tests, or prepare a Heroku-ready `runtime.txt` and Git branch for deployment.

