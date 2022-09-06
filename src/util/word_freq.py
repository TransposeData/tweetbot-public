import math
import csv


def load_word_freq(path: str) -> dict:
    word_freq = {}

    # load csv file
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == 'word': continue
            word_freq[row[0]] = math.log10(int(row[1]))

    # normalize data
    max_freq = max(word_freq.values())
    for word in word_freq:
        if word_freq[word] > 0:
            word_freq[word] /= max_freq

    return word_freq


word_freq = load_word_freq('./unigram_freq.csv')
def check_word_freq(word: str, sensitivity: float=0.5) -> bool:
    if word in word_freq:

        # raise sensitivity towards 1.0 to return more popular results
        return word_freq[word] > sensitivity
    else:
        return False 