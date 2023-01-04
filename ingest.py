import pandas as pd
import os

def load_data():
    folder = 'Languages/'
    languages = os.listdir(folder)
    if len(languages) == 0:
        pass
    else:
        language_path = folder + languages[0] + '/'
        vocab_list_names = [i for i in os.listdir(language_path) if '.csv' in i]
        vocab_lists = {i[:-4]: pd.read_csv(language_path + '/' + i) for i in vocab_list_names}
        return vocab_lists, languages[0]
