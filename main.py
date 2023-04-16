# Core packages
import streamlit as st

# NLP packages
import re
import spacy
import spacy_streamlit
from responses_functions import *

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

def main():
    st.title("FoodKeeper Named Research Project")

    menu = ['Home', 'NER']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Home':
        st.title('This is a title')


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