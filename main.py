# Core packages
import streamlit as st

# NLP packages
import spacy
import spacy_streamlit
nlp = spacy.load('output/model-last')


def main():
    st.title("FoodKeeper Named Entity Recognition Demo")

    menu = ['Home', 'NER']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Home':
        st.subheader('Tokenization')
        raw_text = st.text_area('Enter your text', 'Enter text here')
        docx = nlp(raw_text)
        if st.button('Tokenize'):
            spacy_streamlit.visualize_tokens(docx, attrs=['text', 'pos_', 'dep_', 'ent_type_'])

    elif choice == 'NER':
        st.subheader('Named Entity Recognition')
        raw_text = st.text_area('Your Text', 'Enter text here')
        docx = nlp(raw_text)
        spacy_streamlit.visualize_ner(docx, labels=nlp.get_pipe("ner").labels)

if __name__ == '__main__':
    main()