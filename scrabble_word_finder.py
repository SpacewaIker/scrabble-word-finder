import itertools
import re
import pandas as pd

SOWPODS_FR = pd.read_csv('projects/scrabble/sowpods_fr.csv', names=['Word'],
                         keep_default_na=False)

POINTS_FR = {
    'A': 1,
    'B': 3,
    'C': 3,
    'D': 2,
    'E': 1,
    'F': 4,
    'G': 2,
    'H': 4,
    'I': 1,
    'J': 8,
    'K': 10,
    'L': 1,
    'M': 2,
    'N': 1,
    'O': 1,
    'P': 3,
    'Q': 8,
    'R': 1,
    'S': 1,
    'T': 1,
    'U': 1,
    'V': 4,
    'W': 10,
    'X': 10,
    'Y': 10,
    'Z': 10
}


def points_for_word(word, points=POINTS_FR):
    ''' Calculates the number of points for a word.
        A&P:
            word:
                str, word to calculate the number of points of
            points:
                dict, number of points given for each letter'''

    word = word.upper()
    pts = 0

    for letter in range(len(word)):
        pts += points[word[letter]]

    return pts


def check_word_with_letters(letters, length=[1, 2, 3, 4, 5, 6, 7], alone=True,
                            add_letters=[0, 1], sowpods=SOWPODS_FR,
                            points=False):
    ''' Finds and returns the possible words with certain letters.
        A&P:
            letters:
                list, list of the player's letters
            length:
                list, list of numbers of letters in the word
            alone:
                bool, if the letters must form a word on their own
            add_letters:
                list of int, number of additional letters for combinations
            sowpods:
                pd.DataFrame, list of words
            points:
                bool, if the DataFrame returned should include the points'''

    possible_words = pd.DataFrame([], columns=['Word'])
    letters = [i.upper() for i in letters]

    for word_length in length:
        all_combinations = list(
            itertools.combinations(letters, word_length)
        )
        all_combinations = [''.join(all_combinations[i])
                            for i in range(len(all_combinations))]
        # list of all combinations as tuples, then join into list of words

        for poss_comb in all_combinations:
            for pos in range(word_length + 1):
                for num_add_let in add_letters:
                    if alone:
                        pattern = re.compile(
                            poss_comb[0:pos] + '[A-Z]{' + str(num_add_let)
                            + '}' + poss_comb[pos:]
                        )
                        sowpods_bool = sowpods['Word'].apply(
                            lambda _: True if pattern.fullmatch(_) is not None
                            and (len(_) < 16) else False
                        )
                        possible_words = possible_words.append(
                            sowpods.loc[sowpods_bool, :],
                            ignore_index=True
                        )

                    else:  # word must not be alone
                        pattern1 = re.compile(
                            poss_comb[0:pos] + '[A-Z]{' + str(num_add_let)
                            + '}' + poss_comb[pos:] + '[A-Z]*'
                        )
                        pattern2 = re.compile(
                            '[A-Z]*' + poss_comb[0:pos] + '[A-Z]{' +
                            str(num_add_let) + '}' + poss_comb[pos:]
                        )
                        sowpods_bool = sowpods['Word'].apply(
                            lambda _: True if
                            ((pattern1.fullmatch(_) is not None) or
                             (pattern2.fullmatch(_) is not None)) and
                            (len(_) < 16) else False
                        )
                        possible_words = possible_words.append(
                            sowpods.loc[sowpods_bool, :],
                            ignore_index=True
                        )

    possible_words = possible_words.drop_duplicates()
    if points:
        possible_words['Points'] = possible_words['Word'].apply(
            points_for_word
        )
        possible_words.sort_values('Points', inplace=True, ascending=False)
    return possible_words


letters = ['r', 'o', 'u', 'g', 'e', 'f', 'c']

print(
    check_word_with_letters(letters, add_letters=[0, 1],
                            alone=False, points=True).head(15)
)
