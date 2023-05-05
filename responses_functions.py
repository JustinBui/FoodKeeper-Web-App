# from gensim.summarization.summarizer import summarize
# from gensim.summarization import keywords as extract_keywords

import nltk
from nltk.corpus import wordnet
from nltk.corpus import stopwords
import spacy
import warnings
import random
import numpy as np
import random
from food_item_info import *

warnings.filterwarnings('ignore')



# ================================================= Functions Recently Made (Justin, Aditya)=================================================

def get_surrounding_words(sentence, ents):    
    words = []
    
    for w in sentence.split():
        words.append(w)
        
    # Filtering out:
    # 1) Keywords from keyword_ that have NO synset, because we need words with synset in order to perform word similarity
    # 2) Keywords that are not actual entities detected (Because we want to extract keywords SURROUNDING the entities)
    words = [w for w in words if len(wordnet.synsets(w)) > 0 and w not in ents]

    # Filtering stopwords
    stops = stopwords.words('english')
    words = [w for w in words if w not in stops]
    
    # Part of speech tagging (We want only nouns, and verbs - However this is bound to change)
    prefered_pos = ['NN', 'NNS', 'VB', 'VBD', 'VBG', 'VBN',  'VBP', 'VBZ']
    # prefered_pos = ['VB', 'VBD', 'VBG', 'VBN',  'VBP', 'VBZ']
    tagged = nltk.pos_tag(words)

    words = []
    for word, pos in tagged:    
        if pos in prefered_pos:
            words.append(word)
    
    return words # Array of words being returned

def get_cooking_similarity(context_words: list):
    if len(context_words) == 0: # Empty list
        return {'': 0}
    
    cooking_keywords = ["cook", 
                        "recipe", 
                        "ingredient", 
                        "leftovers", 
                        "leftover"
                        "boiled", 
                        "fried", 
                        "baked", 
                        "expired", 
                        "spoiled", 
                        "pantry", 
                        "refrigerate", 
                        "freeze",
                        "storage"]
    
    nlp_word_sim = spacy.load('en_core_web_md') # Another spacy nlp model for word similarity
    
    similarity_scores = dict()
    
    for current_word in context_words:        
        cooking_similarity_dict = dict()        
        current_token = nlp_word_sim(current_word)
        
        for cook_word in cooking_keywords:
            # Comparing current word with cooking words: "cook", "cooking", "recipe", "ingredient".
            # Get the corresponding cooking word with the highest score
            cook_token = nlp_word_sim(cook_word)
                
            cooking_similarity_dict[cook_word] = cook_token.similarity(current_token)
        
        highest_cooking_word = max(cooking_similarity_dict, key=cooking_similarity_dict.get)
        similarity_scores[current_word] = cooking_similarity_dict[highest_cooking_word]
    
    return similarity_scores

def is_relevant_context(similarity_scores, threshold):
    highest_corr_word = max(similarity_scores, key=similarity_scores.get)
    highest_score = similarity_scores[highest_corr_word]
    print(f'Highest correlated word \'{highest_corr_word}\': {highest_score} similarity rate')
    
    if highest_score >= threshold:
        return True
    else:
        return False


def generate_response(tweet, entities, thresh_value):
    if len(entities) == 0:
        print('No tips to give!')
    else:
        types = ['Pantry', 'Refrigerate', 'Freeze']
        ents_str = [e.text for e in entities] # Convert tuple of <class 'spacy.tokens.span.Span'> to list of entity strings

        # Retrieving words surrounding each entity
        filtered_words = get_surrounding_words(tweet, ents_str)

        # Retrieving Similarity Scores (SpaCy)
        similarity_scores = get_cooking_similarity(filtered_words)

        # Identify if our sentence (Based on context is related to cooking)
        if is_relevant_context(similarity_scores, threshold=thresh_value):
            for e in entities:
                item = repr(e)
                print(item)
                if entityFound(item):
                    for t in types:
                        print(foodStorage(item, t))
                else: print('Entity not found in our dataset!')
        else:
            print('Context of this sentence is not relevant to give a tip')