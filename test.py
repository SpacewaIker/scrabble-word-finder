import pandas as pd

POINTS_FR = pd.read_csv('points_fr.csv', names=['Letter', 'Value'])


def points_for_word(word, points=POINTS_FR):
    ''' Calculates the number of points for a word.
        A&P:
            word:
                str, word to calculate the number of points of
            points:
                pd.DataFrame, number of points given for each letter'''

    word = word.upper()
    pts = 0

    for letter in word:
        x = points.loc[(points['Letter'] == letter), 'Value']
        pts += x.reset_index(drop=True).loc[0]

    return pts


print(
    points_for_word('mot')
)
