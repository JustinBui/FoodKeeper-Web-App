# Core packages
import streamlit as st
from streamlit_lottie import st_lottie
import spacy_streamlit
from streamlit_option_menu import option_menu
import streamlit_chat

import spacy
import re
import requests
import csv
import random 

from responses_functions import *
from food_item_info import *


with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True )

# ============================ Global Variables ============================
nlp = spacy.load('output/model-last')  # Our custom named entity recognition model
FONT = "Consolas"


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

def show_chat_message(input_msg, document):
    st.session_state.generated, st.session_state.past  = [], [] # Clear chatbot results to brand new
    st.session_state.past.append(input_msg)

    types = ['Pantry', 'Refrigerate', 'Freeze']
    if len(document.ents) == 0:
        print('No entities found')
        st.session_state.generated.append('Sorry, no food entities were found in this message!')
    else:
        for e in document.ents:
            item = e.text
            response_msg = f'----- TIPS FOR {item.upper()} -----\n'

            if entityFound(item): # If the food entity is found in our current dataset (FoodKeeper)
                for t in types:
                    tips = foodStorage(item, t)
                    response_msg += t + ': '

                    for sent in tips:
                        response_msg += sent + ' '
                    response_msg += '\n\n' if t != 'Freeze' else ''
            else:
                response_msg += 'Sorry, no tips can be found here!'
            
            st.session_state.generated.append(response_msg)
        
    text = "Responses:"
    font_size = "25px"
    st.markdown(f"<span style='font-family:{FONT};font-size:{font_size}'>{text}</span>", unsafe_allow_html=True)

    # Printing messages
    if st.session_state.past:
        for i in range(0, len(st.session_state['past'])):
            streamlit_chat.message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

            for j in range(len(st.session_state['generated'])):
                streamlit_chat.message(st.session_state["generated"][j], key=str(i+j))



def main():
    #st.write('<h1 style="font-size: 40px;">FoodKeeper Named Research Project</h1>', unsafe_allow_html=True)
    text = "FoodKeeper Research Project"
    # Render the markdown string as HTML using the st.markdown method
    font_size = "42px"
    st.markdown(f"<span style='font-family:{FONT};font-size:{font_size}'>{text}</span>", unsafe_allow_html=True)
    

    menu_options = ['NER', 'Home']
    # choice = st.sidebar.selectbox('Menu', menu_options)

    choice = option_menu(
        menu_title=None,
        options=menu_options,
        default_index=0,
        icons=["chat", "house"],
        orientation="horizontal"
    )


    if choice == 'NER':
        text = "Named Entity Recognition: Foods"
        font_size = "25px"
        st.markdown(f"<span style='font-family:{FONT};font-size:{font_size}'>{text}</span>", unsafe_allow_html=True)

        option = st.selectbox('Try Out Our Prototype!',('Input Custom Text', 'Generate Tweet'))
        
        if option == 'Input Custom Text':

            
            #image integration
            # st.markdown(
            #     """
            # <style>
            # textarea::-webkit-scrollbar {
            #     width: 10px;
            # }
            # textarea::-webkit-scrollbar-thumb {
            #     background-color: #a3a3a3;
            #     border-radius: 5px;
            # }
            # textarea {
            #     border: 1px solid #ccc;
            #     border-radius: 5px;
            #     padding: 10px;
            #     font-size: 16px;
            #     resize: none;
            #     width: 300px;
            #     height: 150px;
            # }
            # </style>
            # """,
            #     unsafe_allow_html=True,
            # )

            #st.subheader('Named Entity Recognition: Foods')
            raw_text = st.text_area('Your Text', placeholder="Enter a food related tweet", key="my_text_area")
            if st.button('View Results', type="primary"):
                preprocessed_message = preProcess(raw_text)
                docx = nlp(preprocessed_message)
                spacy_streamlit.visualize_ner(docx, labels=nlp.get_pipe("ner").labels,)
                show_chat_message(raw_text, docx)

        elif option == 'Generate Tweet':
            if st.button("Random food tweet",type="primary" ):
                with open('test_data.csv', newline='') as file:
                    reader = csv.reader(file)
                    data = list(reader)
                    random_tweet = random.choice(data)[0]

                preprocessed_message = preProcess(random_tweet)
                docx = nlp(preprocessed_message)
                spacy_streamlit.visualize_ner(docx, labels=nlp.get_pipe("ner").labels,)
                show_chat_message(random_tweet, docx)
                

    
       

    
    elif choice == 'Home':  
        def include_css():
            st.markdown(
                """
                <style>
                    .container {
                        display: flex;
                        justify-content: center;
                    }
        
                    .center-lottie {
                        display: inline-block;
                    }
                </style>
                """,
                unsafe_allow_html=True,
        )
        include_css()
        
        # st.image("animatedfood.gif", caption="Animated GIF", use_column_width=True)
        food_animation = load_lottieurl('https://assets6.lottiefiles.com/temp/lf20_nXwOJj.json')
        st.markdown('<div class="container">', unsafe_allow_html=True)
        st_lottie(
            food_animation,
            speed=2,
            reverse=False,
            loop=True,
            height=455,
            width=704,
            
        )
        st.markdown('</div>', unsafe_allow_html=True)

     

        # animation = load_animation('Lottie Files/69733-food-beverage.json')
        # show_lottie_animation(animation, speed=1)

        text = "Overview"
        font_size = "30px"
        st.markdown(f"<span style='font-family:{FONT};font-weight:bold;font-size:{font_size}'>{text}</span>", unsafe_allow_html=True)

        text = '''
            Welcome to our website where we shed light on the critical issue of food waste in the United States. 
            Did you know that approximately 30-40% of the food supply is wasted in the US, which amounts to about 133 billion pounds? 
            Unfortunately, consumers also play a significant role in contributing to food waste. In fact, the average household wastes 
            nearly 32% of the food it buys. One major reason for this waste is date label confusion, which leads to the premature disposal of food by 
            80% of Americans. At our website, we aim to raise awareness about food waste and provide helpful tips and resources to reduce it.

        '''

        box_style = """
            background-color:#4C516D;
            border-radius: 10px;
            padding: 10px;
        """
        font_size = "15px"
        st.markdown(f'<div style="{box_style}">'
            f"<p style='font-family:{FONT};font-size:{font_size}'>{text}"
            f'', unsafe_allow_html=True)
        # st.markdown('Welcome to our website where we shed light on the critical issue of food waste in the United States. Did you know that approximately 30-40% of the food supply is wasted in the US, which amounts to about 133 billion pounds? Unfortunately, consumers also play a significant role in contributing to food waste. In fact, the average household wastes nearly 32% of the food it buys. One major reason for this waste is date label confusion, which leads to the premature disposal of food by 80% of Americans. At our website, we aim to raise awareness about food waste and provide helpful tips and resources to reduce it.')
        
        
        text = "How to Use"
        font_size = "30px"
        st.markdown(f"<span style='font-family:{FONT};font-weight:bold;font-size:{font_size}'>{text}</span>", unsafe_allow_html=True)


        text = '''
        Discover the ultimate food preservation guide with our state-of-the-art NLP system! Simply input any food-related tweet and watch as our 
        system identifies various food entities mentioned. For each entity detected, our system provides expert recommendations on how to store,
        refrigerate, and freeze specific foods to keep them fresh and delicious for as long as possible. Whether you're a seasoned chef or a beginner 
        cook, our NLP technology makes food preservation easier than ever before.
        '''
        box_style = """
            background-color:#4C516D;
            border-radius: 10px;
            padding: 10px;
        """
        font_size = "15px"
        st.markdown(f'<div style="{box_style}">'
            f"<p style='font-family:{FONT};font-size:{font_size}'>{text}"
            f'', unsafe_allow_html=True)

if __name__ == '__main__':
    main()