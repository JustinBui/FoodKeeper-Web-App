# Core packages
import streamlit as st
import re
import spacy
import spacy_streamlit
from responses_functions import *
from streamlit_lottie import st_lottie
from PIL import Image
import json
import requests

nlp = spacy.load('output/model-last')  # Our custom named entity recognition model



# ====================== NLP Functionalities ======================
def preProcess(tweet):
    #Converts a tweet to lowercase, replaces anyusername w/ <USERNAME> and URLS with <URL>
    tweet = tweet.lower()
    tweet = re.sub('@[a-zA-z0-9]*', '', tweet)              # <USERNAME>
    tweet = re.sub('http[a-zA-z0-9./:]*', '', tweet)       # <URL>
    tweet = re.sub('[.,-]*', '', tweet)
    
    # Utilize for instragram posts, remove hashtag for food-related posts
    tweet = re.sub(r'#', '', tweet) 
    tweet = re.sub('&amp;', 'and', tweet)
    #print(tweet)
    return tweet

# ==================================================================

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200: # Not ok
        return None
    return r.json()

def main():
    st.write('<h1 style="font-size: 40px;">FoodKeeper Named Research Project</h1>', unsafe_allow_html=True)
    menu = ['Home', 'NER']
    choice = st.sidebar.selectbox('Menu', menu)


    if choice == 'Home':
        st.title('This is a title')
        # st.image("animatedfood.gif", caption="Animated GIF", use_column_width=True)

        food_animation = load_lottieurl('https://assets1.lottiefiles.com/private_files/lf30_y0m027fl.json')
        st_lottie(
            food_animation,
            speed=1,
            reverse=False,
            loop=True,
            height=600,
            width=600
        )

    elif choice == 'NER':
        st.subheader('Named Entity Recognition: Foods')
        raw_text = st.text_area('Your Text', '')

        if st.button('View Results'):
            docx = nlp(raw_text)
            types = ['Pantry', 'Refrigerate', 'Freeze']

            spacy_streamlit.visualize_ner(docx, labels=nlp.get_pipe("ner").labels)
            print('Entities Found: ' + str(docx.ents))

            # ------------ Generating responses, if it is relevant to food ------------
            message = raw_text
            preprocessed_message = preProcess(message)
            
            st.subheader('Here are some Pantry, Refrigerate, and Freezing tips according to the U.S. Department of Food Safety and Inspection:')
            for e in docx.ents:
                item = e.text
                st.markdown(f"<h4>{item}</h4>", unsafe_allow_html=True)

                if entityFound(item):
                    for t in types:
                        tips = foodStorage(item, t)
                        st.markdown(f"**{t}**: {str(tips)}")



if __name__ == '__main__':
    main()