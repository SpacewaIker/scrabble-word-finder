import pandas as pd

sowpods = pd.read_csv('projects/scrabble/sowpods_en.csv', names=['Word'], keep_default_na=False)

possible_combination = 'RE'
possible_words = pd.DataFrame([], columns=['Word'])

comb_in_word = lambda _: True if (possible_combination in _) else False

flt = lambda _: True if type(_) == type(1.0) else False

sowpods_bool = sowpods['Word'].apply(comb_in_word)
words_from_sowpods = sowpods.loc[sowpods_bool, 'Word'].reset_index()
possible_words = pd.DataFrame(possible_words.append(words_from_sowpods)['Word'])

print(possible_words)

# print(sowpods.loc[sowpods['Word'].apply(flt), 'Word'])
# print(sowpods.loc[[147735, 147736, 147737, 153520, 153521, 153522], :])