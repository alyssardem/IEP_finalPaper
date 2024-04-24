"""
Original: Victoria Schaller and Angela Wu 04/19/2023
Authors: Alyssa DeMarco
Date: 04/22/2024
File: sankey_diagram.py
Purpose: to create visuals about users and their words for the dashboard in main.py
"""
# import statements
import os
import pandas as pd
import collections
from sankey import make_sankey

#define function body
def make_nlp_sankey(countries, countries_names):
    """get all CSV file paths in the folder
    leaders: list of strings repsrenting the leaders to show
    returns: sankey diagram"""
    # declare a dataframe containing all countries
    df_all = pd.concat(countries, ignore_index=True)

    # get the most common words from column 5 of all CSV files combined
    common_words = [
      word for word, count in collections.Counter(' '.join(
        df_all.iloc[:, 6].values.tolist()).split()).most_common(20)
    ]
    # create a dictionary to map common words to thickness values
    word_thickness = {
      word: sum(df_all.iloc[:, 6].str.contains(word).astype(int))
      for word in common_words
    }

    # create a df with CSV names as source and common words as target
    df_sankey = pd.DataFrame({
      'source': countries_names * len(common_words),
      'target':
      common_words * len(countries)
    })
    # add thickness values to df
    df_sankey['value'] = [word_thickness[word] for word in df_sankey['target']]

    # make the sankey
    word_sankey = make_sankey(df_sankey, 'source', 'target', 'value', pad=20)
    return word_sankey