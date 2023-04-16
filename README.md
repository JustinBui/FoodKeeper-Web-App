# FoodKeeper Web App

This is a web app demonstration of our NLP models and approaches from our original research project: https://github.com/egomez3412/FoodKeeperResearch. The purpose of this project is to spread awareness and educate people on food sustainability and safety on social media (Like Twitter). To do this, we've developed an expert system that can automatically respond to food-realted Tweets with useful preservation methods of specific foods according to the U.S. Department of Food Safety and Inspection Service.
 - Research paper: http://www.fullerton.edu/ecs/faculty/apanangadan/publications/IEEE_IRI_2022__entity_extraction.pdf


### Setting Up Virtual Environment:
```
python -m venv env
env/Scripts/activate
```

### Install Packages in venv:
```
pip install spacy-streamlit
python -m spacy download en_core_web_md
pip install pandas
pip install xlrd
pip install numpy
```

### Running App Locally:
```
streamlit run main.py
```

To deactivate virtual environment, run `deactivate`