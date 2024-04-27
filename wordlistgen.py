import argparse
from itertools import permutations

arg_parser = argparse.ArgumentParser(description="Creates wordlists from simple words")
arg_parser.add_argument("-w", "--words", required=True, help="Keywords separated by commas. example: hello, wordlist")
arg_parser.add_argument("-c", "--capitalize", action='store_true', required=False, help="Capitalize words. Example: HelloWordlist")


args = vars(arg_parser.parse_args())
words_all = args["words"]
capitalize = args["capitalize"]


wordlist_sorted = []
wordlist_raw = []
wordlist_cap_raw = []


def combine_words(words):
    combined = []
    for word in words:
        other_words = [w for w in words if w != word]
        for r in range(1, len(other_words) + 1):
            for combo in permutations(other_words, r):
                combined.append(word + "".join(combo))
    return combined


def main(capitalize):
    wordlist_all = []
    if "," in words_all:
        word_parts = words_all.split(",")
        
        for word in word_parts:
            word = word.replace(" ","")
            wordlist_raw.append(word)
            
            if capitalize:
                word_cap = word.capitalize()
                wordlist_cap_raw.append(word_cap)
        
        wordlist_1 = combine_words(wordlist_raw)
        for word1 in wordlist_1:
            wordlist_all.append(word1)
        
        if capitalize:
            wordlist_cap = combine_words(wordlist_cap_raw)
            for word2 in wordlist_cap:
                wordlist_all.append(word2)
    
        
        unique_list = list(set(wordlist_all))
        
        wordlist_sorted = sorted(unique_list, key=len)
        for word_final in wordlist_sorted:
            print(word_final)
        

main(capitalize=capitalize)
