# Core packages
import streamlit as st
from streamlit_lottie import st_lottie
import spacy_streamlit
from streamlit_option_menu import option_menu

import spacy
import re
import requests


from responses_functions import *
from food_item_info import *
#from lottie import load_animation


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

# Reading from lottie's URL website
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200: # Not ok
        return None
    return r.json()

# Reading from a local filepath
def load_lottiefile(path: str):
    r = requests.get(path)
    if r.status_code != 200:
        return None
    return r.json()

def main():
    #st.write('<h1 style="font-size: 40px;">FoodKeeper Named Research Project</h1>', unsafe_allow_html=True)
    text = "FoodKeeper Research Project"
    font = "Consolas"
    font_size = "42px"
    st.markdown(f"<span style='font-family:{font};font-size:{font_size}'>{text}</span>", unsafe_allow_html=True)

    menu_options = ['Home', 'NER']
    # choice = st.sidebar.selectbox('Menu', menu_options)

    choice = option_menu(
        menu_title=None,
        options=menu_options,
        default_index=0,
        icons=["house", "book"],
        orientation="horizontal"
    )


    if choice == 'Home':
        
        # st.image("animatedfood.gif", caption="Animated GIF", use_column_width=True)
        food_animation = load_lottieurl('https://assets6.lottiefiles.com/temp/lf20_nXwOJj.json')
        st_lottie(
            food_animation,
            speed=2,
            reverse=False,
            loop=True,
            height=450,
            width=450,
        )

        # animation = load_animation('Lottie Files/69733-food-beverage.json')
        # show_lottie_animation(animation, speed=1)

        text = "Overview"
        font = "Consolas"
        font_size = "30px"
        st.markdown(f"<span style='font-family:{font};font-size:{font_size}'>{text}</span>", unsafe_allow_html=True)

        text = '''
            Welcome to our website where we shed light on the critical issue of food waste in the United States. 
            Did you know that approximately 30-40% of the food supply is wasted in the US, which amounts to about 133 billion pounds? 
            Unfortunately, consumers also play a significant role in contributing to food waste. In fact, the average household wastes 
            nearly 32% of the food it buys. One major reason for this waste is date label confusion, which leads to the premature disposal of food by 
            80% of Americans. At our website, we aim to raise awareness about food waste and provide helpful tips and resources to reduce it.

        '''
        font = "Consolas"
        font_size = "15px"
        st.markdown(f"<p style='font-family:{font};font-size:{font_size}'>{text}", unsafe_allow_html=True)
        # st.markdown('Welcome to our website where we shed light on the critical issue of food waste in the United States. Did you know that approximately 30-40% of the food supply is wasted in the US, which amounts to about 133 billion pounds? Unfortunately, consumers also play a significant role in contributing to food waste. In fact, the average household wastes nearly 32% of the food it buys. One major reason for this waste is date label confusion, which leads to the premature disposal of food by 80% of Americans. At our website, we aim to raise awareness about food waste and provide helpful tips and resources to reduce it.')
        
        
        text = "How to Use"
        font = "Consolas"
        font_size = "30px"
        st.markdown(f"<span style='font-family:{font};font-size:{font_size}'>{text}</span>", unsafe_allow_html=True)


        text = '''
        Discover the ultimate food preservation guide with our state-of-the-art NLP system! Simply input any food-related tweet and watch as our 
        system identifies various food entities mentioned. For each entity detected, our system provides expert recommendations on how to store,
        refrigerate, and freeze specific foods to keep them fresh and delicious for as long as possible. Whether you're a seasoned chef or a beginner 
        cook, our NLP technology makes food preservation easier than ever before.
        '''
        font = "Consolas"
        font_size = "15px"
        st.markdown(f"<p style='font-family:{font};font-size:{font_size}'>{text}", unsafe_allow_html=True)

    elif choice == 'NER':
        
        text = "Named Entity Recognition: Foods"
        font = "Consolas"
        font_size = "25px"
        st.markdown(f"<span style='font-family:{font};font-size:{font_size}'>{text}</span>", unsafe_allow_html=True)
        
        
        #st.subheader('Named Entity Recognition: Foods')
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